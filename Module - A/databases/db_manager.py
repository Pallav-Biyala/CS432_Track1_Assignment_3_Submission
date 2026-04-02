# Creating Db manager class
from databases.table import Table

class DB_Manager:
    def __init__(self):
        self.databases = {}      # {db_name : {table_name : Table}}
        self.current_db = None

    #_____________database operations_____________#
    def create_database(self, name):
        if name in self.databases:
            print(f"Database {name} already exists.")
        else:
            self.databases[name] = {}
            print(f"Database {name} created.")

    def show_databases(self):
        if not self.databases:
            print("No databases found.")
        else:
            print("Databases:")
            for db in self.databases:
                print(f"- {db}")

    def drop_database(self, name):
        if name in self.databases:
            del self.databases[name]

            if self.current_db == name:
                self.current_db = None

            print(f"Database {name} dropped.")
        else:
            print(f"Database {name} does not exist.")

    def use_database(self, name):
        if name in self.databases:
            self.current_db = name
            print(f"Using database {name}")
        else:
            print(f"Database {name} does not exist.")
    
    #_____________table operations________________#
    # Adding table to database
    def create_table(self, name, columns, order=4):
        if self.current_db is None:
            print("No database selected.")
            return

        db = self.databases[self.current_db]

        if name in db:
            print(f"Table {name} already exists.")
        else:
            db[name] = Table(name, columns, order)
            print(f"Table {name} created.")

    # Removing table from database
    def drop_table(self, name):
        if self.current_db is None:
            print("No database selected.")
            return

        db = self.databases[self.current_db]

        if name in db:
            del db[name]
            print(f"Table {name} dropped.")
        else:
            print(f"Table {name} does not exist.")

    # Displaying all tables
    def list_tables(self):
        if self.current_db is None:
            print("No database selected.")
            return []

        return list(self.databases[self.current_db].keys())

    # Extracting table so that we can use it
    def get_table(self, name):
        if self.current_db is None:
            print("No database selected.")
            return None

        return self.databases[self.current_db].get(name)

    # Get all tables of database
    def get_all_tables(self):
        if self.current_db is None:
            print("No database selected.")
            return {}
    
        return self.databases[self.current_db]