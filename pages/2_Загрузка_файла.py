import streamlit as st
import pandas as pd
import ds
import model
import json
import ds

st.header("Загрузка файла CSV для прогнозирования")

uploaded_file = st.file_uploader("Выберите файл xlsx", type=["xlsx"])

if uploaded_file is not None:
    # try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.dataframe(df)
        df = ds.prepare_df(df)
        

        # Прогноз для каждой строки в файле
        results = []
        for index, row in df.iterrows():
            params_dict = {
                'Пол': 0 if row['Пол'] == 'М' else 1,
                'Льготы': 0 if row['Льготы'] == False else 1,
                'Нуждается в общежитии': 0 if row['Нуждается в общежитии'] == False else 1,
                'Иностранный язык': 1 if row['Иностранный язык'] == 'Изучался' else 0,
                'Спорт': 0 if row['Спорт'] == False else 1,
                'Служба в армии': 0 if row['Служба в армии'] == False else 1,
                'Полученное образование': row['Полученное образование'],
                'Форма получения док. об образ.': row['Форма получения док. об образ.'],
                'Вид возмещения затрат': 0 if row['Вид возмещения затрат'] == 'Договор' else 1,
                'Форма обучения': row['Форма обучения'],
                'Вид приема': row['Вид приема'],
                'Формирующее подр.': row['Формирующее подр.'],
                'Набор ОП': row['Набор ОП'],
                'Целевой прием': 1 if row['Целевой прием'] == True else 0,
                'Сумма баллов': ds.normalize_sum_ball(int(row['Сумма баллов'])),
                'Сумма баллов за индивидуальные достижения': ds.mormalize_achieve_ball(
                    int(row['Сумма баллов за индивидуальные достижения'])),
                'Возраст': ds.normalize_Age(int(row['Возраст'])),
                'Населённый пункт': row['Населенный пункт']
            }

            json_data = json.dumps(params_dict, ensure_ascii=False)
            result = model.predict(json_data)
            results.append(result)

        # Добавьте столбец с результатами в DataFrame
        df['Результат прогноза'] = results
        st.dataframe(df)

    # except Exception as e:
    #     st.error(f"Ошибка при чтении файла: {e}")



