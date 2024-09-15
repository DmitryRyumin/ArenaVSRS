"""
File: rating_utils.py
Author: Dmitry Ryumin
Description: Utility functions for handling rating evaluation.
License: MIT License
"""

from typing import List, Dict

# Importing necessary components for the Gradio app
from app.data_utils import read_csv_file


def get_existing_ids(
    ratings_file: str, surname: str, username: str, affiliation: str
) -> List[int]:
    """
    Получение ID, которые уже были оценены конкретным пользователем (по комбинации фамилии, имени и принадлежности)

    Args:
        ratings_file (str): Путь к CSV файлу с оценками
        surname (str): Значение фамилии (SURNAME) для фильтрации
        username (str): Значение имени (USERNAME) для фильтрации
        affiliation (str): Значение принадлежности (AFFILIATION) для фильтрации

    Returns:
        List[int]: Список ID, которые уже оценены этим пользователем
    """

    try:
        ratings_df = read_csv_file(ratings_file)

        # Отбираем только те строки, которые соответствуют комбинации фамилии, имени и принадлежности
        matching_rows = ratings_df[
            (ratings_df["SURNAME"] == surname)
            & (ratings_df["USERNAME"] == username)
            & (ratings_df["AFFILIATION"] == affiliation)
        ]

        # Возвращаем список ID, которые уже были оценены этим пользователем
        return matching_rows["ID"].tolist()
    except FileNotFoundError:
        return []


def get_user_ids_by_combination(
    ratings_files: List[str], surname: str, username: str, affiliation: str
) -> List[int]:
    """
    Получение всех ID для строк, где значения персональных данных равны заданным

    Args:
        ratings_files (List[str]): Список путей к CSV файлам с оценками
        surname (str): Значение фамилии (SURNAME) для поиска
        username (str): Значение имени (USERNAME) для поиска
        affiliation (str): Значение принадлежности (AFFILIATION) для поиска

    Returns:
        List[int]: Список ID, которые соответствуют найденным пользователям
    """

    matching_ids = []

    if not (surname and username and affiliation):
        return matching_ids

    for ratings_file in ratings_files:
        df = read_csv_file(ratings_file)

        required_columns = ["SURNAME", "USERNAME", "AFFILIATION", "ID"]

        if not all(col in df.columns for col in required_columns):
            continue

        # Находим все строки с совпадающими фамилией, именем и принадлежностью
        matching_rows = df[
            (df["SURNAME"] == surname)
            & (df["USERNAME"] == username)
            & (df["AFFILIATION"] == affiliation)
        ]

        # Добавляем все найденные ID
        matching_ids.extend(matching_rows["ID"].tolist())

    return matching_ids


def get_rows_to_evaluate(
    csv_files: List[str],
    ratings_files: List[str],
    limit_per_file: int,
    surname: str = None,
    username: str = None,
    affiliation: str = None,
) -> List[Dict]:
    """
    Получение строк для оценки из файлов с исходными данными, которые еще не были оценены,
    проверяя комбинации персональных данных и чередуя строки между файлами

    Args:
        csv_files (List[str]): Список путей к CSV файлам с исходными данными
        ratings_files (List[str]): Список путей к CSV файлам с оценками
        limit_per_file (int): Ограничение на количество строк для оценки из каждого файла
        surname (str): Значение фамилии (SURNAME) для поиска
        username (str): Значение имени (USERNAME) для поиска
        affiliation (str): Значение принадлежности (AFFILIATION) для поиска

    Returns:
        List[Dict]: Список строк, которые нужно оценить, в виде словарей
    """

    all_existing_ids = set()

    # Собираем все ID, которые уже были оценены
    for ratings_file in ratings_files:
        all_existing_ids.update(
            get_existing_ids(ratings_file, surname, username, affiliation)
        )

    # print(all_existing_ids)

    all_dataframes = [read_csv_file(csv_file) for csv_file in csv_files]

    rows_to_evaluate = []
    rows_added = [0] * len(csv_files)

    # Получаем ID пользователей с заданной комбинацией
    matching_ids = get_user_ids_by_combination(
        ratings_files, surname, username, affiliation
    )

    if not matching_ids:
        all_existing_ids = set()

    # print(matching_ids)

    while any(
        rows_added[i] < min(limit_per_file, len(all_dataframes[i]))
        for i in range(len(csv_files))
    ):
        for i, df in enumerate(all_dataframes):
            if rows_added[i] >= min(limit_per_file, len(df)):
                continue

            row = df.iloc[rows_added[i]]

            # Проверяем, чтобы ID не было среди matching_ids или all_existing_ids
            if row["ID"] not in matching_ids and row["ID"] not in all_existing_ids:
                row_dict = row.to_dict()
                row_dict["source_file"] = csv_files[i]
                # print(row_dict["source_file"], row["ID"], row.get("Name", "No Name"))
                rows_to_evaluate.append(row_dict)

            rows_added[i] += 1

    return rows_to_evaluate
