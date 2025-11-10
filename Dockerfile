FROM python:3.13-slim

WORKDIR /app

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Копируем зависимости
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-dev

# Копируем модули
COPY handlers/ ./handlers/
COPY keyboards/ ./keyboards/
COPY parser/ ./parser/
COPY bot.py config.py ./

# Настраиваем окружене
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

# Запускаем бота
CMD ["python", "bot.py"]
