import streamlit as st
import pandas as pd
import ds

st.header("Прогнозирование поступления ПГГПУ")

with st.form("my_form"):
    with st.container(border=True):
        sex = st.radio(
            "Пол",
            ["М", "Ж"],
            index=None,
        )

    with st.container(border=True):
        benefit = st.checkbox('Льгота')

    with st.container(border=True):
        hostel = st.checkbox('Нуждается в общежитии')

    with st.container(border=True):
        language = st.selectbox(
            'Иностранный язык',
            ("Изучался", "Не изучался"), placeholder="Иностранный язык")

    with st.container(border=True):
        sport = st.checkbox('Спорт')

    with st.container(border=True):
        army = st.checkbox('Служба в армии')

    with st.container(border=True):
        education = st.selectbox(
            'Полученное образование',
            (ds.get_edu()))

    with st.container(border=True):
        document_educatuon = st.radio(
            "Форма получения док. об образ.",
            ["Оригинал", "Копия"],
            index=None,
        )

    with st.container(border=True):
        pay_type = st.radio(
            "Вид возмещения затрат",
            ["Бюджет", "Договор"],
            index=None,
        )

    with st.container(border=True):
        education_form = st.selectbox(
            'Форма обучения',
            (ds.get_form()))

    with st.container(border=True):
        reception_type = st.selectbox(
            'Вид приема',
            (ds.get_enroll_type()))

    with st.container(border=True):
        department = st.selectbox(
            'Формирующее подр.',
            (ds.get_faculty()))

    with st.container(border=True):
        education_program = st.selectbox(
            'Набор ОП',
            (ds.get_op()))

    with st.container(border=True):
        targeted_reception = st.checkbox('Целевой прием')

    with st.container(border=True):
        agreement = st.checkbox('Итоговое согласие')

    with st.container(border=True):
        total_points = st.text_input('Сумма баллов')

    with st.container(border=True):
        total_achievements_points = st.number_input('Сумма баллов за индивидуальные достижения', min_value=0,
                                                    max_value=10)

    with st.container(border=True):
        age = st.number_input('Возраст', min_value=17, max_value=25)

    with st.container(border=True):
        settlement = st.selectbox(
            'Населенный пункт',
            (ds.get_cites()))

    submitted = st.form_submit_button("Сформировать прогноз")

    if submitted:
        if not sex:
            st.error("Отметьте пол")
        elif not language:
            st.error("Выберите языки")
        elif not education:
            st.error("Выберите полученное образование")
        elif not document_educatuon:
            st.error("Выберите форму получения документа об образовании")
        elif not pay_type:
            st.error("Выберите вид возмещения затрат")
        elif not education_form:
            st.error("Выберите форму обучения")
        elif not reception_type:
            st.error("Выберите вид приема")
        elif not department:
            st.error("Выберите формирующее подразделение")
        elif not education_program:
            st.error("Выберите набор образовательных программ")
        elif not total_points:
            st.error("Введите сумму баллов")
        elif not total_achievements_points:
            st.error("Введите сумму баллов за индивидуальные достижения")
        elif not age:
            st.error("Введите возраст")
        elif not settlement:
            st.error("Выберите населенный пункт")
        else:
            st.success("Загрузка...")

st.write(age)
