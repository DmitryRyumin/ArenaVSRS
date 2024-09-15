"""
File: data_init.py
Author: Dmitry Ryumin
Description: Начальная загрузка данных
License: MIT License
"""

# import time
import pandas as pd

# Импорт необходимых компонентов для Gradio приложения
from app.config import config_data
from app.rating_utils import get_rows_to_evaluate
from app.data_utils import (
    get_csv_files,
    load_excel_files,
    parse_course_data,
    randomize_results,
    wrap_subjects,
)

# start_time = time.time()
csv_vsa_files = get_csv_files(config_data.StaticPaths_VSA)
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Время выполнения 1: {execution_time:.3f} секунд")


# start_time = time.time()
csv_vsa_files = get_csv_files(config_data.StaticPaths_VSA)
# end_time = time.time()
# execution_time = end_time - start_time
# print(f"Время выполнения 1: {execution_time:.3f} секунд")

ratings_files = get_csv_files(config_data.StaticPaths_ARENA)

rows_to_evaluate = get_rows_to_evaluate(
    csv_vsa_files,
    ratings_files,
    config_data.Settings_EVALUATE_LIMIT,
    surname=None,
    username=None,
    affiliation=None,
)

first_row_to_evaluate = rows_to_evaluate[0]
first_vsa_dataframe_headers = list(first_row_to_evaluate.keys())
first_vsa_row = pd.Series(first_row_to_evaluate)

xlsx_subjects_dataframe = load_excel_files(config_data.StaticPaths_SUBJECTS)
xlsx_subjects_dataframe_unique = xlsx_subjects_dataframe.drop_duplicates(
    subset=[config_data.DataframeHeaders_RU_SUBJECT]
)
xlsx_unique_subjects = set(
    xlsx_subjects_dataframe_unique[config_data.DataframeHeaders_RU_SUBJECT].str.lower()
)

state = {
    "random_order": None,
    "dataframe_a": wrap_subjects(
        parse_course_data(first_vsa_row[first_vsa_dataframe_headers[7]], [2, 3]),
        xlsx_unique_subjects,
    ),
    "dataframe_b": wrap_subjects(
        parse_course_data(first_vsa_row[first_vsa_dataframe_headers[6]], None, True),
        xlsx_unique_subjects,
    ),
}

parsed_first_dataframe_a, headers_a, parsed_first_dataframe_b, headers_b = (
    randomize_results(config_data, state)
)
