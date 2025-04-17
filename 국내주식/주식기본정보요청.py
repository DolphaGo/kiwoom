import requests

from config import MY_ACCESS_TOKEN, host  # 공통 설정 파일에서 토큰 가져오기


# 주식기본정보요청
def fn_ka10001(stk_cd, token=MY_ACCESS_TOKEN, cont_yn='N', next_key=''):
	# 1. 요청할 API URL 및 데이터
	url = host + '/api/dostk/stkinfo'
	params = {
		'stk_cd': stk_cd,  # 종목코드 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
	}

	# 2. header 데이터
	headers = {
		'Content-Type': 'application/json;charset=UTF-8', # 컨텐츠타입
		'authorization': f'Bearer {token}', # 접근토큰
		'cont-yn': cont_yn, # 연속조회여부
		'next-key': next_key, # 연속조회키
		'api-id': 'ka10001', # TR명
	}

	# 3. http POST 요청
	response = requests.post(url, headers=headers, json=params)

	# 4. 응답 상태 코드와 데이터 출력
	# print('Code:', response.status_code)
	# print('Header:', json.dumps({key: response.headers.get(key) for key in ['next-key', 'cont-yn', 'api-id']}, indent=4, ensure_ascii=False))
	# print('Body:', json.dumps(response.json(), indent=4, ensure_ascii=False))  # JSON 응답을 파싱하여 출력

	data = response.json()
	return data['stk_nm'], data['cur_prc']

# 실행 구간
if __name__ == '__main__':
	종목명, 현재가 = fn_ka10001('039490')
	print("종목명:", 종목명)
	print("현재가:", 현재가)
	# next-key, cont-yn 값이 있을 경우
	# fn_ka10001(token=MY_ACCESS_TOKEN, data=params, cont_yn='N', next_key='nextkey..')

