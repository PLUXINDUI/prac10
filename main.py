# # main.py
# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.responses import StreamingResponse
# from io import BytesIO
# import pandas as pd
# import numpy as np
# from typing import List
# import matplotlib.pyplot as plt
# import seaborn as sns
# from datetime import datetime

# # Инициализация FastAPI приложения
# app = FastAPI(
#     title="Excel to Markdown API",
#     description="API для обработки Excel файлов и генерации отчетов в формате Markdown",
#     version="1.0.0"
# )

# @app.get("/")
# def read_root():
#     """Корневой маршрут, возвращающий информацию о сервисе"""
#     return {
#         "message": "Excel to Markdown API работает",
#         "endpoints": {
#             "/process-excel/": "Загрузка и обработка Excel-файла с генерацией отчета в формате Markdown"
#         }
#     }

# @app.post("/process-excel/")
# async def process_excel(file: UploadFile = File(...)):
#     """
#     Обрабатывает загруженный Excel-файл и возвращает отчет в формате Markdown
#     """
#     # Проверка формата файла
#     if not file.filename.endswith(('.xlsx', '.xls')):
#         raise HTTPException(
#             status_code=400,
#             detail="Поддерживаются только файлы Excel (.xlsx, .xls)"
#         )

#     try:
#         # Чтение содержимого файла
#         contents = await file.read()
#         buffer = BytesIO(contents)

#         # Загрузка Excel-файла в DataFrame
#         df = pd.read_excel(buffer)

#         # Генерация отчета в формате Markdown на основе данных
#         report = generate_markdown_report(df)

#         # Создание байтового объекта для хранения отчета
#         output = BytesIO(report.encode())
#         output.seek(0)

#         # Возвращаем отчет как скачиваемый файл
#         filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
#         return StreamingResponse(
#             output,
#             media_type="text/markdown",
#             headers={"Content-Disposition": f"attachment; filename={filename}"}
#         )

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Ошибка обработки файла: {str(e)}")

# def generate_markdown_report(df: pd.DataFrame) -> str:
#     """
#     Генерирует отчет в формате Markdown на основе предоставленного DataFrame
#     """
#     # Создаем заголовок отчета
#     report = f"# Отчет по анализу данных\n\n"
#     report += f"Дата создания: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

#     # Основная информация о данных
#     report += f"## Общая информация\n\n"
#     report += f"- **Количество строк**: {df.shape[0]}\n"
#     report += f"- **Количество столбцов**: {df.shape[1]}\n"
#     report += f"- **Столбцы**: {', '.join(df.columns)}\n\n"

#     # Статистика по числовым столбцам
#     report += f"## Статистический анализ\n\n"

#     # Проверяем наличие числовых столбцов
#     numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
#     if numeric_columns:
#         report += f"### Числовые данные\n\n"
#         stats_df = df[numeric_columns].describe().transpose()
#         # Форматируем статистику в виде таблицы Markdown
#         stats_table = "| Столбец | Количество | Среднее | Ст. отклонение | Мин | 25% | 50% | 75% | Макс |\n"
#         stats_table += "| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"

#         for column, row in stats_df.iterrows():
#             stats_table += f"| {column} | {row['count']:.0f} | {row['mean']:.2f} | {row['std']:.2f} | {row['min']:.2f} | {row['25%']:.2f} | {row['50%']:.2f} | {row['75%']:.2f} | {row['max']:.2f} |\n"

#         report += stats_table + "\n\n"

#     # Анализ категориальных данных
#     categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
#     if categorical_columns:
#         report += f"### Категориальные данные\n\n"

#         for column in categorical_columns:
#             value_counts = df[column].value_counts().head(5)  # Топ-5 значений
#             report += f"#### {column}\n\n"

#             # Создаем таблицу с частотами значений
#             report += "| Значение | Количество | Процент |\n"
#             report += "| --- | --- | --- |\n"

#             for value, count in value_counts.items():
#                 percentage = (count / len(df)) * 100
#                 report += f"| {value} | {count} | {percentage:.2f}% |\n"

#             report += "\n"

#     # Анализ пропущенных значений
#     report += f"## Анализ пропущенных значений\n\n"
#     missing_values = df.isnull().sum()
#     if missing_values.sum() > 0:
#         report += "| Столбец | Пропущенные значения | Процент пропущенных |\n"
#         report += "| --- | --- | --- |\n"

#         for column, missing in missing_values.items():
#             if missing > 0:
#                 percentage = (missing / len(df)) * 100
#                 report += f"| {column} | {missing} | {percentage:.2f}% |\n"

