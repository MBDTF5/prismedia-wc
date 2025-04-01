from playwright.sync_api import sync_playwright
import re

start_url =  "https://quotes.toscrape.com/" # 크롤링 시작할 페이지

print(f" '{start_url}' 에서 링크 크롤링 시작")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    try:
        page.goto(start_url, timeout=60000)
        print(f"현재 페이지: {page.url}")

        link_element = page.locator("a")

        print(f"\n총 {link_element()}개의 링크 요소를 찾았습니다.")
        found_urls = set()

        for i in range(link_element.count()):
            link = link_element.nth(i)
            href = link.get_attribute("href")

            if href:
                absolute_url = page.urljoin(href)

                if absolute_url.startswith("http://") or absolute_url.startswith("https://"):
                    found_urls.add(absolute_url)

        if found_urls:
            for url in sorted(list(found_urls)):
                print(f"  - {url}")

        else:
            print("  찾은 URL이 없습니다.")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        browser.close()
        print("\n크롤링 완료 및 브라우저 종료.")



