from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "postgres"
PASSWORD = "123456" # "Lakers123"
HOST = "localhost"
PORT = "5432" # "6543"
DATABASE = "postgres"
DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

''' SQL FOR CREATE TABLE

CREATE TABLE site_metadata (
    site_id TEXT PRIMARY KEY,
    site_name_long TEXT,
    site_name_short TEXT,
    water_body TEXT,
    latitude FLOAT8,
    longitude FLOAT8
);

select * from site_metadata;

CREATE TABLE water_quality_data (
    record_id SERIAL PRIMARY KEY, -- unique identifier for each row
    site_id TEXT NOT NULL,
    site_name_short TEXT,
    water_body TEXT,
    date DATE,
    type TEXT,
    do_mg FLOAT8,
    sal FLOAT8,
    tss FLOAT8,
    n_total FLOAT8,
    p_po4 FLOAT8,
    p_total FLOAT8,
    CONSTRAINT fk_site
        FOREIGN KEY (site_id)
        REFERENCES site_metadata (site_id)
        ON DELETE CASCADE
);

select * from water_quality_data;
'''
