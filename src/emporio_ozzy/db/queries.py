"""Consultas parametrizadas e seguras ao banco relacional SQLite para alimentar o agente Ozzy."""

import json
import random
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from emporio_ozzy.db.models import (
    Category,
    Customer,
    Order,
    OrderItem,
    Product,
    Promotion,
    Ticket,
)


def search_products(
    db: Session,
    term: Optional[str] = None,
    category_name: Optional[str] = None,
    max_price: Optional[float] = None,
    in_stock_only: bool = True,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Busca produtos no catálogo por termo, categoria, teto de preço e estoque."""
    stmt = (
        select(Product, Category.name.label("category_name"))
        .join(Category, Product.category_id == Category.category_id)
        .where(Product.status == "active")
    )

    if term:
        like_pattern = f"%{term.strip().lower()}%"
        stmt = stmt.where(
            func.lower(Product.name).like(like_pattern)
            | func.lower(Product.description).like(like_pattern)
        )

    if category_name:
        stmt = stmt.where(func.lower(Category.name).like(f"%{category_name.strip().lower()}%"))

    if max_price is not None:
        stmt = stmt.where(Product.price_brl <= max_price)

    if in_stock_only:
        stmt = stmt.where(Product.stock_quantity > 0)

    stmt = stmt.order_by(Product.price_brl.asc()).limit(limit)
    rows = db.execute(stmt).all()

    results = []
    for product, cat_name in rows:
        # Verifica se há promoção ativa
        promo = (
            db.execute(
                select(Promotion)
                .where(Promotion.product_id == product.product_id)
                .where(Promotion.is_active == 1)
            )
            .scalars()
            .first()
        )

        final_price = product.price_brl
        original_price = None
        discount_percent = 0

        if promo:
            discount_percent = promo.discount_percent
            original_price = product.price_brl
            final_price = round(product.price_brl * (1 - (discount_percent / 100)), 2)

        results.append(
            {
                "product_id": product.product_id,
                "name": product.name,
                "category": cat_name,
                "price": final_price,
                "original_price": original_price,
                "discount_percent": discount_percent,
                "stock_quantity": product.stock_quantity,
                "description": product.description,
            }
        )

    return results


def get_product_detail(db: Session, product_id: int) -> Optional[dict[str, Any]]:
    """Retorna detalhes completos de um produto específico, incluindo especificações e promoções."""
    stmt = (
        select(Product, Category.name.label("category_name"))
        .join(Category, Product.category_id == Category.category_id)
        .where(Product.product_id == product_id)
    )
    row = db.execute(stmt).first()
    if not row:
        return None

    product, cat_name = row
    promo = (
        db.execute(
            select(Promotion)
            .where(Promotion.product_id == product.product_id)
            .where(Promotion.is_active == 1)
        )
        .scalars()
        .first()
    )

    final_price = product.price_brl
    original_price = None
    discount_percent = 0
    promo_desc = None

    if promo:
        discount_percent = promo.discount_percent
        original_price = product.price_brl
        final_price = round(product.price_brl * (1 - (discount_percent / 100)), 2)
        promo_desc = promo.description

    specs_dict = {}
    if product.specs:
        try:
            specs_dict = json.loads(product.specs)
        except Exception:
            specs_dict = {"raw": product.specs}

    return {
        "product_id": product.product_id,
        "name": product.name,
        "category": cat_name,
        "price": final_price,
        "original_price": original_price,
        "discount_percent": discount_percent,
        "promotion": promo_desc,
        "stock_quantity": product.stock_quantity,
        "status": product.status,
        "specs": specs_dict,
        "description": product.description,
    }


def list_active_promotions(
    db: Session, category_name: Optional[str] = None
) -> list[dict[str, Any]]:
    """Lista as promoções vigentes na loja."""
    stmt = (
        select(Promotion, Product, Category.name.label("category_name"))
        .join(Product, Promotion.product_id == Product.product_id)
        .join(Category, Product.category_id == Category.category_id)
        .where(Promotion.is_active == 1)
    )

    if category_name:
        stmt = stmt.where(func.lower(Category.name).like(f"%{category_name.strip().lower()}%"))

    rows = db.execute(stmt).all()
    results = []

    for promo, product, cat_name in rows:
        final_price = round(product.price_brl * (1 - (promo.discount_percent / 100)), 2)
        results.append(
            {
                "promotion_id": promo.promotion_id,
                "campaign": promo.description,
                "discount_percent": promo.discount_percent,
                "product_id": product.product_id,
                "product_name": product.name,
                "category": cat_name,
                "original_price": product.price_brl,
                "discounted_price": final_price,
                "stock_quantity": product.stock_quantity,
            }
        )

    return results


def verify_customer(
    db: Session, email_or_phone: str, order_id: int
) -> Optional[dict[str, Any]]:
    """Verifica se os dados fornecidos conferem com o pedido para acesso seguro."""
    clean_identifier = email_or_phone.strip().lower()

    # Busca pedido
    order = db.execute(select(Order).where(Order.order_id == order_id)).scalars().first()
    if not order:
        return None

    # Busca cliente associado ao pedido
    customer = (
        db.execute(select(Customer).where(Customer.customer_id == order.customer_id))
        .scalars()
        .first()
    )
    if not customer:
        return None

    # Normalização de telefone removendo pontuação
    digits_input = "".join(filter(str.isdigit, clean_identifier))
    digits_cust_phone = "".join(filter(str.isdigit, customer.phone))

    match_email = customer.email.lower() == clean_identifier
    match_phone = len(digits_input) >= 8 and digits_input in digits_cust_phone

    if match_email or match_phone:
        return {
            "verified": True,
            "customer_id": customer.customer_id,
            "name": customer.name,
            "email": customer.email,
            "order_id": order.order_id,
        }

    return None


def get_order_details(db: Session, order_id: int) -> Optional[dict[str, Any]]:
    """Retorna detalhes completos de um pedido, com itens e rastreio."""
    order = db.execute(select(Order).where(Order.order_id == order_id)).scalars().first()
    if not order:
        return None

    # Itens do pedido
    items_stmt = (
        select(OrderItem, Product.name.label("product_name"), Product.price_brl)
        .join(Product, OrderItem.product_id == Product.product_id)
        .where(OrderItem.order_id == order_id)
    )
    items_rows = db.execute(items_stmt).all()

    items = [
        {
            "product_id": item.product_id,
            "product_name": prod_name,
            "quantity": item.quantity,
            "unit_price": price_brl,
        }
        for item, prod_name, price_brl in items_rows
    ]

    return {
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "order_date": order.order_date,
        "status": order.status,
        "total_brl": order.total_brl,
        "payment_method": order.payment_method,
        "tracking_code": order.tracking_code,
        "estimated_delivery": order.estimated_delivery,
        "notes": order.notes,
        "items": items,
    }


def get_customer_orders(db: Session, customer_id: int) -> list[dict[str, Any]]:
    """Lista histórico de pedidos de um cliente autenticado."""
    stmt = (
        select(Order)
        .where(Order.customer_id == customer_id)
        .order_by(Order.order_date.desc())
    )
    orders = db.execute(stmt).scalars().all()

    return [
        {
            "order_id": o.order_id,
            "order_date": o.order_date,
            "status": o.status,
            "total_brl": o.total_brl,
            "tracking_code": o.tracking_code,
        }
        for o in orders
    ]


def create_ticket(
    db: Session,
    reason: str,
    priority: str = "Alta",
    conversation_summary: Optional[str] = None,
    customer_id: Optional[int] = None,
) -> dict[str, Any]:
    """Cria e persiste um ticket de atendimento humano na base SQLite."""
    random_num = random.randint(1000, 9999)
    ticket_id = f"#TK-{random_num}"
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ticket = Ticket(
        ticket_id=ticket_id,
        customer_id=customer_id,
        reason=reason,
        priority=priority,
        status="aberto",
        conversation_summary=conversation_summary,
        created_at=now_iso,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "ticket_id": ticket.ticket_id,
        "customer_id": ticket.customer_id,
        "reason": ticket.reason,
        "priority": ticket.priority,
        "status": ticket.status,
        "created_at": ticket.created_at,
    }
