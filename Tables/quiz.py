# this file contains the functions needed for my custom quizes

# third party imports:

# first party imports:
import sql
from GAUD import get, add, update
import color as c
import functions
import format


def lengthOfQuiz(quizId, showOperation):
    return int(get.getIntern("quizes", ["numberofquestions"], f"quiz_id = {quizId}", showOperation)[0][0])


def requestQuizId(showOperation):
    # get all quizes
    quizes = get.getIntern("quizes", [
                           "quiz_name", "quiz_learned", "quiz_numberofquestions"], "", showOperation)

    # print all quizes numbered
    functions.printTable(quizes, ["quiz_name", "quiz_learned", "quiz_numberofquestions"], "blue", [
                         "cyan"], "blue", showIndexes=True)
    # ask for desired quizNumber
    quizNumber = input("Enter the quiz number: ")
    # turn quiznumber into quizId
    if quizNumber != "":
        return int(get.getIntern("quizes", [
            "quiz_id", ], f"quiz_name = '{quizes[int(quizNumber ) - 1][0]}'", showOperation)[0][0])
    else:
        return 0


def requestQuestions():
    c.printBlue("Enter s to stop")
    frage = ""
    fragenAntwortListe = []
    while frage != "s":
        frage = input("Enter the question: ")
        if frage != "s":
            oneAnswer = input(
                "Enter 0 or 1 or 2 depending on whether there is only one correct answer: ")
            if(oneAnswer == "2"):
                antworten = []
                c.printBlue(
                    "start answer with 'correct' if it is the correct one")
                text = input("Enter next answer: ")
                while(text != "s"):
                    antworten.append(text)
                    text = input("Enter next answer: ")
                antwort = "--a--".join(antworten)
            else:
                antwort = input("Enter the answer: ")
            fragenAntwortListe.append([frage, antwort, oneAnswer])
    return fragenAntwortListe


def requestSpecificQuestionData(quizId, showOperation):
    questions = get.getIntern("questions", ["question_question", "question_answer", "question_classification",
                              "question_id"], f"question_quiz_id = {quizId} ORDER BY question_id", showOperation)
    print(questions)
    functions.printTable(questions, [
                         "question", "answer", "classification", "id"], "blue", ["cyan"], "blue", showIndexes=False)
    questionNumber = input("Select a number: ")
    return questions[int(questionNumber) - 1]


def saveQuestions(fragenAntwortListe, quizId, showOperation):
    for row in fragenAntwortListe:
        add.addIntern("questions", ["question_question", "question_answer", "question_classification", "question_quiz_id"], [
            row[0], row[1], int(row[2]), quizId], showOperation)


def saveQuiz(quizName, numberOfQuestions, showOperation):
    add.addIntern("quizes", ["quiz_name", "quiz_learned", "quiz_numberofquestions"], [
                  quizName, 0, numberOfQuestions], showOperation)


def addquiz(showOperation, sqloperation):
    quizName = input("Enter the quiz name: ")
    if quizName != "":
        fragenAntwortListe = requestQuestions()
        saveQuiz(quizName, len(fragenAntwortListe), showOperation)
        quizId = int(get.getIntern("quizes", [
                     "quiz_id"], f"quiz_name = '{quizName}' AND quiz_numberofquestions = {len(fragenAntwortListe)}", showOperation)[0][0])
        saveQuestions(fragenAntwortListe, quizId, showOperation)
        if sqloperation.__contains__("-r"):
            addquiz(showOperation, sqloperation)


def practicequiz(showOperation, sqloperation):
    quizId = requestQuizId(showOperation)
    if quizId != 0:
        start = format.currentDateTime()
        richtig = 0
        fragenAntwortListe = get.getIntern("questions", [
                                           "question_question", "question_answer", "question_classification", "question_id"], f"question_quiz_id = {quizId} ORDER BY question_id ASC", showOperation)
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
        c.printGreen(
            f"Du hast {richtig} von {len(fragenAntwortListe)} Fragen richtig beantwortet")
        if richtig == len(fragenAntwortListe):
            update.updateIntern("quizes", ["quiz_learned"], [
                                1], f"quiz_id = {quizId}", showOperation)
            c.printGreen("Congratulations, you got it!!")
        add.addIntern("quizing", ["quizing_datetime", "quizing_quiz_id", "quizing_correct"], [start, quizId,
                                                                                              richtig], showOperation)


def addquizquestions(showOperation, sqloperation):
    quizId = requestQuizId(showOperation)
    if quizId != 0:
        fragenAntwortListe = requestQuestions()
        saveQuestions(fragenAntwortListe, quizId, showOperation)
        sql.execute(
            f"UPDATE quizes set quiz_numberofquestions = {len(fragenAntwortListe) + lengthOfQuiz(quizId, showOperation)} WHERE quiz_id = {quizId}", showOperation, "post")


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
    sql.execute(
        f"DELETE FROM questions WHERE question_quiz_id = {quizId}", showOperation, "post")
    sql.execute(
        f"DELETE FROM quizes WHERE quiz_id = {quizId}", showOperation, "post")
