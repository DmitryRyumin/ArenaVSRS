"""
File: page_refresh.py
Author: Dmitry Ryumin
Description: Event handler for Gradio app to page refresh.
License: MIT License
"""

import math
import pandas as pd
import gradio as gr

# Importing necessary components for the Gradio app
from app.config import config_data
from app.rating_utils import get_rows_to_evaluate
from app.components import (
    dataframe,
    textbox_create_ui,
    dropdown_create_ui,
    button,
    html_message,
)
from app.data_utils import (
    get_csv_files,
    parse_course_data,
    randomize_results,
    wrap_subjects,
)
from app.data_init import xlsx_unique_subjects


def event_handler_page_refresh():
    csv_vsa_files = get_csv_files(config_data.StaticPaths_VSA)
    ratings_files = get_csv_files(config_data.StaticPaths_ARENA)

    rows_to_evaluate = get_rows_to_evaluate(
        csv_vsa_files,
        ratings_files,
        config_data.Settings_EVALUATE_LIMIT,
    )

    first_row_to_evaluate = rows_to_evaluate[0]
    first_vsa_dataframe_headers = list(first_row_to_evaluate.keys())
    first_vsa_row = pd.Series(first_row_to_evaluate)

    state = {
        "random_order": None,
        "dataframe_a": wrap_subjects(
            parse_course_data(first_vsa_row[first_vsa_dataframe_headers[7]], [2, 3]),
            xlsx_unique_subjects,
        ),
        "dataframe_b": wrap_subjects(
            parse_course_data(
                first_vsa_row[first_vsa_dataframe_headers[6]], None, True
            ),
            xlsx_unique_subjects,
        ),
    }

    parsed_first_dataframe_a, headers_a, parsed_first_dataframe_b, headers_b = (
        randomize_results(config_data, state)
    )

    if isinstance(first_vsa_row["KeySkills"], str):
        key_skills = [
            item.strip()
            for item in first_vsa_row["KeySkills"].split(",")
            if item.strip()
        ]
        noti_keyskills_visible = False
    elif math.isnan(first_vsa_row["KeySkills"]):
        key_skills = None
        noti_keyskills_visible = True

    return (
        textbox_create_ui(
            value=first_vsa_row["source_file"],
            type="text",
            label=None,
            placeholder=None,
            info=None,
            max_lines=1,
            show_label=False,
            interactive=False,
            visible=False,
            show_copy_button=False,
            scale=1,
            container=False,
        ),
        textbox_create_ui(
            value=first_vsa_row["ID"],
            type="text",
            label=None,
            placeholder=None,
            info=None,
            max_lines=1,
            show_label=False,
            interactive=False,
            visible=False,
            show_copy_button=False,
            scale=1,
            container=False,
        ),
        textbox_create_ui(
            value=first_vsa_row["Name"],
            type="text",
            label=None,
            placeholder=None,
            info=None,
            max_lines=1,
            show_label=False,
            interactive=False,
            visible=True,
            show_copy_button=False,
            scale=1,
            container=False,
        ),
        gr.HTML(value=first_vsa_row["Description"], elem_classes="vacancy_description"),
        dropdown_create_ui(
            label=config_data.Labels_DROPDOWN_KEYSKILLS,
            info=config_data.InformationMessages_DROPDOWN_KEYSKILLS.format(
                len(key_skills) if isinstance(key_skills, list) else 0
            ),
            choices=key_skills,
            value=key_skills,
            multiselect=True,
            interactive=False,
            visible=not noti_keyskills_visible,
            elem_classes="dropdown-keyskills",
        ),
        html_message(
            message=config_data.InformationMessages_NOTI_KEYSKILLS,
            error=True,
            visible=noti_keyskills_visible,
        ),
        dataframe(
            headers=headers_a,
            values=parsed_first_dataframe_a,
            label=config_data.Labels_RESULT_A,
            show_label=True,
            visible=True,
        ),
        dataframe(
            headers=headers_b,
            values=parsed_first_dataframe_b,
            label=config_data.Labels_RESULT_B,
            show_label=True,
            visible=True,
        ),
        dropdown_create_ui(
            label=f"{config_data.Labels_DROPDOWN_RATING} {config_data.Settings_RATING_SCALE}",
            info=config_data.InformationMessages_DROPDOWN_RATING_INFO,
            choices=range(1, config_data.Settings_RATING_SCALE + 1),
            value=None,
            visible=True,
            elem_classes="dropdown-container",
        ),
        dropdown_create_ui(
            label=f"{config_data.Labels_DROPDOWN_RATING} {config_data.Settings_RATING_SCALE}",
            info=config_data.InformationMessages_DROPDOWN_RATING_INFO,
            choices=range(1, config_data.Settings_RATING_SCALE + 1),
            value=None,
            visible=True,
            elem_classes="dropdown-container",
        ),
        button(
            value=config_data.OtherMessages_CALCULATE_RATING,
            interactive=False,
            scale=1,
            icon=config_data.StaticPaths_IMAGES + "calculate_rating.ico",
            visible=True,
            elem_classes="calculate_rating",
        ),
        html_message(
            message=config_data.InformationMessages_NOTI_CALCULATE_RATING[0],
            error=True,
            visible=True,
        ),
    )
