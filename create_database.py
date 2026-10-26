import sqlite3

#we will first create dummy database
#If amazon.db does not exist then SQLite creates it automatically and connects the database 
conn=sqlite3.connect('amazon.db')

#cursor as a messenger that carries SQL queries to the database.
cursor=conn.cursor()

cursor.execute("""
               CREATE TABLE IF NOT EXISTS customers(
               customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               email TEXT ,
               city TEXT,
               join_date TEXT
               )
               """)
cursor.execute("""
               CREATE TABLE IF NOT EXISTS products(
               product_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
              category TEXT ,
               price REAL
               )
               """)
#REAL data type stores decimal numbers 

cursor.execute("""
               CREATE TABLE IF NOT EXISTS order_items(
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
               order_id INTEGER,
               product_id INTEGER,
               quantity INTEGER ,
               subtotal REAL,
               FOREIGN KEY(order_id) REFERENCES orders(order_id),
               FOREIGN KEY(product_id) REFERENCES products(product_id)
               )
               """)


#step3 enter dummy data
#customers
cursor.executemany("""
INSERT INTO customers (name, email, city, join_date)
VALUES (?, ?, ?, ?)
""", [
    ("John Smith", "john.smith@email.com", "New York", "2023-01-15"),
    ("Emma Johnson", "emma.johnson@email.com", "Los Angeles", "2023-02-20"),
    ("Michael Brown", "michael.brown@email.com", "Chicago", "2023-03-10"),
    ("Sophia Davis", "sophia.davis@email.com", "Houston", "2023-04-05"),
    ("William Wilson", "william.wilson@email.com", "Phoenix", "2023-05-12"),
    ("Olivia Martinez", "olivia.martinez@email.com", "Seattle", "2023-06-18"),
    ("James Anderson", "james.anderson@email.com", "Boston", "2023-07-22"),
    ("Ava Taylor", "ava.taylor@email.com", "San Francisco", "2023-08-30"),
    ("Benjamin Thomas", "benjamin.thomas@email.com", "Dallas", "2023-09-14"),
    ("Mia Garcia", "mia.garcia@email.com", "Miami", "2023-10-25")
])

#PRODUCTS
cursor.executemany("""
INSERT INTO products (name, category, price)
VALUES (?, ?, ?)
""", [
    ("iPhone 15", "Electronics", 999.99),
    ("Samsung Galaxy S24", "Electronics", 899.99),
    ("MacBook Air M3", "Computers", 1299.99),
    ("Dell XPS 13", "Computers", 1199.99),
    ("Nike Air Max", "Footwear", 149.99),
    ("Adidas Ultraboost", "Footwear", 179.99),
    ("Sony WH-1000XM5", "Accessories", 399.99),
    ("Apple Watch Series 9", "Wearables", 429.99),
    ("Coffee Maker", "Home Appliances", 89.99),
    ("Air Fryer", "Kitchen", 129.99)
])

#order items
cursor.executemany("""
INSERT INTO order_items (order_id, product_id, quantity, subtotal)
VALUES (?, ?, ?, ?)
""", [
    (1, 1, 2, 1999.98),   # 2 iPhones
    (1, 3, 1, 1299.99),   # 1 MacBook
    (2, 2, 1, 899.99),    # 1 Samsung Galaxy
    (2, 5, 2, 299.98),    # 2 Nike Shoes
    (3, 4, 1, 1199.99),   # 1 Dell XPS
    (3, 7, 1, 399.99),    # 1 Sony Headphones
    (4, 8, 1, 429.99),    # 1 Apple Watch
    (4, 9, 2, 179.98),    # 2 Coffee Makers
    (5, 10, 1, 129.99),   # 1 Air Fryer
    (5, 6, 3, 539.97)     # 3 Adidas Shoes
])
conn.commit() #safety measure
conn.close()
print("database executed")
