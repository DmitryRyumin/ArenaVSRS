"""
File: description.py
Author: Dmitry Ryumin
Description: Описание Gradio приложения
License: MIT License
"""

# Импорт необходимых компонентов для Gradio приложения
from app.config import config_data

DESCRIPTION = f"""\
# Оценка связки вакансий из HH с предметами преподаваемыми в ВШЭ

<div class="app-flex-container">
    <img src="https://img.shields.io/badge/version-v{config_data.AppSettings_APP_VERSION}-stable" alt="Version">
</div>
"""
