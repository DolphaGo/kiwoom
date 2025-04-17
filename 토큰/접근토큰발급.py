from pathlib import Path

import requests
from config import MY_APP_KEY, MY_SECRET_KEY

# 접근토큰 발급
def fn_au10001(data):
	# 1. 요청할 API URL
	# host = 'https://mockapi.kiwoom.com' # 모의투자
	host = 'https://api.kiwoom.com' # 실전투자
	endpoint = '/oauth2/token'
	url =  host + endpoint

	# 2. header 데이터
	headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
	}

	# 3. http POST 요청
	response = requests.post(url, headers=headers, json=data)

	# 4. 응답 상태 코드와 데이터 출력
	# print('Code:', response.status_code)
	# print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	# print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

	return response.json()


import os
from dotenv import load_dotenv

# env 파일 업데이트 함수
def update_env_file(key, value, env_file=".env"):
	# 현재 파일의 경로를 기준으로 프로젝트 루트 디렉터리의 .env 파일에 업데이트 합니다
	env_file = Path(__file__).resolve().parent.parent / ".env"

	# .env.example 파일 로드
	load_dotenv(env_file)

	# 기존 환경 변수 읽기
	env_vars = {}
	if os.path.exists(env_file):
		with open(env_file, "r") as file:
			for line in file:
				if line.strip() and not line.startswith("#"):
					k, v = line.strip().split("=", 1)
					env_vars[k] = v

	# 새로운 키-값 추가 또는 업데이트
	env_vars[key] = value

	# .env.example 파일에 다시 쓰기
	with open(env_file, "w") as file:
		for k, v in env_vars.items():
			file.write(f"{k}={v}\n")


# 실행 구간
if __name__ == '__main__':
	# 1. 요청 데이터
	params = {
		'grant_type': 'client_credentials',  # grant_type
		'appkey': MY_APP_KEY,  # 앱키
		'secretkey': MY_SECRET_KEY,  # 시크릿키
	}

	# 2. API 실행
	my_access_token = fn_au10001(data=params).get('token')
	print(my_access_token)
	update_env_file("MY_ACCESS_TOKEN", my_access_token)

