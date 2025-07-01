# Machine Learning

people= int(0)
cat=int(0)
dog=int(0)
pig=int(0)

while people<14:
    question=input("Cat or Dog? ").lower()

    if question=="cat":
        cat=cat+1
        people=people+1;
    
    elif question=="dog":
        dog=dog+1
        people=people+1
    elif question=="pig":
        pig=pig+1
        people=people+1

    else: print("Error")
    
if cat>dog:
    print("Cat is better!")
elif cat<dog:
    print("Dogs are better")
elif pig>cat:
    print("Pigs are better")
elif pig>dog:
    print("Pigs are better")
        
