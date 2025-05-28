from fastapi import APIRouter
from data_ingestion.market_data import fetch_market_data

router = APIRouter()

@router.get("/market_data")
def get_market_data(symbol: str):
    data = fetch_market_data(symbol)
    return data
