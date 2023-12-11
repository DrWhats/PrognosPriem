import streamlit as st
import pandas as pd
import ds
import model
import json

st.header("Загрузка файла CSV для прогнозирования")

uploaded_file = st.file_uploader("Выберите файл CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        # Прогноз для каждой строки в файле
        results = []
        for index, row in df.iterrows():
            params_dict = {
                'Пол': 0 if row['Пол'] == 'М' else 1,
                'Льготы': 0 if row['Льготы'] == False else 1,
                # ... (добавьте остальные параметры)
            }

            json_data = json.dumps(params_dict, ensure_ascii=False)
            result = model.predict(json_data)
            results.append(result)

        # Добавьте столбец с результатами в DataFrame
        df['Результат прогноза'] = results
        st.dataframe(df)

    except Exception as e:
        st.error(f"Ошибка при чтении файла: {e}")
