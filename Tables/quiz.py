# this file contains the functions needed for my custom quizes

# third party imports:

# first party imports:
import sql
from GAUD import get, add, update
import color as c
import functions
import format

def addquiz(showOperation, sqloperation):
    quizName = input("Enter the quiz name: ")
    if quizName != "":
        fachgebiet = input("Enter the fachgebiet: ")
        c.printBlue("Enter s to stop")
        frage = ""
        fragenAntwortListe = []
        while frage != "s":
            frage = input("Enter the question: ")
            if frage != "s":
                oneAnswer = input("Enter 0 or 1 depending on whether there is only one correct answer: ")
                antwort = input("Enter the answer: ")
                fragenAntwortListe.append([frage, antwort, oneAnswer])
        add.addIntern("quiz", ["all except id"], [quizName, fachgebiet, 0, len(fragenAntwortListe)], showOperation, database="quizbase")
        quizId = int(get.getIntern("quiz", ["id"], f"name = '{quizName}'", showOperation, database="quizbase")[0][0])
        for row in fragenAntwortListe:
            add.addIntern("fragen", ["all except id"], [row[0], row[1], quizId, int(row[2])], showOperation, database="quizbase")
        if sqloperation.__contains__("-r"):
            addquiz(showOperation, sqloperation) 


def practicequiz(showOperation, sqloperation):
    quizes = get.getIntern("quiz", ["name", "fachgebiet", "gelernt", "fragenzahl"], "", showOperation, database="quizbase")
    functions.printTable(quizes, ["name", "fachgebiet", "gelernt", "fragenzahl"], "blue", ["cyan"], "blue", showIndexes=True)
    quizNumber = input("Enter the quiz number: ")
    if quizNumber != "":
        quizId = get.getIntern("quiz", ["id", ], f"name = '{quizes[int(quizNumber ) - 1][0]}'", showOperation, database="quizbase")[0][0]
        start = format.currentDateTime()
        richtig = 0
        fragenAntwortListe = get.getIntern("fragen", ["name", "antwort", "eine_antwort"], f"quiz_id = {quizId}", showOperation, database="quizbase")
        for row in fragenAntwortListe:
            c.printBlue(row[0])
            if int(row[2]) == 1:
                antwort = input("your precise answer: ")
                if antwort == row[1]:
                    c.printGreen("Correct!")
                    richtig = richtig + 1
                else: 
                    c.printRed("Wrong!")
                    c.printBlue("correct answer: ")
                    c.printBlue(row[1])
            else:
                antwort = input("your answer: ")
                c.printBlue("your answer: ")
                c.printBlue(antwort)
                print("")
                c.printBlue("desired answer: ")
                c.printBlue(row[1])
                correct = input("if correct enter y: ")
                if correct == "y":
                    richtig = richtig + 1
        end = format.currentDateTime()
        if richtig == len(fragenAntwortListe):
            update.updateIntern("quiz", ["gelernt"], [1], f"id = {quizId}", showOperation, database="quizbase")
        add.addIntern("quizing", ["all"], [start, end, quizId, str(richtig)], showOperation, database="quizbase")


def addquizquestion(showOperation, sqloperation):
    print("not yet defined")


def removequizquestion(showOperation, sqloperation):
    print("not yet defined")

def removequiz(showOperation, sqloperation):
    print("not yet defined")    
                        





        
    

               



