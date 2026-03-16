import uuid
from sqlalchemy import Column, Integer, String, Numeric, Date, DateTime, Interval, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from db import Base


class Run(Base):
    __tablename__ = "runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)    
    start_date_time    = Column(DateTime)       # when the run started (not necessarily the same as the file creation time)
    name          = Column(String(200))                # activity name from .fit file
    distance_m    = Column(Numeric(10, 2))             # meters — convert to miles/km in display
    run_duration_s    = Column(Integer)                    # seconds
    total_duration_s  = Column(Float)                    # seconds — includes pauses
    avg_pace_s    = Column(Float)                    # seconds per mile — you calculate this

    total_power = Column(Integer)  # watts * seconds, can be used to calculate Training Stress Score (TSS) if you want to add that later
    
    avg_hr        = Column(Integer)                    # bpm
    max_hr        = Column(Integer)
    time_in_zone_1 = Column(Interval)                   # time in HR zone 1 (recovery)
    time_in_zone_2 = Column(Interval)                   # time in HR zone 2 (endurance)
    time_in_zone_3 = Column(Interval)                   # time in HR zone 3 (threshold)
    time_in_zone_4 = Column(Interval)                   # time in HR zone 4 (VO2 max)
    time_in_zone_5 = Column(Interval)                   # time in HR zone 5 (anaerobic)

    elevation_gain_m = Column(Numeric(8, 2))
    imported_at   = Column(DateTime, server_default=func.now())

    # runner_id     = Column(Integer, ForeignKey("runners.id"), nullable=False)
    # runner        = relationship("Runner", back_populates="runs")

    def distance_miles(self):
        """TODO: convert self.distance_m to miles and return."""
        pass

    def duration_formatted(self):
        """TODO: format self.duration_s as HH:MM:SS and return."""
        pass

    def pace_formatted(self):
        """TODO: format self.avg_pace_s as MM:SS /mi and return."""
        pass

    def __repr__(self):
        return f"<Run {self.start_date_time} {self.distance_m}m>"
