import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
from io import BytesIO
from datetime import datetime

from database.database import async_session_factory
from database.queries.orm import save_to_postgres

BASE_URL = "https://www.spimex.com"
RESULTS_URL = BASE_URL + "/markets/oil_products/trades/results/"


def parse_bulletin(raw_bytes: bytes) -> pd.DataFrame:
    df_all = pd.read_excel(BytesIO(raw_bytes), header=None, engine="xlrd")

    # ищем таблицу построчно начиная с 6-й строки
    start_idx = None
    for i in range(5, len(df_all)):
        row = df_all.iloc[i]
        if row.astype(str).str.contains("Единица измерения: Метрическая тонна").any():
            start_idx = i
            break
    if start_idx is None:
        raise ValueError("Таблица 'Единица измерения: Метрическая тонна' не найдена")

    header_idx = start_idx + 1
    df_table = pd.read_excel(BytesIO(raw_bytes), header=header_idx, engine="xlrd")
    df_table = df_table.dropna(how="all").reset_index(drop=True)
    df_table.columns = df_table.columns.str.strip().str.replace("\n", " ").str.replace("\r", "")

    colmap = {
        "Код Инструмента": "exchange_product_id",
        "Наименование Инструмента": "exchange_product_name",
        "Базис поставки": "delivery_basis_name",
        "Объем Договоров в единицах измерения": "volume",
        "Договоров, руб": "total",  # ищем по части названия
        "Количество Договоров, шт": "count"
    }

    colmap_clean = {}
    for key, new_name in colmap.items():
        for c in df_table.columns:
            if key.replace(" ", "").lower() in c.replace(" ", "").lower():
                colmap_clean[c] = new_name

    df_table = df_table[list(colmap_clean.keys())].rename(columns=colmap_clean)

    # останавливаемся на строке с "Итого:"
    stop_idx = df_table[df_table.apply(lambda x: x.astype(str).str.contains("Итого:").any(), axis=1)].index
    if len(stop_idx) > 0:
        df_table = df_table.loc[:stop_idx[0]-1]

    # преобразуем числовые колонки
    for num_col in ["volume", "total", "count"]:
        if num_col in df_table.columns:
            df_table[num_col] = pd.to_numeric(
                df_table[num_col].astype(str).str.replace(" ", "").str.replace(",", "."),
                errors="coerce"
            )

    if "count" in df_table.columns:
        df_table = df_table[df_table["count"] > 0]

    return df_table.reset_index(drop=True)


def extract_bulletins(html) -> list:
    soup = BeautifulSoup(html, "html.parser")
    blocks = soup.select("div.accordeon-inner__wrap-item")
    results = []
    for block in blocks:
        link_tag = block.select_one("a.accordeon-inner__item-title")
        date_tag = block.select_one("div.accordeon-inner__item-inner__title span")
        if link_tag and date_tag:
            file_url = BASE_URL + link_tag["href"]
            trade_date = datetime.strptime(date_tag.text.strip(), "%d.%m.%Y").date()
            results.append((trade_date, file_url))
    return results


async def process_bulletin(session, http_session, trade_date, file_url):
    async with http_session.get(file_url, headers={"User-Agent": "Mozilla/5.0"}) as r:
        raw = await r.read()
    df = parse_bulletin(raw)
    await save_to_postgres(session, df, trade_date)
    print(f"Сохранили бюллетень {trade_date}, {len(df)} строк")


async def main():
    async with async_session_factory() as session:
        async with aiohttp.ClientSession() as http_session:
            page = 1
            while True:
                # берём HTML страницу с бюллетенями
                async with http_session.get(f"{RESULTS_URL}?page=page-{page}", headers={"User-Agent": "Mozilla/5.0"}) as resp:
                    html = await resp.text()

                # получаем список бюллетеней на странице
                bulletins = extract_bulletins(html)
                bulletins = [(d, url) for d, url in bulletins if d.year >= 2023]
                if not bulletins:
                    break

                # обрабатываем каждый бюллетень и сохраняем нужные данные в бд
                for trade_date, file_url in bulletins:
                    await process_bulletin(session, http_session, trade_date, file_url)

                page += 1

