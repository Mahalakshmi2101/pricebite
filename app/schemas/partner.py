from datetime import time
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class AvoidArea(BaseModel):
    name: str
    reason: Optional[str] = None


class PartnerPreferenceResponse(BaseModel):
    id: int
    user_id: int
    no_delivery_after: Optional[time] = None
    avoid_areas: Optional[List[AvoidArea]] = None

    model_config = ConfigDict(from_attributes=True)


class PartnerPreferenceUpdate(BaseModel):
    no_delivery_after: Optional[time] = None
    avoid_areas: Optional[List[AvoidArea]] = None

    @field_validator("avoid_areas", mode="before")
    @classmethod
    def coerce_avoid_areas(cls, v):
        if v is None:
            return v
        if not isinstance(v, list):
            raise ValueError("avoid_areas must be a list")
        if len(v) > 20:
            raise ValueError("Maximum 20 blocked areas allowed")
        return v