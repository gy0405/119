import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

# 카카오톡 API URL
kakao_api_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

# 카카오톡 Access Token 
access_token = "mvo6yJR5HKklvI0VWp4NgLT_Kd1p9M6JAAAAAQo9c-sAAAGUkn3X_XLErHmNOyL0"

# 사용자가 입력한 키워드 받기
keyword = input("검색할 키워드를 입력하세요: ")

# 크롤링
def crawl_and_filter(url, keyword):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # 크롤링한 데이터 저장
        filtered_items = []
        items = soup.select(".notice")  # 공지사항 클래스 선택
        for item in items:
            title = item.select_one(".td-subject strong")  # 제목 추출
            link = item.select_one(".td-subject a")  # 링크 추출
            if title and link:
                title_text = title.get_text()
                link_url = link['href']
                # 키워드 필터링
                if keyword in title_text:
                    filtered_items.append({"title": title_text, "link": link_url})
        
        # JSON 파일 저장
        with open("filtered_data.json", "w", encoding="utf-8") as json_file:
            json.dump(filtered_items, json_file, ensure_ascii=False, indent=4)
        
        return filtered_items
    else:
        print(f"페이지 요청 실패: {response.status_code}")
        return []

# 카카오톡 전송 함수
def send_to_kakao(filtered_items, base_url):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 3개씩 전송
    chunk_size = 3
    for i in range(0, len(filtered_items), chunk_size):
        chunk = filtered_items[i:i + chunk_size]
        
        # 카카오톡 메시지 템플릿
        template_object = {
            "object_type": "list",
            "header_title": "공지사항",
            "header_link": {
                "web_url": base_url,
                "mobile_web_url": base_url
            },
            "contents": []
        }
        
        for item in chunk:
            # 링크 디버깅 출력
            web_url = urljoin(base_url, item["link"])
            print(f"Generated URL for {item['title']}: {web_url}")  # 링크 출력 (디버깅)

            template_object["contents"].append({
                "title": item["title"],
                "description": "자세히 보기",
                "link": {
                    "web_url": web_url,
                    "mobile_web_url": web_url
                }
            })
        
        # API 요청
        data = {"template_object": json.dumps(template_object)}
        response = requests.post(kakao_api_url, headers=headers, data=data)
        
        if response.status_code == 200:
            print("카카오톡 전송 성공!")
        else:
            print(f"카카오톡 전송 실패: {response.status_code}, {response.text}")

url = "https://chemedu.jnu.ac.kr/chemedu/15994/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGY2hlbWVkdSUyRjIzMDklMkZhcnRjbExpc3QuZG8lM0Y%3D"

filtered_items = crawl_and_filter(url, keyword)
if filtered_items:
    send_to_kakao(filtered_items, "https://chemedu.jnu.ac.kr/")
else:
    print("키워드에 해당하는 항목이 없습니다.")
