"""Testes automatizados de qualidade e integridade do ETL."""

import json
from pathlib import Path

import pandas as pd


def test_processed_files_exist():
    """Valida se todos os 6 arquivos foram gerados em data/processed."""
    processed_dir = Path("data/processed")
    expected_files = [
        "categories.csv",
        "customers.csv",
        "orders.csv",
        "order_items.csv",
        "products.csv",
        "promotions.csv",
    ]
    for fname in expected_files:
        assert (processed_dir / fname).exists(), f"Arquivo {fname} não foi gerado em data/processed"


def test_customers_uniqueness_and_deactivation():
    """Valida se os e-mails são 100% únicos e o cliente duplicado 43 está desativado."""
    df = pd.read_csv("data/processed/customers.csv")
    assert df["email"].is_unique, "Há e-mails duplicados na tabela de clientes tratada"
    assert "is_active" in df.columns, "Coluna is_active ausente em clientes"

    # Cliente 11 (Bruno Carvalho Martins) ativo
    cust_11 = df[df["customer_id"] == 11].iloc[0]
    assert cust_11["is_active"] == 1
    assert cust_11["email"] == "bruno.martins@jmail.com"

    # Cliente 43 (Bruno Martins) inativo
    cust_43 = df[df["customer_id"] == 43].iloc[0]
    assert cust_43["is_active"] == 0
    assert "desativado" in cust_43["email"]


def test_order_items_primary_key():
    """Valida se a chave primária order_item_id foi criada corretamente."""
    df = pd.read_csv("data/processed/order_items.csv")
    assert "order_item_id" in df.columns
    assert df["order_item_id"].is_unique
    assert df["order_item_id"].isna().sum() == 0


def test_referential_integrity():
    """Valida todas as integridades referenciais entre as tabelas."""
    categories = pd.read_csv("data/processed/categories.csv")
    customers = pd.read_csv("data/processed/customers.csv")
    orders = pd.read_csv("data/processed/orders.csv")
    order_items = pd.read_csv("data/processed/order_items.csv")
    products = pd.read_csv("data/processed/products.csv")
    promotions = pd.read_csv("data/processed/promotions.csv")

    # Orders -> Customers
    assert orders["customer_id"].isin(customers["customer_id"]).all()

    # Order_items -> Orders
    assert order_items["order_id"].isin(orders["order_id"]).all()

    # Order_items -> Products
    assert order_items["product_id"].isin(products["product_id"]).all()

    # Products -> Categories
    assert products["category_id"].isin(categories["category_id"]).all()

    # Promotions -> Products
    assert promotions["product_id"].isin(products["product_id"]).all()


def test_products_specs_json():
    """Valida se todas as especificações técnicas de produtos são JSONs válidos."""
    df = pd.read_csv("data/processed/products.csv")
    for spec in df["specs"]:
        parsed = json.loads(spec)
        assert isinstance(parsed, dict)


def test_sample_anonymization():
    """Valida se os dados na pasta data/sample/ estão anonimizados conforme a LGPD."""
    cust_sample = pd.read_csv("data/sample/customers.csv")
    for _, row in cust_sample.iterrows():
        assert "Cliente Amostra" in row["name"]
        assert "@exemplo.com" in row["email"]
        assert "bruno.martins@jmail.com" != row["email"]
