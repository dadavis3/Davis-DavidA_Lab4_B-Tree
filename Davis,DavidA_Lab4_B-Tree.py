# Davis, David A  80610756
# Lab #4 B-Tree
# Goal: To learn to use B-Tree as a data structure.
# In this lab assigment we were asked to do different methods using B-Tree as
# a data structure and we did multiple things such as finding the smallest and
# the largest number in the tree, counting the nodes in the tree, know if the 
# nodes and the leaves are full, finding the height of the tree, printing the
# items at a certain depth and treturning the nodes at a certain depth, and 
# converting the tree into a sorted list.

# ---------------------     PRE-METHOD FOR B-TREES      ------------------

class BTree(object):
    # Constructor
    def __init__(self,item=[],child=[],isLeaf=True,max_items=5):  
        self.item = item
        self.child = child 
        self.isLeaf = isLeaf
        if max_items <3: #max_items must be odd and greater or equal to 3
            max_items = 3
        if max_items%2 == 0: #max_items must be odd and greater or equal to 3
            max_items +=1
        self.max_items = max_items

def FindChild(T,k):
    # Determines value of c, such that k must be in subtree T.child[c], if k is in the BTree    
    for i in range(len(T.item)):
        if k < T.item[i]:
            return i
    return len(T.item)
             
def InsertInternal(T,i):
    # T cannot be Full
    if T.isLeaf:
        InsertLeaf(T,i)
    else:
        k = FindChild(T,i)   
        if IsFull(T.child[k]):
            m, l, r = Split(T.child[k])
            T.item.insert(k,m) 
            T.child[k] = l
            T.child.insert(k+1,r) 
            k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
            
def Split(T):
    #print('Splitting')
    #PrintNode(T)
    mid = T.max_items//2
    if T.isLeaf:
        leftChild = BTree(T.item[:mid]) 
        rightChild = BTree(T.item[mid+1:]) 
    else:
        leftChild = BTree(T.item[:mid],T.child[:mid+1],T.isLeaf) 
        rightChild = BTree(T.item[mid+1:],T.child[mid+1:],T.isLeaf) 
    return T.item[mid], leftChild,  rightChild   
      
def InsertLeaf(T,i):
    T.item.append(i)  
    T.item.sort()

def IsFull(T):
    return len(T.item) >= T.max_items

def Insert(T,i):
    if not IsFull(T):
        InsertInternal(T,i)
    else:
        m, l, r = Split(T)
        T.item =[m]
        T.child = [l,r]
        T.isLeaf = False
        k = FindChild(T,i)  
        InsertInternal(T.child[k],i)   
        
def Search(T,k):
    # Returns node where k is, or None if k is not in the tree
    if k in T.item:
        return T
    if T.isLeaf:
        return None
    return Search(T.child[FindChild(T,k)],k)
                  
def Print(T):
    # Prints items in tree in ascending order
    if T.isLeaf:
        for t in T.item:
            print(t,end=' ')
    else:
        for i in range(len(T.item)):
            Print(T.child[i])
            print(T.item[i],end=' ')
        Print(T.child[len(T.item)])    
 
def PrintD(T,space):
    # Prints items and structure of B-tree
    if T.isLeaf:
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
    else:
        PrintD(T.child[len(T.item)],space+'   ')  
        for i in range(len(T.item)-1,-1,-1):
            print(space,T.item[i])
            PrintD(T.child[i],space+'   ')
    
def SearchAndPrint(T,k):
    node = Search(T,k)
    if node is None:
        print(k,'not found')
    else:
        print(k,'found',end=' ')
        print('node contents:',node.item)
        
        
        
# ----------------------    METHODS FOR THE LAB    -------------------
        
# Finds the height of the tree        
def height(T):
    if T.isLeaf:
        return 0
    return 1 + height(T.child[0])  # recursively adds 1 if the tree is not leaf

