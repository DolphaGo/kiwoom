import json

import requests

from config import MY_ACCESS_TOKEN, MY_APP_KEY, MY_SECRET_KEY, host


# 접근토큰폐기
def fn_au10002(data):
	# 1. 요청할 API URL
	url = host + '/oauth2/revoke'

	# 2. header 데이터
	headers = {
		'Content-Type': 'application/json;charset=UTF-8'
	}

	# 3. http POST 요청
	response = requests.post(url, headers=headers, json=data)

	# 4. 응답 상태 코드와 데이터 출력
	print('Code:', response.status_code)
	print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

# 실행 구간
if __name__ == '__main__':
	# 1. 요청 데이터
	params = {
		'appkey': MY_APP_KEY,
		'secretkey': MY_SECRET_KEY,
		'token': MY_ACCESS_TOKEN,  # 토큰
	}

	# 2. API 실행
	fn_au10002(data=params)

