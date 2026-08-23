import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from app.config.settings import settings

logger = logging.getLogger("smartresume.database")


class Database:
    """
    Singleton wrapper holding the Motor AsyncIOMotorClient reference.
    """
    client: Optional[AsyncIOMotorClient] = None


# Shared database client container
db = Database()


async def connect_to_mongo() -> None:
    """
    Establish asynchronous connection to MongoDB using motor.
    Should be called during application startup.
    """
    logger.info("Initializing MongoDB connection to %s...", settings.MONGODB_URL)
    try:
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,
        )
        # Verify connectivity using ping
        await db.client.admin.command('ping')
        logger.info("Successfully connected to MongoDB database '%s'.", settings.DATABASE_NAME)
    except Exception as exc:
        logger.warning(
            "Failed to ping MongoDB on startup (%s). App will continue, but database operations may fail.",
            exc
        )


async def close_mongo_connection() -> None:
    """
    Close the MongoDB motor client connection.
    Should be called during application shutdown.
    """
    if db.client is not None:
        logger.info("Closing MongoDB connection...")
        db.client.close()
        db.client = None
        logger.info("MongoDB connection closed.")


def get_database() -> AsyncIOMotorDatabase:
    """
    Retrieve the active AsyncIOMotorDatabase instance.

    Raises:
        RuntimeError: If database connection has not been initialized.
    """
    if db.client is None:
        raise RuntimeError("Database client is not initialized. Call connect_to_mongo() first.")
    return db.client[settings.DATABASE_NAME]


def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    """
    Retrieve an AsyncIOMotorCollection instance by name.

    Args:
        collection_name: Name of the MongoDB collection.

    Returns:
        AsyncIOMotorCollection instance.
    """
    database = get_database()
    return database[collection_name]
