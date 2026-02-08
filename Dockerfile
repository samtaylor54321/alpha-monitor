FROM python:3.13-slim

RUN pip install --no-cache-dir uv==0.5.10

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

CMD ["python", "-c", "print('alpha-monitor container built')"]
