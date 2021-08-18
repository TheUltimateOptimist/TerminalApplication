# file contains everything needed for visualizing something

# third party imports:

# first party imports:
import color as c

def visualizeList(numberList, largestLength = 20, axis = "vertical", color = "red"):
    largestNumber = 0
    for number in numberList:
        if number > largestNumber:
            largestNumber = number
    heights = []
    for number in numberList:
        heights.append(round((number/largestNumber)*largestLength))        
    if axis == "horizontal":        
        for height in heights:
            c.printColored("+" + height * 2* "-" + "+", color)
            c.printColored("|" + height*"  " + "|", color)
            c.printColored("+" + height * 2* "-" + "+", color)
    elif axis == "vertical":
        top = ""    
        for height in heights:
            if height == largestLength:
                top = top + "+-+ "
            else: 
                top = top + "    "  
        c.printColored(top, color)          
        for i in range(largestLength):
            s = ""
            for height in heights:
                if height == largestLength - i -1:
                    s = s + "+-+ "
                elif height >= largestLength - i:
                    s = s + "| | "
                else:
                    s = s + "    "
            c.printColored(s, color)     
        bottom = ""
        for _ in numberList:
            bottom = bottom + "+-+ "
        c.printColored(bottom,color)     


