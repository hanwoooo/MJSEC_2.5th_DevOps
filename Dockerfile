# 베이스 이미지 선택
FROM python:3.10-slim

# 작업 디렉토리 생성
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 앱 파일 복사
COPY . .

# 포트 오픈
EXPOSE 5000

# 앱 실행
CMD ["python", "app.py"]
