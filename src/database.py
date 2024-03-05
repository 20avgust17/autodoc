from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from config import settings

live_engine = create_engine(
    settings.database_url_live,
    poolclass=QueuePool,
    pool_size=50,
    max_overflow=20
)
SessionLocalLive = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=live_engine
)
