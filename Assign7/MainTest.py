#echo "graph G {Hello--World}" | dot -Tpng >hello.png
import csv
import sys, os, math

Names = []
OverlapList = []
olist = []  
LifeSpans = []
SLNO = []
Songs = []
Graph = []
BiggestTeam = []
Temp = []
DFSFile = []
flag = False

MaxSize = 0

#Function to create Biggest Team and Smallest Tree Files
def CreateTree(D , Filename):
    fp = open(Filename,"w");
    fp.write("graph {\n");
    for x in D :
        fp.write(x + "\n");
    fp.write("}");    
    fp.close();

#Function to create input.dot file for centred interval tree file     
def createFile(n1):
    fp = open("input.dot","w");
    fp.write("graph {");
    myqueue = []
    myqueue.append(n1);
    while len(myqueue) != 0:
        n1 = myqueue.pop(0);
        
        n2 = n1.lChild;
        n3 = n1.rChild;
        if n2 is not None :
            myqueue.append(n2);
        if n3 is not None :    
            myqueue.append(n3);
        
        str1 = '"'
        str1 = str1 + str(n1.data) + "\\n" + "Span[" + str(n1.spanx) + "," + str(n1.spany) +"]";
        str1 = str1 + "\\n";
        for i in range(0,len(n1.slnos)):
            for k in range(0, len(Names)):                   
                if Names[k] == n1.intervals[i] :
                    break;
                     
            str1 = str1 + " [" + str(n1.slnos[i]) + "," + n1.intervals[i]+ " " + LifeSpans[k]+"]"
        str1 = str1 + '"'       
        
        if n2 is not None:    
            str2 = '"'     
            str2 = str2 + str(n2.data) + "\\n" + "Span[" + str(n2.spanx) + "," + str(n2.spany) +"]";
            str2 = str2 + "\\n";
            for i in range(0,len(n2.slnos)):
                for k in range(0 , len(Names)) :
                    if Names[k] == n2.intervals[i] :
                        break;
                str2 = str2 + " [" + str(n2.slnos[i]) + "," + n2.intervals[i]+ " " + LifeSpans[k] + "]"
            str2 = str2 + '"'            
            fp.write(str1 + "--" + str2)    
        if n3 is not None:
            str3 = '"'
            str3 = str3 + str(n3.data) + "\\n" + "Span[" + str(n3.spanx) + "," + str(n3.spany) +"]";
            str3 = str3 + "\\n";
            for i in range(0,len(n3.slnos)):
                for k in range(0, len(Names)) :
                    if Names[k] == n3.intervals[i] :
                        break;    
                str3 = str3 + " [" + str(n3.slnos[i]) + "," + n3.intervals[i]+ " " + LifeSpans[k] + "]"
            str3 = str3 + '"'            
            fp.write(str1 + "--" + str3)
             
    fp.write("\n}");
    fp.close();
    
#Function To sort all life spans    
def mergeSort(alist):
    
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

    #print("Merging ",alist)

#Class to store Node informations along with their name, lifespan 
#and interval which overlap with them.

class Node:
    rChild,lChild,parent,data = None,None,None,0    
    intervals = None;
    slnos = None;
    overlaps = None;
    spanx , spany = 0,0;
    def __init__(self,key,parent,x,y):
        self.intervals = []
        self.slnos = []
        self.overlaps = []
        
        self.rChild = None
        self.lChild = None
        self.parent = parent
        self.data = key 
        self.spanx = x;
        self.spany = y;

#To construct a Tree in Main Memory for storing all information in Node
#This class contains functions for Centered Binary Tree.
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


