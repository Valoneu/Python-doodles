print("select program:","1 -> linear functions",sep = "\n")
print()

prognum = int(input("program: "))

if prognum == 1:
    print()
    print("program linear functions selected","please select module","1 -> y = ax + b","2 -> y = ax ","3 -> y = |ax|+ b","4 -> y = |ax + b|",sep = "\n")
    print()
    
    prog1mod = int(input("module: "))
    
    if prog1mod == 1:
        print()
        print("selected y = ax + b","select action","1 -> calculate a,b from 2 points","2 -> calculates y from x","3 -> calculates x from y",sep = "\n")
        print()
        
        actnum = int(input("action: "))
        
        if actnum == 1:
            print()
            
            print("y = a * x + b")
            x1 = int(input("input x1: "))
            y1 = int(input("input y1: "))
            x2 = int(input("input x2: "))
            y2 = int(input("input y2: "))
            
            print()
            print ("point one:[",x1,y1,"],point2 :[",x2,y2,"]")
            print()
            
            a = (y1-y2) / (x1-x2)
            print ("a is:", a)
            print()
            
            b = y1 - x1 * a
            print ("b is:", b)
            print()
            
            print ("full is y =",a,"* x +",b)
            
        elif actnum == 2:
            print()    
            
            print("y = a * x + b")
            a = int(input("input a: "))
            x = int(input("input x: "))
            b = int(input("input b: "))
            
            y = a * x + b
    
            print ("value y is",y,"at x",x)
            
        elif actnum == 3:
            print()    
            
            print("x = (y - b) / a")
            a = int(input("input a: "))
            y = int(input("input y: "))
            b = int(input("input b: "))
            
            x = (y - b) / a
    
            print ("value x is",x,"at y",y)
         
        else:
            print()
            print("action num",actnum,"doesent exist")
            
    elif prog1mod == 2:
        print()
        print("selected y = ax","select action","1 -> calculate a from 2 points","2 -> calculates y from x","3 -> calculates x from y",sep = "\n")
        
        actnum = int(input("action: "))
        
        if actnum == 1:
            print()
            
            print("y = a * x")
            x1 = int(input("input x1: "))
            y1 = int(input("input y1: "))
            x2 = int(input("input x2: "))
            y2 = int(input("input y2: "))
            
            print()
            print ("point one:[",x1,y1,"],point2 :[",x2,y2,"]")
            print()
            
            a = (y1-y2) / (x1-x2)
            print ("a is:", a)
            print()
            
            print ("full is y =",a,"* x")
            
        elif actnum == 2:
            print()    
            
            print("y = a * x")
            a = int(input("input a: "))
            x = int(input("input x: "))
            
            y = a * x
    
            print ("value y is",y,"at x",x)
            
        elif actnum == 3:
            print()    
            
            print("x = y / a")
            a = int(input("input a: "))
            y = int(input("input y: "))
            
            x = y / a
    
            print ("value x is",x,"at y",y)
         
        else:
            print()
            print("action num",actnum,"doesent exist")
        
    elif prog1mod == 3:
        print()
        print("selected y = |ax| + b","select action","1 -> calculate a,b from 2 points","2 -> calculates y from x","3 -> calculates x from y",sep = "\n")
        
        actnum = int(input("action: "))
        
        if actnum == 1:
            print()
            
            print("y = |a * x| + b")
            x1 = int(input("input x1: "))
            y1 = int(input("input y1: "))
            x2 = int(input("input x2: "))
            y2 = int(input("input y2: "))
            
            print()
            print ("point one:[",x1,y1,"],point2 :[",x2,y2,"]")
            print()
            
            a = (y1-y2) / (x1-x2)
            print ("a is:", a)
            print()
            
            b = y1 - x1 * a
            print ("b is:", b)
            print()
            
            print ("full is y = |",a,"* x | +",b)
            
        elif actnum == 2:
            print()    
            
            print("y = a * x + b")
            a = int(input("input a: "))
            x = int(input("input x: "))
            b = int(input("input b: "))
            
            y = a * x + b
    
            print ("value y is",y,"at x",x)
            
        elif actnum == 3:
            print()    
            
            print("x = (y - b) / a")
            a = int(input("input a: "))
            y = int(input("input y: "))
            b = int(input("input b: "))
            
            x = (y - b) / a
    
            print ("value x is",x,"at y",y)
         
        else:
            print()
            print("action num",actnum,"doesent exist")
        
    elif prog1mod == 4:
        print()
        print("selected y = |ax + b|")
        print("select action")   
        
    else:
        print()
        print("module num",prog1mod,"doesent exist")
    
else:
    print()
    print("program num",prognum,"doesent exist")