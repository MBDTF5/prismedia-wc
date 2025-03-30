import urllib.parse # 1. 올바른 import 방식

# 2. base_url은 상대 경로가 포함된 '페이지'의 URL이어야 합니다.
#    (실제 페이지 URL로 바꿔주세요)
base_url = "https://likms.assembly.go.kr/record/mhs-60-010.do#none" # 예시 페이지 URL

# 3. 찾은 상대 경로 (정확한지 다시 확인해보세요)
relative_path = "/record/res/img/sub/sub_pdf.gif" # 이게 정말 PDF 경로가 맞나요?

# urljoin 함수 호출 (모듈 이름과 함께)
absolute_url = urllib.parse.urljoin(base_url, relative_path)

print(f"기준 페이지 URL: {base_url}") # 변수 의미 명확화
print(f"상대 경로: {relative_path}")
print(f"변환된 절대 URL: {absolute_url}")