
    while True:
        print "1. FindOverlaps.   2. MaxOverlaps.   3. FindSongs"
        
        print "4. BuiltIG  5. BiggestTeam  6. FindGroup  7.Exit"
    
        while True:
            try:
                x = int(raw_input("Enter your choice :"));
                break;
            except ValueError:
                print "Please Enter proper no";
            
    #print "Value of x is :" , x;
        if x in range(1, 8):
            if x == 1:    
                istart = int(raw_input("Enter beginning of interval :"));
                iend = int(raw_input("Enter end of interval :"));
                global olist;
                olist = []
                t.FindOverlaps(istart , iend , t.root);
                                         
            elif x == 2:
                istart = int(raw_input("Enter beginning of interval :"));
                iend = int(raw_input("Enter end of interval :"));
                global olist;
                olist = []
                t.FindMaxOverlaps(istart , iend , t.root);
            elif x == 3:
                istart = int(raw_input("Enter beginning of interval :"));
                iend = int(raw_input("Enter end of interval :"));
                global olist;
                olist = []
                t.FindSongs(istart , iend , t.root);
            elif x == 4:
                OverlapGraph();
            elif x == 5:
                t.FindBiggestTeam(t.root);
            #elif x == 6:
            elif x == 7:
                sys.exit(0);

