from fastapi import APIRouter
from data_ingestion.filings_scraper import scrape_sec_filings

router = APIRouter()

@router.get("/scrape_filings")
def scrape_filings(ticker: str):
    links = scrape_sec_filings(ticker)
    return {"filing_links": links}
