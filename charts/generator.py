import matplotlib.pyplot as plt
import numpy as np
import psycopg2

def get_conn():
    try:
        conn = psycopg2.connect(
            host="5.53.124.214",
            port="5432",
            database="lamtech_db",
            user="postgres",
            password="root"
        )

        return conn
    except Exception as e:
        print(e)

def get_general(conn):
    conn = get_conn()

    cursor = conn.cursor()

    # Выполнение SQL-запроса для получения размера базы данных и свободного пространства
    cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database())), pg_size_pretty(pg_database_size(current_database()) - pg_total_relation_size('posts') - pg_total_relation_size('users') - pg_total_relation_size('comments'))")
    data = cursor.fetchone()

    # Извлечение данных
    db_size_mb = data[0].replace(' MB', '')  # Удаление 'MB' и преобразование в число
    table_size_mb = data[1].replace(' MB', '')  # Удаление 'MB' и преобразование в число


    # Создание данных для кругового графика
    labels = ['Занято', 'Свободно']
    sizes = [float(db_size_mb), float(table_size_mb)]
    colors = ['red', 'green']

    # Создание кругового графика
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Занятое и свободное пространство в базе данных')

    # Отображение кругового графика
    plt.axis('equal')  # Убираем искажение пропорций
    plt.savefig('./charts/Занятое_и_свободное_пространство_в_базе_данных.png')

    cursor.close()
    conn.close()

def get_tables_stat(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT relname, seq_scan, seq_tup_read FROM pg_stat_user_tables WHERE relname not like '%pgbench%'")

    # Извлечение данных
    data = cursor.fetchall()
    table_names = [row[0] for row in data]
    seq_scan_values = [row[1] for row in data]
    seq_tup_read_values = [row[2] for row in data]

    # Создание столбчатой диаграммы
    plt.figure(figsize=(12, 6))
    plt.bar(table_names, seq_scan_values, color='b', label='Количество сканирований таблиц')
    plt.bar(table_names, seq_tup_read_values, color='g', label='Количество записей таблиц', alpha=0.5)
    plt.xlabel('Таблицы')
    plt.ylabel('Количество')
    plt.title('Статистика сканирований и чтений таблиц')
    plt.xticks(rotation=90)
    plt.legend()


    plt.tight_layout()
    plt.savefig('./charts/количества_сканирований_таблиц_(seq_scan)_и_записей_таблиц.png')

    # Закрытие курсора и соединения
    cursor.close()
    conn.close()

def get_indexes_stat(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT indexrelname, idx_scan, idx_tup_read, idx_tup_fetch FROM pg_stat_user_indexes WHERE indexrelname not like '%pgbench%'")

    # Извлечение данных
    data = cursor.fetchall()
    index_names = [row[0] for row in data]
    idx_scan_values = [row[1] for row in data]
    idx_tup_read_values = [row[2] for row in data]
    idx_tup_fetch_values = [row[3] for row in data]

    # Создание столбчатой диаграммы
    plt.figure(figsize=(12, 6))
    plt.bar(index_names, idx_scan_values, color='b', label='Количество сканирований индексов')
    plt.bar(index_names, idx_tup_read_values, color='g', label='Количество чтений индексов', alpha=0.5)
    plt.bar(index_names, idx_tup_fetch_values, color='r', label='Количество записей индексов', alpha=0.5)
    plt.xlabel('Индексы')
    plt.ylabel('Количество')
    plt.title('Статистика по индексам')
    plt.xticks(rotation=90)
    plt.legend()


    plt.tight_layout()
    plt.savefig('./charts/статистики_по_индексам.png')

    # Закрытие курсора и соединения
    cursor.close()
    conn.close()

