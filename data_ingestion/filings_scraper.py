import requests
from bs4 import BeautifulSoup

def scrape_sec_filings(ticker: str):
    base_url = "https://www.sec.gov"
    target_url = f"{base_url}/cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-K"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [base_url + a["href"] for a in soup.select("a[href*='Archives']")[:5]]
    return links
