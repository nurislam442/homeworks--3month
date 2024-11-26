import sqlite3
from db import queries
import aiosqlite

db = sqlite3.connect('db/store.sqlite3.db')
cursor = db.cursor()

async def sql_create():
    if db:
        print('База данных подключена!')
        cursor.execute(queries.CREATE_TABLE_product_details)
        cursor.execute(queries.CREATE_TABLE_collection_products)
        cursor.execute(queries.CREATE_TABLE_STORE)


async def sql_insert_store_to_product_details(productid, category, infoproduct):
    cursor.execute(
        queries.INSERT_product_details,
        (productid, category, infoproduct)
    )
    db.commit()

async def sql_insert_store_to_collection_products(productid, collection):
    cursor.execute(
        queries.INSERT_collection_products,
        (productid, collection)
    )
    db.commit()

async def sql_insert_store(name_product, product_id, size, price, photo):
    cursor.execute(queries.INSERT_STORE, (
        name_product, product_id, size, price, photo
    ))

def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = cursor.execute("""
SELECT product_details.productid, product_details.category, product_details.infoproduct, store.name_product, store.size, 
store.price, store.photo
FROM product_details
INNER JOIN store 
ON product_details.productid = store.product_id
""").fetchall()
    conn.close()
    return products
def fetch_one_product(product_name):
    conn = get_db_connection()
    cursor.execute("SELECT * FROM store WHERE name_product = ?", (product_name,))
    product = cursor.fetchone()
    conn.close()
    return  product

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM STORE WHERE product_id = ?', (product_id,))
    conn.commit()
    conn.close()


def update_product_field(product_id, field_name, new_valeu):
    store_table = ["name_product", "size", "price", "photo"]
    store_detail_table = ["info_product", "category"]
    conn = get_db_connection()
    try:
        if field_name in store_table:
            query = f'UPDATE store SET {field_name} = ? WHERE product_id = ?'
        elif field_name in store_detail_table:
            query = f'UPDATE product_detail SET {field_name} = ? WHERE productid = ?'
        else:
            raise ValueError(f'Нет такого поля {field_name}')

        conn.execute(query, (new_valeu, product_id))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'Ошибка - {e}')
    finally:
        conn.close()
