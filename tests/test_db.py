"""Testes do banco relacional SQLite e das queries do Ozzy."""

import pytest
from sqlalchemy import select

from emporio_ozzy.db.models import Category, Customer, Order, Product, Promotion, Ticket
from emporio_ozzy.db.queries import (
    create_ticket,
    get_customer_orders,
    get_order_details,
    get_product_detail,
    list_active_promotions,
    search_products,
    verify_customer,
)
from emporio_ozzy.db.session import get_session_factory


@pytest.fixture
def db_session():
    """Fixture que fornece uma sessão limpa para cada teste."""
    session_factory = get_session_factory()
    session = session_factory()
    try:
        yield session
    finally:
        session.close()


def test_database_populated(db_session):
    """Valida se o banco SQLite possui registros em todas as tabelas."""
    assert db_session.execute(select(Category)).scalars().first() is not None
    assert db_session.execute(select(Customer)).scalars().first() is not None
    assert db_session.execute(select(Product)).scalars().first() is not None
    assert db_session.execute(select(Order)).scalars().first() is not None
    assert db_session.execute(select(Promotion)).scalars().first() is not None


def test_search_products(db_session):
    """Valida a busca parametrizada de produtos no catálogo."""
    # Busca por termo
    guitars = search_products(db_session, term="Yamaha", limit=5)
    assert len(guitars) > 0
    assert all("yamaha" in p["name"].lower() for p in guitars)

    # Busca com filtro de preço máximo
    cheaper = search_products(db_session, max_price=1000.0)
    assert len(cheaper) > 0
    assert all(p["price"] <= 1000.0 for p in cheaper)


def test_get_product_detail(db_session):
    """Valida a recuperação de detalhes e especificações de um produto."""
    product = search_products(db_session, limit=1)[0]
    detail = get_product_detail(db_session, product["product_id"])
    assert detail is not None
    assert detail["name"] == product["name"]
    assert isinstance(detail["specs"], dict)


def test_list_active_promotions(db_session):
    """Valida a listagem de promoções vigentes."""
    promos = list_active_promotions(db_session)
    assert len(promos) == 4
    for p in promos:
        assert p["discount_percent"] > 0
        assert p["discounted_price"] < p["original_price"]


def test_customer_verification_and_orders(db_session):
    """Valida autenticação leve de cliente e histórico de pedidos."""
    # Pedido #10 pertence ao cliente 11 (Bruno Carvalho Martins)
    verified = verify_customer(db_session, "bruno.martins@jmail.com", 10)
    assert verified is not None
    assert verified["customer_id"] == 11

    # Falha na verificação com dados incorretos
    unverified = verify_customer(db_session, "outro.email@jmail.com", 10)
    assert unverified is None

    # Detalhes do pedido
    order_info = get_order_details(db_session, 10)
    assert order_info is not None
    assert order_info["order_id"] == 10
    assert len(order_info["items"]) > 0

    # Histórico do cliente
    cust_orders = get_customer_orders(db_session, 11)
    assert len(cust_orders) >= 1
    assert any(o["order_id"] == 10 for o in cust_orders)


def test_create_ticket(db_session):
    """Valida a abertura e persistência de ticket de atendimento humano."""
    ticket = create_ticket(
        db_session,
        reason="Dúvida técnica sobre regulagem de ponte flutuante",
        priority="Alta",
        conversation_summary="Cliente tem dúvida sobre Floyd Rose",
        customer_id=11,
    )
    assert ticket["ticket_id"].startswith("#TK-")
    assert ticket["status"] == "aberto"

    # Confirma que foi gravado no banco SQLite
    persisted = (
        db_session.execute(select(Ticket).where(Ticket.ticket_id == ticket["ticket_id"]))
        .scalars()
        .first()
    )
    assert persisted is not None
    assert persisted.customer_id == 11