#Function to Create Centered Binary Tree.
    def sortedArrayToBST(self, alist , start, end, parent , x , y):
        if start > end :
            return Node(None , parent , x , y);
 
        #Get the middle element and make it root 
        n = end - start + 1;
               
        mid = 1;
        while mid <= n//2:  
            mid = mid * 2
        if mid//2 - 1 <= (n-mid):
           mid = mid - 1      # case 1 when left has equal no of elements than right
        else:
            mid = n - mid//2   # case 2 when left has more elements than right  
        mid = mid + start;    
        
        #mid = int(mid);
        #mid = int(math.ceil((start+float(end))/2));
        
        root = Node(alist[mid], parent , x , y);
 
        #Recursively construct the left subtree and make it
        #left child of root 
        
        root.lChild =  self.sortedArrayToBST(alist, start, mid-1, root, root.spanx, root.data);
 
        #Recursively construct the right subtree and make it
        #right child of root 
        root.rChild = self.sortedArrayToBST(alist, mid+1, end , root, root.data, root.spany);       
                      
        return root;
        
#Function to display Songs of given span a,b        
    def FindSongs(self, a, b, N) :
        global olist
        olist = [];
        
        self.OnlyFindOverlaps(a, b, N);
        
        for i in range(0, len(olist)) :
            for j in range(0, len(Names)) :
                #print olist[i] + " " + Names[j];
                if olist[i] == Names[j] :
                    break;
            print        
            print
            print "SLNO : " + SLNO[j] + " Name : " + Names[j] + " LifeSpan : " + LifeSpans[j];        
            for k in range(0, len(Songs[j])) :
                if "N.A." not in Songs[j][k] :                     
                    print "\nSongs of Genre" + str(k+1) + "  " ,
                    for p in range(0, len(Songs[j][k])) :  
                        print Songs[j][k][p] + "  ",
                        
#Function to find max biggest team                        
    def FindMax(self , N) :
        global MaxSize;
        if N is not None :
            if len(N.intervals) >= MaxSize:
                if N not in BiggestTeam :
                    MaxSize = len(N.intervals);
                    BiggestTeam.append(N);
            self.FindMax(N.lChild);
            self.FindMax(N.rChild);        
            
#To find the spans which has more than 50% lifespan overlap with given span            
    def FindMaxOverlaps(self, a,b, N) :
        global olist
        olist = [];
        self.OnlyFindOverlaps(a , b , N);
        print "List of Composers having maximal Overflows with intervals :";        
        for i in range(0,len(olist)) :
            for j in range(0, len(Names)):
                if olist[i] == Names[j] :
                    break;
            arr = LifeSpans[j].split("-");        
            diff = 0;
            x = int(arr[0]);
            y = int(arr[1]);
            if (a <= x and y <= b):
                diff = y - x;                
            elif (a >= x and y >= a):
                diff = y - a;   
            elif (b >= x and y >= b) :   
                diff = b - x;
            if a >= x and b <=y:
                diff = b - a;    
            if diff > (y - x) // 2 :
                print SLNO[j] + "  " + Names[j] + "  " + LifeSpans[j]    

#Function To find Overlaps.                
    def OnlyFindOverlaps(self, a,b, N) :
        if N is not None :
            for x in range (0,len(N.intervals)) :
                if N.intervals[x] not in olist:
                    for j in range (0, len(Names)):
                        if Names[j] == N.intervals[x] :
                            break;
                    #print "    " + LifeSpans[j];
                    arr = LifeSpans[j].split("-");
                    if (a <= int(arr[0]) and int(arr[1]) <= b) or (a >= int(arr[0]) and int(arr[1]) >= a) or (b >= int(arr[0]) and int(arr[1]) >= b) :
                        olist.append(N.intervals[x]);                               
        if N is not None:
            if a <= N.data :
                self.OnlyFindOverlaps(a, b , N.lChild);
            if N.data <= b :
                self.OnlyFindOverlaps(a, b, N.rChild);
                
#Function to find Overlaps and print them                
    def FindOverlaps(self, a,b, N) :
        if N is not None :
            for x in range (0,len(N.intervals)) :
                if N.intervals[x] not in olist:
                    for j in range (0, len(Names)):
                        if Names[j] == N.intervals[x] :
                            break;
                    #print "    " + LifeSpans[j];
                    arr = LifeSpans[j].split("-");
                    if (a <= int(arr[0]) and int(arr[1]) <= b) or (a >= int(arr[0]) and int(arr[1]) >= a) or (b >= int(arr[0]) and int(arr[1]) >= b) :
                        olist.append(N.intervals[x]);
                        print "SlNo : " + str(N.slnos[x]) + " Name : " + Names[j] + "  LifeSpan : " + LifeSpans[j] + " #NoOfOverlaps :" + str(len(OverlapList[j])-1)         
        if N is not None:
            if a <= N.data :
                self.FindOverlaps(a, b , N.lChild);
            if N.data <= b :
                self.FindOverlaps(a, b, N.rChild);
                
