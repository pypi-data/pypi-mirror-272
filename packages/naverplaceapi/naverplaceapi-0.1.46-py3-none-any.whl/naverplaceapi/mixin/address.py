import sys
import os
from urllib.parse import quote
from urllib.parse import urlencode
from selenium import webdriver
from seleniumwire import webdriver, utils
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bs4 import BeautifulSoup


class AddressMixin:
    def get_address_info(self, address, lng=None, lat=None, tor_port=9050):
        encoded_address = quote(address)  # URL 인코딩된 주소
        base_url = "https://map.naver.com/p/api/entry/addressInfo"
        params = {
            'address': encoded_address
        }
        if lng is not None:
            params['lng'] = lng
        if lat is not None:
            params['lat'] = lat

        encoded_params = urlencode(params)
        url = base_url + '?' + encoded_params

        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        is_headless = True
        if is_headless:
            options.add_argument('headless')
            options.add_argument('--no-sandbox')

        seleniumwire_options = {}
        use_tor = False
        if use_tor:
            seleniumwire_options['proxy'] = {
                'http': f'socks5://127.0.0.1:{tor_port}',
                'https': f'socks5://127.0.0.1:{tor_port}',
                'no_proxy': 'localhost,127.0.0.1'
            }

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options,
                                  seleniumwire_options=seleniumwire_options)

        try:
            driver.get(url)
            html_text = driver.page_source
            soup = BeautifulSoup(html_text, "lxml")
            # 데이터 파싱 로직이 필요한 경우 여기에 구현
            # 예시: address_data = soup.find('div', class_='address-info')
        except Exception as e:
            driver.quit()
            print(f"Error occurred: {e}")
            return None

        driver.quit()
        # return address_data 또는 필요한 데이터 반환
        return soup  # 임시로 soup 반환, 필요에 따라 조정
