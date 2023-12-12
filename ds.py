import pandas as pd

df = pd.read_csv("train.csv", sep=";")
kladr = pd.read_csv("KLADR.csv", sep=";", encoding='utf-8').rename(
    columns={"NAME": "Населённый пункт", "CODE": "Код насел. пункта"})[["Населённый пункт", "Код насел. пункта"]]


def normalize_sum_ball(ball):
    ball = (ball - df['Сумма баллов'].min()) / (
            df['Сумма баллов'].max() - df['Сумма баллов'].min())
    return ball


def mormalize_achieve_ball(ball):
    ball = (ball - df['Сумма баллов за индивидуальные достижения'].min()) / (
            df['Сумма баллов за индивидуальные достижения'].max() -
            df['Сумма баллов за индивидуальные достижения'].min())
    return ball


def normalize_Age(age):
    age = (age - df['Возраст'].min()) / (df['Возраст'].max() - df['Возраст'].min())


def get_cites():
    return df['Населённый пункт'].unique()


def get_op():
    return df['Набор ОП'].unique()


def get_edu():
    return df['Полученное образование'].unique()


def get_faculty():
    return df['Формирующее подр.'].unique()


def get_payment():
    return df['Вид возмещения затрат'].unique()


def get_form():
    return df['Форма обучения'].unique()


def get_enroll_type():
    return df['Вид приема'].unique()


def prepare_df(new_df):
    new_df['Дата подачи'] = pd.to_datetime(new_df['Дата подачи'])
    new_df['Дата рождения'] = pd.to_datetime(new_df['Дата рождения'])
    new_df['Возраст'] = (new_df['Дата подачи'] - new_df['Дата рождения']).astype('<m8[Y]')
    new_df.loc[
        new_df['Полученное образование'].str.contains('Среднее общее образование'), 'Полученное образование'] = 'СОО'
    new_df.loc[new_df['Полученное образование'].str.contains(
        'Среднее профессиональное образование'), 'Полученное образование'] = 'СПО'
    new_df.loc[new_df['Полученное образование'].str.contains('Высшее образование'), 'Полученное образование'] = 'ВО'
    new_df["Льготы"][new_df["Льготы"].notnull()] = 1
    new_df["Льготы"][new_df["Льготы"].isnull()] = 0
    new_df["Спорт"][new_df["Спорт"].notnull()] = 1
    new_df["Спорт"][new_df["Спорт"].isnull()] = 0
    new_df["Иностранный язык"][new_df["Иностранный язык"].isnull()] = "Нет"
    new_df["Код насел. пункта"] = new_df["Код насел. пункта"].astype("int64")
    dataframe = new_df.merge(kladr, how="left", on="Код насел. пункта")
    cities = dataframe[['Населённый пункт']].value_counts()
    rare_cities = cities[cities < 100]
    dataframe['Населённый пункт'] = dataframe['Населённый пункт'].replace(rare_cities.index.values,
                                                                          'Редкие нас. пункты')
    dataframe['Населённый пункт'][dataframe['Населённый пункт'].isnull()] = 'Редкие нас. пункты'
    dataframe['Состояние выбран. конкурса'][dataframe['Состояние выбран. конкурса'].isin(
        ["Сданы ВИ", "Забрал документы", "Выбыл из конкурса", "Отказ от зачисления",
         "Исключен (зачислен на другой конкурс)", "Активный"])] = 0
    dataframe['Состояние выбран. конкурса'][dataframe['Состояние выбран. конкурса'].isin(["Зачислен"])] = 1

    def trunc(str):
        return str.split(",")[0]

    dataframe["Служба в армии"] = dataframe["Служба в армии"].apply(trunc)
    dataframe["Служба в армии"][dataframe["Служба в армии"].isin(["Да", "да", "ДА", "дА"])] = 1
    dataframe["Служба в армии"][dataframe["Служба в армии"].isin(["Нет", "нет", "НЕТ", "нЕт", "неТ"])] = 0
    dataframe = (
        dataframe[
            [
                col for col in dataframe.columns if col not in [
                'Дата рождения', 'Код насел. пункта',
                'Дата подачи', 'Личный номер', 'Законченное образ. учреждение']]
        ].reset_index()
    )
    dataframe["Пол"][dataframe["Пол"] == "Ж"] = 1
    dataframe["Пол"][dataframe["Пол"] == "М"] = 0
    dataframe["Нуждается в общежитии"][dataframe["Нуждается в общежитии"] == "нет"] = 0
    dataframe["Нуждается в общежитии"][dataframe["Нуждается в общежитии"] == "да"] = 1
    dataframe.loc[dataframe["Иностранный язык"] != "Нет", "Иностранный язык"] = 1
    dataframe.loc[dataframe["Иностранный язык"] == "Нет", "Иностранный язык"] = 0
    dataframe.loc[dataframe["Целевой прием"] != "нет", "Целевой прием"] = 1
    dataframe.loc[dataframe["Целевой прием"] == "нет", "Целевой прием"] = 0
    dataframe.loc[dataframe["Итоговое согласие"] != "нет", "Итоговое согласие"] = 1
    dataframe.loc[dataframe["Итоговое согласие"] == "нет", "Итоговое согласие"] = 0
    dataframe.loc[dataframe["Вид возмещения затрат"] != "бюджет", "Вид возмещения затрат"] = 0
    dataframe.loc[dataframe["Вид возмещения затрат"] == "бюджет", "Вид возмещения затрат"] = 1
    dataframe['Сумма баллов'] = (dataframe['Сумма баллов'] - dataframe['Сумма баллов'].min()) / (
            dataframe['Сумма баллов'].max() - dataframe['Сумма баллов'].min())
    dataframe['Сумма баллов за индивидуальные достижения'] = (dataframe['Сумма баллов за индивидуальные достижения'] -
                                                              dataframe[
                                                                  'Сумма баллов за индивидуальные достижения'].min()) / (
                                                                     dataframe[
                                                                         'Сумма баллов за индивидуальные достижения'].max() -
                                                                     dataframe[
                                                                         'Сумма баллов за индивидуальные достижения'].min())
    dataframe['Возраст'] = (dataframe['Возраст'] - dataframe['Возраст'].min()) / (
            dataframe['Возраст'].max() - dataframe['Возраст'].min())

    return dataframe
