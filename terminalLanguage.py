# this file contains all terminal operations

# third party imports
import userHelp as h
from Tables import humans
from Tables import sleep, projects, pi, reading, quiz, finance
import sql
from Tables import tasks
from Tables import training, habits
from GAUD import get, add, update, delete
import pomodoro

# all operations:
allOperations = [h.lhelp, finance.gettransactions, finance.getbalance, finance.buy, finance.sell, pomodoro.pomodoro, quiz.editquiz, quiz.addquiz, quiz.practicequiz, quiz.removequizquestion, quiz.removequiz, humans.nget, humans.addhuman, sql.sql, sleep.frombed, sleep.tobed, humans.getgroup, sleep.sevendays, reading.read, reading.addbook,
                 humans.nextbirthday, update.updatecompletecolumn, add.addtable, delete.deletetable, add.addcolumn, training.addexercise, delete.deletecolumn, delete.deleterow,
                 get.getcolumnnames, training.addtrainingplan, training.train, training.getdevelopment, add.add, get.get, update.renamecolumn, habits.habits, tasks.tasks, projects.projects, pi.pi]

# all operation additions:
allAdditions = ["-s", "-h", "-r", "-n", "-d"]
