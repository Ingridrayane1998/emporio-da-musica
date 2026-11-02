"""Módulo de limpeza e tratamento (ETL) dos CSVs para data/processed e data/sample."""

import json
from pathlib import Path

import pandas as pd


def clean_categories(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e formata a tabela de categorias."""
    df = raw_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df["name"] = df["name"].astype(str).str.strip()
    df["description"] = df["description"].astype(str).str.strip()
    df["category_id"] = df["category_id"].astype(int)
    return df


def clean_customers(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Limpa e normaliza a tabela de clientes, resolvendo duplicatas de e-mail."""
    df = raw_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df["customer_id"] = df["customer_id"].astype(int)
    df["name"] = df["name"].astype(str).str.strip()
    df["phone"] = df["phone"].astype(str).str.strip()
    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["city"] = df["city"].astype(str).str.strip()

    # Adiciona flag is_active (1 = ativo, 0 = inativo)
    df["is_active"] = 1

    # Regra de negócio aprovada:
    # Cliente 11 (Bruno Carvalho Martins) cadastrado primeiro e com pedido #10 -> Mantém ativo
    # Cliente 43 (Bruno Martins) duplicado sem pedidos -> Desativado e e-mail diferenciado
    mask_inactive = df["customer_id"] == 43
    df.loc[mask_inactive, "is_active"] = 0
    df.loc[mask_inactive, "email"] = "bruno.martins+desativado43@jmail.com"

    return df


def clean_orders(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Limpa a tabela de pedidos, preservando nulos semânticos e datas ISO."""
    df = raw_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df["order_id"] = df["order_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.strftime("%Y-%m-%d")
    df["status"] = df["status"].astype(str).str.strip().str.lower()
    df["total_brl"] = df["total_brl"].astype(float).round(2)
    df["payment_method"] = df["payment_method"].astype(str).str.strip().str.lower()

    # Preserva nulos semânticos legítimos
    df["tracking_code"] = df["tracking_code"].apply(
        lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != "" else None
    )
    df["estimated_delivery"] = df["estimated_delivery"].apply(
        lambda x: (
            pd.to_datetime(x).strftime("%Y-%m-%d")
            if pd.notna(x) and str(x).strip() != ""
            else None
        )
    )
    df["notes"] = df["notes"].apply(
        lambda x: str(x).strip() if pd.notna(x) and str(x).strip() != "" else None
    )

    return df


def clean_order_items(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Limpa os itens dos pedidos e atribui chave primária order_item_id sequencial."""
    df = raw_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df["order_id"] = df["order_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)
    df["quantity"] = df["quantity"].astype(int)

    # Criação de chave primária explícita
    df.insert(0, "order_item_id", range(1, len(df) + 1))
    return df


def clean_products(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Limpa o catálogo de produtos e valida integridade de specs em formato JSON."""
    df = raw_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df["product_id"] = df["product_id"].astype(int)
    df["name"] = df["name"].astype(str).str.strip()
    df["category_id"] = df["category_id"].astype(int)
    df["price_brl"] = df["price_brl"].astype(float).round(2)
    df["stock_quantity"] = df["stock_quantity"].astype(int)
    df["status"] = df["status"].astype(str).str.strip().str.lower()
    df["description"] = df["description"].astype(str).str.strip()
    df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")

    # Validação e normalização de JSON em specs
    def normalize_json(val: str) -> str:
        try:
            parsed = json.loads(val)
            return json.dumps(parsed, ensure_ascii=False)
        except Exception:
            return json.dumps({"raw": str(val)}, ensure_ascii=False)

    df["specs"] = df["specs"].astype(str).apply(normalize_json)
    return df


def clean_promotions(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Limpa a tabela de promoções."""
    df = raw_df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df["promotion_id"] = df["promotion_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)
    df["discount_percent"] = df["discount_percent"].astype(int)
    df["description"] = df["description"].astype(str).str.strip()
    df["is_active"] = df["is_active"].astype(int)
    return df


def run_etl(raw_dir: Path, processed_dir: Path, sample_dir: Path) -> dict[str, pd.DataFrame]:
    """Executa o pipeline completo de limpeza e gera arquivos processados e amostras."""
    processed_dir.mkdir(parents=True, exist_ok=True)
    sample_dir.mkdir(parents=True, exist_ok=True)

    cleaned_data = {}

    # 1. Categories
    cat_raw = pd.read_csv(raw_dir / "categories.csv")
    cleaned_cat = clean_categories(cat_raw)
    cleaned_cat.to_csv(processed_dir / "categories.csv", index=False)
    cleaned_cat.to_csv(sample_dir / "categories.csv", index=False)
    cleaned_data["categories"] = cleaned_cat

    # 2. Customers
    cust_raw = pd.read_csv(raw_dir / "customers.csv")
    cleaned_cust = clean_customers(cust_raw)
    cleaned_cust.to_csv(processed_dir / "customers.csv", index=False)

    # Amostra anonimizada para GitHub (LGPD)
    cust_sample = cleaned_cust.head(10).copy()
    for idx, row in cust_sample.iterrows():
        cust_sample.at[idx, "name"] = f"Cliente Amostra {idx + 1}"
        cust_sample.at[idx, "phone"] = f"(11) 98000-{1000 + idx}"
        cust_sample.at[idx, "email"] = f"cliente.amostra.{idx + 1}@exemplo.com"
        cust_sample.at[idx, "city"] = "São Paulo"
    cust_sample.to_csv(sample_dir / "customers.csv", index=False)
    cleaned_data["customers"] = cleaned_cust

    # 3. Orders
    ord_raw = pd.read_csv(raw_dir / "orders.csv")
    cleaned_ord = clean_orders(ord_raw)
    cleaned_ord.to_csv(processed_dir / "orders.csv", index=False)
    cleaned_ord.head(10).to_csv(sample_dir / "orders.csv", index=False)
    cleaned_data["orders"] = cleaned_ord

    # 4. Order Items
    items_raw = pd.read_csv(raw_dir / "order_items.csv")
    cleaned_items = clean_order_items(items_raw)
    cleaned_items.to_csv(processed_dir / "order_items.csv", index=False)
    cleaned_items.head(10).to_csv(sample_dir / "order_items.csv", index=False)
    cleaned_data["order_items"] = cleaned_items

    # 5. Products
    prod_raw = pd.read_csv(raw_dir / "products.csv")
    cleaned_prod = clean_products(prod_raw)
    cleaned_prod.to_csv(processed_dir / "products.csv", index=False)
    cleaned_prod.head(10).to_csv(sample_dir / "products.csv", index=False)
    cleaned_data["products"] = cleaned_prod

    # 6. Promotions
    promo_raw = pd.read_csv(raw_dir / "promotions.csv")
    cleaned_promo = clean_promotions(promo_raw)
    cleaned_promo.to_csv(processed_dir / "promotions.csv", index=False)
    cleaned_promo.head(10).to_csv(sample_dir / "promotions.csv", index=False)
    cleaned_data["promotions"] = cleaned_promo

    return cleaned_data


if __name__ == "__main__":
    r_dir = Path("data/raw")
    p_dir = Path("data/processed")
    s_dir = Path("data/sample")
    results = run_etl(r_dir, p_dir, s_dir)
    print("ETL concluído com sucesso!")
    for k, v in results.items():
        print(f"- {k}: {len(v)} registros tratados.")
