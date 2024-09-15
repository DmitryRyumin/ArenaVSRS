"""
File: event_handlers.py
Author: Dmitry Ryumin
Description: Обработчики событий для Gradio компонентов
License: MIT License
"""

import gradio as gr

# Импорт необходимых компонентов для Gradio приложения
# from app.event_handlers.page_refresh import event_handler_page_refresh
from app.event_handlers.auth import event_handler_auth
from app.event_handlers.login import event_handler_login
from app.event_handlers.dropdown_rating import event_handler_dropdown_rating
from app.event_handlers.calculate_rating import event_handler_calculate_rating


def setup_app_event_handlers(
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
    # gradio_app,
):
    # Events
    # gradio_app.load(
    #     event_handler_page_refresh,
    #     inputs=None,
    #     outputs=[
    #         surname,
    #         username,
    #         dropdown_user,
    #         auth,
    #         notifications_auth,
    #         step_2,
    #         csv_vsa_file,
    #         vacancy_id,
    #         vacancy_name,
    #         vacancy_description,
    #         dropdown_keyskills,
    #         noti_keyskills,
    #         res_a,
    #         res_b,
    #         dropdown_rating_a,
    #         dropdown_rating_b,
    #         calculate_rating,
    #         notifications_calculate,
    #     ],
    # )
    gr.on(
        triggers=[surname.change, username.change, dropdown_user.change],
        fn=event_handler_auth,
        inputs=[surname, username, dropdown_user],
        outputs=[
            auth,
            notifications_auth,
        ],
        queue=True,
    )
    auth.click(
        fn=event_handler_login,
        inputs=[surname, username, dropdown_user],
        outputs=[
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
        ],
        queue=True,
    )
    gr.on(
        triggers=[dropdown_rating_a.change, dropdown_rating_b.change],
        fn=event_handler_dropdown_rating,
        inputs=[dropdown_rating_a, dropdown_rating_b],
        outputs=[calculate_rating, notifications_calculate],
        queue=True,
    )
    calculate_rating.click(
        fn=event_handler_calculate_rating,
        inputs=[
            surname,
            username,
            dropdown_user,
            csv_vsa_file,
            vacancy_id,
            dropdown_rating_a,
            dropdown_rating_b,
        ],
        outputs=[
            csv_vsa_file,
            vacancy_id,
            vacancy_name,
            vacancy_description,
            dropdown_keyskills,
            noti_keyskills,
            res_a,
            res_b,
            dropdown_rating_a,
            dropdown_rating_b,
            calculate_rating,
            notifications_calculate,
        ],
        queue=True,
    )
