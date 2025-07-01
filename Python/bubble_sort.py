# Giorgio Valdman - Computer Science  - 21/05/2025

# It shows number smallest to largest

# Original List
numbers=[5, 3, 8, 4, 2]
# index=[0, 1, 2, 3, 4]

print("Original List: " , numbers) # Prints the original list, unsorted

# Bubble Sort Algorythm

n =len(numbers) # Gets the lenght of the list

for i in range(n-1): # Loop through the list n-1 times because of the index position 
    
    # Inner loop for pairwise comparison
    for j in range(n-1-i):
        if numbers[j] > numbers[j+1]: 
            
            # Swap if the current number is bigger than the next
            numbers[j], numbers[j+1] = numbers[j+1],numbers[j]
        print(f"After pass {i+1}: {numbers}")

print("Sorted List: " , numbers) # Prints the sorted list