#Function To add overlap in the node of a tree                
    def addOverlap(self, N , I) :
        if N is not None :
            self.addOverlap(N.lChild, I);
            if I not in N.overlaps :
                N.overlaps.append(I);
            self.addOverlap(N.rChild, I);
            
#Function to add interval in the node of tree the tree.
    def addInterval(self, slno, I, a, b , N) :
        if N is None :
            return;

        #print "Checking " , I , " " , a , " " , b , " " , N.data;
        global flag;
        flag = False;
                    
        if a <= N.spanx and N.spany <= b :
            if N.parent is not None :
                if not(a <= N.parent.spanx and N.parent.spany <= b):
                    #print "interval added to " , N.data;
                    if I not in N.overlaps :
                        N.overlaps.append(I)
                        N.intervals.append(I)
                        self.addOverlap(N, I);
                    
                    N.slnos.append(slno);
                    flag = True;                    
                    N.overlaps.append(I);
                    x = N;                       
                        
        if flag == False:
            if a < N.data :
                #print "Check1";
                self.addInterval(slno, I , a , b , N.lChild);
            if N.data < b :
                #print "Check2";
                self.addInterval(slno, I , a , b , N.rChild);
                
#To find Overlap list of r node from tree                
    def FindOverlapList(self, indx, lspan, rspan, r) :
        if r is None :
            return;
        if lspan < r.data :
            for x in r.intervals :
                if x not in OverlapList[indx] :
                    OverlapList[indx].append(x)
            self.FindOverlapList(indx, lspan, rspan, r.lChild);
            
        if rspan > r.data :
            for x in r.intervals :
                if x not in OverlapList[indx] :
                    OverlapList[indx].append(x)
            self.FindOverlapList(indx, lspan, rspan, r.rChild);    
                               
    
#To print Tree in inorder for testing purpose                            
    def printTree(self,someNode):
        if someNode is None:
            pass
        else:
            self.printTree(someNode.lChild)
            print
            print someNode.data, "Span is[",someNode.spanx,",", someNode.spany , "]"
            if someNode.parent is not None:
                print " ========= Parent data is :" , someNode.parent.data;
            print "Interval Nodes :" ;
            print someNode.intervals;
            print "Overlaps : " ;
            print someNode.overlaps;
                    
            self.printTree(someNode.rChild)
            
#Clique is used Biggest Team            
def isClique(p) :
    flag = True;
    for i in p:
        #raw_input("Hit a key");
        for k in p :
            j = Names.index(k);            
            if i not in OverlapList[j] :
                #print "Return False";
                return False;
    #print "Return True"            
    return True;                    
                     
#To find Biggest Team                        
def FindBiggestTeam() :
    Clq = []
    for x in Names :
        c = []
        c.append(x);
        Clq.append(c);
        
    for x in Clq:
        c1 = list(x);        
        for y in c1:          
            indx = Names.index(y)
            for z in Graph[indx]:
                p = list(x);
                if z not in p:
                    p.append(z);
                    p.sort();
                    if p not in Clq:
                        if isClique(p) :
                            Clq.append(p);        
    print Clq;
    mx = 0;
    print "Biggest Teams :"
    for x in Clq:
        if mx < len(x):
            mx = len(x);
    for x in Clq:
        if len(x) == mx :        
            print "Team : " , x; 
            arr = LifeSpans[Names.index(x[0])].split("-")
            MaxFromLeft = int(arr[0]);
            MinFromRight = int(arr[1]);
            for i in range(1, len(x)) :
                arr = LifeSpans[Names.index(x[i])].split("-")
                if MaxFromLeft < int(arr[0]):
                    MaxFromLeft = int(arr[0])
                if MinFromRight > int(arr[1]) :
                    MinFromRight = int(arr[1]);
                diff = abs(MaxFromLeft - MinFromRight)    
            print "Span which composers spent together is " + str(diff)        
            print MaxFromLeft, "-", MinFromRight    
            

