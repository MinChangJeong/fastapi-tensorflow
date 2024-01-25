# 레이어 1: 베이스 이미지 설정
FROM python:3.9 AS base

# 작업 디렉토리 설정
WORKDIR /

# pip 업데이트
RUN pip install --upgrade pip

# 필요한 라이브러리 설치 (레이어 1)
RUN apt-get update && apt-get install -y libsndfile1

# 소스코드 추가
COPY . .

# 레이어 2: 기본 라이브러리 설치
FROM base as layer1

RUN pip install fastapi \
    sqlalchemy \
    python-multipart \
    numpy \
    librosa \
    tensorflow \
    uvicorn[standard] \
    soundfile

# 레이어 3: Alembic 마이그레이션 업데이트
FROM layer1 as layer2

WORKDIR /
RUN alembic upgrade head

# 레이어 4: FastAPI 서버 실행
FROM layer2 as final

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
