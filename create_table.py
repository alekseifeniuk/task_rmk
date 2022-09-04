from resources.sql_operations import create_table, is_table_in_db

if __name__ == "__main__":
    if not is_table_in_db():
        create_table()
    else:
        print("Таблица существует в базе данных!")

