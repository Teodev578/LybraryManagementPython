import threading
import time

class DatabaseObserver:
    def __init__(self, db_connection, interval=25):
        self.db_connection = db_connection
        self.interval = interval
        self.observers = []
        self.running = False
        self.thread = None

    def register_observer(self, observer):
        self.observers.append(observer)

    def unregister_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, fetch_method):
        data = fetch_method()
        for observer in self.observers:
            observer.update(data)

    def fetch_data_users(self):
        try:
            query = "SELECT id, username, password FROM users"  # Removed password from selection
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            print(f"Error fetching user data: {e}")
            return []

    def fetch_data_categories(self):
        try:
            query = "SELECT * FROM Categories"
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            print(f"Error fetching category data: {e}")
            return []
    
    def fetch_data_members(self):
        try:
            query = "SELECT * FROM Membres"
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            if cursor.nextset():
                pass  # Process or clean up next result set if necessary
            
            cursor.close()
            
            return data
        except Exception as e:
            print(f"Error fetching member data: {e}")
            return []
    
    def fetch_data_loans(self):
        try:
            query = "SELECT * FROM Prets"
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            
            if cursor.nextset():
                pass  # Process or clean up next result set if necessary
            
            cursor.close()
            
            return data
        except Exception as e:
            print(f"Error fetching member data: {e}")
            return []
    
    def fetch_data_Livre(self):
        try:
            query = "SELECT * FROM Livre"
            cursor = self.db_connection._connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            print(f"Error fetching book data: {e}")
            return []

    def start(self, fetch_method):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.run, args=(fetch_method,))
            self.thread.start()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

    def run(self, fetch_method):
        while self.running:
            self.notify_observers(fetch_method)
            time.sleep(self.interval)
    
    def check_for_updates(self, fetch_method):
        self.notify_observers(fetch_method)

    def check_for_updates_members(self):
        self.notify_observers(self.fetch_data_members)

    def check_for_updates_Livre(self):
        self.notify_observers(self.fetch_data_Livre)
    
    def check_fetch_data_loans(self):
        self.notify_observers(self.fetch_data_loans)
    
    def check_fetch_data_users(self):
        self.notify_observers(self.fetch_data_users)

    #fetch_data_users

    def close(self):
        if hasattr(self.db_connection, 'close'):
            self.db_connection.close()

    def __del__(self):
        self.close()