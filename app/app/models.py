from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True)
    entity_type = Column(String(100), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    name_ar = Column(String(255), nullable=False)
    plan_name = Column(String(255), nullable=True)
    entity_level = Column(String(10), nullable=False, default="B")
    reference_capacity = Column(Float, nullable=False, default=0)
    capacity_index = Column(Float, nullable=False, default=1)
    reference_services_count = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True, nullable=False)
    name_ar = Column(String(255), nullable=False)
    raw_weight = Column(Float, nullable=False, default=0)
    relative_weight = Column(Float, nullable=False, default=0)
    is_group_title = Column(Boolean, nullable=False, default=False)
    is_scored = Column(Boolean, nullable=False, default=True)
    note = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Period(Base):
    __tablename__ = "periods"

    id = Column(Integer, primary_key=True)
    code = Column(String(100), unique=True, nullable=False)
    label_ar = Column(String(255), nullable=False)
    period_type = Column(String(20), nullable=False)
    start_date = Column(String(20), nullable=False)
    end_date = Column(String(20), nullable=False)
    parent_period_id = Column(Integer, ForeignKey("periods.id"), nullable=True)
    status = Column(String(30), nullable=False, default="open")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String(100), primary_key=True)
    value = Column(Text, nullable=False)


class MonthlyEntry(Base):
    __tablename__ = "monthly_entries"
    __table_args__ = (
        UniqueConstraint("period_id", "entity_id", "product_id", name="uq_period_entity_product"),
    )

    id = Column(Integer, primary_key=True)
    period_id = Column(Integer, ForeignKey("periods.id"), nullable=False)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    target_value = Column(Float, nullable=False, default=0)
    achieved_value = Column(Float, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    actor_username = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)
    table_name = Column(String(100), nullable=False)
    record_id = Column(String(100), nullable=True)
    before_json = Column(Text, nullable=True)
    after_json = Column(Text, nullable=True)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
