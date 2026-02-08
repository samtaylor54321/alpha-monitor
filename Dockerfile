FROM python:3.13-slim

# Pin uv to keep builds deterministic
RUN pip install --no-cache-dir uv==0.5.10

WORKDIR /app

# Copy dependency metadata first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies only (not the package)
RUN uv sync --frozen

# Copy application code
COPY . .

# Default command (adjust later for Streamlit / app entrypoint)
CMD ["python", "-c", "import alpha_monitor; print('alpha-monitor ready')"]
