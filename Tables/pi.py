# this file contains enerything that has to do with the number pi

# third party imports:
# first party imports:
import color
from GAUD import get

numberPi = "31415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679821480865132823066470938446095505822317253594081284811174502841027019385211055596446229489549303819644288109756659334461284756482337867831652712019091456485669234603486104543266482133936072602491412737245870066063155881748815209209628292540917153643678925903600113305305488204665213841469519415116094330572703657595919530921861173819326117931051185480744623799627495673518857527248912279381830119491298336733624406566430860213949463952247371907021798609437027705392171762931767523846748184676694051320005681271452635608277857713427577896091736371787214684409012249534301465495853710507922796892589235420199561121290219608640344181598136297747713099605187072113499999983729780499510597317328160963185950244594553469083026425223082533446850352619311881710100031378387528865875332083814206171776691473035982534904287554687311595628638823537875937519577818577805321712268066130019278766111959092164201989"
def pi(showOperation, operation):
    color.printBlue("l: learn | t: test")
    next = input("next: ")
    if next == "l":
        start = input("number of decimal place to start at: ")
        ready = ""
        i = int(start)
        while ready == "":
            print(f"{i}:")
            color.printMagenta(f"{numberPi[i]} {get.getIntern('numbers_pictures', ['picture'], f'number = {numberPi[i]}', showOperation)[0][0]}")
            i += 1
            ready = input("ready? ")
        pi(showOperation, operation)    
    elif next == "t":
        start = int(input("number of decimal place to start at: ")) 
        numbers = int(input("to which decimal place? "))
        for i in range(start, numbers + 1):
            number = input(f"{i} Enter number: ")
            if number == numberPi[i]:
                color.printGreen("Correct")
            else:
                while number != numberPi[i]:
                    color.printRed("Wrong")
                    number = input(f"{i} Enter number: ")
                color.printGreen("Correct")  
        pi(showOperation, operation)          

