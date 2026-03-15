from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from db import Base

class Runner(Base):
    __tablename__ = "runners"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    height_in = Column(Integer)
    weight_lbs = Column(Integer)
    gender = Column(String(20))  # optional, can be used for more accurate pace/HR zone calculations if you want to add that later

    age = Column(Integer)  # optional, can be calculated from DOB if you want to add that later

    threshold_hr = Column(Integer)  # optional, can be calculated from max HR if you want to add that later
    threshold_pace_s = Column(Integer)  # optional, can be calculated from splits if you want to add that later
    
    total_runs = Column(Integer, default=0)
    total_distance_m = Column(Numeric(12, 2), default=0)

    fivek_PR_time_s = Column(Integer)  # optional, can be calculated from splits if you want to add that later
    tenK_PR_time_s = Column(Integer)
    half_marathon_PR_time_s = Column(Integer)
    marathon_PR_time_s = Column(Integer)

    resting_hr = Column(Integer)  # optional, can be calculated from fit data if you want to add that later
    maximum_hr = Column(Integer)  # optional, can be calculated from fit data if you want to add that later
    # recovery_hr_min = Column(Integer)  # optional, can be calculated from fit data if you want to add that later
    recovery_hr_max = Column(Integer)  # optional, can be calculated from fit data if you want to add that later
    aerobic_hr_min = Column(Integer)  # optional, can be calculated from fit data if you want to add that later
    aerobic_hr_max = Column(Integer)  # optional, can be calculated from fit data if

    # runs = relationship("Run", back_populates="runner")

    def __repr__(self):
        return f"<Runner(id={self.id}, name='{self.name}')>"