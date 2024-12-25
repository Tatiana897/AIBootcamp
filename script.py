import pandas as pd
import json
import os

def clean_csv(file_path):
    try:
        # Прочитаем CSV с параметром для пропуска некорректных строк
        df = pd.read_csv(file_path, on_bad_lines='skip')
        
        # Преобразуем строки к нижнему регистру и удаляем лишние пробелы
        df = df.applymap(lambda x: x.lower().strip() if isinstance(x, str) else x)
        
        # Обрабатываем пустые значения
        df = df.dropna(how='all')  # Удаляем полностью пустые строки
        df.fillna("unknown", inplace=True)  # Заполняем остальные пустые значения значением "unknown"

        print(f"Очищенные данные из {file_path}:")
        print(df.head())  # Показываем только первые строки для проверки
        return df
    except Exception as e:
        print(f"Ошибка при обработке CSV: {e}")
        return None

def clean_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.json_normalize(data)
        
        # Преобразуем строки к нижнему регистру и удаляем лишние пробелы
        df = df.applymap(lambda x: x.lower().strip() if isinstance(x, str) else x)
        
        # Обрабатываем пустые значения
        df = df.dropna(how='all')  # Удаляем полностью пустые строки
        df.fillna("unknown", inplace=True)  # Заполняем остальные пустые значения значением "unknown"

        print(f"Очищенные данные из {file_path}:")
        print(df.head())  # Показываем только первые строки для проверки
        return df
    except Exception as e:
        print(f"Ошибка при обработке JSON: {e}")
        return None

def clean_file(file_path):
    if file_path.endswith('.csv'):
        return clean_csv(file_path)
    elif file_path.endswith('.json'):
        return clean_json(file_path)
    else:
        print(f"Формат файла {file_path} не поддерживается.")
        return None

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Пример использования
folder_path = r"D:/Users/ASUS-X509J/Desktop/cleaning"
output_folder = r"D:/Users/ASUS-X509J/Desktop/cleaned"

# Убедимся, что директория для сохранения данных существует
ensure_directory_exists(output_folder)

file_paths = [
    os.path.join(folder_path, "customers.csv"),  # Этот файл ты упомянул
    os.path.join(folder_path, "employees.json"),
    os.path.join(folder_path, "error_logs.csv"),
    os.path.join(folder_path, "products.json")
]

for file_path in file_paths:
    cleaned_data = clean_file(file_path)
    if cleaned_data is not None:
        # Сохраняем очищенные данные в новый файл
        output_file = os.path.join(output_folder, os.path.basename(file_path).replace(".csv", "_cleaned.csv").replace(".json", "_cleaned.csv"))
        cleaned_data.to_csv(output_file, index=False)
        print(f"Очищенные данные сохранены в: {output_file}")
