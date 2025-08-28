import datetime
from datetime import date

from bs4 import BeautifulSoup


def parse_page_links(html, start_date, end_date, url="https://spimex.com"):
    """
    Парсит ссылки на бюллетени с одной страницы:
    <a class="accordeon-inner__item-title link xls" href="/upload/reports/oil_xls/oil_xls_20240101_test.xls">link1</a>

    Args:
        html (str): HTML страницы.
        start_date (date): Начальная дата диапазона.
        end_date (date): Конечная дата диапазона.
        url (str): Базовый URL для относительных ссылок.

    Returns:
        list[tuple[str, date]]: Список (ссылка, дата).
    """

    results = []
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("a.accordeon-inner__item-title link xls") # find_all заменён на select

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
        except Exception as e:
            print(f"Не удалось извлечь дату из ссылки {href}: {e}")
            continue

        if start_date <= file <= end_date:
            u = href if href.startswith("http") else f"{url}{href}"
            results.append((u, file))
        # больше не выводим ссылки, которые нам не подошли
        
    return results

