import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from random import shuffle
from random import randint

class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("HomeScreen.ui", self)
        self.teamsTable.setColumnWidth(0, 600)
        self.teamsTable.setColumnWidth(1, 210)
        self.insertTeamButton.clicked.connect(self.insert)
        self.team_dict = []
        self.teams = []
        self.ranks = []
        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.tier4 = []

        self.row = 0
        self.createGroupsButton.clicked.connect(self.gotosort)

    def insert(self):
        name = self.teamNameField.text()
        rank = self.teamRankField.text()
        self.teamNameField.setText('')
        self.teamRankField.setText('')
        if len(name) == 0 or len(rank) == 0:
            self.teamError.setText('Please enter all the fields')
        else:
            if self.row == 32:
                self.teamError.setText('the list is Full')
            else:
                if rank.isdigit():
                    intRank = int(rank)
                    self.ranks += [intRank]
                    self.teamError.setText('')
                    self.team_dict += [{"name": name, "rank": rank}]
                    self.teams += [[name]]
                    self.loadData()
                else:
                    self.teamError.setText('rank must be integer')

    def loadData(self):
        if self.row < 32:
            curr = self.row + 1
            self.teamsTable.setRowCount(curr)
            self.teamsTable.setItem(self.row, 0, QtWidgets.QTableWidgetItem(self.team_dict[self.row]['name']))
            self.teamsTable.setItem(self.row, 1, QtWidgets.QTableWidgetItem(self.team_dict[self.row]['rank']))
            self.row = curr

    def gotosort(self):
        if self.row < 4:    # edit it later to 32
            self.groupError.setText('Please enter all teams first')
        else:
            self.sortTeams(self.ranks, self.teams)
            self.gotoGroups()

    def sortTeams(self, array1, array2):
        size = len(array1)
        for ind in range(size):
            min_index = ind

            for j in range(ind + 1, size):
                # select the minimum element in every iteration
                if array1[j] < array1[min_index]:
                    min_index = j
            # swapping the elements to sort the array
            (array1[ind], array1[min_index]) = (array1[min_index], array1[ind])
            (array2[ind], array2[min_index]) = (array2[min_index], array2[ind])

    def gotoGroups(self):
        groups = GroupStage()
        groups.teams = self.teams
        groups.createTiers()
        print('tiers created')################
        print(self.teams)
        groups.insertTables()
        print('table inserted')########################
        widget.addWidget(groups)
        widget.setCurrentIndex(widget.currentIndex()+1)


class GroupStage(QDialog):
    def __init__(self):
        super(GroupStage, self).__init__()
        loadUi('GroupStage.ui', self)
        self.teams = []
        self.teamTables = []
        self.teamPoints = []
        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.tier4 = []

    def createTiers(self):
        self.tier1 = self.teams[0:8]
        self.tier2 = self.teams[8:16]
        self.tier3 = self.teams[16:24]
        self.tier4 = self.teams[24:]
        shuffle(self.tier1)
        shuffle(self.tier2)
        shuffle(self.tier3)
        shuffle(self.tier4)
        self.teamTables.append(self.tier1)
        self.teamTables.append(self.tier2)
        self.teamTables.append(self.tier3)
        self.teamTables.append(self.tier4)

    def insertTables(self):
        print('we came here') ##########################
        for i in range(4):
            self.TableA.setRowCount(i+1)
            self.TableB.setRowCount(i+1)
            self.TableC.setRowCount(i+1)
            self.TableD.setRowCount(i+1)
            self.TableE.setRowCount(i+1)
            self.TableF.setRowCount(i+1)
            self.TableG.setRowCount(i+1)
            self.TableH.setRowCount(i+1)
            self.TableA.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][0][0]))
            self.TableA.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))
            self.TableB.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][1][0]))
            self.TableB.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))
            self.TableC.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][2][0]))
            self.TableC.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))
            self.TableD.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][3][0]))
            self.TableD.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))
            self.TableE.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][4][0]))
            self.TableE.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))
            self.TableF.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][5][0]))
            self.TableF.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))
            self.TableG.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][6][0]))
            self.TableG.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))
            self.TableH.setItem(i, 0, QtWidgets.QTableWidgetItem(self.teamTables[i][7][0]))
            self.TableH.setItem(i, 1, QtWidgets.QTableWidgetItem(str(0)))



# Main
app = QApplication(sys.argv)
mainWindow = HomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedHeight(860)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
