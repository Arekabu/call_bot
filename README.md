# Call Calendar Bot

## 📦 Установка проекта

### 1. Клонируем репозиторий

   ```bash
   git clone git@git.yiilab.com:ylab-internal/call-calendar/call-calendar-bot.git
   cd call-calendar-bot
   ```

### 2. Устанавливаем uv
**Windows:**
   ```bash
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
**MacOS и Linux:**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### 3. Запускаем файл setup.sh
**Windows:**
   ```bash
   setup.sh
   ```

**MacOS и Linux:**
   ```bash
   bash setup.sh
   ```

**ИЛИ просто последовательно вводим команды:**
   ```bash
   uv sync --all-groups
   uv run pre-commit install
   uv run pre-commit run --all-files
   ```


### 4. Копируем и заполняем своими данными переменную окружения из шаблона

   ```bash
   cp .env.example .env
   ```

### 5. Запускаем бота
Напрямую:
   ```bash
   python bot.py
   ```
Или через Docker контейнер:
   ```bash
   docker build -t call-calendar-bot . && docker run --name call-calendar-bot-container call-calendar-bot
   ```
