# Creating Db manager class
from databases.table import Table
import pickle
import os

class DB_Manager:
    def __init__(self):
        self.databases = {}      # {db_name : {table_name : Table}}
        self.current_db = None
        self.storage_file = "system_data.db"

    # Saving data to disk so that if system crashes we can use it to recover our database
    def save_to_disk(self):
        # Saving all databases and tables to a physical file
        with open(self.storage_file, "wb") as f:
            # Saving entire database to this file
            pickle.dump(self.databases, f)
        print(f"Database state saved to {self.storage_file}")

    # Loading whole database from disk after crash
    def load_from_disk(self):
        # Loads the database state from the file if it exists.
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "rb") as f:
                self.databases = pickle.load(f)
            print("Database state loaded from disk.")
            return True
        print("No existing database file found. Starting fresh.")
        return False
    
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