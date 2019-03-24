class ChatModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             id_user1 INTEGER,
                             message VARCHAR(128),
                             order_name VARCHAR(50),
                             id_user2 INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, id_user1, message, order_name, id_user2):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO messages 
                          (id_user1, message, order_name, id_user2) 
                          VALUES (?,?,?,?)''', (str(id_user1), message, order_name, str(id_user2)))
        cursor.close()
        self.connection.commit()

    def get_all(self, id_user):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM messages Where id_user1 = ?", (str(id_user)))
        rows = cursor.fetchall()
        return rows