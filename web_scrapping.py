import requests
from bs4 import BeautifulSoup
import pandas as pd

# Zillow 웹사이트의 특정 지역 부동산 목록 페이지 URL
url = 'https://www.zillow.com/homes/for_sale/San-Francisco-CA/'

# 사용자 에이전트(User-Agent) 설정 - 일부 웹사이트는 스크래퍼를 차단하기 때문에, 브라우저처럼 보이게 설정할 필요가 있습니다.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

# BeautifulSoup 객체를 생성하여 HTML을 파싱합니다.
soup = BeautifulSoup(response.text, 'html.parser')

# 수집할 데이터를 저장할 리스트를 초기화합니다.
properties = []

# 웹페이지에서 매물 목록을 찾고 각 매물에 대한 정보를 추출합니다.
# 아래의 클래스 이름은 예시이며, 실제 웹사이트의 구조에 맞게 수정해야 합니다.
for listing in soup.find_all('article', class_='list-card'):
    title = listing.find('h3', class_='list-card-addr').text.strip() if listing.find('h3', class_='list-card-addr') else 'No Title'
    price = listing.find('div', class_='list-card-price').text.strip() if listing.find('div', class_='list-card-price') else 'No Price'
    details = listing.find('ul', class_='list-card-details').text.strip() if listing.find('ul', class_='list-card-details') else 'No Details'

    # 추출한 정보를 딕셔너리로 만들고 리스트에 추가합니다.
    properties.append({
        'Title': title,
        'Price': price,
        'Details': details
    })

# 데이터를 pandas DataFrame으로 변환합니다.
df = pd.DataFrame(properties)

# DataFrame을 확인하고 CSV 파일로 저장합니다.
print(df)
df.to_csv('zillow_real_estate_listings.csv', index=False)
