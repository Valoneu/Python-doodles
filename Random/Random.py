#stake dice sim

import random

Broke = False
Balance = 10000
BetSize = 1
StartingBetSize = 1
Over = True
Bias = 550
RollNumber = 0

while Broke == False :
    if Over == True :
        RandomNumber = random.randrange(0, 1000)
        if RandomNumber >= Bias :
            Balance = Balance + (BetSize * 2.2)
            BetSize = StartingBetSize
            RollNumber = RollNumber + 1
            print (RollNumber,"",BetSize,"",Balance,"",RandomNumber)
        else :
            Balance = Balance - BetSize
            BetSize = BetSize * 1.65
            RollNumber = RollNumber + 1
            print (RollNumber,"",BetSize,"",Balance,"",RandomNumber)
    if Over == False :
        RandomNumber = random.randrange(0, 1000)
        if RandomNumber <= Bias :
            Balance = Balance + (BetSize * 2.2)
            BetSize = 1
            RollNumber = RollNumber + 1
            print (RollNumber,"",BetSize,"",Balance,"",RandomNumber)
        else :
            Balance = Balance - BetSize
            BetSize = BetSize * 1.65
            RollNumber = RollNumber + 1
            print (RollNumber,"",BetSize,"",Balance,"",RandomNumber)
    if RollNumber == 100000 or Balance <= 0:
        Broke = True