#Function for DFS to find Biggest and Smallest Teams.                     
def DFS(OverlapList, visited, v) :
    visited[Names.index(v)] = True;
    Temp.append(v); 
    #print Graph[Names.index(v)];
    for w in OverlapList[Names.index(v)] :
        if(not visited[Names.index(w)]) :
            DfsFile.append(v+"--"+w);
            DFS(OverlapList, visited, w);

#Function to create Overlap graph.                         
def OverlapGraph() :
    fp = open("Overlap.dot", "w");
    l = []
    global Graph
    Graph = []
    fp.write("graph {");
         
    for i in range(0, len(OverlapList)) :
        Vertex = []
        if len(OverlapList[i]) == 1 :
            s1 = OverlapList[i][0];
            fp.write(s1 + "\n");
        for j in range(1, len(OverlapList[i])) :
            for k in range(0, len(Names)):
                if Names[k] == OverlapList[i][j] :
                    break;                           
            s1 = OverlapList[i][0] + "--" + OverlapList[i][j]
            s2 = OverlapList[i][j] + "--" + OverlapList[i][0]
             
            if s1 not in l  and s2 not in l :
                Vertex.append(OverlapList[i][j]);
                l.append(s1);
                fp.write(s1 + "\n");
        Graph.append(Vertex);          
    fp.write(" }");                 
    #print Graph;    
    fp.close(); 

