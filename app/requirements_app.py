"""
File: requirements_app.py
Author: Dmitry Ryumin
Description: Зависимости Gradio приложения
License: MIT License
"""

import pandas as pd

# Импорт необходимых компонентов для Gradio приложения
from app.config import config_data


def parse_requirements(file_path: str = "requirements.txt") -> pd.DataFrame:
    """
    Чтение файла с зависимостями и преобразование его содержимого в pandas DataFrame

    Args:
        file_path (str): Путь к файлу зависимостей

    Returns:
        pd.DataFrame: Таблица с данными о библиотеках
    """

    with open(file_path, "r") as file:
        lines = file.readlines()

    data = []

    pypi = (
        lambda x: f"<a href='https://pypi.org/project/{x}' target='_blank'><img src='https://img.shields.io/pypi/v/{x}' alt='PyPI' /></a>"
    )

    for line in lines:
        line = line.strip()
        if "==" in line:
            library, version = line.split("==")
            data.append(
                {
                    config_data.Requirements_LIBRARY: library,
                    config_data.Requirements_REC_VERSION: version,
                    config_data.Requirements_CURR_VERSION: pypi(library),
                }
            )

    df = pd.DataFrame(data)

    return df
