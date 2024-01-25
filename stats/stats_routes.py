from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from fastapi.responses import JSONResponse
from stats.model.models import WaterUsage
from stats.schemas.schemas import WaterSaverRequest, MonthlyStatsRequest, MonthlyStatsResponse, DuringStatsRequest, DuringStatsResponse
from config import SessionLocal

stats_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@stats_router.post("/update")
async def update_water_usage(request: WaterSaverRequest, db: Session = Depends(get_db)):
    existing_data = db.query(WaterUsage).filter(
        WaterUsage.user_id == request.userId,
        WaterUsage.date == request.date
    ).first()

    if existing_data:
        # 이미 데이터가 존재하면 값을 업데이트
        existing_data.amount += request.amount
        existing_data.time += request.time
        existing_data.tax += request.tax
    else:
        # 데이터가 없으면 새로운 레코드 삽입
        new_data = WaterUsage(
            user_id=request.user_id,
            date=request.date,
            amount=request.amount,
            time=request.time,
            tax=request.tax
        )
        db.add(new_data)

    # 변경사항을 커밋
    db.commit()

@stats_router.post("/", response_model=MonthlyStatsResponse)
async def get_monthly_stats(request: MonthlyStatsRequest, db: Session = Depends(get_db)):
    try:
        result1 = db.query(
            func.SUM(WaterUsage.amount).label("total_amount"),
            func.SUM(WaterUsage.time).label("total_time"),
            func.SUM(WaterUsage.tax).label("total_tax")
        ).filter(
            WaterUsage.user_id == request.userId,
            func.DATE_FORMAT(WaterUsage.date, '%Y-%m') == request.month
        ).first()

        result2 = db.query(
                WaterUsage.date, 
                WaterUsage.amount, 
                WaterUsage.time, 
                WaterUsage.tax
            ).filter(
            WaterUsage.user_id == request.userId,
            func.DATE_FORMAT(WaterUsage.date, '%Y-%m') == request.month
        ).all()

        water_usage_list = [
            {
                "date": str(record.date),
                "amount": float(record.amount),
                "time": int(record.time),
                "tax": float(record.tax),
            }
            for record in result2
        ]

        if not result1 or not result2:
            raise HTTPException(status_code=404, detail="No data found for the specified user and month")

        # 결과를 API 응답 모델로 매핑
        response_data = {
            "month": request.month,
            "total_amount": float(result1.total_amount),
            "total_time": int(result1.total_time),
            "total_tax": float(result1.total_tax),
            "water_used_list": water_usage_list
        }

        return MonthlyStatsResponse(**response_data)

    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)


@stats_router.post("/during", response_model=DuringStatsResponse)
async def get_during_stats(request: DuringStatsRequest, db: Session = Depends(get_db)):
    try:
        result1 = db.query(
            func.SUM(WaterUsage.amount).label("total_amount"),
            func.SUM(WaterUsage.time).label("total_time"),
            func.SUM(WaterUsage.tax).label("total_tax")
        ).filter(
            WaterUsage.user_id == request.userId,
            func.DATE_FORMAT(WaterUsage.date, '%Y-%m-%d') >= request.start_date,
            func.DATE_FORMAT(WaterUsage.date, '%Y-%m-%d') <= request.end_date
        ).first()

        result2 = db.query(
                WaterUsage.date, 
                WaterUsage.tax
        ).filter(
            WaterUsage.user_id == request.userId,
            func.DATE_FORMAT(WaterUsage.date, '%Y-%m-%d') >= request.start_date,
            func.DATE_FORMAT(WaterUsage.date, '%Y-%m-%d') <= request.end_date
        ).all()

        water_tax_list = [
            {
                "date": str(record.date),
                "tax": float(record.tax),
            }
            for record in result2
        ]

        print(result1)
        print(result2)

        if not result1 or not result2:
            raise HTTPException(status_code=500, detail="No data found for the specified user during dates")

        # 결과를 API 응답 모델로 매핑
        response_data = {
            "start_date": str(request.start_date),
            "end_date" : str(request.end_date),
            "total_tax": float(result1.total_tax),
            "total_amount": float(result1.total_amount),
            "total_time": int(result1.total_time),
            "water_tax_list": water_tax_list
        }

        return DuringStatsResponse(**response_data)

    except Exception as e:
        return JSONResponse(content={"detail": str(e)}, status_code=500)
