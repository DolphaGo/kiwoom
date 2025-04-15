import os
from dotenv import load_dotenv

load_dotenv()  # .env.example 파일에 있는 환경변수들을 로드

MY_ACCESS_TOKEN = os.getenv("MY_ACCESS_TOKEN")
MY_APP_KEY = os.getenv("MY_APP_KEY")
MY_SECRET_KEY = os.getenv("MY_SECRET_KEY")

if not MY_ACCESS_TOKEN:
    raise Exception("MY_ACCESS_TOKEN 환경변수가 설정되지 않았습니다.")

if not MY_APP_KEY:
    raise Exception("MY_APP_KEY 환경변수가 설정되지 않았습니다.")

if not MY_SECRET_KEY:
    raise Exception("MY_SECRET_KEY 환경변수가 설정되지 않았습니다.")