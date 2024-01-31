# 레이어 1: 베이스 이미지 설정
FROM python:3.9-slim AS base

# 작업 디렉토리 설정
WORKDIR /


# 필요한 라이브러리 설치 (레이어 1)
RUN apt-get update \
    && apt-get install gcc default-libmysqlclient-dev -y python3-dev pkg-config -y

COPY . .

# 레이어 2: 기본 라이브러리 설치
FROM base as layer1

RUN pip install --upgrade pip && pip install alembic \
    fastapi \
    sqlalchemy \
    python-multipart \
    uvicorn[standard] \
    mysqlclient \
    numpy \
    librosa \
    tensorflow

FROM layer1 as layer2

WORKDIR /
# RUN alembic upgrade head

# 레이어 4: 최종 실행
FROM layer2 as final

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
