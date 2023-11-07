import re

import requests
import os
from bs4 import BeautifulSoup

path_to_save_pdf = ""
def get_links(min_range, max_range):
    base_url = 'https://www.laleggepertutti.it/page/{}?advanced&s&post_type=post&anno=-1&mese=-1&cat=-1'

    unique_links = set()
    # setting proxies was necessary because after a while the server detected unusual traffic and blocked requests
    proxies = {
        'http': f'https://myproxy'
    }

    for page_num in range(min_range, max_range):
        url = base_url.format(page_num)

        response = requests.get(url, proxies=proxies)

        soup = BeautifulSoup(response.content, 'html.parser')

        div = soup.find('div', class_='faq-section-left-grid row-fluid')

        anchors = div.find_all('a')

        href_values = [a.get('href') for a in anchors]
        unique_links.update(href_values)

    with open('links.txt', 'a') as file:
        for link in unique_links:
            file.write(link + '\n')


def get_pdfs(min_range, max_range):
    with open("links.txt", 'r') as file:
        links = file.read().splitlines()
    proxies = {
        'http': f'myproxy'
    }

    for index, link in enumerate(links[min_range:max_range]):
        response = requests.get(link + '?print=pdf', proxies=proxies)
        if response.status_code == 200:
            id_match = re.search(r'/(\d{5,6})_', link)
            if id_match:
                file_id = id_match.group(1)
                file_name = f'{file_id}.pdf'
                file_path = os.path.join(path_to_save_pdf, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f'Downloaded: {file_path}')
            else:
                print(f'Failed to extract ID from link: {link}')
        else:
            print(f'Failed to download: {link}')
