#       Team 14 - Tournament Gui


import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidgetItem, QTableWidget, QMessageBox
from random import shuffle


class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("HomeScreen.ui", self)
        self.teamsTable.setColumnWidth(0, 600)
        self.teamsTable.setColumnWidth(1, 210)
        self.insertTeamButton.clicked.connect(self.insert)
        self.autofillButton.clicked.connect(self.autofillData)
        self.team_dict = []
        self.initTeams = [{'name': 'Brazil', 'rank': 1}, {'name': 'Belgium', 'rank': 2},
                          {'name': 'Argentina', 'rank': 3}, {'name': 'France', 'rank': 4},
                          {'name': 'England', 'rank': 5}, {'name': 'Spain', 'rank': 7},
                          {'name': 'Netherlands', 'rank': 8}, {'name': 'Portugal', 'rank': 9},
                          {'name': 'Denmark', 'rank': 10}, {'name': 'Germany', 'rank': 11},
                          {'name': 'Croatia', 'rank': 12}, {'name': 'Mexico', 'rank': 13},
                          {'name': 'Uruguay', 'rank': 14}, {'name': 'Switzerland', 'rank': 15},
                          {'name': 'USA', 'rank': 16}, {'name': 'Senegal', 'rank': 18},
                          {'name': 'Wales', 'rank': 19}, {'name': 'Iran', 'rank': 20},
                          {'name': 'Serbia', 'rank': 21}, {'name': 'Morocco', 'rank': 22},
                          {'name': 'Japan', 'rank': 24}, {'name': 'Poland', 'rank': 26},
                          {'name': 'South Korea', 'rank': 28}, {'name': 'Tunisia', 'rank': 30},
                          {'name': 'Costa Rica', 'rank': 31}, {'name': 'Australia', 'rank': 38},
                          {'name': 'Canada', 'rank': 41}, {'name': 'Cameroon', 'rank': 43},
                          {'name': 'Ecuador', 'rank': 44}, {'name': 'Qatar', 'rank': 50},
                          {'name': 'Ghana', 'rank': 61}, {'name': 'Saudi Arabia', 'rank': 51}]
        self.teams = []
        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.tier4 = []
        self.next_btn = False
        self.row = 0
        self.createGroupsButton.clicked.connect(self.gotosort)
        self.nextButton.clicked.connect(self.gotoGroupPage)

    # insert data into list and dictionary
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
                    int_rank = int(rank)
                    self.teamError.setText('')
                    self.team_dict += [{"name": name, "rank": rank}]
                    self.teams += [[name, 0, int_rank]]
                    self.loadData()
                else:
                    self.teamError.setText('rank must be integer')

    # load date into the GUI table
    def loadData(self):
        if self.row < 32:
            curr = self.row + 1
            self.teamsTable.setRowCount(curr)
            self.teamsTable.setItem(self.row, 0, QtWidgets.QTableWidgetItem(self.team_dict[self.row]['name']))
            self.teamsTable.setItem(self.row, 1, QtWidgets.QTableWidgetItem(self.team_dict[self.row]['rank']))
            self.row = curr

    # insert predefined into the list and loading it into the GUI table
    def autofillData(self):
        self.teamsTable.setRowCount(32)
        for i in range(self.row, 32):
            self.teamsTable.setItem(i, 0, QtWidgets.QTableWidgetItem(self.initTeams[i]['name']))
            self.teamsTable.setItem(i, 1, QtWidgets.QTableWidgetItem(str(self.initTeams[i]['rank'])))
            self.teams += [[self.initTeams[i]['name'], 0, self.initTeams[i]['rank']]]
        self.row = 32

    # sorting the list : 'teams' and redirecting into the Groups GUI
    def gotosort(self):
        if self.row < 32:
            self.groupError.setText('Please enter all teams first')
        else:
            self.teams.sort(key=lambda x: x[2])  # sorting the list depending on its 3rd element (rank)
            self.showWarning()
            self.groupError.setText('')

    # Creates a group object
    def createGroups(self):
        if self.next_btn:
            widget.removeWidget(widget.widget(1))
        self.next_btn = True
        groups = GroupStage()
        groups.teams = self.teams
        groups.createTiers()
        widget.addWidget(groups)

    # show warning before creating data
    def showWarning(self):
        msg = QMessageBox()
        msg.setWindowTitle('Warning!!')
        msg.setText('All the previous data will be lost!')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setEscapeButton(QMessageBox.Cancel)
        msg.setInformativeText('Would you like to continue ?!')
        msg.buttonClicked.connect(self.popup_button)
        if self.next_btn:
            x = msg.exec_()
        else :
            self.createGroups()

    # Pop up window's Action if 'yes' was pressed
    def popup_button(self, i):
        if i.text() == '&Yes':
            self.createGroups()

    # Back to home page
    def gotoGroupPage(self):
        if not self.next_btn:
            self.groupError.setText('Please create groups first')
        else:
            widget.setCurrentIndex(widget.currentIndex() + 1)
            self.groupError.setText('')


# GroupStageUi class
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

        # button to back to the homepage
        self.backButton.clicked.connect(self.goback)

    # input : team list
    # output : slice the team list, then shuffle it and append it into one suitable list
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
        print(self.teamTables)
        self.insetTables()

    # a function to automatically insert data into the group tables
    def insetTables(self):
        row_index = 0
        for tiers in self.teamTables:
            for team, tables in zip(tiers, self.GroupsWidget.findChildren(QTableWidget)):
                tables.setRowCount(tables.rowCount() + 1)
                col_index = 0
                for info in team[:2]:
                    item = QTableWidgetItem(str(info))
                    tables.setItem(row_index, col_index, item)
                    col_index += 1
            row_index += 1

    # go back to home page (stack widget)
    def goback(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)


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
