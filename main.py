#       Team 14 - Tournament Gui


import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QTableWidgetItem, QTableWidget, QMessageBox, QFrame, \
    QSizePolicy, QLabel, QLineEdit, QVBoxLayout
from random import shuffle
from random import randint


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
        self.gotoGroupPage()

    # Creates a group object
    def createGroups(self):
        if self.next_btn:
            widget.removeWidget(widget.widget(1))
        self.next_btn = True
        groups = GroupStage()
        groups.teams = self.teams
        for team in groups.teams:
            team[1] = 0
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
        else:
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
        self.teams = []  # list with the 32 teams will be using it for making tiers
        self.groups_teams = []  # a temporary list help to slice the games of each group separately
        self.games_result = []  # 96 elements (game) each element has 2 value (team1 points - team2 points)
        self.tier1 = []  # temp list to have the first tier shuffled
        self.tier2 = []  # temp list to have the second tier shuffled
        self.tier3 = []  # temp list to have the third tier shuffled
        self.tier4 = []  # temp list to have the fourth tier shuffled
        self.round16_matches = []
        self.flag = True         # a flag to check if we need to create round 16 or just edit it
        self.sorted_groups = []  # group based list (8 groups) each group has 4 teams (sorted)
        self.qualified_teams = []
        self.backButton.clicked.connect(self.goback)        # button to back to the homepage
        self.Groups.setCurrentIndex(0)  # setting the group tab to be default
        self.matches = 0  # counter for the matches (used for naming frames of every game)
        self.saveButton.clicked.connect(self.clearPoints)  # save data button
        self.qualifiedButton.clicked.connect(self.qualifiedTeams)       # round 16 button

    # input : team list
    # output : slice the team list, then shuffle it and append it into one suitable list --->(createGroupTeams)
    def createTiers(self):
        self.tier1 = self.teams[0:8]
        self.tier2 = self.teams[8:16]
        self.tier3 = self.teams[16:24]
        self.tier4 = self.teams[24:]
        shuffle(self.tier1)
        shuffle(self.tier2)
        shuffle(self.tier3)
        shuffle(self.tier4)
        self.createGroupTeams()

    # a function to automatically insert data into the group tables
    def insertTables(self):
        for grp, tables in zip(self.sorted_groups, self.GroupsWidget.findChildren(QTableWidget)):
            row_index = 0
            for team in grp:
                if tables.rowCount() < 4:
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

    # create a list of group teams with 0 points --->(insertTables & groupGames)
    def createGroupTeams(self):
        for i in range(8):
            self.sorted_groups += [[self.tier1[i], self.tier2[i], self.tier3[i], self.tier4[i]]]
        self.insertTables()
        self.groupGames()

    # sorting each group in descending order (points) ---> (insertTables)
    def sortGroups(self):
        for grp in self.sorted_groups:
            grp.sort(reverse=True, key=lambda x: int(x[1]))
        self.insertTables()

    # updates [overwrites] (games_result) list depending on matches results (group_games) ---> (updatePoints)
    def gameResult(self):
        self.games_result = []
        for match in self.groups_teams:
            points1 = 0
            points2 = 0
            if int(match[1]) > int(match[3]):
                points1 += 3
            elif int(match[3]) > int(match[1]):
                points2 += 3
            else:
                points1 += 1
                points2 += 1
            self.games_result += [[points1, points2]]
        self.updatePoints()

    # create a 96-element list each representing a match
    def groupGames(self):
        for i in range(8):
            for j in range(4):
                for k in range(4):
                    if k != j:
                        team1 = self.sorted_groups[i][j][0]
                        team2 = self.sorted_groups[i][k][0]
                        self.groups_teams += [[team1, '0', team2, '0']]
        self.showMatchHistory()

    # update points list to be used in filling the group table's data  ---> (sortGroups)
    def updatePoints(self):
        self.sortAfterClear()
        game_counter = 0  # starts at game 0 , ends at game 96 (to iterate the games result list)
        for i in range(8):
            for j in range(4):
                for k in range(4):
                    if k != j:
                        # adding point1 to team 1
                        self.sorted_groups[i][j][1] = str(int(self.sorted_groups[i][j][1]) +
                                                          self.games_result[game_counter][0])
                        # adding point2 to team 2
                        self.sorted_groups[i][k][1] = str(int(self.sorted_groups[i][k][1]) +
                                                          self.games_result[game_counter][1])
                        game_counter += 1
        self.sortGroups()

    # create new matches (without scores) just Initialising using (createFrame)
    def showMatchHistory(self):
        for match in self.groups_teams:
            # self.createFrame(match[0], match[2], str(match[1]), str(match[3]))
            self.createFrame(match[0], match[2])

    # clear points ---> (sortAfterClear)
    def clearPoints(self):
        for grp in self.sorted_groups:
            for team in grp:
                team[1] = '0'
        self.sortAfterClear()
        self.loadScores()

    # getting teams in it is first order to keep having the same matches
    def sortAfterClear(self):
        for grp in self.sorted_groups:
            grp.sort(key=lambda x: int(x[2]))

    # selection
    def qualifiedTeams(self):
        self.qualified_teams = []
        self.round16_matches = []
        for grp in self.sorted_groups:
            for team in grp[:2]:
                self.qualified_teams += [team]
        for i in range(0, len(self.qualified_teams), 4):
            self.round16_matches += [[self.qualified_teams[i], self.qualified_teams[i+3]]]
            self.round16_matches += [[self.qualified_teams[i+1], self.qualified_teams[i+2]]]
        print("round 16 matches: ", self.round16_matches)
        self.editRound16()

    # loading score from the gui into the (groups_teams) list ----> (gameResult)
    def loadScores(self):
        counter = 0
        semiCounter = 0
        for lineEdit in self.MatchesWidget.findChildren(QLineEdit):
            if counter % 2 == 0:
                if lineEdit.text().isdigit():
                    self.groups_teams[semiCounter][1] = lineEdit.text()
                else:
                    rand = randint(0, 5)
                    self.groups_teams[semiCounter][1] = str(rand)
                    lineEdit.setText(str(rand))
                counter += 1
            else:
                if lineEdit.text().isdigit():
                    self.groups_teams[semiCounter][3] = lineEdit.text()
                else:
                    rand = randint(0, 5)
                    self.groups_teams[semiCounter][3] = str(rand)
                    lineEdit.setText(str(rand))
                counter += 1
                semiCounter += 1
        self.gameResult()

    # creating gui frame for 1 match
    def createFrame(self, team1, team2, score1='-', score2='-'):
        frame_name = 'Match_' + str(self.matches)
        self.matches += 1
        self.frame = QFrame(self.scrollAreaWidgetContents)
        self.frame.setObjectName(frame_name)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMinimumSize(QSize(100, 65))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.team1 = QLabel(self.frame)
        self.team1.setObjectName(u"team1")
        self.team1.setGeometry(QRect(40, 10, 351, 41))
        self.team1.setStyleSheet(u"font: 75 12pt \"Unispace\";\n"
                                 "color:rgb(255, 255, 255);\n"
                                 "")
        self.team1.setAlignment(Qt.AlignCenter)
        self.team1.setText(f'(H) {team1}')
        self.team2 = QLabel(self.frame)
        self.team2.setObjectName(u"team2")
        self.team2.setGeometry(QRect(680, 10, 351, 41))
        self.team2.setStyleSheet(u"font: 75 12pt \"Unispace\";\n"
                                 "color:rgb(255, 255, 255);\n"
                                 "")
        self.team2.setAlignment(Qt.AlignCenter)
        self.team2.setText(f'{team2} (A)')
        self.label_17 = QLabel(self.frame)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(480, 10, 111, 41))
        self.label_17.setStyleSheet(u"font: 75 12pt \"Unispace\";\n"
                                    "color:rgb(255, 255, 255);\n"
                                    "")
        self.label_17.setAlignment(Qt.AlignCenter)
        self.label_17.setText('VS')
        self.team1_score = QLineEdit(self.frame)
        self.team1_score.setObjectName(u"team1_score")
        self.team1_score.setGeometry(QRect(390, 10, 91, 41))
        self.team1_score.setStyleSheet(u"QLineEdit{\n"
                                       "background: #F8EAFF;\n"
                                       "border: 2px solid #803CE0;\n"
                                       "border-radius: 10px;\n"
                                       "color:#803CE0;\n"
                                       "font-family: Arial;\n"
                                       "font: 11pt;\n"
                                       "}\n"
                                       "QLineEdit:focus{\n"
                                       "border: 2px solid #FBAD25;\n"
                                       "}")
        self.team1_score.setText(score1)
        self.team1_score.setAlignment(Qt.AlignCenter)
        self.team2_score = QLineEdit(self.frame)
        self.team2_score.setObjectName(u"team2_score")
        self.team2_score.setGeometry(QRect(590, 10, 91, 41))
        self.team2_score.setStyleSheet(u"QLineEdit{\n"
                                       "background: #F8EAFF;\n"
                                       "border: 2px solid #803CE0;\n"
                                       "border-radius: 10px;\n"
                                       "color:#803CE0;\n"
                                       "font-family: Arial;\n"
                                       "font: 11pt;\n"
                                       "}\n"
                                       "QLineEdit:focus{\n"
                                       "border: 2px solid #FBAD25;\n"
                                       "}")
        self.team2_score.setText(score2)
        self.team2_score.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.frame)
        self.verticalLayout_4.setSpacing(50)
    
    # just editing the round 16 frames
    def editRound16(self):
        if self.flag:
            self.createRound16()
            self.flag = False
        else:
            j = 0
            for i in range(0, len(self.round16Widget.findChildren(QFrame)), 4):
                self.round16Widget.findChildren(QFrame)[i+1].setText(str(self.round16_matches[j][0][0]))
                self.round16Widget.findChildren(QFrame)[i+2].setText(str(self.round16_matches[j][1][0]))
                j += 1

    def createRound16(self):
        for match in self.round16_matches:
            self.createRound16Frame(match[0][0], match[1][0])

    def createRound16Frame(self, team1, team2, score1='-', score2='-'):
        frame_name = 'Match_' + str(self.matches)
        self.matches += 1
        self.frame = QFrame(self.round16Widget)
        self.frame.setObjectName(frame_name)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMinimumSize(QSize(100, 65))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.team1 = QLabel(self.frame)
        self.team1.setObjectName(u"team1")
        self.team1.setGeometry(QRect(40, 10, 351, 41))
        self.team1.setStyleSheet(u"font: 75 12pt \"Unispace\";\n"
                                 "color:rgb(255, 255, 255);\n"
                                 "")
        self.team1.setAlignment(Qt.AlignCenter)
        self.team1.setText(f'{team1}')
        self.team2 = QLabel(self.frame)
        self.team2.setObjectName(u"team2")
        self.team2.setGeometry(QRect(680, 10, 351, 41))
        self.team2.setStyleSheet(u"font: 75 12pt \"Unispace\";\n"
                                 "color:rgb(255, 255, 255);\n"
                                 "")
        self.team2.setAlignment(Qt.AlignCenter)
        self.team2.setText(f'{team2}')
        self.label_17 = QLabel(self.frame)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(480, 10, 111, 41))
        self.label_17.setStyleSheet(u"font: 75 12pt \"Unispace\";\n"
                                    "color:rgb(255, 255, 255);\n"
                                    "")
        self.label_17.setAlignment(Qt.AlignCenter)
        self.label_17.setText('VS')
        self.team1_score = QLineEdit(self.frame)
        self.team1_score.setObjectName(u"team1_score")
        self.team1_score.setGeometry(QRect(390, 10, 91, 41))
        self.team1_score.setStyleSheet(u"QLineEdit{\n"
                                       "background: #F8EAFF;\n"
                                       "border: 2px solid #803CE0;\n"
                                       "border-radius: 10px;\n"
                                       "color:#803CE0;\n"
                                       "font-family: Arial;\n"
                                       "font: 11pt;\n"
                                       "}\n"
                                       "QLineEdit:focus{\n"
                                       "border: 2px solid #FBAD25;\n"
                                       "}")
        self.team1_score.setText(score1)
        self.team1_score.setEnabled(False)
        self.team1_score.setAlignment(Qt.AlignCenter)
        self.team2_score = QLineEdit(self.frame)
        self.team2_score.setObjectName(u"team2_score")
        self.team2_score.setGeometry(QRect(590, 10, 91, 41))
        self.team2_score.setStyleSheet(u"QLineEdit{\n"
                                       "background: #F8EAFF;\n"
                                       "border: 2px solid #803CE0;\n"
                                       "border-radius: 10px;\n"
                                       "color:#803CE0;\n"
                                       "font-family: Arial;\n"
                                       "font: 11pt;\n"
                                       "}\n"
                                       "QLineEdit:focus{\n"
                                       "border: 2px solid #FBAD25;\n"
                                       "}")
        self.team2_score.setText(score2)
        self.team2_score.setEnabled(False)
        self.team2_score.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.frame)
        self.verticalLayout_6.setSpacing(50)

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
