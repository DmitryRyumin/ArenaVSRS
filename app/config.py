"""
File: config.py
Author: Dmitry Ryumin
Description: Работа с настройками Gradio приложения
License: MIT License
"""

import toml
from typing import Callable, Dict, Any
from types import SimpleNamespace

CONFIG_NAME = "config.toml"


def flatten_dict(prefix: str, d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Рекурсивное преобразование словаря в словарь с префиксами ключей

    Args:
        prefix (str): Префикс, который будет добавлен к ключам словаря
        d (Dict[str, Any]): Входной словарь

    Returns:
        Dict[str, Any]: Словарь, где ключи имеют префикс
    """

    result = {}

    for k, v in d.items():
        result.update(
            flatten_dict(f"{prefix}{k}_", v)
            if isinstance(v, dict)
            else {f"{prefix}{k}": v}
        )

    return result


def load_tab_creators(
    file_path: str, available_functions: Dict[str, Callable]
) -> Dict[str, Callable]:
    """
    Загрузка информации о вкладках из конфигурационного файла и сопоставление их с доступными функциями

    Args:
        file_path (str): Путь к конфигурационному файлу
        available_functions (Dict[str, Callable]): Словарь доступных функций для создания вкладок

    Returns:
        Dict[str, Callable]: Словарь, где ключи - имена вкладок, а значения - функции, которые их создают
    """

    config = toml.load(file_path)
    tab_creators_data = config.get("TabCreators", {})

    return {key: available_functions[value] for key, value in tab_creators_data.items()}


def load_config(file_path: str) -> SimpleNamespace:
    """
    Загрузка конфигурационного файла и преобразование его в объект

    Args:
        file_path (str): Путь к конфигурационному файлу

    Returns:
        SimpleNamespace: Объект на основе конфигурационного файла
    """

    config = toml.load(file_path)
    config_data = flatten_dict("", config)

    return SimpleNamespace(**config_data)


config_data = load_config(CONFIG_NAME)
