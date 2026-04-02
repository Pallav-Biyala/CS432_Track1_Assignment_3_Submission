# Building transaction manager class
from databases.wal import WAL

class Transaction_Manager:
    # Keeping track of transactions
    def __init__(self,db_manager):
        self.db = db_manager
        self.operation_stack = {}
        self.transaction_counter = 0
        self.wal = WAL() # storing the logs in case of crash 
        self.wal.recover(self.db) # Adding auto reocvery so that every time a transaction is created, it recovers all past transactions

    # Begin transaction
    def begin(self):
        self.transaction_counter += 1
        tid = self.transaction_counter

        # creating stack of operations
        self.operation_stack[tid] = []

        # Beginning the log
        self.wal.log_begin(tid)

        print(f"Transaction {tid} started")
        return tid
    
    # Log operation: storing operations
    def log_operation(self, tid, operation):
        if tid not in self.operation_stack:
            print("Transaction not active")
            return
        
        self.wal.log_operation(
            tid,
            operation.table.name,
            operation.op_type,
            operation.key,
            operation.old_value,
            operation.new_value
        )
        self.operation_stack[tid].append(operation)

    # Commit
    def commit(self, tid):
        if tid not in self.operation_stack:
            print("Transaction not active")
            return

        # We log commit first before performing operations. Write ahead logging
        self.wal.log_commit(tid)
        
        # now we can apply staged operations now
        for op in self.operation_stack[tid]:
            op.perform()
        
        print(f"Transaction {tid} committed")
        
        del self.operation_stack[tid]

    # Rollback
    def rollback(self, tid):
        if tid not in self.operation_stack:
            print("Transaction not active")
            return
    
        print(f"Rolling back transaction {tid}")

        stack = self.operation_stack[tid]

        while stack:
            op = stack.pop()
            op.undo()

        del self.operation_stack[tid] # rollback so removing it 

    def active(self):
        print("Active transactions:", list(self.operation_stack.keys()))