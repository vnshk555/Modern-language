import random
import pandas as pd
import numpy as np
import os
from joblib import Parallel, delayed


# генерация файлов
def generate_csv(file_name):
    data = []
    categories = ['A', 'B', 'C', 'D']

    for _ in range(25):
        random_category = random.choice(categories)
        value = round(random.uniform(0.0, 100.0), 2)
        data.append([random_category, value])

    df = pd.DataFrame(data, columns=['Category', 'Value'])
    df.to_csv(file_name, index=False)
    print(f"Создан файл: {file_name}")


# обработка файлов
def process_single_file(file_path):
    df = pd.read_csv(file_path)
    results = {}

    for category in ['A', 'B', 'C', 'D']:
        category_data = df[df['Category'] == category]['Value']
        if len(category_data) > 0:
            results[category] = {
                'median': np.median(category_data),
                'std': np.std(category_data)
            }
        else:
            results[category] = {'median': None, 'std': None}

    return results


def parallel_process_and_save(file_list, n_jobs=-1):
    all_results = Parallel(n_jobs=n_jobs)(
        delayed(process_single_file)(file_path)
        for file_path in file_list
    )

    valid_results = [r for r in all_results if r is not None]

    # Создаем папку для результатов
    results_dir = "results_files"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    # Сохраняем результаты каждого файла в папку results_files
    for i, result in enumerate(valid_results):
        file_data = []
        for category in ['A', 'B', 'C', 'D']:
            if result[category]['median'] is not None:
                file_data.append({
                    'Category': category,
                    'Median': round(result[category]['median'], 2),
                    'Std': round(result[category]['std'], 2)
                })
        result_df = pd.DataFrame(file_data)
        result_df.to_csv(os.path.join(results_dir, f'result_file_{i}.csv'), index=False)

    # Считаем финальные результаты из файлов в папке results_files
    result_files = [os.path.join(results_dir, f) for f in os.listdir(results_dir) if f.endswith('.csv')]

    all_medians = {}
    for category in ['A', 'B', 'C', 'D']:
        all_medians[category] = []

    for result_file in result_files:
        df = pd.read_csv(result_file)
        for _, row in df.iterrows():
            category = row['Category']
            all_medians[category].append(row['Median'])

    # Считаем медиану медиан и отклонение медиан
    final_stats = {}
    for category in ['A', 'B', 'C', 'D']:
        if all_medians[category]:
            final_stats[category] = {
                'median_of_medians': np.median(all_medians[category]),
                'std_of_medians': np.std(all_medians[category])
            }

    output_data = []
    for category, stats in final_stats.items():
        output_data.append({
            'Category': category,
            'Median_of_Medians': round(stats['median_of_medians'], 2),
            'Std_of_Medians': round(stats['std_of_medians'], 2)
        })

    result_df = pd.DataFrame(output_data)
    result_df.to_csv('final_results.csv', index=False)


if __name__ == '__main__':
    output_dir = "output_files"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = [os.path.join(output_dir, f'file_{i}.csv') for i in range(5)]
    for file in files:
        generate_csv(file)

    results = parallel_process_and_save(files, n_jobs=-1)