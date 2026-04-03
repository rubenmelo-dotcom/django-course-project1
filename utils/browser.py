from pathlib import Path
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from time import sleep
import os

# Use o caminho absoluto para não ter erro de interpretação do Python
DRIVER_PATH = '/home/ruben/curso-django/django/projeto1/bin/msedgedriver'

# msedge_options.add_argument("--headless")
# msedge_options.add_argument("--no-sandbox")
# msedge_options.add_argument("--disable-dev-shm-usage")


def make_edge_browser(*options):
    msedge_options = Options()

    if options is not None:
        for option in options:
            msedge_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == 1:
        msedge_options.add_argument('--headless')

    msedge_service = Service(executable_path=DRIVER_PATH)
    browser = webdriver.Edge(service=msedge_service, options=msedge_options)
    return browser


if __name__ == '__main__':
    browser = make_edge_browser()
    browser.get('https://www.udemy.com/')
    print(f"Sucesso! Título: {browser.title}")
    sleep(6)
    browser.quit()
    # No seu código, após o browser.get():