def main():  
    total = len(sys.argv)
    cmdargs = str(sys.argv)
    if total != 2:
        print ("Insufficient no of arguments");
        exit(0);


    filename = str(sys.argv[1]);
    try :
        fp = open(filename, 'r');
        fp.close();
    except IOError :
        print "Error in file";
        exit(0);
        
    alist = []
    global Songs;
        
    Songs = []
    global olist
    olist = []
    
    #Reading File Code
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        count = 0;
        for row in readCSV:
            count = count + 1;
            if len(row) == 0 or count == 1:
                if len(row) == 0 :
                    count = count - 1;
                continue;
            slno =  str(row[0]).strip();
            cname = str(row[1]).strip();
            lspan = str(row[2]).strip();
            arr = lspan.split('-');
            if len(arr) != 2 :
                print "Span Error";
                exit(0);
            
            for i in range(0,len(arr)):
                alist.append(int(arr[i]));
            genrelist = []    
           
            i = 3;
            while i < len(row) :
                rowsong = row[i].strip();
                if rowsong[0] == '"':
                    rowsong = rowsong[1:];
                    songlist = []
                   
                    while rowsong[len(rowsong) - 1] != '"' :
                        songlist.append(rowsong)
                        i = i + 1
                        rowsong = row[i].strip();
                        
                    rowsong = rowsong[:-1]
                    songlist.append(rowsong);
                    i = i + 1;            
                    genrelist.append(songlist);
                else :
                    if rowsong == "N.A." : 
                        songlist = []
                        songlist.append("N.A.");
                        genrelist.append(songlist);
                    i = i + 1;
                        
            Songs.append(genrelist);           
            Names.append(cname)
            OverlapList.append([]);
            LifeSpans.append(lspan)
            SLNO.append(slno);
        
        mergeSort(alist)
        
        t = Tree()
        
        t.root = t.sortedArrayToBST(alist , 0, 2*(count-1)-1 , None , float("-inf"),float("inf")); 
        
        for i in range(0, len(Names)) :
            arr = LifeSpans[i].split('-');
            t.addInterval(SLNO[i], Names[i], int(arr[0]),int(arr[1]),t.root);
            
        #print "Binary Search Tree :";
        #print "Root is :" , t.root.data;     
        #t.printTree(t.root)
        
        createFile(t.root);  #file is created with name input.dot
        
        for i in range(0, len(Names)) :
            arr = LifeSpans[i].split("-");
            OverlapList[i].append(Names[i]);
            t.FindOverlapList(i, int(arr[0]) , int(arr[1]), t.root)
            
        OverlapGraph();
        #print(Names)
            

    while True:
        print
        print
        print "1. Insert Interval\n2. FindOverlaps.\n3. MaxOverlaps.\n4. FindSongs"
        
        print "\n5. BuiltIG  \n6. BiggestTeam  \n7. FindGroup  \n8. Exit"
        
        while True:
            try:
                x = int(raw_input("Enter your choice :"));
                break;
            except ValueError:
                print "Please Enter proper no";
            
    
        if x in range(1, 9):
            if x == 1:
                
                sl = raw_input("Enter Slno :")
                nm = raw_input("Enter name :")
                interv1 = raw_input("Enter lower limit of interval :")
                interv2 = raw_input("Enter upper limit of interval :")
                if interv1 <= interv2 :
                    t.addInterval(sl, nm, int(interv1),int(interv2),t.root)
                    if flag == True:
                        Names.append(nm)
                        print Names;
                        s = interv1 + "-" + interv2
                        LifeSpans.append(s);
                        OverlapList.append([]);
                        SLNO.append(sl);
                        
                        createFile(t.root);  #file is created with name input.dot
                        #print "-----------" , Names.index(nm)
                        OverlapList[Names.index(nm)].append(nm);
                        t.FindOverlapList(Names.index(nm) , int(interv1) , int(interv2), t.root)
                        OverlapGraph();
                    
                else :
                    print "lower limit must be <= upper limit"    
                
                
            elif x == 2:    
                istart = int(raw_input("Enter beginning of interval :"));
                iend = int(raw_input("Enter end of interval :"));
                #global olist;
                olist = []
                t.FindOverlaps(istart , iend , t.root);
                                         
            elif x == 3:
                istart = int(raw_input("Enter beginning of interval :"));
                iend = int(raw_input("Enter end of interval :"));
                #global olist;
                olist = []
                t.FindMaxOverlaps(istart , iend , t.root);
                
            elif x == 4:
                istart = int(raw_input("Enter beginning of interval :"));
                iend = int(raw_input("Enter end of interval :"));
                #global olist;
                olist = []
                t.FindSongs(istart , iend , t.root);
                
            elif x == 5:
                OverlapGraph();
                #for i in range(0, len(OverlapList)) :
                #    print 
                #    print "Overlap of " + Names[i],
                #    for j in range(0,len(OverlapList[i])) :
                #        print " " + OverlapList[i][j],
                #    print     
                    
            elif x == 6:
                FindBiggestTeam();
                
            elif x == 7:
                AllDfs = []
                AllDfsFiles = []
                for x in Names :
                    visited = []
                    global DfsFile
                    DfsFile = []
                    global Temp;
                    Temp = [];                
                    n = len(OverlapList)
                    for i in range(n) :
                        visited.append(False)                    
                    DFS(OverlapList, visited, x)
                    if len(DfsFile) == 0 :
                        DfsFile.append(x);
                    AllDfs.append(Temp)
                    AllDfsFiles.append(DfsFile)
                print AllDfs
                print AllDfsFiles
                mx = len(AllDfs[0])
                mxIndex = 0
                mn = len(AllDfs[0])
                mnIndex = 0
                for x in range(0, len(AllDfs)) :
                    if mx < len(AllDfs[x]) :
                        mx = len(AllDfs[x])
                        mxIndex = x;
                    elif mn > len(AllDfs[x]) :
                        mn = len(AllDfs[x])
                        mnIndex = x
                print str(mx) + "  " + str(mxIndex) + " " + str(mn) + " " + str(mnIndex)        
                print "Biggest Group is ", 
                print AllDfs[mxIndex]
                print "Smallest Group is ",
                print  AllDfs[mnIndex]
                
                CreateTree(AllDfsFiles[mxIndex] , "BiggestGroup.dot")
                CreateTree(AllDfsFiles[mnIndex] , "SmallestGroup.dot")            
                            
                    
            elif x == 8:
                sys.exit(0);
                         

if __name__ == '__main__':
    
    main()
    

