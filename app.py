# # # app.py
import streamlit as st
import pandas as pd
import requests
import io
from urllib.parse import urljoin

# Конфигурация приложения
st.set_page_config(
    page_title="Excel Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# URL бэкенда на render.com
# Замените на свой URL после развертывания на render.com
BACKEND_URL = "https://prac10.onrender.com"

# Функции для взаимодействия с бэкендом
def check_api_status():
    """Проверяем доступность API"""
    try:
        response = requests.get(BACKEND_URL, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

def process_excel(file):
    """Отправляем Excel-файл на обработку в API и получаем Markdown-отчет"""
    url = urljoin(BACKEND_URL, "/process-excel/")
    files = {"file": file}
    try:
        response = requests.post(url, files=files)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            st.error(f"Ошибка при обработке файла: {response.text}")
            return None
    except requests.RequestException as e:
        st.error(f"Ошибка соединения с API: {str(e)}")
        return None

# Интерфейс приложения
def main():
    st.title("📊 Анализатор Excel файлов")
    st.markdown("""
    Этот инструмент позволяет загрузить Excel-файл и получить аналитический отчет
    в формате Markdown. Просто загрузите файл и нажмите кнопку "Анализировать".
    """)

    # Проверка статуса API
    if not check_api_status():
        st.error("⚠️ Не удалось подключиться к API. Пожалуйста, проверьте соединение или попробуйте позже.")
        return

    # Загрузка файла
    uploaded_file = st.file_uploader("Выберите Excel файл", type=['xlsx', 'xls'])

    if uploaded_file is not None:
        # Показываем предварительный просмотр данных
        try:
            df = pd.read_excel(uploaded_file)
            st.subheader("Предварительный просмотр данных")
            st.dataframe(df.head(5))

            # Получение основных статистик для информации
            st.subheader("Базовая информация")
            col1, col2, col3 = st.columns(3)
            col1.metric("Строки", df.shape[0])
            col2.metric("Столбцы", df.shape[1])
            col3.metric("Пропущенные значения", df.isna().sum().sum())

            # Сбрасываем указатель файла для повторного чтения
            uploaded_file.seek(0)

            if st.button("Анализировать"):
                with st.spinner("Обрабатываем данные..."):
                    markdown_report = process_excel(uploaded_file)

                if markdown_report:
                    st.success("Отчет успешно создан!")

                    # Показываем отчет в интерфейсе
                    st.subheader("Отчет")
                    st.markdown(markdown_report)

                    # Предоставляем возможность скачать отчет
                    st.download_button(
                        label="Скачать отчет",
                        data=markdown_report,
                        file_name="report.md",
                        mime="text/markdown",
                    )

        except Exception as e:
            st.error(f"Ошибка при чтении файла: {str(e)}")

if __name__ == "__main__":
    main()

# # app.py
# import streamlit as st
# import pandas as pd
# import requests
# from io import BytesIO
# from urllib.parse import urljoin

# # Конфигурация приложения
# st.set_page_config(
#     page_title="Конвертер координат",
#     page_icon="🌍",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # URL бэкенда на render.com
# BACKEND_URL = "https://prac10.onrender.com "  # Замените на ваш актуальный URL

# # Список доступных систем координат
# COORD_SYSTEMS = [
#     "СК-42", "СК-95", "ПЗ-90", "ПЗ-90.02", "ПЗ-90.11",
#     "WGS-84 (G1150)", "ITRF-2008", "ГСК-2011"
# ]

# # Функции для взаимодействия с бэкендом
# def check_api_status():
#     """Проверяем доступность API"""
#     try:
#         response = requests.get(BACKEND_URL, timeout=10)
#         return response.status_code == 200
#     except requests.RequestException:
#         return False

# def convert_coordinates(file, source_system, target_system):
#     """Отправляем файл на обработку и получаем результат преобразования"""
#     url = urljoin(BACKEND_URL, "/convert-coordinates/")
#     files = {"file": file}
#     data = {
#         "source_system": source_system,
#         "target_system": target_system
#     }
#     try:
#         response = requests.post(url, files=files, data=data)
#         if response.status_code == 200:
#             return response.content
#         else:
#             st.error(f"Ошибка при преобразовании: {response.text}")
#             return None
#     except requests.RequestException as e:
#         st.error(f"Ошибка соединения с API: {str(e)}")
#         return None

# def generate_report(file, source_system, target_system):
#     """Генерируем Excel-отчет через API"""
#     url = urljoin(BACKEND_URL, "/generate-report/")
#     files = {"file": file}
#     data = {
#         "source_system": source_system,
#         "target_system": target_system
#     }
#     try:
#         response = requests.post(url, files=files, data=data)
#         if response.status_code == 200:
#             return response.content
#         else:
#             st.error(f"Ошибка при генерации отчёта: {response.text}")
#             return None
#     except requests.RequestException as e:
#         st.error(f"Ошибка соединения с API: {str(e)}")
#         return None

# # Интерфейс приложения
# def main():
#     st.title("🌍 Конвертер координат между системами")
#     st.markdown("""
#     Этот инструмент позволяет загрузить CSV или Excel-файл с координатами 
#     и преобразовать их из одной системы координат в другую.
    
#     Поддерживаемые системы:
#     - СК-42
#     - СК-95
#     - ПЗ-90
#     - ПЗ-90.02
#     - ПЗ-90.11
#     - WGS-84 (G1150)
#     - ITRF-2008
#     - ГСК-2011
#     """)

#     # Проверка статуса API
#     if not check_api_status():
#         st.error("⚠️ Не удалось подключиться к API. Пожалуйста, проверьте соединение.")
#         return

#     uploaded_file = st.file_uploader("Выберите CSV или Excel файл", type=['csv', 'xlsx', 'xls'])

#     if uploaded_file is not None:
#         try:
#             # Чтение файла для предпросмотра
#             if uploaded_file.name.endswith('.csv'):
#                 df = pd.read_csv(uploaded_file)
#             else:
#                 df = pd.read_excel(uploaded_file)

#             required_columns = ["Name", "X", "Y", "Z"]
#             if not all(col in df.columns for col in required_columns):
#                 st.error(f"Файл должен содержать колонки: {required_columns}")
#                 return

#             st.subheader("📥 Предварительный просмотр данных")
#             st.dataframe(df.head())

#             # Сброс указателя файла для повторного чтения
#             uploaded_file.seek(0)

#             # Выбор систем координат
#             col1, col2 = st.columns(2)
#             with col1:
#                 source_system = st.selectbox("Исходная система", options=COORD_SYSTEMS)
#             with col2:
#                 target_system = st.selectbox("Целевая система", options=COORD_SYSTEMS)

#             if st.button("🚀 Преобразовать координаты"):
#                 with st.spinner("Преобразование координат..."):
#                     converted_data = convert_coordinates(uploaded_file, source_system, target_system)
#                 if converted_data:
#                     result_df = pd.read_csv(BytesIO(converted_data))
#                     st.subheader("✅ Результат преобразования")
#                     st.dataframe(result_df.head())
#                     st.download_button(
#                         label="⬇️ Скачать CSV с результатами",
#                         data=converted_data,
#                         file_name="converted.csv",
#                         mime="text/csv"
#                     )

#             if st.button("📊 Сформировать отчет в Excel"):
#                 with st.spinner("Формирование отчета..."):
#                     report_data = generate_report(uploaded_file, source_system, target_system)
#                 if report_data:
#                     st.success("✅ Отчет успешно создан!")
#                     st.download_button(
#                         label="⬇️ Скачать Excel-отчет",
#                         data=report_data,
#                         file_name="report.xlsx",
#                         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#                     )

#         except Exception as e:
#             st.error(f"❌ Ошибка при обработке файла: {str(e)}")

# if __name__ == "__main__":
#     main()