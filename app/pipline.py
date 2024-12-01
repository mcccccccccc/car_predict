import pandas as pd
from sklearn.base import TransformerMixin, BaseEstimator
import pickle


numeric_features = ["year", "km_driven", "mileage", "seats", "engine", "max_power"]
categorical_features = ["fuel", "seller_type", "transmission", "owner"]


# Я ПОЛ ДНЯ БИЛСЯ - ТАК И НЕ СМОГ ЗАСУНУТЬ ЭТОТ КАСТОМНЫЙ ТРАНСФОРМЕР В ПИКЛ, ТАК ЧТОБЫ ОН ПОДТЯШИВАЛСЯ ИМЕНО В ФАСТАПИ. в колабе получилось, нор у фаст апи какая-то своя система импортов
# и вываливатеся ошибка о том что не найден класс TransformStrCols.
# class TransformStrCols(TransformerMixin):
#     def __init__(self, cols):
#         self.cols = cols
#
#     def fit(self, X, y=None):
#         return self
#
#     def transform(self, X, y=None):
#         X_res = X.copy()
#
#         # cols_to_convert = ['mileage', 'engine', 'max_power', 'torque']
#         for c in self.cols:
#
#             # отдельно обработаем колонку torque. Сделаем из нее 2 числовых: nuton_metr, rpm
#             if c == 'torque':
#                 nm_rps = X_res['torque'].str.split(r"@|at", n=1, expand=True)
#                 nm_rps.rename(columns={0: 'nuton_metr', 1: 'rpm'}, inplace=True)
#                 nm_rps['nuton_metr'] = nm_rps['nuton_metr'].str.replace(r'[^\d.-]', '', regex=True).astype(float)
#                 j = nm_rps['rpm'].str.replace(r'[^\d.-]', '', regex=True).str.split(r"-", n=1, expand=True).astype(
#                     float)
#                 nm_rps['rpm'] = j.mean(axis=1)
#                 X_res = X_res.join(nm_rps)
#                 X_res = X_res.drop(columns=['torque'])
#             else:
#                 X_res[c] = X_res[c].str.replace(r'[^\d.-]', '', regex=True)
#                 X_res[c] = pd.to_numeric(X_res[c], errors='coerce')
#
#         # disp(X_res)
#
#         return X_res


def remove_duplicates(df):
    df = df.drop_duplicates(keep='first')
    df = df.reset_index(drop=True)

    return df


def drop_cols(df):
    df = df[categorical_features + numeric_features]

    return df

def convert_str_cols(df):
    for c in ['mileage', 'engine', 'max_power']:
        df[c] = df[c].str.replace(r'[^\d.-]', '', regex=True)
        df[c] = pd.to_numeric(df[c], errors='coerce')

    return df


def get_pipe(filename):
    with open(filename, 'rb') as f:
        pipe = pickle.load(f)

    return pipe
