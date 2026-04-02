from databases.bplustree import BPlusTree
from databases.operations import Operations
# Table Class
class Table:
    def __init__(self, name, columns, order):
        self.name = name
        self.columns = columns
        self.index = BPlusTree(order)

    # Inserting row into table
    def insert(self, row, tm = None, tid = None):
        key = row[0]  # First column as primary key
        if self.index.search(key):
            raise ValueError("Duplicate primary key")
        # log operation
        if tm and tid:
            op = Operations(self, "insert", key, None, row)
            tm.log_operation(tid, op)
        else:
            self.index.insert(key, row)
        return
        
    # Searching the data in table
    def search(self, key):
        return self.index.search(key)

    # Deleting row from table
    def delete(self, key,tm=None, tid=None):
        row = self.index.search(key)
        if not row:
            return None

        if tm and tid:
            op = Operations(self, "delete", key, row, None)
            tm.log_operation(tid, op)
        else:   
            self.index.delete(key)
        return row

    # Range query in table
    def range_query(self, start, end):
        return self.index.range_query(start, end)
    
    # Update Table
    def update(self, key, updates, tm=None, tid=None):
        row = self.index.search(key)

        if not row:
            raise ValueError("Entry Doesn't exist")
    
        new_row = list(row)
    
        for col, val in updates.items():
            idx = self.columns.index(col)
            new_row[idx] = val
    
        new_row = tuple(new_row)
    
        if tm and tid:
            op = Operations(self, "update", key, row, new_row)
            tm.log_operation(tid, op)
    
        else:
            self.index.update(key, new_row)
    
        return True

    # Printing Table
    def show(self):
        print(f"\nTable: {self.name}")
        print(self.columns)
        
        records = self.index.get_all()
        for key, row in records:
            print(row)