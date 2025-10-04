import requests
from bs4 import BeautifulSoup
import re

def fetch_page(url: str, timeout: int = 15):
    """Загружает HTML-страницу и возвращает soup или сообщение об ошибке."""
    if not url or not isinstance(url, str):
        return None, "Error: Invalid or empty URL. Please provide a valid product link."

    if not re.match(r"^https?://", url.strip()):
        return None, "Error: Invalid URL format. Must start with http:// or https://"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/108.0.0.0 Safari/537.36"
        )
    }

    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code in (404, 410):
            return None, f"Error: Product page does not exist (HTTP {e.response.status_code})."
        return None, f"Error: HTTP request failed with status code {e.response.status_code}."
    except requests.exceptions.Timeout:
        return None, "Error: Request timed out."
    except requests.exceptions.RequestException as e:
        return None, f"Error: Network error: {str(e)}"

    soup = BeautifulSoup(r.text, "lxml")

    # Проверка на признаки пустого товара
    page_text = soup.get_text(" ", strip=True).lower()
    if any(kw in page_text for kw in [
        "out of stock", "sold out", "currently unavailable",
        "no longer available", "not available"
    ]):
        return None, "Error: Product exists but is not available (out of stock / discontinued)."

    return soup, None
