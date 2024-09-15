"""
File: description_steps.py
Author: Dmitry Ryumin
Description: Описание шагов Gradio приложения
License: MIT License
"""

# Импорт необходимых компонентов для Gradio приложения
from app.config import config_data

STEPS_TEMPLATE = """\
<h2 align="center">{text}</h2>
"""

STEP_1 = STEPS_TEMPLATE.format(text=config_data.InformationMessages_STEP_1)

STEP_2 = STEPS_TEMPLATE.format(text=config_data.InformationMessages_STEP_2)