# Finds the minimum element of the tree
def MinElementAtDepth(T, d):
    if T.isLeaf:
        return T.item[0]
    if d==0:
        return T.item[0] # returns the minimum number of the tree until depth = 0
    else:
        # recursively subtract the depth by 1 
        return MinElementAtDepth(T.child[0],d-1) 
    
# Finds the maximum element of the tree    
def MaxElementAtDepth(T,d):
    if T.isLeaf:
        return T.item[-1]
    if d==0:
        return T.item[-1] # returns largest number until depth is 0
    else:
        # recursively subtracts the depth by 1 
        return MaxElementAtDepth(T.child[-1],d-1)
    
# Prints the items at a given depth   
def ItemsAtDepth(T,d):
    if d ==0:
        for t in T.item: 
            print(t,end= ' ') # prints the items until depth = 0
    if not T.isLeaf:
        for i in range(len(T.child)):
            # recursively subtracts depth by 1
            ItemsAtDepth(T.child[i],d-1)
            
# Returns the number of items at a given depth
def NodesNumAtDepth(T, d): 
    counter = 0
    if d == 0:
        return len(T.item)
    if T.isLeaf:
        return len(T.item) # returns the number of 
    for i in range(len(T.child)):
        counter += NodesNumAtDepth(T.child[i],d-1)
    return counter

# Checks how many nodes are full 
def FullNodes(T):
    counter = 0
    if not T.isLeaf:
        for i in range(len(T.child)): # when T is.Leaf then recursively 
                                      # we add 1 to each element
            counter += FullNodes(T.child[i])
    if len(T.item) == T.max_items: # else we add 1 if the length of the item
        counter += 1               # is equals to max_items
    return counter
                
    
# Checks how many leaves are full
def FullLeaves(T):
    counter = 0
    if T.isLeaf:
        if len(T.item) is T.max_items:    
            return 1
    else:
        for i in range(len(T.child)):
            counter += FullLeaves(T.child[i]) #this one do the same as the other
                                              #one, but here recursivley checks if 
                                              #the item is leaf
    return counter
        
# returns the depth of a certain number
def DepthOfKey(T, k):
    if k in T.item:
        return 0
    if T.isLeaf:
        return -1   #should return -1 if teh key is not in the tree
    if k>T.item[-1]:
        d = DepthOfKey(T.child[-1],k)   #recursively looks for for the key if 
                                        #k is in the right side
    else:
        for i in range(len(T.item)):
            if k < T.item[i]:
                d = DepthOfKey(T.child[i],k)    # check the left side
    if d == -1:
        return -1
    return d + 1                                #returns the depth

# Converts the tree into a sorted list
def BTreeToList(T):
    if T.isLeaf:
        return T.item
    L = []
    for i in range(len(T.item)):
        L = L + (BTreeToList(T.child[i])) # it appends the items of the tree 
        L.append(T.item[i])               # in ascending order
    return L + BTreeToList(T.child[-1])   # returns the list and recursively 
                                          # and goes to the last item 
    
L = [30, 50, 10, 20, 60, 70, 100, 40, 90, 80, 110, 120, 1, 11 , 3, 4, 5,105, 115, 200, 2, 45, 6]
T = BTree()    
for i in L:
    Insert(T,i)


depth = 2
key = 105
print('This is the actual tree:')
print('-----------------------------------------------------')
PrintD(T, ' ')
print('-----------------------------------------------------')
print('1.  The height of the tree is:',height(T))
print('2.  B-Tree converted into a sorted list:')
print(BTreeToList(T))
print('3.  The minimum element at a depth of',depth,'is:',MinElementAtDepth(T,depth))
print('4.  The maximum element at a depth of',depth,'is:',MaxElementAtDepth(T,depth))
print('5.  Number of nodes at a depth of', depth,':',NodesNumAtDepth(T,depth))
print('6.  All items at a depth of', depth, ':')
ItemsAtDepth(T,2)
print()
print('7.  Number of nodes that are full:',FullNodes(T))
print('8.  Number of leaves that are full:',FullLeaves(T))
print('9. ',key,'can be found at a depth of:',DepthOfKey(T,key))







