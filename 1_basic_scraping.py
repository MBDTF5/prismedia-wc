from playwright.sync_api import sync_playwright

target_url = "https://likms.assembly.go.kr/record/mhs-60-010.do#none"

print(f"'{target_url}' 에서 스크래핑 시작...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print(f"페이지 로딩 중: {target_url}")
    page.goto (target_url)
    print("페이지 로딩 완료")

    # --- 스크래핑 시작 ---

    first_quote_element = page.locator("div.quote > span.text").first  # 여러 개 중 첫 번째 요소 선택
    first_quote_text = first_quote_element.inner_text()  # 요소 안의 텍스트 추출
    print(f"\n첫 번째 명언: {first_quote_text}")

    first_author_element = page.locator("div.quote > span > small.author").first
    first_author_name = first_author_element.inner_text()
    print(f"저자: {first_author_name}")

    print("\n페이지의 모든 명언:")
    quote_elements = page.locator("div.quote > span.text")  # 해당하는 모든 요소를 선택
    all_quotes = quote_elements.all_inner_texts()  # 모든 요소의 텍스트를 리스트로 가져옴
    for i, quote in enumerate(all_quotes):
        print(f"  {i + 1}: {quote}")

    # --- 스크래핑 끝 ---

    browser.close()
    print("\n스크래핑 완료 및 브라우저 종료.")


