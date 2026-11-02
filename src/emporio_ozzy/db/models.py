"""Modelos relacionais em SQLAlchemy para o banco SQLite da Empório da Música."""

from typing import List, Optional

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Classe base declarativa para os modelos do SQLAlchemy."""

    pass


class Category(Base):
    """Categorias de produtos da loja."""

    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="category")


class Customer(Base):
    """Clientes cadastrados na loja."""

    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")
    tickets: Mapped[List["Ticket"]] = relationship("Ticket", back_populates="customer")


class Product(Base):
    """Catálogo de instrumentos musicais e equipamentos."""

    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("categories.category_id"), nullable=False
    )
    price_brl: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="active", nullable=False)
    specs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    order_items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product")
    promotions: Mapped[List["Promotion"]] = relationship("Promotion", back_populates="product")


class Order(Base):
    """Pedidos realizados pelos clientes."""

    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customers.customer_id"), index=True, nullable=False
    )
    order_date: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    total_brl: Mapped[float] = mapped_column(Float, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    tracking_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    estimated_delivery: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    customer: Mapped["Customer"] = relationship("Customer", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """Itens pertencentes a cada pedido."""

    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.order_id"), index=True, nullable=False
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.product_id"), index=True, nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="order_items")


class Promotion(Base):
    """Campanhas promocionais atreladas a produtos."""

    __tablename__ = "promotions"

    promotion_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.product_id"), index=True, nullable=False
    )
    discount_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    is_active: Mapped[int] = mapped_column(Integer, default=0, index=True, nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="promotions")


class Ticket(Base):
    """Tickets de atendimento humano / luthier acionados pelo Ozzy."""

    __tablename__ = "tickets"

    ticket_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    customer_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("customers.customer_id"), nullable=True
    )
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="Alta", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="aberto", nullable=False)
    conversation_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(String(30), nullable=False)

    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="tickets")
