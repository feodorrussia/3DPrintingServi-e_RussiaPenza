class DeliveryModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             type_delivery VARCHAR(50),
                             cod_type_delivery INTEGER,
                             cod_delivery INTEGER,
                             id_order INTEGER,
                             name_order VARCHAR(50),
                             price_order INTEGER,
                             user_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, type_delivery, cod_type_delivery, cod_delivery, id_order, name_order, price_order, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO orders 
                          (type_delivery, cod_type_delivery, cod_delivery, id_order, name_order, price_order, user_id) 
                          VALUES (?,?,?,?,?,?,?)''',
                       (type_delivery, cod_type_delivery, cod_delivery, id_order, name_order,
                        price_order, user_id))
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
