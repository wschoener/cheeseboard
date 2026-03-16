"""
Example data:
---
 * activity_type: running
 * distance: 0.0 (m)
 * heart_rate: 83 (bpm)
 * position_lat: 504500163 (semicircles)
 * position_long: -999275486 (semicircles)
 * timestamp: 2026-03-10 12:08:03
---
 * Effort Pace: 1.3359999656677246 (m/s)
 * activity_type: running
 * distance: 0.0 (m)
 * enhanced_speed: 1.336 (m/s)
 * heart_rate: 84 (bpm)
 * position_lat: 504500345 (semicircles)
 * position_long: -999275459 (semicircles)
 * speed: 1.336 (m/s)
 * stance_time: 0.0 (ms)
 * step_length: 400.0 (mm)
 * timestamp: 2026-03-10 12:08:04
 * vertical_oscillation: 0.0 (mm)
 * vertical_ratio: 0.0 (percent)
---
 * Effort Pace: 1.8519999980926514 (m/s)
 * activity_type: running
 * distance: 0.0 (m)
 * enhanced_speed: 1.853 (m/s)
 * heart_rate: 85 (bpm)
 * position_lat: 504500527 (semicircles)
 * position_long: -999275433 (semicircles)
 * speed: 1.853 (m/s)
 * stance_time: 0.0 (ms)
 * step_length: 800.0 (mm)
 * timestamp: 2026-03-10 12:08:05
 * vertical_oscillation: 0.0 (mm)
 * vertical_ratio: 0.0 (percent)
---

"""
import uuid
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db import Base

class FitData(Base):
    __tablename__ = "fit_data"
    
    id = Column(Integer, primary_key=True)
    run_id = Column(UUID(as_uuid=True), ForeignKey("runs.id"), nullable=False)    
    timestamp = Column(DateTime, nullable=False)

    elevation = Column(Numeric(10, 2))  # m 
    heart_rate = Column(Integer)  # bpm
    position_lat = Column(Float)  # semicircles converted to degrees
    position_long = Column(Float)  # semicircles converted to degrees
    speed = Column(Numeric(10, 4))  # m/s
    step_length = Column(Numeric(10, 2))  # mm
    cadence = Column(Integer)  # spm
    heart_rate = Column(Integer)  # bpm
    heart_rate_zone = Column(Integer)  # 1-5  

    power = Column(Integer)  # watts  
