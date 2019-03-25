class DeliveryModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS delivery 
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
        cursor.execute('''INSERT INTO delivery 
                          (type_delivery, cod_type_delivery, cod_delivery, id_order, name_order, price_order, user_id) 
                          VALUES (?,?,?,?,?,?,?)''',
                       (type_delivery, cod_type_delivery, cod_delivery, id_order, name_order,
                        price_order, user_id))
        cursor.close()
        self.connection.commit()

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM delivery WHERE id_order = ?", (str(user_id)))
        row = cursor.fetchone()
        return row
