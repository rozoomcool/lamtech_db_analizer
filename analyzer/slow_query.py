import requests
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

def get_tables_list(conn):
    q = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' and table_name not like '%pgbench%'"
    cursor = conn.cursor()
    cursor.execute(q)

    tables = []

    rows = cursor.fetchall()
    for row in rows:
        tables.append(row[0])

    cursor.close()
    conn.close()

    return tables

def check_query_time(conn, tables_list):
    result = {}
    cursor = conn.cursor()

    for table in tables_list:
        query_to_explain = f"select * from {table}"
        cursor.execute("EXPLAIN ANALYZE " + query_to_explain)

        temp = {
            "table": table,
            'executed_query': query_to_explain
        }
        
        query_plan = cursor.fetchall()
        
        for row in query_plan:
            if "Planning Time" in row[0]:
                text = list(row)
                text[0] = text[0].split(':')[1].split(' ')[1]
                temp["planning_time"] = text[0]
            if "Execution Time" in row[0]:
                text = list(row)
                text[0] = text[0].split(':')[1].split(' ')[1]
                temp["execution_time"] = text[0]
            else:
                continue
        result[table] = temp

    cursor.close()
    conn.close()

    return result

data = get_tables_list(conn=get_conn())

res = check_query_time(get_conn(), data)