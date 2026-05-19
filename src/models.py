from sqlalchemy import Column, String, Float, ForeignKey, Boolean, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Well(Base):
    __tablename__ = 'Well'
    Id = Column(UUID, primary_key=True)
    WellName = Column(String(255), unique=True)
    WellType = Column(String(255))

class WellPhaseDrilling(Base):
    __tablename__ = 'WellPhaseDrilling'
    Id = Column(UUID, primary_key=True)
    WellId = Column(UUID, ForeignKey('Well.Id'))
    DrillingMinStandard = Column(String(100))
    PlanDdptf = Column(Float)
    PlanDcpf = Column(Float)
    PlanWcpf = Column(Float)
    ActualDdptf = Column(Float)
    ActualDcpf = Column(Float)
    ActualWcpf = Column(Float)

class WellGeneralDetails(Base):
    __tablename__ = 'WellGeneralDetails'
    Id = Column(UUID, primary_key=True)
    WellId = Column(UUID, ForeignKey('Well.Id'))
    isDeleted = Column(Boolean, default=False)
