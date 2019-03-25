class OrdersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             order_name VARCHAR(50), 
                             order_description VARCHAR(128),
                             file_name VARCHAR(128),
                             order_status VARCHAR(50), 
                             order_status_cod INTEGER,
                             creation_data VARCHAR(65536),
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, order_name, order_description, file_name, creation_data, user_id, status, cod):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO orders 
                          (order_name, order_description, file_name, order_status, order_status_cod, creation_data, user_id) 
                          VALUES (?,?,?,?,?,?,?)''',
                       (order_name, order_description, file_name, status, cod, creation_data,
                        user_id))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = ?", (str(user_id)))
        row = cursor.fetchall()
        return row

    def get_order(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (str(id)))
        row = cursor.fetchone()
        return row

    def get_status(self, status):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_status_cod = ?", (str(status)))
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

    def update(self, cod, status, order_id):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE orders SET order_status = ?, order_status_cod = ? WHERE id = ?''',
                       (status, str(cod), str(order_id)))
        cursor.close()
        self.connection.commit()
