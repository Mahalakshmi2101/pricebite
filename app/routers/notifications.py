"""
app/routers/notifications.py
Notification endpoints — personal, Swiggy-style messages per user.
GET  /notifications        — list all notifications for current user
PATCH /notifications/{id}/read — mark one notification as read
PATCH /notifications/read-all  — mark all as read
POST /notifications/seed   — dev-only: seed sample notifications for testing
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.deps import get_db, get_current_user
from app.models.user import User
from app.models.stubs import Notification
from app.schemas.notification import NotificationListResponse, NotificationResponse

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=NotificationListResponse)
def list_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = (
        select(Notification)
        .where(Notification.user_id == current_user.id)
        .order_by(Notification.created_at.desc())
    )
    notifications = db.execute(stmt).scalars().all()

    unread = sum(1 for n in notifications if not n.is_read)

    return NotificationListResponse(
        total=len(notifications),
        unread_count=unread,
        items=notifications
    )


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Notification).where(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    )
    notif = db.execute(stmt).scalar_one_or_none()

    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.is_read = True
    db.commit()
    db.refresh(notif)
    return notif


@router.patch("/read-all")
def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = select(Notification).where(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    )
    unread = db.execute(stmt).scalars().all()
    for n in unread:
        n.is_read = True
    db.commit()
    return {"marked_read": len(unread)}


@router.post("/seed", status_code=201)
def seed_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Dev-only endpoint: seeds 4 sample notifications for the logged-in user."""
    samples = [
        {
            "type": "price_drop",
            "title": "Price drop on Chicken Biryani 🎉",
            "body": "Buhari Hotel dropped Chicken Biryani from ₹290 to ₹245. Your saved dish is now cheaper!"
        },
        {
            "type": "best_time",
            "title": "Best time to order now 🕐",
            "body": "Mutton Biryani at Dindigul Thalappakatti is ₹40 cheaper between 2pm–5pm today. Order now!"
        },
        {
            "type": "combo",
            "title": "Combo deal found 🍱",
            "body": "Biryani + Lassi + Gulab Jamun cheapest combo today: A2B (₹330 total). Save ₹85 vs Copper Chimney."
        },
        {
            "type": "order_update",
            "title": "Hey, you haven't ordered in a while 👀",
            "body": "Murugan Idli Shop has a new Ghee Podi Idli offer. You loved it last time — ₹130 only today."
        }
    ]

    for s in samples:
        db.add(Notification(user_id=current_user.id, **s))

    db.commit()
    return {"seeded": len(samples)}