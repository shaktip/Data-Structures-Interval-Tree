#http://stackoverflow.com/questions/5444394/implementing-binary-search-tree-in-#python

class Node:
    rChild,lChild,parent,data = None,None,None,0    

    def __init__(self,key):
        self.rChild = None
        self.lChild = None
        self.parent = None
        self.data = key 

class Tree:
    root,size = None,0
    def __init__(self):
        self.root = None
        self.size = 0
    def insert(self,someNumber):
        self.size = self.size+1
        if self.root is None:
            self.root = Node(someNumber)
        else:
            self.insertWithNode(self.root, someNumber)    

    def insertWithNode(self,node,someNumber):
        if node.lChild is None and node.rChild is None:#external node
            if someNumber > node.data:
                newNode = Node(someNumber)
                node.rChild = newNode
                newNode.parent = node
            else:
                newNode = Node(someNumber)
                node.lChild = newNode
                newNode.parent = node
        else: #not external
            if someNumber > node.data:
                if node.rChild is not None:
                    self.insertWithNode(node.rChild, someNumber)
                else: #if empty node
                    newNode = Node(someNumber)
                    node.rChild = newNode
                    newNode.parent = node 
            else:
                if node.lChild is not None:
                    self.insertWithNode(node.lChild, someNumber)
                else:
                    newNode = Node(someNumber)
                    node.lChild = newNode
                    newNode.parent = node                    

    def printTree(self,someNode):
        if someNode is None:
            pass
        else:
            self.printTree(someNode.lChild)
            print someNode.data
            self.printTree(someNode.rChild)

def main():  
    t = Tree()
    t.insert(5)  
    t.insert(3)
    t.insert(7)
    t.insert(4)
    t.insert(2)
    t.insert(1)
    t.insert(6)
    t.printTree(t.root)

if __name__ == '__main__':
    main()
