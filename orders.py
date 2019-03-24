class OrdersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             order_name VARCHAR(50),
                             order_description VARCHAR(128),
                             creation_data VARCHAR(65536),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, order_name, order_description, creation_data, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO orders 
                          (order_name, order_description, creation_data, user_id) 
                          VALUES (?,?,?,?)''', (order_name, order_description, creation_data,
                                                user_id))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (str(user_id)))
        row = cursor.fetchall()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        return rows

    def delete(self, order_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM orders WHERE id = ?''', (str(order_id)))
        cursor.close()
        self.connection.commit()
