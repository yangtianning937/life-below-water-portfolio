from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, Date, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base

from Backend.db.db import Base


class SiteMetadata(Base):
    __tablename__ = "site_metadata"

    site_id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    site_name_long: Mapped[str | None] = mapped_column(String)
    site_name_short: Mapped[str | None] = mapped_column(String, index=True)
    water_body: Mapped[str | None] = mapped_column(String, index=True)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)

    measurements: Mapped[list["WaterQualityData"]] = relationship(
        "WaterQualityData", back_populates="site", cascade="all, delete-orphan"
    )

class WaterQualityData(Base):
    __tablename__ = "water_quality_data"

    record_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    site_id: Mapped[str] = mapped_column(String, ForeignKey("site_metadata.site_id"), index=True)
    site_name_short: Mapped[str | None] = mapped_column(String)
    water_body: Mapped[str | None] = mapped_column(String, index=True)
    date: Mapped["Date | None"] = mapped_column(Date, index=True)
    type: Mapped[str | None] = mapped_column(String)

    do_mg: Mapped[float | None] = mapped_column(Float)
    sal: Mapped[float | None] = mapped_column(Float)
    tss: Mapped[float | None] = mapped_column(Float)
    n_total: Mapped[float | None] = mapped_column(Float)
    p_po4: Mapped[float | None] = mapped_column(Float)
    p_total: Mapped[float | None] = mapped_column(Float)

    site: Mapped["SiteMetadata"] = relationship("SiteMetadata", back_populates="measurements")
