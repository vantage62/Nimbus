import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.database.base import Base
from app.core.config import settings

# Import all models for autogenerate
from app.modules.auth.models import User, RefreshToken, Role, Permission
from app.modules.business.models import Business, BusinessMembership, Store
from app.modules.categories.models import Category
from app.modules.suppliers.models import Supplier
from app.modules.products.models import Product
from app.modules.inventory.models import Inventory, StockMovement
from app.modules.sales.models import Sale
from app.modules.forecasting.models import MLModel, ForecastRun, Forecast
from app.modules.notifications.models import Notification
from app.modules.settings.models import Setting
from app.modules.upload.models import CsvUpload
from app.modules.analytics.models import AnalyticsSnapshot
from app.modules.chat.models import AiConversation
from app.modules.audit.models import AuditLog

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
