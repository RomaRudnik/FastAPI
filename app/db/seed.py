from sqlalchemy import select
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.db.models import Category, Order, Product, Profile, User


async def seed_data(session: AsyncSession) -> None:
    try:
        existing = await session.execute(select(User.id).limit(1))
        if existing.first():
            return
    except ProgrammingError:
        return

    user_1 = User(
        name="Ivan Petrenko",
        email="ivan@example.com",
        age=22,
        password_hash=hash_password("password123"),
    )
    user_2 = User(
        name="Olena Koval",
        email="olena@example.com",
        age=25,
        password_hash=hash_password("password123"),
    )
    profile_1 = Profile(user=user_1, bio="FastAPI student", phone="+380000000001")
    profile_2 = Profile(user=user_2, bio="Backend student", phone="+380000000002")

    category_1 = Category(name="Books", description="Books and manuals")
    category_2 = Category(name="Electronics", description="Devices and gadgets")

    product_1 = Product(name="FastAPI Guide", price=19.99, category=category_1)
    product_2 = Product(name="Python Handbook", price=29.99, category=category_1)
    product_3 = Product(name="USB-C Hub", price=39.99, category=category_2)

    order_1 = Order(user=user_1, product=product_1, quantity=2)
    order_2 = Order(user=user_2, product=product_3, quantity=1)

    session.add_all(
        [
            user_1,
            user_2,
            profile_1,
            profile_2,
            category_1,
            category_2,
            product_1,
            product_2,
            product_3,
            order_1,
            order_2,
        ]
    )
    await session.commit()
