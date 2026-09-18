from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    JSON
)

from datetime import datetime

from database import Base


class DetectionEvent(Base):

    __tablename__ = "detection_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    video_name = Column(
        String(255),
        nullable=False,
        index=True
    )

    event_type = Column(
        String(100),
        nullable=False
    )

    class_name = Column(
        String(100),
        nullable=False,
        index=True
    )

    confidence = Column(
        Numeric(5, 4),
        nullable=False
    )

    timestamp = Column(
        DateTime,
        nullable=False
    )

    frame_number = Column(
        Integer,
        nullable=True
    )

    json_data = Column(
        JSON,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )