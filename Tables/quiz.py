# this file contains the functions needed for my custom quizes

# third party imports:

# first party imports:
import sql
from GAUD import get, add, update
import color as c
import functions
import format


def testFunction(testString):
    testList = testString.split(';')
    file = open("test_function.py", "w")
    file.write(
        "from write_function import function\nfrom color import coloredText, printGreen, printRed\n")
    file.close()
    file = open("test_function.py", "a")
    file.write("def test():\n")
    file.write(f"   tests = {len(testList)}\n   passedTests = 0\n")
    for specificTest in testList:
        testData = specificTest.split(": ")
        file.write(
            f"   if {testData[0]} == {testData[1]}:\n      passedTests+=1\n")
    file.write(
        "   if passedTests >= tests:\n      printGreen('all tests passed')\n      return True\n   else:\n      printRed(f'{passedTests} of {tests} tests passed')\n      return False")
    file.close()
    from test_function import test
    return test()


def updateQuizLength(quizId, showOperation):
    length = int(sql.execute(
        f"SELECT count(*) FROM questions WHERE question_quiz_id = {quizId}", showOperation, "get")[0][0])
    sql.execute(
        f"UPDATE quizes set quiz_numberofquestions = {length} WHERE quiz_id = {quizId}", showOperation, "post")


def requestQuizId(showOperation):
    # get all quizes
    quizes = get.getIntern("quizes", [
                           "quiz_name", "quiz_learned", "quiz_numberofquestions", "quiz_duration"], "", showOperation)
    for i, row in enumerate(quizes):
        if row[3] != "None":
            quizes[i][3] = format.secondsToHourMinuteFormat(int(row[3]))
    # print all quizes numbered
    functions.printTable(quizes, ["quiz_name", "quiz_learned", "quiz_numberofquestions", "quiz_duration"], "blue", [
                         "cyan"], "blue", showIndexes=True)
    # ask for desired quizNumber
    quizNumber = input("Enter the quiz number: ")
    # turn quiznumber into quizId
    if quizNumber != "":
        return int(get.getIntern("quizes", [
            "quiz_id", ], f"quiz_name = '{quizes[int(quizNumber ) - 1][0]}'", showOperation)[0][0])
    else:
        return 0


def requestQuiz(quizId, showOperation):
    """
    asks user for specific quiz\n
    returns all questions of that quiz\n
    in form of a list\n
    index 0: question text\n
    index 1: question answer\n
    index 2: question classification\n
    index 3: question id
    """
    result = get.getIntern("questions", [
        "question_question", "question_answer", "question_classification", "question_id"], f"question_quiz_id = {quizId} ORDER BY question_id ASC", showOperation)
    return result


def requestQuestions(quizId, showOperation):
    c.printBlue("Enter s to stop")
    frage = ""
    fragenAntwortListe = []
    while frage != "s":
        frage = input("Enter the question: ")
        if frage != "s":
            oneAnswer = input(
                "Enter 0 or 1 or 2 or 3 depending on whether there is only one correct answer: ")
            if oneAnswer == "2":
                antworten = []
                c.printBlue(
                    "start answer with 'correct' if it is the correct one")
                text = input("Enter next answer: ")
                while(text != "s"):
                    antworten.append(text)
                    text = input("Enter next answer: ")
                antwort = "--a--".join(antworten)
            elif oneAnswer == 3:
                antwort = input("Enter the tests: ")
            else:
                antwort = input("Enter the answer: ")
            saveQuestion([frage, antwort, oneAnswer], quizId, showOperation)
    return fragenAntwortListe


def requestSpecificQuestionData(quizId, showOperation):
    questions = get.getIntern("questions", ["question_question", "question_answer", "question_classification",
                              "question_id"], f"question_quiz_id = {quizId} ORDER BY question_id", showOperation)
    functions.printTable(questions, [
                         "question", "answer", "classification", "id"], "blue", ["cyan"], "blue", showIndexes=False)
    questionNumber = input("Select a number: ")
    return questions[int(questionNumber) - 1]


def saveQuestion(fragenAntwortListe, quizId, showOperation):
    add.addIntern("questions", ["question_question", "question_answer", "question_classification", "question_quiz_id"], [
        fragenAntwortListe[0], fragenAntwortListe[1], int(fragenAntwortListe[2]), quizId], showOperation)


def saveQuiz(quizName, showOperation):
    add.addIntern("quizes", ["quiz_name", "quiz_learned", "quiz_numberofquestions"], [
                  quizName, 0, 0], showOperation)


def deleteTextFileContent(filename):
    file = open(filename, "w")
    file.write("")
    file.close()


def writeQuiz(quizId, showOperation):
    questions = requestQuiz(quizId, showOperation)
    deleteTextFileContent("quiz.txt")
    file = open("quiz.txt", "a", encoding="utf-8")
    for question in questions:
        file.write(f"qq-{str(question[2])}: {str(question[0])}\n")
        for answer in question[1].split('--a--'):
            file.write(str(answer) + "\n")
        file.write("\n")
    file.close()


def quizDateiAuswerten(quizId, showOperation, questionsExist=False):
    if questionsExist:
        maxId = sql.execute(
            f"SELECT MAX(question_id) FROM questions WHERE question_quiz_id = {quizId}", showOperation, "get")[0][0]
    print("Saving...")
    with open("quiz.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    fragenAntwortListe = []
    answers = []
    numberOfQuestions = 0
    print(lines)
    for line in lines:
        print(line)
        print("list: " + str(fragenAntwortListe))
        if line.split("-")[0] == "qq":
            fragenAntwortListe.append(
                (line.split(": ", maxsplit=1)[1]).split("\n")[0])
            fragenAntwortListe.append(line.split("-")[1].split(":")[0])
        elif line != "\n" and line != "end\n" and line != "end":
            answers.append(line.split("\n")[0])
        else:
            if len(fragenAntwortListe) == 2:
                fragenAntwortListe.insert(1, "--a--".join(answers))
                saveQuestion(fragenAntwortListe, quizId, showOperation)
                numberOfQuestions += 1
                fragenAntwortListe = []
                answers = []
    if questionsExist:
        sql.execute(
            f"Delete from questions WHERE question_id <= {maxId} and question_quiz_id = {quizId}", showOperation, "post")
    sql.execute(
        f"UPDATE quizes SET quiz_numberofquestions = {numberOfQuestions} WHERE quiz_id = {quizId}", showOperation, "post")
    c.printGreen("Saved")


def addquiz(showOperation, sqloperation):
    quizName = input("Enter the quiz name: ")
    if quizName != "":
        saveQuiz(quizName, showOperation)
        quizId = int(get.getIntern("quizes", [
                     "quiz_id"], f"quiz_name = '{quizName}'", showOperation)[0][0])
        # requestQuestions(quizId, showOperation)
        deleteTextFileContent("quiz.txt")
        import os
        os.system("notepad quiz.txt")
        s = input("to save questions enter y: ")
        if s == "y":
            quizDateiAuswerten(quizId, showOperation)
        if sqloperation.__contains__("-r"):
            addquiz(showOperation, sqloperation)


def practicequiz(showOperation, sqloperation):
    quizId = requestQuizId(showOperation)
    if quizId > 0:
        fragenAntwortListe = requestQuiz(quizId, showOperation)
        import time
        start = time.time()
        richtig = 0
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
            elif int(row[2]) == 0:
                antwort = input("your answer: ")
                c.printBlue("your answer: ")
                c.printBlue(antwort)
                print("")
                c.printBlue("desired answer: ")
                c.printBlue(row[1])
                correct = input("if correct enter y: ")
                if correct == "y":
                    richtig = richtig + 1
            elif int(row[2]) == 2:
                answers = row[1].split("--a--")
                for i, answer in enumerate(answers):
                    if(answer.__contains__("correct ")):
                        answer = answer.split("correct ")[1]
                        correctNumber = i + 1
                    c.printBlue(str(i + 1) + f". {answer}")
                    print("")
                enteredNumber = input("Enter correct answer: ")
                if int(enteredNumber) == correctNumber:
                    c.printGreen("Correct")
                    richtig = richtig + 1
                else:
                    c.printRed(f"Wrong: {correctNumber} is correct")
            elif int(row[2]) == 3:
                with open("write_function.py", "w", encoding="utf8") as file:
                    file.write(f"# {row[0]}\ndef function():")
                import os
                os.system("notepad write_function.py")
                s = input("If done enter anything to continue! ")
                if testFunction(row[1]):
                    richtig = richtig + 1
        c.printGreen(
            f"Du hast {richtig} von {len(fragenAntwortListe)} Fragen richtig beantwortet")
        if richtig == len(fragenAntwortListe):
            update.updateIntern("quizes", ["quiz_learned"], [
                                1], f"quiz_id = {quizId}", showOperation)
            c.printGreen("Congratulations, you got it!!")
        add.addIntern("quizing", ["quizing_datetime", "quizing_quiz_id", "quizing_correct", "quizing_duration"], [format.toDateTime(start), quizId,
                                                                                                                  richtig, round(time.time() - start)], showOperation)
        update.updateIntern("quizes", ["quiz_duration"], [
                            round(time.time() - start)], f"quiz_id = {quizId}", showOperation)
        if sqloperation.__contains__("-r"):
            practicequiz(showOperation, sqloperation)


def editquiz(showOperation, sqloperation):
    quizId = requestQuizId(showOperation)
    if quizId != 0:
        writeQuiz(quizId, showOperation)
        import os
        os.system("notepad quiz.txt")
        s = input("save Changes? (y = yes, n = no) ")
        if s == "y":
            quizDateiAuswerten(quizId, showOperation, True)
        if sqloperation.__contains__("-r"):
            editquiz(showOperation, sqloperation)


def removequizquestion(showOperation, sqloperation):
    quizId = requestQuizId(showOperation)
    if quizId != 0:
        questionData = requestSpecificQuestionData(quizId, showOperation)
        sql.execute(
            f"DELETE FROM questions WHERE question_id = {questionData[3]}", showOperation, "post")
        if(sqloperation.__contains__("-r")):
            removequizquestion(showOperation, sqloperation)


def removequiz(showOperation, sqloperation):
    quizId = requestQuizId(showOperation)
    if quizId != 0:
        sql.execute(
            f"DELETE FROM questions WHERE question_quiz_id = {quizId}", showOperation, "post")
        sql.execute(
            f"DELETE FROM quizes WHERE quiz_id = {quizId}", showOperation, "post")
        if sqloperation.__contains__("-r"):
            removequiz(showOperation, sqloperation)
