# this file contains all functions that have to do with reading

# third party imports:
import time

# first party imports:
import sql
import color
import format


def addbook(showOperation, operation):
    if operation.__contains__("addbook") == False:
        title = operation
    else:
        title = input("title: ")
    author = input("author: ")
    topic = input("topic: ")
    pages = input("pages: ")
    sql.execute(
        f"INSERT INTO books(title, author, topic, page, pages) VALUES('{title}', '{author}', '{topic}', 1, {int(pages)})", showOperation, "post")
    if operation.__contains__("-r"):
        addbook(showOperation, operation)


def read(showOperation, operation):
    if operation.__contains__("read"):
        book = input("book title: ")
    else:
        book = operation
    if sql.valueExists(book, "books", "title"):
        duration = input("how many minutes: ")
        color.printGreen("Start Reading!")
        currentPage = str(sql.execute(
            f"SELECT page FROM books WHERE title = '{book}'", showOperation)[0][0])
        color.printGreen(f"you are at page {currentPage}")
        startTime = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        for i in range(int(duration)):
            color.printBlue(str(int(duration) - i) + " minutes left")
            time.sleep(60)
        color.printGreen("Reading Finished!")
        keepReading = input("keep reading? ")
        if keepReading == "y":
            start = time.time()
            _ = input("Press any key to stop: ")
            readingTime = time.time() - start + int(duration)*60
        else:
            readingTime = int(duration)*60
        nextPage = input("page to start next time: ")
        sql.execute(
            f"INSERT INTO reading VALUES('{startTime}', '{book}', {round(readingTime)})", showOperation, "post")
        sql.execute(
            f"UPDATE books SET page = {nextPage} WHERE title = '{book}'", showOperation, "post")
        sql.execute(f"UPDATE habits SET habits_count = habits_count + 1, habits_done = 'true' WHERE habits_name = 'reading for half an hour'", showOperation, "post")
    elif sql.valueExists(book, "books", "title") == False:
        color.printRed("ERROR: Book does not exist!")
        color.printBlue("a: add the book | e: enter new book")
        next = input("next:")
        if next == "a":
            addbook(showOperation, book)
            read(showOperation, book)
        elif next == "e":
            read(showOperation, "read")
