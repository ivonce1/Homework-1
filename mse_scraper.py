from _pydatetime import timedelta

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta
import time
import threading

base_url = "https://www.mse.mk/mk/issuers/free-market"
url_history = 'https://www.mse.mk/mk/stats/symbolhistory/'

def fetch_issuers_names():
    response = requests.get(base_url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    first_issuer = soup.select_one("#otherlisting-table > tbody > tr > td:nth-of-type(1)").text

    response = requests.get(url_history + first_issuer)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    element_codes = soup.select("#Code > option")
    issuers_names = []
    for code in element_codes:
        if not any(char.isdigit() for char in code.text):
            issuers_names.append(code.text)

    return issuers_names

def fetch_issuer_data(code, from_date, to_date):
    url = (
        f"https://www.mse.mk/mk/stats/symbolhistory/{code}"
        f"?FromDate={from_date.strftime('%d.%m.%Y')}"
        f"&ToDate={to_date.strftime('%d.%m.%Y')}"
    )

    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    element_data_rows = soup.select("#resultsTable tbody tr")
    matrix = []
    for row in element_data_rows:
        data = [code]
        for cell in row.select("td"):
            data.append(cell.text)

        matrix.append(data)

    return matrix

def last_available_date(code):
    data_frame = pd.read_csv("data/data_frame_" + code + ".csv")
    last_date = pd.to_datetime(data_frame['Датум'], format='%m/%d/%Y').max()
    print(last_date)

def fetch_issuers_history_sync(issuers_codes):
    current_date = datetime.now()

    for code in issuers_codes:
        from_date = current_date - timedelta(days=365 * 10)
        matrix = []
        while from_date <= current_date:
            to_date = from_date + timedelta(days=365)
            matrix.extend(fetch_issuer_data(code, from_date, to_date))
            from_date = to_date

        columns = ['Шифра на фирма', 'Датум', 'Цена на последна трансакција', 'Мак.', 'Мин.', 'Просечна цена', '%пром.', 'Количина', 'Промет во БЕСТ во денари', 'Вкупен промет во денари']
        data_frame = pd.DataFrame(matrix, columns=columns)
        data_frame.to_csv("data/data_frame_" + code + ".csv", index=False)
        print(code)
        print(data_frame)

def is_empty_frame(issuers_codes):
    for code in issuers_codes:
        df = pd.read_csv("data/data_frame_" + code + ".csv")
        if df.empty:
            fetch_issuers_history_sync([code])

start_time = time.time()
codes = fetch_issuers_names()
fetch_issuers_history_sync(codes)
is_empty_frame(codes)
end_time = time.time()
print(start_time, end_time, (end_time - start_time) / 60)
