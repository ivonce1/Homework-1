import os.path
from _pydatetime import timedelta
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime, timedelta
import time


def fetch_issuers_names(base_url, url_history):
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

        print(f"Data for {code} saved with {data_frame.shape[0]} rows")

def fetch_issuers_history_threads(issuers_codes):
    current_date = datetime.now()

    def process_issuer(code):
        from_date = current_date - timedelta(days=365 * 10)
        matrix = []

        while from_date < current_date:
            to_date = from_date + timedelta(days=365)
            matrix.extend(fetch_issuer_data(code, from_date, to_date))
            from_date = to_date

        columns = ['Шифра на фирма', 'Датум', 'Цена на последна трансакција', 'Мак.', 'Мин.', 'Просечна цена', '%пром.', 'Количина', 'Промет во БЕСТ во денари', 'Вкупен промет во денари']
        data_frame = pd.DataFrame(matrix, columns=columns)
        data_frame.to_csv("data/data_frame_" + code + ".csv", index=False)
        print(f"Data for {code} saved with {data_frame.shape[0]} rows")

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_issuer, issuers_codes)


def get_last_available_date(issuer_code):
    file_path = "data/data_frame_" + issuer_code + ".csv"
    if not os.path.exists(file_path):
        return None

    df = pd.read_csv(file_path)
    df["Датум"] = pd.to_datetime(df["Датум"], format="%d.%m.%Y")
    available_date = df['Датум'].max().date()

    return available_date


def check_empty_frame(issuer_codes):
    empty_codes = []
    for issuer_code in issuer_codes:
        last_available = get_last_available_date(issuer_code)
        if last_available != datetime.today().date() or last_available is None:
            empty_codes.append(issuer_code)

    fetch_issuers_history_threads(empty_codes)

def main():
    base_url = "https://www.mse.mk/mk/issuers/free-market"
    url_history = 'https://www.mse.mk/mk/stats/symbolhistory/'

    codes = fetch_issuers_names(base_url, url_history)

    if not os.path.exists("data"):
        os.mkdir("data")
        fetch_issuers_history_threads(codes)
    else:
        check_empty_frame(codes)



if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(start_time, end_time, (end_time - start_time) / 60)
