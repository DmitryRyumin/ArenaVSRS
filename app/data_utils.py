"""
File: utils.py
Author: Dmitry Ryumin
Description: Utility functions.
License: MIT License
"""

import re
import random
import pandas as pd
from typing import List, Tuple, Any, Dict, Union, Optional
from pathlib import Path

# Importing necessary components for the Gradio app


def get_csv_files(directory: Union[str, Path], ext: str = "*.csv") -> List[Path]:
    """
    Возвращение списка всех CSV файлов в указанной директории

    Args:
        directory (Union[str, Path]): Путь к директории
        ext (str): Расширение файлов для поиска. По умолчанию "*.csv"

    Returns:
        List[Path]: Список путей к CSV файлам
    """

    def custom_sort_key(file_name: Path) -> tuple:
        name = file_name.stem

        # Классификация: 1 для английских, 2 для русских, 3 для цифр
        if re.match(r"^[A-Za-z]", name):  # Английские буквы
            return (1, name)
        elif re.match(r"^[А-Яа-яЁё]", name):  # Русские буквы
            return (2, name)
        elif re.match(r"^\d", name):  # Цифры
            return (3, name)
        else:
            return (4, name)  # Все остальные символы

    path_to_files = Path(directory)
    csv_files = list(path_to_files.rglob(ext))

    # Сортировка по кастомному ключу
    sorted_csv_files = sorted(csv_files, key=custom_sort_key)

    return sorted_csv_files


def read_csv_file(
    file_path: Union[str, Path], sep: str = ";", drop_columns: List[str] = []
) -> pd.DataFrame:
    """
    Чтение CSV файла и возвращение предварительно обработанный DataFrame

    Args:
        file_path (Union[str, Path]): Путь к файлу CSV
        sep (str, optional): Разделитель в CSV файле. По умолчанию ";"
        drop_columns (List[str], optional): Список колонок для удаления

    Returns:
        pd.DataFrame: Обработанный DataFrame с индексом
    """

    df = pd.read_csv(file_path, encoding="utf-8-sig", sep=sep)

    if drop_columns:
        df = pd.DataFrame(df.drop(drop_columns, axis=1))

    return preprocess_scores_df(df, "ID")


def preprocess_scores_df(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """
    Предварительная обработка DataFrame: установка имени индекса и преобразование индексов в строковый формат

    Args:
        df (pd.DataFrame): Входной DataFrame
        name (str): Имя для индекса

    Returns:
        pd.DataFrame: Обработанный DataFrame
    """

    df.index.name = name
    df.index += 1
    df.index = df.index.map(str)

    return df


def parse_course_data(
    course_data: str,
    fields_to_extract: Optional[List[int]] = None,
    is_simple_format: bool = False,
) -> List[List[str]]:
    """
    Парсинг строки с данными о курсах

    Args:
        course_data (str): Исходная строка с курсами
        fields_to_extract (List[int]): Список номеров полей, которые нужно извлечь (индексация с 1)
        is_simple_format (bool): Если True, строка обрабатывается как упрощенная, разделенная только по ";"

    Returns:
        List[List[str]]: Список курсов, где каждый курс представлен как список данных
    """

    course_data = course_data.replace("CS=", "").strip()

    courses = [course.strip() for course in course_data.split(";") if course.strip()]

    if is_simple_format:
        return [[course] for course in courses]

    parsed_courses = [course.split("|") for course in courses]

    if fields_to_extract is None:
        return [[field.strip() for field in course] for course in parsed_courses]

    return [
        [course[i - 1].strip() for i in fields_to_extract if 0 <= i - 1 < len(course)]
        for course in parsed_courses
    ]


def randomize_results(
    config_data: Any, state: Dict[str, Any]
) -> Tuple[List[Any], List[str], List[Any], List[str]]:
    """
    Рандомизация результатов для отображения датафреймов

    Args:
        config_data (Any): Объект конфигурации, содержащий параметры интерфейса и настройки отображения
        state (Dict[str, Any]): Состояние, содержащее текущие данные и порядок отображения

    Returns:
        Tuple[List[Any], List[str], List[Any], List[str]]:
            - List[Any]: Данные для первого отображаемого датафрейма
            - List[str]: Заголовки для первого отображаемого датафрейма
            - List[Any]: Данные для второго отображаемого датафрейма
            - List[str]: Заголовки для второго отображаемого датафрейма
    """

    if config_data.Settings_RANDOM_RESULTS:
        if state["random_order"] is None:
            state["random_order"] = random.choice([True, False])
        if state["random_order"]:
            headers_a, headers_b = [
                config_data.DataframeHeaders_RESULT[0]
            ], config_data.DataframeHeaders_RESULT
            parsed_first_dataframe_a, parsed_first_dataframe_b = (
                state["dataframe_b"],
                state["dataframe_a"],
            )
        else:
            headers_a, headers_b = config_data.DataframeHeaders_RESULT, [
                config_data.DataframeHeaders_RESULT[0]
            ]
            parsed_first_dataframe_a, parsed_first_dataframe_b = (
                state["dataframe_a"],
                state["dataframe_b"],
            )
    else:
        headers_a, headers_b = config_data.DataframeHeaders_RESULT, [
            config_data.DataframeHeaders_RESULT[0]
        ]
        parsed_first_dataframe_a, parsed_first_dataframe_b = (
            state["dataframe_a"],
            state["dataframe_b"],
        )

    return parsed_first_dataframe_a, headers_a, parsed_first_dataframe_b, headers_b


def load_excel_files(directory: str, ext: str = "*.xlsx") -> pd.DataFrame:
    """
    Загрузка и объединение всех Excel файлов из указанной директории в один DataFrame

    Args:
        directory (str): Путь к директории, содержащей Excel файлы
        ext (str): Расширение файлов для поиска. По умолчанию "*.xlsx"

    Returns:
        pd.DataFrame: DataFrame, содержащий данные из всех Excel файлов
    """

    path_to_files = Path(directory)
    xlsx_files = list(path_to_files.rglob(ext))

    df = pd.DataFrame()

    for file in xlsx_files:
        df_temp = pd.read_excel(file)
        df = pd.concat([df, df_temp], ignore_index=True)

    return df


def wrap_subjects(
    parsed_data: List[List[str]],
    unique_subjects: set,
) -> List[List[str]]:
    """
    Проверка, есть ли название курса в уникальных значениях DataFrame, и обертка его, если найдено

    Args:
        parsed_data (List[List[str]]): Список курсов с результатами для проверки
        unique_subjects (set): Список с уникальными названиями дисциплин

    Returns:
        List[List[str]]: Модифицированный список курсов
    """

    def wrap_course_name(course_name: str) -> str:
        if course_name.lower() not in unique_subjects:
            return f"<span class='wrapper_subject'><span class='err'>{course_name}</span></span>"
        return course_name

    wrapped_data = [
        (
            [wrap_course_name(course[0])] + course[1:]
            if len(course) > 1
            else [wrap_course_name(course[0])]
        )
        for course in parsed_data
    ]

    return wrapped_data
