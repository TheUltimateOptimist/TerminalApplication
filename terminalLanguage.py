# this file contains all terminal operations

# third party imports
import userHelp as h
from Tables import humans
from Tables import sleep
import sql
from Tables import tasks
from Tables import training
from GAUD import get, add, update, delete

# all operations:
allOperations = [h.lhelp, humans.nget, humans.addhuman, sql.sql, sleep.frombed, sleep.tobed, humans.getgroup, sleep.sevendays,
                 humans.nextbirthday, update.updatecompletecolumn, add.addtable, delete.deletetable, add.addcolumn, delete.deletecolumn, delete.deleterow,
                 get.getcolumnnames, add.add, tasks.gettasks, get.get, update.renamecolumn, tasks.addtask, tasks.taskdone]

# all operation additions:
allAdditions = ["-s", "-h", "-r", "-n", "-d"]