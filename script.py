# 1. 웹페이지에 접속 요청을 보내는 도구
import requests
# 2. 웹페이지의 HTML 코드를 분석하고 원하는 정보를 찾기 쉽게 도와주는 도구
from bs4 import BeautifulSoup
# 3. (선택 사항) 다운로드 중간에 잠시 쉬게 하는 도구 (서버 배려)
import time
# 4. (선택 사항) URL 주소를 다루기 편하게 해주는 도구 (상대 경로 처리용)
from urllib.parse import urljoin

print("필요한 도구들을 준비했습니다.")

# *** 중요: 이 URL을 실제 국회 회의록 '목록' 페이지 주소로 바꿔야 합니다! ***
# 예시: target_url = "https://likms.assembly.go.kr/record/index.do" # 이 주소는 예시일 뿐, 정확한 목록 페이지를 찾아야 함
target_url = "https://likms.assembly.go.kr/record/res/img/sub/sub_pdf.gifsc"

print(f"목표 웹사이트 주소: {target_url}")

# target_url이 http로 시작하는지 간단히 확인 (오류 방지)
if not target_url.startswith('http'):
    print("오류: target_url이 'http://' 또는 'https://'로 시작하는 웹 주소가 아닙니다.")
    print("국회 회의록 목록이 있는 웹페이지의 주소를 입력해주세요.")
    exit()

print(f"'{target_url}' 페이지에 접속을 시도합니다...")

try:
    # requests.get() 함수를 사용해서 해당 URL에 접속 요청을 보냄
    response = requests.get(target_url, timeout=10)
    response.raise_for_status() # 접속 및 요청 성공 확인

    print(f"페이지 접속 성공! (상태 코드: {response.status_code})")

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')
    print("HTML 내용을 BeautifulSoup으로 분석 준비 완료!")

    print("페이지 내용에서 PDF 링크를 찾습니다...")
    pdf_links = []
    all_links_on_page = soup.find_all('a', href=True)
    print(f"페이지에서 총 {len(all_links_on_page)}개의 링크 태그(<a>)를 찾았습니다.")

    for link_tag in all_links_on_page:
        href = link_tag.get('href') # .get() 사용하면 href 속성이 없어도 오류 안남
        if href and href.lower().endswith('.pdf'): # href가 존재하고, .pdf로 끝나는지 확인
            full_pdf_url = urljoin(target_url, href)
            link_text = link_tag.get_text(strip=True)
            print(f"  PDF 링크 찾음! -> 텍스트: '{link_text}', 주소: {full_pdf_url}")
            pdf_links.append({'text': link_text, 'url': full_pdf_url})

    print("-" * 30)

    if pdf_links:
        print(f"총 {len(pdf_links)}개의 PDF 링크를 찾았습니다.")
        for i, pdf_info in enumerate(pdf_links[:5]):
            print(f"  {i+1}. {pdf_info['text']} ({pdf_info['url']})")
        if len(pdf_links) > 5:
            print("  ...")
    else:
        print("페이지에서 PDF 링크를 찾지 못했습니다.")
        # ... (이하 기존 코드와 동일) ...

except requests.exceptions.RequestException as e:
    print(f"오류 발생: 페이지에 접속할 수 없습니다.")
    print(f"에러 내용: {e}")
    exit()
except Exception as e: # 다른 예기치 못한 오류 처리
    print(f"알 수 없는 오류 발생: {e}")
    exit()