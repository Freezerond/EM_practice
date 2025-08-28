import datetime
from datetime import date

from bs4 import BeautifulSoup


def parse_page_links(html: str, start_date: date, end_date: date) -> List[Tuple[str, date]]: # убран параметр url, поскольку в функции он не используется
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>
    """
    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", class_="accordeon-inner__item-title link xls")

    for link in links:
        href = link.get("href")
        if not href:
            continue

        href = href.split("?")[0]
        if not ("/upload/reports/oil_xls/oil_xls_" in href and href.endswith(".xls")):
            continue

        try:
            date_bulletin = href.split("oil_xls_")[1][:8] # название переменной изменено с date на date_bulletin, чтобы не перекрывать импортированный date из datetime
            file = datetime.datetime.strptime(date_bulletin, "%Y%m%d").date()
            if start_date <= file <= end_date:
                u = href if href.startswith("http") else f"https://spimex.com{href}"
                results.append((u, file))
            else:
                print(f"Ссылка {href} вне диапазона дат")
        except Exception as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")

    return results