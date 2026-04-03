# Now we need to handle crash and failure. So we need to add Write ahead logging
# This means write the log to disk before modifying the data
# Hence Log operation --> then B+ tree change

# So we will store all logs in a log file
import ast
import os
from databases.operations import Operations
from databases.db_manager import DB_Manager

class WAL:
    def __init__(self, filename = 'wal.log'):
        self.filename = filename

    # Adding entry to the log
    def log(self, entry):
        with open(self.filename, "a") as f:
            f.write(entry+"\n")
            f.flush()

    # Beginning one transaction
    def log_begin(self, tid):
        self.log(f"Begin {tid}")

    # Adding the operations
    def log_operation(self, tid, table, op_type, key, old_value, new_value):
        self.log(f"{tid}|{table}|{op_type}|{key}|{old_value}|{new_value}")

    # Completing the transaction
    def log_commit(self, tid):
        self.log(f"COMMIT {tid}")

    # Now in case of crash we need to recover all by reading log file. so need recover
    def recover(self, db_manager):
        if not os.path.exists(self.filename):
            print("No WAL file found. Skipping recovery.")
            return
            
        active = {}
        committed = set()

        with open(self.filename, "r") as f:
            for line in f:
                line = line.strip()
        
                if line.startswith("Begin"):
                    tid = int(line.split()[1])
                    active[tid] = []
        
                elif line.startswith("COMMIT"):
                    tid = int(line.split()[1])
                    committed.add(tid)
        
                else:
                    parts = line.split("|")
                    tid = int(parts[0])
                    table_name = parts[1]
                    op_type = parts[2]
                    key = int(parts[3])
                    
                    # Getting the actual Table object
                    table_obj = db_manager.get_table(table_name)
                    
                    # Parsing the values
                    raw_old = parts[4]
                    raw_new = parts[5]
                    old_value = None if raw_old == "None" else ast.literal_eval(raw_old)
                    new_value = None if raw_new == "None" else ast.literal_eval(raw_new)
        
                    # Creating the operation using the table_obj
                    if table_obj:
                        op = Operations(table_obj, op_type, key, old_value, new_value)
                        active.setdefault(tid, []).append(op)
                    else:
                        print(f"Warning: Table {table_name} not found during recovery.")

        # Re-apply all changes from transactions that actually finished
        for tid in committed:
            if tid in active:
                print(f"Redoing committed transaction {tid} to ensure durability.")
                for op in active[tid]:
                    op.perform() # This pushes data into the B+ Tree

        # Roll back anything that didn't have a COMMIT tag
        for tid, ops in active.items():
            if tid not in committed:
                print(f"Undoing incomplete transaction {tid} for atomicity.")
                for op in reversed(ops):
                    op.undo()

    # to clear old logs
    def reset(self):
        open(self.filename, "w").close()

    # Printing logs
    def show_logs(self):
        with open(self.filename, "r") as f:
            for line in f:
                print(line.strip())