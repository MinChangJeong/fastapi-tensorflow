from pydantic import BaseModel
from datetime import datetime
from typing import List

class WaterSaverRequest(BaseModel):
    userId : int
    date: str
    amount: float
    time: int
    tax: float

class MonthlyStatsRequest(BaseModel):
    userId: int
    month: str

class WaterUsageResponse(BaseModel):
    date: str
    amount: float
    time: int
    tax: float

class MonthlyStatsResponse(BaseModel):
    month: str
    total_tax: float
    total_amount: float
    total_time: int
    water_used_list: List[WaterUsageResponse]

class DuringStatsRequest(BaseModel):
    userId: int
    start_date: str
    end_date: str

class WaterTaxResponse(BaseModel): 
    date: str
    tax: int

class DuringStatsResponse(BaseModel): 
    start_date: str
    end_date: str
    total_tax: float
    total_amount: float
    total_time: int
    water_tax_list: List[WaterTaxResponse]