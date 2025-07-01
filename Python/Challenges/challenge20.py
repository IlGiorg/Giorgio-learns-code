# topack <- []
# tasks <- []
# INPUT Holiday where are you going?
# INPUT Numpack how many things are you packing?
# INPUT Tasksnum How many things do you need to do?
# FOR i IN Numpack
#   ADD topack INPUT How many things do you need 
# FOR i IN Tasksnum
#   ADD topack INPUT How many things do you need 
# FILENAME <- holiday + " checklist.txt"
# WITH open(FILENAME, ) as file:
#    WRITEFILE("Destination: " + holiday + "\n")
#   WRITEFILE("Packing List:\n")
#   for ITEM in topack:
#        WRITEFILE(item + "\n")
#    WRITEFILE("\nTask List:\n")
#    for task in tasks:
#        WRITEFILE(task + "\n")
# OUTPUT("Your list has been saved to", FILENAME)



topack = []
tasks = []

holiday = input("Where are you going? ")
numpack = int(input("How many things do you need to pack? "))
tasksnum = int(input("How many things do you need to do? "))

# Loop for packing items
for i in range(numpack):
    topack.append(input(f"What item do you need to bring? {i + 1}? "))

# Loop for tasks
for i in range(tasksnum):
    tasks.append(input(f"What task do you need to complete? {i + 1}? "))

# Save to file
file_name = holiday + " checklist.txt"
with open(file_name, "w") as file:
    file.write("Destination: " + holiday + "\n")
    file.write("Packing List:\n")
    for item in topack:
        file.write(item + "\n")
    
    file.write("\nTask List:\n")
    for task in tasks:
        file.write(task + "\n")

print("Your list has been saved to", file_name)
