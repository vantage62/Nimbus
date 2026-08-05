import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import AsyncSessionLocal

logger = logging.getLogger("nimbus.seed")

async def seed_database(db: AsyncSession):
    """
    Main entrypoint for seeding development data.
    Architecture supports generating Businesses, Users, Categories, Suppliers,
    Products, Inventory, Stock Movements, Sales History, Forecasts, etc.
    """
    logger.info("Starting database seed...")
    # NOTE: Logic to generate massive datasets will be implemented here later.
    # Currently just establishing the framework.
    logger.info("Database seed completed successfully.")

async def main():
    async with AsyncSessionLocal() as session:
        await seed_database(session)

if __name__ == "__main__":
    asyncio.run(main())
