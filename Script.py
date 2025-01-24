import os
import json
import requests
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

########################## 카카오 API 토큰 처리 ##########################
def get_kakao_tokens():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    kakao_code_path = os.path.join(cur_dir, "kakao_code.json")

    if not os.path.exists(kakao_code_path):
        print("kakao_code.json 파일이 존재하지 않습니다. 인증 코드 요청을 시작합니다.")

        email = input("카카오 계정 이메일을 입력하세요: ")
        password = input("카카오 계정 비밀번호를 입력하세요: ")

        driver = webdriver.Chrome()
        driver.get("https://accounts.kakao.com")

        email_field = driver.find_element(By.ID, "loginId--1")
        password_field = driver.find_element(By.ID, "password--2")

        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        time.sleep(25)
        driver.get("https://kauth.kakao.com/oauth/authorize?client_id=&redirect_uri=https://example.com/oauth&response_type=code&scope=profile_nickname,friends,talk_message")

        time.sleep(5)
        current_url = driver.current_url
        driver.quit()

        if "code=" in current_url:
            authorize_code = current_url.split("code=")[1]
            print("인증 코드 요청 성공")

        url = 'https://kauth.kakao.com/oauth/token'
        rest_api_key = ''
        redirect_uri = 'https://example.com/oauth'

        data = {
            'grant_type': 'authorization_code',
            'client_id': rest_api_key,
            'redirect_uri': redirect_uri,
            'code': authorize_code,
        }

        response = requests.post(url, data=data)
        tokens = response.json()

        with open(kakao_code_path, "w") as fp:
            json.dump(tokens, fp)

        print("토큰이 저장되었습니다.")
        return tokens

    else:
        print("kakao_code.json 파일이 존재합니다. refresh_token을 사용하여 새 토큰을 요청합니다.")
        with open(kakao_code_path, "r") as fp:
            tokens = json.load(fp)

        refresh_token = tokens["refresh_token"]

        url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": " ",
            "refresh_token": refresh_token,
        }

        response = requests.post(url, data=data)
        new_tokens = response.json()

        if "refresh_token" not in new_tokens:
            new_tokens["refresh_token"] = refresh_token

        with open(kakao_code_path, "w") as fp:
            json.dump(new_tokens, fp)

        print("토큰이 갱신되었습니다.")
        return new_tokens
########################################################################
########################## 크롤링 + 데이터 처리 ##########################
def crawl_data():
    response = requests.get('https://eng.jnu.ac.kr/eng/7343/subview.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZW5nJTJGOTkzJTJGYXJ0Y2xMaXN0LmRvJTNG')
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.select("body div div div div article div div form div table tbody tr")
    results = []

    for row in rows:
        title_element = row.select_one("td a strong")
        link_element = row.select_one("td a")
        if title_element and link_element:
            title = title_element.text.strip()
            href = link_element.get("href")
            
            # href에서 article ID 추출
            if href and "/bbs/eng/993/" in href:
                article_id = href.split("/")[4]
                
                # Base64 인코딩
                base_url = f"/bbs/eng/993/{article_id}/artclView.do?page=1&srchColumn=&srchWrd=&bbsClSeq=&bbsOpenWrdSeq=&rgsBgndeStr=&rgsEnddeStr=&isViewMine=false&password"
                encoded_url = base64.b64encode(f"fnct1|@@|{base_url}".encode("utf-8")).decode("utf-8")
                
                # 최종 URL
                final_url = f"https://eng.jnu.ac.kr/eng/7343/subview.do?enc={encoded_url}"
                
                results.append({"title": title, "url": final_url})

    existing_data = set()
    if os.path.exists("craw_data.txt"):
        with open("craw_data.txt", "r", encoding="utf-8") as file:
            existing_data = set(line.strip() for line in file)

    unique_results = [result for result in results if result["title"] not in existing_data]

    with open("craw_data.txt", "a", encoding="utf-8") as file:
        for data in unique_results:
            file.write(data["title"] + "\n")

    print("중복되지 않은 데이터:")
    for data in unique_results:
        print(data)

    return unique_results
########################################################################
########################## 카카오 메시지 전송 ##########################
def send_kakao_message(tokens, unique_results):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers = {
        "Authorization": "Bearer " + tokens["access_token"]
    }

    chunk_size = 3
    artc = [unique_results[i:i + chunk_size] for i in range(0, len(unique_results), chunk_size)]

    for chunk in artc:
        template = {
            "object_type": "list",
            "header_title": "업데이트된 공지사항",
            "header_link": {
                "web_url": "https://eng.jnu.ac.kr/eng/7343/subview.do",
                "mobile_web_url": "https://eng.jnu.ac.kr/eng/7343/subview.do"
            },
            "contents": [],
        }

        for result in chunk:
            template["contents"].append({
                "title": result["title"],
                "link": {
                    "web_url": result["url"],
                    "mobile_web_url": result["url"]
                }
            })

        dump = {
            "template_object": json.dumps(template)
        }

        res = requests.post(url, data=dump, headers=headers)

        if res.json().get('result_code') == 0:
            print(f'{len(chunk)}개의 메시지를 성공적으로 보냈습니다.')
        else:
            print('메시지를 성공적으로 보내지 못했습니다. 오류메시지: ' + str(res.json()))

##############################################################
########################## 메인 실행 ##########################
if __name__ == "__main__":
    tokens = get_kakao_tokens()
    unique_results = crawl_data()
    send_kakao_message(tokens, unique_results)
