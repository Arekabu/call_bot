# 📅 Call Calendar Bot – Telegram Bot for API Communication

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![aiogram](https://img.shields.io/badge/aiogram-3.22+-green.svg)](https://docs.aiogram.dev/)
[![uv](https://img.shields.io/badge/packaging-uv-orange.svg)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/badge/linter-Ruff-red.svg)](https://github.com/astral-sh/ruff)

Telegram бот для интеграции с системой управления звонками через REST API с поддержкой современных асинхронных паттернов.

## 🚀 Технологический стек

### **Backend & Framework**
<p align="left">
  <img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.13+">
  <img src="https://img.shields.io/badge/aiogram-3.22-000000?style=for-the-badge&logo=telegram&logoColor=white" alt="aiogram">
  <img src="https://img.shields.io/badge/asyncio-✔-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="AsyncIO">
</p>

### **Development & Quality**
<p align="left">
  <img src="https://img.shields.io/badge/uv-Build%20Tool-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="uv">
  <img src="https://img.shields.io/badge/pytest-Testing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/Ruff-Linting-FF6B6B?style=for-the-badge&logo=ruff&logoColor=white" alt="Ruff">
  <img src="https://img.shields.io/badge/isort-Import%20Sorting-EFEFEF?style=for-the-badge&logo=python&logoColor=blue" alt="isort">
  <img src="https://img.shields.io/badge/pre--commit-Hooks-FAB040?style=for-the-badge&logo=git&logoColor=white" alt="pre-commit">
</p>

### **Infrastructure**
<p align="left">
  <img src="https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/REST%20API-Integration-FF6B6B?style=for-the-badge&logo=rest&logoColor=white" alt="REST API">
  <img src="https://img.shields.io/badge/.env-Configuration-ECD53F?style=for-the-badge&logo=dotenv&logoColor=black" alt="Environment Variables">
</p>

## 📦 Установка проекта

### 1. Клонируем репозиторий

   ```bash
   git clone git@git.yiilab.com:ylab-internal/call-calendar/call-calendar-bot.git
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
Для локального запуска в Docker измените в .env:
   ```env
   DJANGO_API_URL=http://host.docker.internal:8000/api
   ```
