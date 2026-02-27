filepath = open("/Users/giorgio/Documents/GitHub/Giorgio-learns-code/GScript/test.gs","rt")
print(filepath.read())

file=filepath.read()
print(file)

function=filepath.read()[1:5]
print(function)