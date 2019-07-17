#This takes input in the form of key press and counts it in binary
i = 0
while True:
    msg = raw_input("Press a key to add one: \n")
    
    if (msg == "exit"):
        break
    
    if (i == 20):
        print("John")
    elif (i == 21):
        print ("Sucks")
        
    else:
        print(bin(i))
    i = i+1