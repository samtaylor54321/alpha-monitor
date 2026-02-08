FROM python:3.13-slim

RUN pip install --no-cache-dir uv==0.5.10

WORKDIR /app

# Copy everything first so the package exists
COPY . .

# Now uv can see alpha_monitor and README.md
RUN uv sync --frozen

CMD ["python", "-c", "import alpha_monitor; print('alpha-monitor ready')"]
