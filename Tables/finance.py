from GAUD import get,add
import format
import sql
import color
import time
import functions

def makeTransaction(showOperation, sqloperation, id):
    # id = 1 -> sell
    # id = 0 -> buy
    medium = input("cash, bank, or debt? ")
    if medium != "":
        reason = input("describe it: ")
        classification = input("food, subscription, goods or time? ")
        amount = input("How much is it? ")
        if sqloperation.__contains__("-old"):
            dateTime = f"'{input('When was the transaction made? ')}'"
        else:
            dateTime = format.currentDateTime()
        add.addIntern("transactions", ["all except id"], [medium, reason, classification, amount, dateTime], showOperation)
        if sqloperation.__contains__("-r"):
            makeTransaction(showOperation, sqloperation, id)


def buy(showOperation, sqloperation):
    makeTransaction(showOperation, sqloperation, 0)


def sell(showOperation, sqloperation):
    makeTransaction(showOperation, sqloperation, 1)    

def printBalance(balance, type):
    if balance >= 0:
        color.printGreen(f"Your {type} balance: {balance}")
    else:
        color.printRed(f"Your {type} balance: {balance}")    


def getbalance(showOperation, sqloperation):
    balance = sql.execute("SELECT SUM(transaction_amount) FROM transactions")[0][0]
    printBalance(sum, "overall")
    print("")
    if sqloperation.__contains__("-sector"):
        cashBalance = sql.execute("SELECT SUM(transaction_amount) FROM transactions WHERE transaction_medium = 'cash'")[0][0]
        debtBalance = sql.execute("SELECT SUM(transaction_amount) FROM transactions WHERE transaction_medium = 'debt'")
        bankBalance = sql.execute("SELECT SUM(transaction_amount) FROM transactions WHERE tansaction_medium = 'bank'")
        printBalance(cashBalance, "cash")
        printBalance(debtBalance, "debt")
        printBalance(bankBalance, "bank")


def gettransactions(showOperation, sqloperation):
    if sqloperation.__contains__("-d"):
        days = int(input("how many days do you want to go back? "))
        dateTime =  time.localtime(time.time() - 86400*days)
        dateTime = f"'{dateTime.tm_year}-{dateTime.tm_mon}-{dateTime.tm_mday} {dateTime.tm_hour}:{dateTime.tm_min}:{dateTime.tm_sec}'" 
    else:
        dateTime = format.currentDateTime()
    table = get.getIntern("transactions", ["all"], f"transaction_datetime > {dateTime}", showOperation)
    functions.printTable(table, ["all"], "blue", "cyan", "blue")
    balance = sql.execute(f"SELECT SUM(transaction_amount) FROM transactions WHERE transaction_datetime > {dateTime}")[0][0]
    printBalance(balance, "overall")
              



        





        