#         report += "\n"
#     else:
#         report += "Пропущенные значения отсутствуют.\n\n"

#     # Заключение
#     report += "## Выводы\n\n"
#     report += "На основе анализа данных можно сделать следующие выводы:\n\n"
#     report += "1. Данные содержат информацию о " + str(df.shape[0]) + " записях с " + str(df.shape[1]) + " характеристиками.\n"

#     if numeric_columns:
#         # Находим столбец с наибольшим средним значением
#         max_mean_column = df[numeric_columns].mean().idxmax()
#         max_mean_value = df[numeric_columns].mean().max()
#         report += f"2. Столбец '{max_mean_column}' имеет наибольшее среднее значение ({max_mean_value:.2f}).\n"

#     if missing_values.sum() > 0:
#         most_missing = missing_values.idxmax()
#         most_missing_count = missing_values.max()
#         report += f"3. Столбец '{most_missing}' имеет наибольшее количество пропущенных значений ({most_missing_count}).\n"

#     report += "\n"

#     return report


from fastapi import FastAPI, UploadFile, File, HTTPException, StreamingResponse
from io import BytesIO
import pandas as pd
import json
import csv
import random
import string
from sympy import Matrix, symbols, N
from typing import Optional

app = FastAPI(
    title="Конвертер координат",
    description="API для преобразования координат между системами и генерации отчётов в Excel",
    version="1.0.0"
)

# --- 1. Генератор случайных данных ---
def generate_csv(file_path: str, num_rows: int):
    def random_name(length=5):
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for _ in range(length))
    def random_number():
        return random.randint(100000000, 999999000) / 1000
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'X', 'Y', 'Z'])
        for _ in range(num_rows):
            writer.writerow([random_name(), random_number(), random_number(), random_number()])

# --- 2. Параметры перехода между системами ---
def create_default_parameters(file_path: str = "parameters.json"):
    parameters = {
        "СК-42": {"ΔX": 23.56, "ΔY": -140.86, "ΔZ": -79.77, "ωx": -8.423e-09, "ωy": -1.678e-06, "ωz": -3.849e-06, "m": -0.2274},
        "СК-95": {"ΔX": 24.46, "ΔY": -130.80, "ΔZ": -81.53, "ωx": -8.423e-09, "ωy": 1.724e-08, "ωz": -6.511e-07, "m": -0.2274},
        "ПЗ-90": {"ΔX": -1.443, "ΔY": 0.142, "ΔZ": 0.230, "ωx": -8.423e-09, "ωy": 1.724e-08, "ωz": -6.511e-07, "m": -0.2274},
        "ПЗ-90.02": {"ΔX": -0.373, "ΔY": 0.172, "ΔZ": 0.210, "ωx": -8.423e-09, "ωy": 1.724e-08, "ωz": -2.061e-08, "m": -0.0074},
        "ПЗ-90.11": {"ΔX": 0.0, "ΔY": -0.014, "ΔZ": 0.008, "ωx": 2.724e-09, "ωy": 9.212e-11, "ωz": -2.566e-10, "m": 0.0006},
        "WGS-84 (G1150)": {"ΔX": -0.013, "ΔY": 0.092, "ΔZ": 0.030, "ωx": -8.423e-09, "ωy": 1.724e-08, "ωz": -2.061e-08, "m": -0.0074},
        "ITRF-2008": {"ΔX": 0.003, "ΔY": -0.013, "ΔZ": 0.008, "ωx": 2.633e-09, "ωy": 2.909e-10, "ωz": -2.667e-10, "m": 0.0006},
        "ГСК-2011": {"ΔX": 0, "ΔY": 0, "ΔZ": 0, "ωx": 0, "ωy": 0, "ωz": 0, "m": 0}
    }
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(parameters, f, ensure_ascii=False, indent=4)

