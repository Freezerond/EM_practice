Тема 2. Базы данных
Задание 2.
Парсер скачивает и обрабатывает бюллетени торгов нефтепродуктами с сайта https://spimex.com/markets/oil_products/trades/results начиная с 2023 года. На момент 16 сентября 2025 года в 16:46 в бд были сохранены 138017 записей. Скрипт отработал за 540,19 секунд.


Список зависимостей:

aiohttp;
BeautifulSoup;

pandas;

xlrd;

SQLAlchemy (async);

asyncpg. 


Архитектура проекта:

zadanie_2/

│
├── .env

├── main.py    

├── parser.py  

├── requirements.txt

├── database/          

│   ├── config.py        

│   ├── database.py        

│   ├── spimex_trading_results.py   

│   └── queries/

│       └── orm.py     

в папке database всё что связано с базой данных: в spimex_trading_results.py описана таблица, в папке queries в orm.py функция для создания таблицы spimex_trading_results и функция по добавлению новой записи.

parser.py - в нём находится скриптя по сбору данных и записи их в бд.

main.py - запуск скрипта

 
Из каждого бюллетеня извлекаются следующие данные:

exchange_product_id — код инструмента;

exchange_product_name — название инструмента;

oil_id — первые 4 символа кода инструмента;

delivery_basis_id — символы 5–7 кода инструмента;

delivery_basis_name — базис поставки;

delivery_type_id — последний символ кода инструмента;

volume — объем договоров;

total — сумма договоров в рублях;

count — количество договоров;

date — дата торгов;

created_on, updated_on — даты создания и обновления записи в БД.


Данные сохраняются в PostgreSQL через SQLAlchemy с асинхронным доступом.


