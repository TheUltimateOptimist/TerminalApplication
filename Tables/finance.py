from GAUD import get, add
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
        add.addIntern("transactions", ["transaction_medium", "transaction_reason", "transaction_classification",
                      "transaction_amount", "transaction_datetime"], [medium, reason, classification, amount, dateTime], showOperation)
        if sqloperation.__contains__("-r"):
            makeTransaction(showOperation, sqloperation, id)


def buy(showOperation, sqloperation):
    makeTransaction(showOperation, sqloperation, 0)


def sell(showOperation, sqloperation):
    makeTransaction(showOperation, sqloperation, 1)


def printBalance(balance, type):
    if balance == "None" or float(balance) >= 0:
        color.printGreen(f"Your {type} balance: {balance}")
    else:
        color.printRed(f"Your {type} balance: {balance}")


def getbalance(showOperation, sqloperation):
    s = "2.3"
    balance = float(sql.execute(
        "SELECT SUM(transaction_amount) FROM transactions", showOperation, "get")[0][0])
    printBalance(balance, "overall")
    print("")
    if sqloperation.__contains__("-sector"):
        cashBalance = sql.execute(
            "SELECT SUM(transaction_amount) FROM transactions WHERE transaction_medium = 'cash'", showOperation, "get")[0][0]
        debtBalance = sql.execute(
            "SELECT SUM(transaction_amount) FROM transactions WHERE transaction_medium = 'debt'", showOperation, "get")[0][0]
        bankBalance = sql.execute(
            "SELECT SUM(transaction_amount) FROM transactions WHERE transaction_medium = 'bank'", showOperation, "get")[0][0]
        printBalance(cashBalance, "cash")
        printBalance(debtBalance, "debt")
        printBalance(bankBalance, "bank")


def gettransactions(showOperation, sqloperation):
    if sqloperation.__contains__("-d"):
        days = int(input("how many days do you want to go back? "))
        dateTime = time.localtime(time.time() - 86400*days)
        dateTime = f"'{dateTime.tm_year}-{dateTime.tm_mon}-{dateTime.tm_mday} {dateTime.tm_hour}:{dateTime.tm_min}:{dateTime.tm_sec}'"
    else:
        dateTime = format.currentDateTime()
    table = get.getIntern(
        "transactions", ["all"], f"transaction_datetime > {dateTime}", showOperation)
    functions.printTable(table, ["all"], "blue", "cyan", "blue")
    balance = float(sql.execute(
        f"SELECT SUM(transaction_amount) FROM transactions WHERE transaction_datetime > {dateTime}", showOperation, "get")[0][0])
    printBalance(balance, "overall")
