from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends

from core.database import db
from core.security import STAFF_ROLES, require_roles

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
async def dashboard_stats(user: dict = Depends(require_roles(*STAFF_ROLES))):
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()

    total_patients = await db.patients.count_documents({"is_active": True})
    new_patients_this_month = await db.patients.count_documents(
        {"is_active": True, "created_at": {"$gte": month_start}}
    )
    appointments_today = await db.appointments.count_documents({"appointment_date": today})
    completed_today = await db.appointments.count_documents(
        {"appointment_date": today, "status": "completed"}
    )

    status_agg = await db.appointments.aggregate([
        {"$match": {"appointment_date": today}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
    ]).to_list(20)
    appointments_by_status = {item["_id"]: item["count"] for item in status_agg}

    gender_agg = await db.patients.aggregate([
        {"$match": {"is_active": True}},
        {"$group": {"_id": "$gender", "count": {"$sum": 1}}},
    ]).to_list(10)
    gender_distribution = {item["_id"]: item["count"] for item in gender_agg}

    days = [(now - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    trend_agg = await db.appointments.aggregate([
        {"$match": {"appointment_date": {"$in": days}}},
        {"$group": {"_id": "$appointment_date", "count": {"$sum": 1}}},
    ]).to_list(10)
    trend_map = {item["_id"]: item["count"] for item in trend_agg}
    appointments_trend = [{"date": d, "count": trend_map.get(d, 0)} for d in days]

    upcoming = (
        await db.appointments.find(
            {"appointment_date": today, "status": {"$nin": ["completed", "cancelled", "no_show"]}},
            {"_id": 0},
        )
        .sort("appointment_time", 1)
        .limit(6)
        .to_list(6)
    )

    recent_patients = (
        await db.patients.find({"is_active": True}, {"_id": 0})
        .sort("created_at", -1)
        .limit(5)
        .to_list(5)
    )

    total_doctors = await db.users.count_documents({"role": "doctor", "is_active": True})

    return {
        "total_patients": total_patients,
        "new_patients_this_month": new_patients_this_month,
        "appointments_today": appointments_today,
        "completed_today": completed_today,
        "total_doctors": total_doctors,
        "appointments_by_status": appointments_by_status,
        "gender_distribution": gender_distribution,
        "appointments_trend": appointments_trend,
        "upcoming_appointments": upcoming,
        "recent_patients": recent_patients,
    }
