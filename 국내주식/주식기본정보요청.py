import json

import requests

from config import MY_ACCESS_TOKEN, host  # 공통 설정 파일에서 토큰 가져오기


# 주식기본정보요청
def fn_ka10001(token, data, cont_yn='N', next_key=''):
	# 1. 요청할 API URL
	url = host + '/api/dostk/stkinfo'

	# 2. header 데이터
	headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		'authorization': f'Bearer {token}', # 접근토큰
		'cont-yn': cont_yn, # 연속조회여부
		'next-key': next_key, # 연속조회키
		'api-id': 'ka10001', # TR명
	}

	# 3. http POST 요청
	response = requests.post(url, headers=headers, json=data)

	# 4. 응답 상태 코드와 데이터 출력
	print('Code:', response.status_code)
	print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력
	return response.json()

# 실행 구간
if __name__ == '__main__':
	# 요청 데이터
	params = {
		'stk_cd': '039490',  # 종목코드 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
	}

	# 3. API 실행
	response = fn_ka10001(token=MY_ACCESS_TOKEN, data=params)
	price = response['cur_prc']  # 현재가
	print(f"현재가: {price}")
	# next-key, cont-yn 값이 있을 경우
	# fn_ka10001(token=MY_ACCESS_TOKEN, data=params, cont_yn='N', next_key='nextkey..')

