"""
File: tabs.py
Author: Dmitry Ryumin
Description: Вкладки Gradio приложения
License: MIT License
"""

import gradio as gr

# Импорт необходимых компонентов для Gradio приложения
from app.description import DESCRIPTION
from app.description_steps import STEP_1, STEP_2
from app.app import APP
from app.authors import AUTHORS
from app.config import config_data
from app.requirements_app import parse_requirements
from app.components import (
    dataframe,
    textbox_create_ui,
    dropdown_create_ui,
    button,
    html_message,
)
from app.data_init import (
    first_vsa_row,
    headers_a,
    headers_b,
    parsed_first_dataframe_a,
    parsed_first_dataframe_b,
)


def app_tab():
    gr.Markdown(value=DESCRIPTION)

    gr.HTML(value=STEP_1)

    with gr.Row(
        visible=True,
        render=True,
        variant="default",
        elem_classes="user-container",
    ):
        surname = textbox_create_ui(
            value=None,
            type="text",
            label=config_data.Labels_SURNAME,
            placeholder=config_data.OtherMessages_IMPORTANT,
            info=config_data.InformationMessages_SURNAME,
            max_lines=1,
            show_label=True,
            interactive=True,
            visible=True,
            show_copy_button=False,
            scale=1,
            container=True,
        )

        username = textbox_create_ui(
            value=None,
            type="text",
            label=config_data.Labels_USERNAME,
            placeholder=config_data.OtherMessages_IMPORTANT,
            info=config_data.InformationMessages_USERNAME,
            max_lines=1,
            show_label=True,
            interactive=True,
            visible=True,
            show_copy_button=False,
            scale=1,
            container=True,
        )

        dropdown_user = dropdown_create_ui(
            label=config_data.Labels_USER_AFFILIATION,
            info=config_data.InformationMessages_USER_AFFILIATION,
            choices=config_data.Settings_DROPDOWN_USER,
            value=None,
            interactive=True,
            visible=True,
            elem_classes="dropdown-user",
        )

    with gr.Row(
        visible=True,
        render=True,
        variant="default",
        elem_classes="auth-container",
    ):
        auth = button(
            value=config_data.OtherMessages_AUTH,
            interactive=False,
            scale=1,
            icon=config_data.StaticPaths_IMAGES + "auth.ico",
            visible=True,
            elem_classes="auth",
        )

    notifications_auth = html_message(
        message=config_data.InformationMessages_NOTI_AUTH[0],
        error=True,
        visible=True,
    )

    step_2 = gr.HTML(value=STEP_2, visible=False)

    with gr.Column(
        scale=1,
        visible=False,
        render=True,
        variant="default",
        elem_classes="vacancy-container",
    ) as vacancy_column:
        with gr.Row(
            visible=True,
            render=True,
            variant="default",
            elem_classes="vacancy_name-container",
        ):
            gr.Image(
                value=config_data.StaticPaths_IMAGES + "vacancy.png",
                container=False,
                interactive=False,
                visible=True,
                show_download_button=False,
                show_fullscreen_button=False,
                elem_classes="metadata_vacancy-logo",
            )

            csv_vsa_file = textbox_create_ui(
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
            )

            vacancy_id = textbox_create_ui(
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
            )

            vacancy_name = textbox_create_ui(
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
            )
        with gr.Accordion(
            label=config_data.Labels_VACANCY_DESCRIPTION,
            open=True,
            visible=True,
        ):
            vacancy_description = gr.HTML(
                value=None, elem_classes="vacancy_description"
            )

            dropdown_keyskills = dropdown_create_ui(
                label=config_data.Labels_DROPDOWN_KEYSKILLS,
                info=config_data.InformationMessages_DROPDOWN_KEYSKILLS,
                choices=None,
                value=None,
                multiselect=True,
                visible=False,
                elem_classes="dropdown-keyskills",
            )

            noti_keyskills = html_message(
                message=config_data.InformationMessages_NOTI_KEYSKILLS,
                error=True,
                visible=False,
            )

    with gr.Row(
        visible=False,
        render=True,
        variant="default",
        elem_classes="rating-container",
    ) as rating_row:
        with gr.Column(scale=1, visible=True, render=True):
            res_a = dataframe(
                headers=headers_a,
                values=parsed_first_dataframe_a,
                label=config_data.Labels_RESULT_A,
                show_label=True,
                visible=True,
            )

            dropdown_rating_a = dropdown_create_ui(
                label=f"{config_data.Labels_DROPDOWN_RATING} {config_data.Settings_RATING_SCALE}",
                info=config_data.InformationMessages_DROPDOWN_RATING_INFO,
                choices=range(1, config_data.Settings_RATING_SCALE + 1),
                value=None,
                visible=True,
                elem_classes="dropdown-container",
            )

        with gr.Column(scale=1, visible=True, render=True):
            res_b = dataframe(
                headers=headers_b,
                values=parsed_first_dataframe_b,
                label=config_data.Labels_RESULT_B,
                show_label=True,
                visible=True,
            )

            dropdown_rating_b = dropdown_create_ui(
                label=f"{config_data.Labels_DROPDOWN_RATING} {config_data.Settings_RATING_SCALE}",
                info=config_data.InformationMessages_DROPDOWN_RATING_INFO,
                choices=range(1, config_data.Settings_RATING_SCALE + 1),
                value=None,
                visible=True,
                elem_classes="dropdown-container",
            )

    calculate_rating = button(
        value=config_data.OtherMessages_CALCULATE_RATING,
        interactive=False,
        scale=1,
        icon=config_data.StaticPaths_IMAGES + "calculate_rating.ico",
        visible=False,
        elem_classes=None,
    )

    notifications_calculate = html_message(
        message=config_data.InformationMessages_NOTI_CALCULATE_RATING[0],
        error=True,
        visible=False,
    )

    return (
        surname,
        username,
        dropdown_user,
        auth,
        notifications_auth,
        step_2,
        vacancy_column,
        csv_vsa_file,
        vacancy_id,
        vacancy_name,
        vacancy_description,
        dropdown_keyskills,
        noti_keyskills,
        rating_row,
        res_a,
        res_b,
        dropdown_rating_a,
        dropdown_rating_b,
        calculate_rating,
        notifications_calculate,
    )


def about_app_tab():
    return gr.HTML(value=APP)


def about_authors_tab():
    return gr.HTML(value=AUTHORS)


def requirements_app_tab():
    requirements_df = parse_requirements()

    return dataframe(
        headers=requirements_df.columns.tolist(),
        values=requirements_df.values.tolist(),
        visible=True,
        elem_classes="requirements-dataframe",
    )
