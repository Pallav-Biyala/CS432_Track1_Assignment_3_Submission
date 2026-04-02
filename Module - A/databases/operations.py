# So to remember what to undo during rollback we need to remember the previous operations
# Hence we need a class operations to get operation

class Operations:
    def __init__(self, table, op_type, key, old_value = None, new_value = None):
        self.table = table
        self.op_type = op_type
        self.key = key
        self.old_value = old_value
        self.new_value = new_value

    def perform(self):
        if self.op_type == "update":
            # performing update operation
            self.table.index.update(self.key, self.new_value)
        elif self.op_type == "insert":
            #performing insert operation
            self.table.index.insert(self.key, self.new_value)
        elif self.op_type == "delete":
            # performing delete operation
            self.table.index.delete(self.key)

    def undo(self):
        if self.op_type == "update":
            # we updated the key to new value. since we need to rollback, we need to get the old value back
            self.table.index.update(self.key, self.old_value)
        
        elif self.op_type == "insert":
            # Since we inserted key, in rollback need to delete it
            self.table.index.delete(self.key)
        
        elif self.op_type == "delete":
            # Since we deleted key, need to insert the key again and its old value
            self.table.index.insert(self.key, self.old_value)
        
# Hence, by this way we can rollback