from sqlalchemy import select
from .db import Base, engine, SessionLocal
from .models import User, Entity, Product, Period, Setting
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    admin = db.execute(select(User).where(User.username == "admin")).scalar_one_or_none()
    if not admin:
        db.add(
            User(
                username="admin",
                full_name="System Admin",
                password_hash=hash_password("admin123"),
                is_active=True,
            )
        )

    if not db.execute(select(Entity)).scalars().first():
        db.add_all([
            Entity(
                entity_type="فرع",
                code="BR001",
                name_ar="فرع الخمسين",
                plan_name="الخمسين",
                entity_level="A",
                reference_capacity=9940,
                capacity_index=1.0,
                reference_services_count=31,
            ),
            Entity(
                entity_type="فرع",
                code="BR002",
                name_ar="فرع الشيخ عثمان",
                plan_name="الشيخ عثمان",
                entity_level="A",
                reference_capacity=6480,
                capacity_index=0.65,
                reference_services_count=26,
            ),
        ])

    if not db.execute(select(Product)).scalars().first():
        db.add_all([
            Product(code="P001", name_ar="فتح الحسابات", raw_weight=12, relative_weight=0.12, is_group_title=False, is_scored=True),
            Product(code="P002", name_ar="الحوالات", raw_weight=10, relative_weight=0.10, is_group_title=False, is_scored=True),
            Product(code="P003", name_ar="الودائع", raw_weight=15, relative_weight=0.15, is_group_title=False, is_scored=True),
            Product(code="P100", name_ar="عنوان تجميعي - الخدمات", raw_weight=0, relative_weight=0, is_group_title=True, is_scored=False),
        ])

    if not db.execute(select(Period)).scalars().first():
        q1 = Period(
            code="2026-Q1",
            label_ar="الربع الأول 2026",
            period_type="quarter",
            start_date="2026-01-01",
            end_date="2026-03-31",
            status="open",
        )
        db.add(q1)
        db.flush()

        db.add_all([
            Period(
                code="2026-01",
                label_ar="يناير 2026",
                period_type="month",
                start_date="2026-01-01",
                end_date="2026-01-31",
                parent_period_id=q1.id,
                status="open",
            ),
            Period(
                code="2026-02",
                label_ar="فبراير 2026",
                period_type="month",
                start_date="2026-02-01",
                end_date="2026-02-28",
                parent_period_id=q1.id,
                status="open",
            ),
            Period(
                code="2026-03",
                label_ar="مارس 2026",
                period_type="month",
                start_date="2026-03-01",
                end_date="2026-03-31",
                parent_period_id=q1.id,
                status="open",
            ),
        ])

    defaults = {
        "threshold_exceeded": "1",
        "threshold_on_track": "0.85",
        "threshold_followup": "0.60",
        "display_period_code": "2026-Q1",
        "input_period_code": "2026-01",
    }

    existing_keys = {x.key for x in db.execute(select(Setting)).scalars().all()}
    for key, value in defaults.items():
        if key not in existing_keys:
            db.add(Setting(key=key, value=value))

    db.commit()
    db.close()


if __name__ == "__main__":
    run()
