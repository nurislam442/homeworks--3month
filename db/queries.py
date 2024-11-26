CREATE_TABLE_collection_products = """
CREATE TABLE IF NOT EXISTS collection_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    productid TEXT,
    collection TEXT
)
"""

CREATE_TABLE_product_details = """
CREATE TABLE IF NOT EXISTS product_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    productid TEXT,
    category TEXT,
    infoproduct TEXT
)
"""

INSERT_collection_products = """

INSERT INTO collection_products (productid, collection) VALUES (?, ?)
"""

INSERT_product_details = """
INSERT INTO product_details (productid, category, infoproduct) VALUES (?, ?, ?)

"""

CREATE_TABLE_STORE = """
CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_product TEXT,
    product_id TEXT,
    size TEXT,
    price TEXT,
    photo
)
"""
INSERT_STORE = """
    INSERT INTO store (name_product, product_id, size, price, photo)
    VALUES (?, ?, ?, ?, ?)
"""
