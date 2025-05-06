# # app.py
# import streamlit as st
# import pandas as pd
# import requests
# import io
# from urllib.parse import urljoin

# # Конфигурация приложения
# st.set_page_config(
#     page_title="Excel Analyzer",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # URL бэкенда на render.com
# # Замените на свой URL после развертывания на render.com
# BACKEND_URL = "https://prac10.onrender.com"

# # Функции для взаимодействия с бэкендом
# def check_api_status():
#     """Проверяем доступность API"""
#     try:
#         response = requests.get(BACKEND_URL, timeout=10)
#         return response.status_code == 200
#     except requests.RequestException:
#         return False

# def process_excel(file):
#     """Отправляем Excel-файл на обработку в API и получаем Markdown-отчет"""
#     url = urljoin(BACKEND_URL, "/process-excel/")
#     files = {"file": file}
#     try:
#         response = requests.post(url, files=files)
#         if response.status_code == 200:
#             return response.content.decode('utf-8')
#         else:
#             st.error(f"Ошибка при обработке файла: {response.text}")
#             return None
#     except requests.RequestException as e:
#         st.error(f"Ошибка соединения с API: {str(e)}")
#         return None

# # Интерфейс приложения
# def main():
#     st.title("📊 Анализатор Excel файлов")
#     st.markdown("""
#     Этот инструмент позволяет загрузить Excel-файл и получить аналитический отчет
#     в формате Markdown. Просто загрузите файл и нажмите кнопку "Анализировать".
#     """)

#     # Проверка статуса API
#     if not check_api_status():
#         st.error("⚠️ Не удалось подключиться к API. Пожалуйста, проверьте соединение или попробуйте позже.")
#         return

#     # Загрузка файла
#     uploaded_file = st.file_uploader("Выберите Excel файл", type=['xlsx', 'xls'])

#     if uploaded_file is not None:
#         # Показываем предварительный просмотр данных
#         try:
#             df = pd.read_excel(uploaded_file)
#             st.subheader("Предварительный просмотр данных")
#             st.dataframe(df.head(5))

#             # Получение основных статистик для информации
#             st.subheader("Базовая информация")
#             col1, col2, col3 = st.columns(3)
#             col1.metric("Строки", df.shape[0])
#             col2.metric("Столбцы", df.shape[1])
#             col3.metric("Пропущенные значения", df.isna().sum().sum())

#             # Сбрасываем указатель файла для повторного чтения
#             uploaded_file.seek(0)

#             if st.button("Анализировать"):
#                 with st.spinner("Обрабатываем данные..."):
#                     markdown_report = process_excel(uploaded_file)

#                 if markdown_report:
#                     st.success("Отчет успешно создан!")

#                     # Показываем отчет в интерфейсе
#                     st.subheader("Отчет")
#                     st.markdown(markdown_report)

#                     # Предоставляем возможность скачать отчет
#                     st.download_button(
#                         label="Скачать отчет",
#                         data=markdown_report,
#                         file_name="report.md",
#                         mime="text/markdown",
#                     )

#         except Exception as e:
#             st.error(f"Ошибка при чтении файла: {str(e)}")

# if __name__ == "__main__":
#     main()

# app.py
import streamlit as st
import pandas as pd
import requests
from urllib.parse import urljoin
from io import BytesIO

# Конфигурация страницы
st.set_page_config(
    page_title="Координатный конвертер",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Базовый URL бэкенда
BACKEND_URL = "https://prac10.onrender.com"  # замените на ваш Render/Heroku URL после деплоя

# Системы координат
COORD_SYSTEMS = ["СК-42", "ПЗ-90.11", "ГСК-2011"]

# Проверка доступности API
def check_api_status():
    try:
        response = requests.get(BACKEND_URL, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Отправка файла на бэкенд и получение Markdown отчёта
def convert_and_generate_report(file, source_system, target_system):
    url = urljoin(BACKEND_URL, "/generate-report/")
    files = {"file": file}
    data = {
        "source_system": source_system,
        "target_system": target_system
    }
    try:
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            st.error(f"Ошибка при обработке: {response.text}")
            return None
    except requests.RequestException as e:
        st.error(f"Ошибка соединения с API: {str(e)}")
        return None

# Основная функция приложения
def main():
    st.title("🧭 Автоматизированная система преобразования координатных данных")
    st.markdown("""
    Это приложение позволяет загрузить Excel или CSV файл с координатами 
    и выполнить их преобразование между различными системами координат.
    
    Поддерживаются следующие системы:
    - СК-42 (Система координат 1942 года)
    - ПЗ-90.11 (Параметры Земли 1990, редакция 2011)
    - ГСК-2011 (Государственная система координат 2011)
    
    После преобразования формируется подробный отчет в формате Markdown.
    """)

    # Проверка статуса API
    if not check_api_status():
        st.error("⚠️ Не удалось подключиться к серверу. Пожалуйста, проверьте интернет или попробуйте позже.")
        return

    # Выбор систем координат
    col1, col2 = st.columns(2)
    with col1:
        source_system = st.selectbox("Выберите исходную систему:", COORD_SYSTEMS, index=0)
    with col2:
        target_system = st.selectbox("Выберите целевую систему:", COORD_SYSTEMS, index=2)

    # Загрузка файла
    uploaded_file = st.file_uploader("Выберите файл с данными (Excel или CSV)", type=["xlsx", "xls", "csv"])

    if uploaded_file is not None:
        try:
            # Чтение и отображение предварительного просмотра
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            st.subheader("📄 Предварительный просмотр данных")
            st.dataframe(df.head(), use_container_width=True)

            # Информация о данных
            st.subheader("📊 Краткая информация")
            col1, col2, col3 = st.columns(3)
            col1.metric("Количество точек", df.shape[0])
            col2.metric("Столбцы", df.shape[1])
            col3.metric("Пропущенные значения", df.isna().sum().sum())

            # Сброс указателя файла
            uploaded_file.seek(0)

            # Кнопка запуска анализа
            if st.button("🚀 Начать преобразование"):
                with st.spinner("Выполняется преобразование координат..."):
                    markdown_report = convert_and_generate_report(uploaded_file, source_system, target_system)

                if markdown_report:
                    st.success("✅ Преобразование завершено! Ниже приведён отчёт.")

                    # Показываем отчет
                    st.subheader("📘 Отчет по преобразованию координат")
                    st.markdown(markdown_report)

                    # Кнопка скачивания
                    st.download_button(
                        label="⬇️ Скачать отчет (.md)",
                        data=markdown_report,
                        file_name=f"report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )

        except Exception as e:
            st.error(f"❌ Ошибка при чтении файла: {str(e)}")

# Запуск приложения
if __name__ == "__main__":
    main()