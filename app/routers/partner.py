"""
app/routers/partner.py
Delivery partner safety preference endpoints.
GET  /partner/preferences  — fetch current partner's safety settings
PATCH /partner/preferences — update cutoff time and blocked areas
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User, UserRole
from app.models.stubs import PartnerPreference
from app.schemas.partner import PartnerPreferenceResponse, PartnerPreferenceUpdate

router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


def require_partner(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.DELIVERY_PARTNER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only delivery partners can access this endpoint"
        )
    return current_user


@router.get("/preferences", response_model=PartnerPreferenceResponse)
def get_preferences(
    current_user: User = Depends(require_partner),
    db: Session = Depends(get_db)
):
    stmt = select(PartnerPreference).where(PartnerPreference.user_id == current_user.id)
    pref = db.execute(stmt).scalar_one_or_none()

    if not pref:
        # Auto-create default empty preferences on first fetch
        pref = PartnerPreference(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)

    return pref


@router.patch("/preferences", response_model=PartnerPreferenceResponse)
def update_preferences(
    payload: PartnerPreferenceUpdate,
    current_user: User = Depends(require_partner),
    db: Session = Depends(get_db)
):
    stmt = select(PartnerPreference).where(PartnerPreference.user_id == current_user.id)
    pref = db.execute(stmt).scalar_one_or_none()

    if not pref:
        pref = PartnerPreference(user_id=current_user.id)
        db.add(pref)

    if payload.no_delivery_after is not None:
        pref.no_delivery_after = payload.no_delivery_after

    if payload.avoid_areas is not None:
        # Store as list of dicts — JSON column accepts this directly
        pref.avoid_areas = [area.model_dump() for area in payload.avoid_areas]

    db.commit()
    db.refresh(pref)
    return pref