# --- 3. Функция преобразования координат ---
def GSK_2011(
    sk1: str,
    sk2: str,
    parameters_path: str,
    df: Optional[pd.DataFrame] = None,
    save_path: Optional[str] = None
) -> pd.DataFrame:
    if sk1 == "СК-95" and sk2 == "СК-42":
        df_temp = GSK_2011("СК-95", "ПЗ-90.11", parameters_path, df=df)
        df_result = GSK_2011("ПЗ-90.11", "СК-42", parameters_path, df=df_temp, save_path=save_path)
        return df_result

    ΔX, ΔY, ΔZ, ωx, ωy, ωz, m = symbols('ΔX ΔY ΔZ ωx ωy ωz m')
    X, Y, Z = symbols('X Y Z')

    formula = (1 + m) * Matrix([[1, ωz, -ωy], [-ωz, 1, ωx], [ωy, -ωx, 1]]) @ Matrix([[X], [Y], [Z]]) + Matrix([[ΔX], [ΔY], [ΔZ]])

    with open(parameters_path, 'r', encoding='utf-8') as f:
        parameters = json.load(f)

    if sk1 not in parameters:
        raise ValueError(f"Исходная система '{sk1}' отсутствует в параметрах")

    param = parameters[sk1]
    elements_const = {
        ΔX: param["ΔX"],
        ΔY: param["ΔY"],
        ΔZ: param["ΔZ"],
        ωx: param["ωx"],
        ωy: param["ωy"],
        ωz: param["ωz"],
        m: param["m"] * 1e-6
    }

    transformed = []
    for _, row in df.iterrows():
        elements = {
            X: row["X"],
            Y: row["Y"],
            Z: row["Z"],
            **elements_const
        }
        results_vector = formula.subs(elements).applyfunc(N)
        transformed.append([
            row["Name"],
            float(results_vector[0]),
            float(results_vector[1]),
            float(results_vector[2]),
        ])

    df_result = pd.DataFrame(transformed, columns=["Name", "X'", "Y'", "Z'"])
    if save_path:
        df_result.to_csv(save_path, index=False)
    return df_result

# --- 4. Генерация отчета в Excel ---
def generate_excel_report(df_before: pd.DataFrame, df_after: pd.DataFrame, source_system: str, target_system: str) -> BytesIO:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Исходные данные
        df_before.to_excel(writer, sheet_name='До преобразования', index=False)
        # После преобразования
        df_after.to_excel(writer, sheet_name='После преобразования', index=False)

        # Лист с информацией
        info_df = pd.DataFrame({
            "Описание": [
                "Дата создания",
                "Исходная система",
                "Целевая система",
                "Количество точек"
            ],
            "Значение": [
                pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                source_system,
                target_system,
                len(df_before)
            ]
        })
        info_df.to_excel(writer, sheet_name='Информация', index=False)

    output.seek(0)
    return output

# --- 5. Эндпоинты API ---

@app.get("/")
def read_root():
    return {
        "message": "API для преобразования координат работает!",
        "endpoints": {
            "/convert-coordinates/": "Преобразование координат",
            "/generate-report/": "Генерация отчёта в Excel"
        }
    }

@app.post("/convert-coordinates/")
async def convert_coordinates(
    file: UploadFile = File(...),
    source_system: str = "СК-42",
    target_system: str = "ГСК-2011"
):
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Поддерживаются только .xlsx, .xls или .csv")
    try:
        input_path = "input.csv"
        output_path = "converted.csv"
        parameters_path = "parameters.json"

        contents = await file.read()
        with open(input_path, "wb") as f:
            f.write(contents)

        if file.filename.endswith(".csv"):
            df = pd.read_csv(input_path)
        else:
            df = pd.read_excel(input_path)

        required_columns = ["Name", "X", "Y", "Z"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"Файл должен содержать колонки: {required_columns}")

        create_default_parameters(parameters_path)
        result_df = GSK_2011(sk1=source_system, sk2=target_system, parameters_path=parameters_path, df=df, save_path=output_path)

        output = BytesIO()
        result_df.to_csv(output, index=False)
        output.seek(0)

        filename = f"converted_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"
        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке: {str(e)}")

@app.post("/generate-report/")
async def generate_report(
    file: UploadFile = File(...),
    source_system: str = "СК-42",
    target_system: str = "ГСК-2011"
):
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Поддерживаются только .xlsx, .xls или .csv")
    try:
        input_path = "input.csv"
        parameters_path = "parameters.json"

        contents = await file.read()
        with open(input_path, "wb") as f:
            f.write(contents)

        if file.filename.endswith(".csv"):
            df = pd.read_csv(input_path)
        else:
            df = pd.read_excel(input_path)

        required_columns = ["Name", "X", "Y", "Z"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail=f"Файл должен содержать колонки: {required_columns}")

        create_default_parameters(parameters_path)
        df_result = GSK_2011(sk1=source_system, sk2=target_system, parameters_path=parameters_path, df=df.copy())

        excel_report = generate_excel_report(df, df_result, source_system, target_system)
        filename = f"report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

        return StreamingResponse(
            excel_report,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при генерации отчёта: {str(e)}")