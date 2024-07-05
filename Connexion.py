import mysql.connector
from mysql.connector import Error

class DatabaseConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def __init__(self, host, username, password, database):
        if self._connection is None:
            self._connection = mysql.connector.connect(
                host=host,
                user=username,
                password=password,
                database=database
            )

    @classmethod
    def get_instance(cls, host, username, password, database):
        if cls._instance is None:
            cls._instance = cls(host, username, password, database)
        return cls._instance

    def execute_query(self, query, params=None):
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connect()
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith("SELECT"):
                result = cursor.fetchall()
            else:
                self._connection.commit()
                result = cursor.rowcount
            
            cursor.close()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            raise
    
    def get_categories(self):
        return self.execute_query("SELECT * FROM Categories")

# Exemple d'utilisation
if __name__ == "__main__":
    # Obtenez une instance de connexion à la base de données
    db_connection = DatabaseConnection.get_instance(
        host="localhost",
        username="root",
        password="OKok__1325__",
        database="Lybrary"
    )

    # Exécutez une requête SQL
    result = db_connection.execute_query("SELECT * FROM Categories;")
    for row in result:
        print(row)
