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

-- 1. Site metadata (includes averages + classification info)
CREATE TABLE site_metadata (
    site_id TEXT PRIMARY KEY,
    site_name_short TEXT,
    latitude FLOAT8,
    longitude FLOAT8,
    latest_date DATE,
    cutoff_date DATE,
    records_count INT,
    DO_mg_mean FLOAT8,
    TSS_mean FLOAT8,
    Sal_mean FLOAT8,
    N_TOTAL_mean FLOAT8,
    P_PO4_mean FLOAT8,
    P_TOTAL_mean FLOAT8,
    avg_water_quality_score FLOAT8,
    avg_quality_level INT,
    avg_quality_label TEXT,
    DO_mg_avg_score FLOAT8,
    TSS_avg_score FLOAT8,
    Sal_avg_score FLOAT8,
    N_TOTAL_avg_score FLOAT8,
    P_PO4_avg_score FLOAT8,
    P_TOTAL_avg_score FLOAT8,
    avg_water_quality_simple TEXT
);

-- 2. Water quality records (raw + classified data per measurement)
CREATE TABLE water_quality_data (
    record_id SERIAL PRIMARY KEY,
    site_id TEXT NOT NULL,
    site_name_short TEXT,
    water_body TEXT,
    date DATE,
    type TEXT,
    DO_mg FLOAT8,
    Sal FLOAT8,
    TSS FLOAT8,
    N_TOTAL FLOAT8,
    P_PO4 FLOAT8,
    P_TOTAL FLOAT8,
    water_quality_score FLOAT8,
    DO_mg_score FLOAT8,
    TSS_score FLOAT8,
    Sal_score FLOAT8,
    N_TOTAL_score FLOAT8,
    P_PO4_score FLOAT8,
    P_TOTAL_score FLOAT8,
    quality_level INT,
    quality_label TEXT,
    water_quality_simple TEXT,
    CONSTRAINT fk_site FOREIGN KEY (site_id)
        REFERENCES site_metadata (site_id)
        ON DELETE CASCADE
);
'''
