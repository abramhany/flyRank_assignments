FROM python:3.13-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 1. SET THIS FIRST! Now every command below happens safely inside /app
WORKDIR /app

# 2. Copy pyproject.toml (Assuming it sits next to the Dockerfile)
COPY /src/pyproject.toml .

# 3. Install dependencies system-wide (using the cache trick)
RUN uv pip install --system .

# 4. Copy the entire project folder exactly as it looks on your computer
COPY . .

# 5. Link the main app code
RUN uv pip install --system -e .

# 6. Run the server explicitly from the module entry point instead of relying on FastAPI CLI path discovery
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]