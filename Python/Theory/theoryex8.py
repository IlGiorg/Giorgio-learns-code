
A = [""] * 10   
L = 10
for c in range(L):
    A[c] = input("Please enter name: ")
for c in range(L):
    for l in range(0, 9):
        if A[l] > A[l + 1]:
            t = A[l]
            A[l] = A[l + 1]
            A[l + 1] = t
for c in range(L):
    print("Name", c + 1, "is", A[c])
