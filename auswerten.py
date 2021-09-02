file = open("text.txt", "r")
s = "".join(file.read()).split("\n")
for element in s:
    print(element)
