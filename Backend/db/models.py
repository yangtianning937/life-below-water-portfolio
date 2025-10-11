from typing import Optional, List

from sqlalchemy import String, Float, Date, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime as dt

from db.db import Base


class SiteMetadata(Base):
    __tablename__ = "site_metadata"

    site_id: Mapped[str] = mapped_column(Text, primary_key=True)
    site_name_short: Mapped[Optional[str]] = mapped_column(Text)

    latitude: Mapped[Optional[float]] = mapped_column(Float)
    longitude: Mapped[Optional[float]] = mapped_column(Float)

    latest_date: Mapped[Optional[dt.date]] = mapped_column(Date)
    cutoff_date: Mapped[Optional[dt.date]] = mapped_column(Date)

    records_count: Mapped[Optional[int]] = mapped_column(Integer)

    # means
    do_mg_mean: Mapped[Optional[float]] = mapped_column(Float)
    tss_mean: Mapped[Optional[float]] = mapped_column(Float)
    sal_mean: Mapped[Optional[float]] = mapped_column(Float)
    n_total_mean: Mapped[Optional[float]] = mapped_column(Float)
    p_po4_mean: Mapped[Optional[float]] = mapped_column(Float)
    p_total_mean: Mapped[Optional[float]] = mapped_column(Float)

    # average scores and labels
    avg_water_quality_score: Mapped[Optional[float]] = mapped_column(Float)
    avg_quality_level: Mapped[Optional[int]] = mapped_column(Integer)
    avg_quality_label: Mapped[Optional[str]] = mapped_column(Text)

    do_mg_avg_score: Mapped[Optional[float]] = mapped_column(Float)
    tss_avg_score: Mapped[Optional[float]] = mapped_column(Float)
    sal_avg_score: Mapped[Optional[float]] = mapped_column(Float)
    n_total_avg_score: Mapped[Optional[float]] = mapped_column(Float)
    p_po4_avg_score: Mapped[Optional[float]] = mapped_column(Float)
    p_total_avg_score: Mapped[Optional[float]] = mapped_column(Float)

    avg_water_quality_simple: Mapped[Optional[str]] = mapped_column(Text)

    # children
    records: Mapped[List["WaterQualityData"]] = relationship(
        back_populates="site",
        passive_deletes=True,  # Relies on database ON DELETE CASCADE
    )


class WaterQualityData(Base):
    __tablename__ = "water_quality_data"

    record_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    site_id: Mapped[str] = mapped_column(
        Text,
        ForeignKey("site_metadata.site_id", ondelete="CASCADE"),
        nullable=False,
    )

    site_name_short: Mapped[Optional[str]] = mapped_column(Text)
    water_body: Mapped[Optional[str]] = mapped_column(Text)

    date: Mapped[Optional[dt.date]] = mapped_column(Date)
    type: Mapped[Optional[str]] = mapped_column(Text)

    # raw measures
    do_mg: Mapped[Optional[float]] = mapped_column(Float)
    sal: Mapped[Optional[float]] = mapped_column(Float)
    tss: Mapped[Optional[float]] = mapped_column(Float)
    n_total: Mapped[Optional[float]] = mapped_column(Float)
    p_po4: Mapped[Optional[float]] = mapped_column(Float)
    p_total: Mapped[Optional[float]] = mapped_column(Float)

    # scores and labels
    water_quality_score: Mapped[Optional[float]] = mapped_column(Float)

    do_mg_score: Mapped[Optional[float]] = mapped_column(Float)
    tss_score: Mapped[Optional[float]] = mapped_column(Float)
    sal_score: Mapped[Optional[float]] = mapped_column(Float)
    n_total_score: Mapped[Optional[float]] = mapped_column(Float)
    p_po4_score: Mapped[Optional[float]] = mapped_column(Float)
    p_total_score: Mapped[Optional[float]] = mapped_column(Float)

    quality_level: Mapped[Optional[int]] = mapped_column(Integer)
    quality_label: Mapped[Optional[str]] = mapped_column(Text)
    water_quality_simple: Mapped[Optional[str]] = mapped_column(Text)

    # relationship back to site
    site: Mapped["SiteMetadata"] = relationship(
        back_populates="records",
        lazy="joined",
    )
