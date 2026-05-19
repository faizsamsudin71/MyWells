from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class WellDrillingSchema(BaseModel):
    """Schema for validating Excel data before DB update"""
    model_config = ConfigDict(from_attributes=True, coerce_numbers_to_str=True)

    WellName: str = Field(alias="Well Name")
    DrillingMinStandard: str = Field(alias="DMS")
    PlanDdptf: Optional[float] = Field(alias="Plan DDPTF", default=None)
    PlanDcpf: Optional[float] = Field(alias="Plan DCPF", default=None)
    PlanWcpf: Optional[float] = Field(alias="Plan WCPF", default=None)
    ActualDdptf: Optional[float] = Field(alias="Actual DDPTF", default=None)
    ActualDcpf: Optional[float] = Field(alias="Actual DCPF", default=None)
    ActualWcpf: Optional[float] = Field(alias="Actual WCPF", default=None)
