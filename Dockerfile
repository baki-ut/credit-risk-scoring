FROM python:3.11-slim
WORKDIR /app

# Устанавливаем сам uv в контейнер
RUN pip install uv

# Копируем оба файла
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости строго по лок-файлу
RUN uv sync --frozen

COPY src/ src/
COPY models/ models/
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]