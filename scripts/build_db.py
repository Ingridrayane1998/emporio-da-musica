#!/usr/bin/env python3
"""
Script idempotente para criação e carga do banco de dados relacional
SQLite a partir dos CSVs processados.
"""

import sys
from pathlib import Path

import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Adiciona o diretório src ao sys.path para import direto
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from emporio_ozzy.config import get_settings  # noqa: E402
from emporio_ozzy.db.models import (  # noqa: E402
    Base,
    Category,
    Customer,
    Order,
    OrderItem,
    Product,
    Promotion,
)
from emporio_ozzy.db.session import get_engine, get_session_factory  # noqa: E402
from emporio_ozzy.etl.clean import run_etl  # noqa: E402


def build_database(
    processed_dir: Path,
    db_path: Path,
    raw_dir: Path | None = None,
    sample_dir: Path | None = None,
) -> None:
    """Cria e popula o banco de dados SQLite de forma idempotente."""
    # Garante que os arquivos limpos existem
    required_files = [
        "categories.csv",
        "customers.csv",
        "orders.csv",
        "order_items.csv",
        "products.csv",
        "promotions.csv",
    ]
    all_exist = all((processed_dir / f).exists() for f in required_files)

    if not all_exist and raw_dir and sample_dir:
        print("Arquivos processados não encontrados. Executando ETL...")
        run_etl(raw_dir, processed_dir, sample_dir)

    print(f"Criando banco de dados SQLite em: {db_path.as_posix()}")
    engine = get_engine(db_path)

    # Recriação idempotente de todas as tabelas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session_factory = get_session_factory(engine)
    session = session_factory()

    try:
        # 1. Categories
        cat_df = pd.read_csv(processed_dir / "categories.csv")
        categories = [
            Category(
                category_id=int(r["category_id"]),
                name=str(r["name"]),
                description=str(r["description"]) if pd.notna(r["description"]) else None,
            )
            for _, r in cat_df.iterrows()
        ]
        session.add_all(categories)
        session.flush()
        print(f"  [OK] {len(categories)} categorias inseridas.")

        # 2. Customers
        cust_df = pd.read_csv(processed_dir / "customers.csv")
        customers = [
            Customer(
                customer_id=int(r["customer_id"]),
                name=str(r["name"]),
                phone=str(r["phone"]),
                email=str(r["email"]),
                city=str(r["city"]),
                is_active=int(r["is_active"]),
            )
            for _, r in cust_df.iterrows()
        ]
        session.add_all(customers)
        session.flush()
        print(f"  [OK] {len(customers)} clientes inseridos.")

        # 3. Products
        prod_df = pd.read_csv(processed_dir / "products.csv")
        products = [
            Product(
                product_id=int(r["product_id"]),
                name=str(r["name"]),
                category_id=int(r["category_id"]),
                price_brl=float(r["price_brl"]),
                stock_quantity=int(r["stock_quantity"]),
                status=str(r["status"]),
                specs=str(r["specs"]) if pd.notna(r["specs"]) else None,
                description=str(r["description"]) if pd.notna(r["description"]) else None,
                created_at=str(r["created_at"]) if pd.notna(r["created_at"]) else None,
            )
            for _, r in prod_df.iterrows()
        ]
        session.add_all(products)
        session.flush()
        print(f"  [OK] {len(products)} produtos inseridos.")

        # 4. Orders
        ord_df = pd.read_csv(processed_dir / "orders.csv")
        orders = [
            Order(
                order_id=int(r["order_id"]),
                customer_id=int(r["customer_id"]),
                order_date=str(r["order_date"]),
                status=str(r["status"]),
                total_brl=float(r["total_brl"]),
                payment_method=str(r["payment_method"]),
                tracking_code=str(r["tracking_code"]) if pd.notna(r["tracking_code"]) else None,
                estimated_delivery=(
                    str(r["estimated_delivery"]) if pd.notna(r["estimated_delivery"]) else None
                ),
                notes=str(r["notes"]) if pd.notna(r["notes"]) else None,
            )
            for _, r in ord_df.iterrows()
        ]
        session.add_all(orders)
        session.flush()
        print(f"  [OK] {len(orders)} pedidos inseridos.")

        # 5. Order Items
        items_df = pd.read_csv(processed_dir / "order_items.csv")
        order_items = [
            OrderItem(
                order_item_id=int(r["order_item_id"]),
                order_id=int(r["order_id"]),
                product_id=int(r["product_id"]),
                quantity=int(r["quantity"]),
            )
            for _, r in items_df.iterrows()
        ]
        session.add_all(order_items)
        session.flush()
        print(f"  [OK] {len(order_items)} itens de pedido inseridos.")

        # 6. Promotions
        promo_df = pd.read_csv(processed_dir / "promotions.csv")
        promotions = [
            Promotion(
                promotion_id=int(r["promotion_id"]),
                product_id=int(r["product_id"]),
                discount_percent=int(r["discount_percent"]),
                description=str(r["description"]),
                is_active=int(r["is_active"]),
            )
            for _, r in promo_df.iterrows()
        ]
        session.add_all(promotions)
        session.flush()
        print(f"  [OK] {len(promotions)} promoções inseridas.")

        session.commit()
        print("[SUCESSO] Banco SQLite construído e populado com sucesso!")

    except Exception as e:
        session.rollback()
        print(f"[ERRO] Erro ao construir banco de dados: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    settings = get_settings()
    processed = Path("data/processed")
    raw = Path("data/raw")
    sample = Path("data/sample")
    build_database(processed, settings.db_path, raw, sample)
