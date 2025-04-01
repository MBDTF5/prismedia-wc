# import dask.array # 사용되지 않으므로 주석 처리 또는 삭제
from playwright.async_api import async_playwright # async_api 사용 확인
from collections import deque
import asyncio
import time

start_url = "https://likms.assembly.go.kr/record/mhs-60-010.do#none"
max_pages_to_visit = 5

urls_to_visit = deque([start_url])
visited_urls = set([start_url])

scraped_data = [] # 변수명 오타 수정 (scarped_data -> scraped_data)

print("크롤링 및 스크래핑 시작")

# --- 비동기 함수 정의 ---
async def main():
    global scraped_data # 전역 변수 사용 선언 (함수 내에서 리스트에 추가하기 위함)
    async with async_playwright() as p: # 'async with' 사용
        browser = await p.chromium.launch(headless=True) # 'await' 추가
        page = await browser.new_page() # 'await' 추가

        page_count = 0
        while urls_to_visit and page_count < max_pages_to_visit:
            current_url = urls_to_visit.popleft()
            page_count += 1

            print(f"\n[{page_count}/{max_pages_to_visit}] 방문 시도: {current_url}")

            try: # try 블록 시작 위치 수정
                # --- 페이지 이동 및 스크래핑 (모두 try 블록 안으로 이동) ---
                await page.goto(current_url, timeout=30000, wait_until="domcontentloaded") # 'await' 추가
                print(f" -> 현재 페이지: {page.url}")

                page_title = await page.title() # 'await' 추가
                print(f"  -> 페이지 제목: {page_title}")
                # 변수명 오타 수정 및 데이터 추가
                scraped_data.append({'url': current_url, 'title': page_title})

                # --- 링크 찾기 및 추가 (모두 try 블록 안으로 이동) ---
                link_elements = page.locator("a")
                link_count = await link_elements.count() # .count()는 await 필요 없음. 수정: .count() 는 동기 함수
                # link_count = link_elements.count() # 이렇게 사용

                for i in range(link_count): # link_count 변수 사용
                    link = link_elements.nth(i) # nth()는 동기 함수
                    href = await link.get_attribute("href") # 'await' 추가
                    if href:
                        # urljoin은 동기 함수
                        absolute_url = page.urljoin(href)

                        if (absolute_url.startswith("http") and
                                absolute_url not in visited_urls and
                                absolute_url not in urls_to_visit and
                                start_url in absolute_url):

                            if len(urls_to_visit) < 100:
                                # 오타 수정 ("새로윤" -> "새로운")
                                print(f" -> 새로운 링크 발견 및 추가: {absolute_url}")
                                visited_urls.add(absolute_url)
                                urls_to_visit.append(absolute_url)

                # --- 대기 시간 (try 블록 안으로 이동) ---
                # 오타 수정 ("요점" -> "요청") 및 asyncio.sleep 사용
                print(" -> 다음 요청 전 1초 대기...")
                await asyncio.sleep(1) # time.sleep 대신 'await asyncio.sleep()' 사용

            except Exception as e:
                # 오류 메시지 출력 위치는 그대로 유지
                print(f"  오류 발생 ({current_url}): {e}")
            # finally 블록은 필요시 추가 (예: 특정 리소스 정리)

        await browser.close() # 'await' 추가

# --- 비동기 함수 실행 ---
asyncio.run(main())

print("\n--- 최종 스크래핑 결과 ---")

for data in scraped_data:
    print(data)

print(f"\n총 {len(scraped_data)} 페이지 방문 및 스크래핑 완료.")