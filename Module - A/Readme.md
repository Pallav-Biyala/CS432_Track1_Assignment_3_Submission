# Mini Database System – ACID Validation (Module A)

## Overview
This module extends our **B+ Tree–based mini database system** by introducing **transaction management** and **recovery mechanisms** in order to validate the four fundamental **ACID properties** of database systems.

The goal of this module is not to build a full production database engine, but to demonstrate how core transactional guarantees are implemented using simplified mechanisms such as **Write‑Ahead Logging (WAL)**, transaction management, and controlled crash simulations along with **Checkpoint** Mechanism.

---

## Features
- B+ Tree based indexed storage  
- Transaction management  
- Write‑Ahead Logging (WAL)  
- Crash recovery  
- Rollback support  
- Checkpoint mechanism  
- ACID property validation  

---

## ACID Properties Demonstrated

### 1. Atomicity
Atomicity ensures that a transaction either completes entirely or has no effect at all.  

**In this system:**
- Each transaction logs its operations in the WAL.  
- If a failure occurs before commit, the system rolls back all operations of that transaction.  
- This guarantees that partial updates never remain in the database.  

---

### 2. Consistency
Consistency ensures that the database always remains in a valid state before and after a transaction.  

**This system enforces consistency using:**
- Primary key constraints  
- Validation before insert/update operations  
- Prevention of duplicate records  

Thus, invalid states cannot be introduced into the database.  

---

### 3. Isolation
Isolation ensures that concurrent transactions do not interfere with each other.  

**Our system demonstrates isolation by:**
- Executing multiple transactions  
- Ensuring uncommitted changes are not visible to other transactions  

This prevents issues such as **dirty reads**.  

---

### 4. Durability
Durability guarantees that once a transaction is committed, its changes will persist even after system failures.  

**This is achieved using Write‑Ahead Logging (WAL):**
- Operations are written to the WAL before being applied to the database.  
- If a crash occurs, the system can replay committed operations from the log.  
- During recovery, the database state is reconstructed using WAL entries.  

---

## Checkpoint Mechanism
To optimize recovery time, the system implements **checkpointing**.  

**At a checkpoint:**
- The current database state is saved to disk (`system_data.db`)  
- Old WAL entries can safely be truncated  

**During recovery:**
- The latest checkpoint is loaded.  
- Remaining WAL entries are replayed.  

This significantly reduces recovery overhead.  

---

## Simulated Crash Testing
Since Python executes operations immediately in memory, true hardware‑level crashes cannot be reproduced.  

Instead, crash scenarios are simulated by:  
- Restarting the database manager  
- Reloading WAL logs  
- Replaying committed operations  

This demonstrates the conceptual behavior of real database crash recovery.  

---

## Conclusion
Through a series of controlled tests and simulated failure scenarios, this project validates the **ACID properties** in a simplified database system.  

- **Atomicity**: Rollbacks ensure no partial updates remain.  
- **Consistency**: Constraints prevent invalid states.  
- **Isolation**: Transactions remain independent until commit.  
- **Durability**: WAL + checkpoints guarantee recovery after crashes.  

## Concepts Used
- B+ Trees
- Transaction Processing
- Write-Ahead Logging (WAL)
- Crash Recovery
- Database Checkpointing
- ACID Properties

## Conclusion
This module demonstrates how core database concepts such as logging, transaction management, and recovery mechanisms work together to enforce ACID guarantees.

Although simplified, the system reflects the fundamental architecture used in real-world database systems, highlighting how reliability and correctness are maintained even in the presence of failures.

## Authors
Developed as part of a Database Systems Assignment.
Although simplified, this design reflects the **core principles used in real‑world DBMS**, including logging, recovery, and indexed data access through B+ Trees.  

---
