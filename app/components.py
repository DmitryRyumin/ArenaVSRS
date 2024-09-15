"""
File: components.py
Author: Dmitry Ryumin
Description: Функции для создания компонентов Gradio
License: MIT License
"""

import gradio as gr
from typing import List, Literal, Optional, Union


def html_message(
    message: str = "", error: bool = True, visible: bool = True
) -> gr.HTML:
    """
    Создание HTML сообщения для отображения в интерфейсе Gradio приложения

    Args:
        message (str): Текст сообщения, которое будет отображено
        error (bool): Определение, отображать сообщение в виде ошибки или нет
        visible (bool): Определение, будет ли сообщение видно. По умолчанию True

    Returns:
        gr.HTML: Компонент HTML с форматированным сообщением для отображения в интерфейсе Gradio приложения
    """

    css_class = "noti_err" if error else "noti_true"

    return gr.HTML(value=f"<h3 class='{css_class}'>{message}</h3>", visible=visible)


def dataframe(
    headers: Optional[List[str]] = None,
    values: Optional[List[List[Union[str, int, float, None]]]] = None,
    label: Optional[str] = None,
    show_label: bool = True,
    height: int = 500,
    wrap: bool = True,
    visible: bool = True,
    interactive: bool = False,
    elem_classes: Optional[str] = "dataframe",
) -> gr.Dataframe:
    """
    Создание Dataframe с заданными параметрами для отображения в интерфейсе Gradio приложения

    Args:
        headers (Optional[List[str]]): Список заголовков столбцов таблицы
        values (Optional[List[List[Union[str, int, float, None]]]]): Список строк данных для таблицы
        label (Optional[str]): Текст метки таблицы
        show_label (bool): Определение, отображать ли метку таблицы
        height (int): Высота таблицы в пикселях
        wrap (bool): Перенос текста в ячейках
        visible (bool): Определение, будет ли таблица видимой
        interactive (bool): Определение возможности взаимодействия с таблицей
        elem_classes (Optional[str]): CSS класс для оформления таблицы

    Returns:
        gr.Dataframe: Компонент таблицы для отображения в интерфейсе Gradio приложения
    """

    if headers is None or values is None:
        datatype = "str"
    else:
        datatype = ["markdown"] * len(headers)

    return gr.Dataframe(
        value=values,
        headers=headers,
        datatype=datatype,
        label=label,
        show_label=show_label,
        height=height,
        wrap=wrap,
        visible=visible,
        interactive=interactive,
        elem_classes=elem_classes,
    )


def textbox_create_ui(
    value: Optional[str] = None,
    type: Literal["text", "password", "email"] = "text",
    label: Optional[str] = None,
    placeholder: Optional[str] = None,
    info: Optional[str] = None,
    max_lines: int = 1,
    show_label: bool = True,
    interactive: bool = True,
    visible: bool = True,
    show_copy_button: bool = True,
    scale: int = 1,
    container: bool = False,
):
    """
    Создание текстового поля с заданными параметрами для отображения в интерфейсе Gradio приложения

    Args:
        value (Optional[str]): Значение текстового поля
        type (Literal["text", "password", "email"]): Тип текстового поля. Доступные значения:
            - "text": обычный текст
            - "password": скрытый текст (для ввода пароля)
            - "email": поле для ввода электронной почты
        label (Optional[str]): Текст метки для текстового поля
        placeholder (Optional[str]): Текст подсказки, отображаемый в поле, когда оно пустое
        info (Optional[str]): Дополнительная информация
        max_lines (int): Максимальное количество строк для многострочного текстового поля
        show_label (bool): Определение, отображать ли метку текстового поля
        interactive (bool): Определение возможности взаимодействия с текстовым полем
        visible (bool): Определение, будет ли текстовое поле видимое
        show_copy_button (bool): Определение, отображать ли кнопку копирования содержимого текстового поля
        scale (int): Масштабирование размера текстового поля
        container (bool): Определение, оборачивать ли текстовое поле в контейнер

    Returns:
        gr.Textbox: Компонент текстового поля для отображения в интерфейсе Gradio приложения
    """

    return gr.Textbox(
        value=value,
        type=type,
        label=label,
        placeholder=placeholder,
        info=info,
        max_lines=max_lines,
        show_label=show_label,
        interactive=interactive,
        visible=visible,
        show_copy_button=show_copy_button,
        scale=scale,
        container=container,
    )


def dropdown_create_ui(
    label: Optional[str] = None,
    info: Optional[str] = None,
    choices: Optional[List[str]] = None,
    value: Optional[List[str]] = None,
    multiselect: bool = False,
    show_label: bool = True,
    interactive: bool = True,
    visible: bool = True,
    render: bool = True,
    elem_classes: Optional[str] = None,
) -> gr.Dropdown:
    """
    Создание выпадающего списка с заданными параметрами для отображения в интерфейсе Gradio приложения

    Args:
        label (Optional[str]): Текст метки для выпадающего списка
        info (Optional[str]): Дополнительная информация
        choices (Optional[List[str]]): Список доступных вариантов для выбора в выпадающем списке
        value (Optional[List[str]]): Начальные выбранные значения
        multiselect (bool): Определение возможности выбора несколько элементов
        show_label (bool): Определение, отображать ли метку выпадающего списка
        interactive (bool): Определение возможности взаимодействия с выподающим списком
        visible (bool): Определение, будет ли выпадающий список видимым
        render (bool): Определение, рендерить ли выпадающий список
        elem_classes (Optional[str]): CSS класс для оформления выпадающего списка

    Returns:
        gr.Dropdown: Компонент выпадающего списка для отображения в интерфейсе Gradio приложения
    """

    return gr.Dropdown(
        choices=choices,
        value=value,
        multiselect=multiselect,
        label=label,
        info=info,
        show_label=show_label,
        interactive=interactive,
        visible=visible,
        render=render,
        elem_classes=elem_classes,
    )


def button(
    value: str = "",
    interactive: bool = True,
    scale: int = 1,
    icon: Optional[str] = None,
    visible: bool = True,
    elem_classes: Optional[str] = None,
) -> gr.Button:
    """
    Создание кнопки с заданными параметрами для отображения в интерфейсе Gradio приложения

    Args:
        value (str): Текст кнопки
        interactive (bool): Определение возможности взаимодействия с кнопкой
        scale (int): Масштабирование размера кнопки
        icon (Optional[str]): Иконка для кнопки
        visible (bool): Определение, будет ли кнопка видимой
        elem_classes (Optional[str]): CSS класс для оформления кнопки

    Returns:
        gr.Button: Компонент кнопки для отображения в интерфейсе Gradio приложения
    """

    return gr.Button(
        value=value,
        interactive=interactive,
        scale=scale,
        icon=icon,
        visible=visible,
        elem_classes=elem_classes,
    )
