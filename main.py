import requests
from bs4 import BeautifulSoup

url: str = 'https://www.pochta.ru/support/database/ops'
domen: str = 'https://www.pochta.ru'


def get_page(link):
    try:
        return requests.get(link)
    except requests.exceptions.HTTPError as e:
        return "Error: " + str(e)


def parse_page(page):
    soup = BeautifulSoup(page.text, "html.parser")
    assets_link = [a['href'] for a in soup.findAll('a', href=True) if "Pindx.zip" in a.text][0]
    if not assets_link:
        assets_link = [a['href'] for a in soup.findAll('a', href=True) if "assets" in a.get('href')][0]
    return assets_link


def download_asset(download_link, save_path, chunk_size=128):
    print(download_link)
    r = requests.get(download_link, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


if __name__ == "__main__":
    try:
        page = get_page(url)
        asset_link = parse_page(page)
        download_asset(domen + asset_link, 'E:/Analytics/Temp/CR/Pochta_index.zip')
    except Exception as err:
        with open('E:/Analytics/Temp/CR/log.txt', 'w') as log:
            log.write(f'Unexpected {err}, {type(err)} , {__file__} , {err.__traceback__.tb_lineno}')
