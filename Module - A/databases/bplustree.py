# B+ Trees implementation
import math
# creating the Node of B+ tree
class BPlusTreeNode:
    def __init__(self,leaf = False):
        self.leaf = leaf # tells if current node is leaf or not
        self.keys = [] # stores all keys in current node
        self.children = [] # stores all children of the current node
        self.values = [] # stores all records
        self.next = None # used for leaf to maintain linked list of leaf nodes
        self.parent = None # parent pointer

class BPlusTree:
    def __init__ (self, order):
        self.root = BPlusTreeNode(leaf = True)
        self.order = order
    
    # This helps to find the leaf node if key is given 
    def findLeaf(self,key):
        node = self.root

        while not node.leaf: # until we reach leaf
            i = 0
            # if key < node[0] go left, key<node[1] go next of left and hence instead we just find the correct i index by incrementing it to 1
            while i< len(node.keys) and key >= node.keys[i]:
                i += 1

            node = node.children[i]

        return node # points to the node having or should have the key

    # Returns the value of key in B+ tree if its there otherwise returns none
    def search(self, key):
        leaf = self.findLeaf(key)
        for i,k in enumerate(leaf.keys):
            if (k == key):
                return leaf.values[i] # Found and hence returning value
            
        return None # Not found

    #___________Insertion Begins________________________#

    # Inserts the key, value in B+ tree
    def insert(self,key, value):
        if self.search(key) is not None:
            # We assume multiple keys aren't allowed and if they are added, we just overwrite values
            leaf = self.findLeaf(key)
            for i, k in enumerate(leaf.keys):
                if k == key:
                    leaf.values[i] = value
                    return
                
        leaf = self.findLeaf(key)

        # Now we need to find correct place to insert leaf otherwise sorted order disturbes
        i = 0
        while i< len(leaf.keys) and key >= leaf.keys[i]:
            i+=1
        
        # Now inserting at i
        leaf.keys.insert(i,key)
        leaf.values.insert(i,value)

        # checking overflow as if it becomes equal to order splitting needed
        if len(leaf.keys) > self.order-1:
            self.split_leaf(leaf)
    
    def split_leaf(self, leaf):
        mid = len(leaf.keys)//2
        new_leaf = BPlusTreeNode(leaf = True)
        new_leaf.parent = leaf.parent

        # Adding second half elements to new leaf
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]

        # deleting second half elements from original
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]

        # Now modifying linked list
        new_leaf.next = leaf.next
        leaf.next = new_leaf

        # Now need to add the first child of newleaf to parent
        self.insertIntoParent(leaf,new_leaf.keys[0], new_leaf)
    
    def insertIntoParent(self,left, key, right):
        parent = left.parent

        # Case 1: Left was root
        if parent is None:
            new_root = BPlusTreeNode()
            
            new_root.keys = [key]
            new_root.children = [left,right]

            left.parent = new_root;
            right.parent = new_root;

            self.root = new_root
            return
        
        # Case - 2: Left is general (not root)
        # Finding position of children left and right to insert 
        pos = parent.children.index(left)

        # Inserting key and right child
        parent.keys.insert(pos,key)
        parent.children.insert(pos+1, right)

        right.parent = parent

        # Checking overflow
        if (len(parent.keys) >= self.order):
            self.split_internal(parent)

    # Now if parent is overflown need to again split it maintaining its children
    def split_internal(self, node):
        mid = len(node.keys)//2

        promoted_key = node.keys[mid]
        new_internal = BPlusTreeNode()

        # Splitting keys
        new_internal.keys = node.keys[mid+1:]
        node.keys = node.keys[:mid]

        # Splitting children
        new_internal.children = node.children[mid+1:]
        node.children = node.children[:mid+1]

        # Update parent pointers
        for child in new_internal.children:
            child.parent = new_internal
        
        new_internal.parent = node.parent

        # Insert into parent
        self.insertIntoParent(node, promoted_key, new_internal)

    #______________Insertion Ends______________________#
    
    # _____________Deletion Begins______________________#
    def delete(self, key):
        # So firstly we need to find the leaf which has key to be deleted
        leaf = self.findLeaf(key)

        # Now we need to check if key exists or not
        if key not in leaf.keys:
            return # key not found
        
        # Now we need to find key through index
        idx = leaf.keys.index(key)

        # removing key and value 
        leaf.keys.pop(idx)
        leaf.values.pop(idx)

        # Now comes cases
        # if leaf is root
        if leaf == self.root:
            if len(leaf.keys) == 0:
                self.root = BPlusTreeNode(leaf=True)
            return
        
        # Now minimum keys that can be in a node is ceil((order - 1) /2) and hence if it reduces from here, we need to fix underflow
        min_keys = math.ceil((self.order - 1)/2)

        if len(leaf.keys)< min_keys:
            self.fix_underflow(leaf)

    # Used to fix underflow
    def fix_underflow(self,node):
        parent = node.parent
        if parent is None:
            # Root case
            if not node.leaf and len(node.children) == 1:
                # Collapse root if it has only one child
                self.root = node.children[0]
                self.root.parent = None
            return

        idx = parent.children.index(node)

        # finding siblings of deleted node
        left_sibling = parent.children[idx-1] if idx>0 else None
        right_sibling = parent.children[idx+1] if idx<len(parent.children) - 1 else None
        
        # Now we can have three cases: Borrow one node from left sibling otherwise borrow one node from right sibling otherwise merge them
        min_keys = math.ceil((self.order - 1)/2)

        # Case 1 borrow from left
        if left_sibling and len(left_sibling.keys)>min_keys:
            self.borrow_from_left(node, left_sibling, parent, idx)
            return

        # Case 2 borrow from right
        if right_sibling and len(right_sibling.keys)>min_keys:
            self.borrow_from_right(node, right_sibling, parent, idx)
            return

        # Case 3 Merge both
        if left_sibling:
            self.merge(left_sibling, node, parent, idx-1)
        else:
            self.merge(node, right_sibling, parent, idx)
    
    # Now our only task is to write functions for all three cases
    def borrow_from_left(self, node, left, parent,idx):
        if node.leaf: # if node is leaf
            key = left.keys.pop(-1) # extracting the rightmost element as thats what we use to merge
            value = left.values.pop(-1)

            node.keys.insert(0, key) # adding the node given by left child to node
            node.values.insert(0,value) 

            parent.keys[idx - 1] = node.keys[0] # as now parent becomes the leftmost pointer in current node

        else:  # if node is internal node
            separator = parent.keys[idx - 1]

            borrowed_key = left.keys.pop(-1)
            borrowed_child = left.children.pop(-1)

            node.keys.insert(0, separator)
            node.children.insert(0, borrowed_child)

            borrowed_child.parent = node

            parent.keys[idx - 1] = borrowed_key
    
    def borrow_from_right(self,node, right, parent, idx):
        if node.leaf: #if node is leaf
            key = right.keys.pop(0) # extracting the leftmost element from right sibling as thats what we use to merge
            value = right.values.pop(0) 

            node.keys.append(key)
            node.values.append(value)
            
            if right.keys:
                parent.keys[idx] = right.keys[0] # as the parent now changes to the leftmost pointer in right silbing

        else:  # if node is internal node
            separator = parent.keys[idx]

            borrowed_key = right.keys.pop(0)
            borrowed_child = right.children.pop(0)

            node.keys.append(separator)
            node.children.append(borrowed_child)

            borrowed_child.parent = node

            parent.keys[idx] = borrowed_key

    def merge(self, left, right, parent, parent_key_index):
        # So we just merge left and right in one
        if left.leaf:
            # Adding all elements of right node to left node (merging them) 
            left.keys.extend(right.keys)
            left.values.extend(right.values)

            # And then we fix left-> next to right next and hence right gets omitted
            left.next = right.next
        
        else:   # internal node merge
            sep = parent.keys[parent_key_index]
    
            left.keys.append(sep)
            left.keys.extend(right.keys)
    
            left.children.extend(right.children)
    
            for child in right.children:
                child.parent = left
    
        # Now removing the index (seperator) of first right child from parent
        parent.keys.pop(parent_key_index)

        # removing right child from children array of parent pointer
        parent.children.remove(right)

        # Hence, right is removed. now just need to manage parent pointer

        # If parent pointer became root and empty
        if parent == self.root and len(parent.keys) == 0:
            self.root = left
            left.parent = None
            return
        
        # if parent becomes underflow then fix it
        min_keys = math.ceil((self.order - 1)/2)

        if parent != self.root and len(parent.keys)<min_keys:
            self.fix_underflow(parent)
            
    #______________Deletion Ends________________________#
    
    # Range query
    def range_query(self, start_key, end_key):
        result = []

        # Firstly we find from where to start
        leaf = self.findLeaf(start_key)

        while leaf:
            for i,key in enumerate(leaf.keys):
                if key>end_key:
                    return result
                
                if key>=start_key:
                    result.append((key, leaf.values[i]))
            
            leaf = leaf.next # Now we added all elements in current leaf, lets go to next leaf and check

        return result
    
    # Update Query
    def update(self, key, new_value):
        # So firstly we find leaf
        leaf = self.findLeaf(key)

        for i,k in enumerate(leaf.keys):
            if k == key:
                leaf.values[i] = new_value
                return True
        
        return False

    # Extracting all keys
    def get_all(self):
        # So firstly we need to go to the leftmost leaf
        result = []
        node = self.root

        while not node.leaf:
            node = node.children[0]
        
        # now we just need to traverse all leaves
        while node:
            for i,key in enumerate(node.keys):
                result.append((key,node.values[i]))
        
            node = node.next
        
        return result
    
    # Printing Tree
    def print_tree(self):
        level = [self.root]
        while level:
            next_level = []
            for node in level:
                print(node.keys, end=" | ")

                if not node.leaf:
                    next_level.extend(node.children)

            print()
            level = next_level
