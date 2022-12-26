#       Team 14 - Tournament Gui
#       team members
#       1- Ahmed Amin Ahmedsamy 2
#       2- Ahmed Alaa el-din    13
#       3- Ehab Tarek Shokri    34
#       4- Ziad Mosaad El-sayed 48
#       python version python 3.10.1
#       you must first type "pip install PyQt5" and "pip install PyQt5-tools "in the cmd



import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QTableWidget, QMessageBox, QFrame, \
    QSizePolicy, QLabel, QLineEdit
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
        self.sorted_groups = []  # group based list (8 groups) each group has 4 teams (sorted)
        self.qualified_teams = []  # qualified to Round of 16
        self.round16Flag = True  # a flag to check if we need to create round 16 or just edit it
        self.round16_matches = []   # storing the results of each game in round 16
        self.round16_winners = []  # storing the winners of the round 16
        self.quarterFlag = True
        self.quarter_matches = []
        self.quarter_winners = []
        self.semiFlag = True
        self.semi_matches = []
        self.semi_winners = []
        self.semi_losers = []
        self.finalFlag = True
        self.first_place_match = []
        self.third_place_match = []
        self.final_matches = []
        self.final_winners = []
        self.final_losers = []
        self.backButton.clicked.connect(self.goback)  # button to back to the homepage
        self.Groups.setCurrentIndex(0)  # setting the group tab to be default
        self.matches = 0  # counter for the matches (used for naming frames of every game)
        self.matchesSave.clicked.connect(self.clearPoints)  # save data (matches tab) button
        self.round16Save.clicked.connect(self.load16Scores)
        self.quarterSave.clicked.connect(self.loadQuarterScores)
        self.semiSave.clicked.connect(self.loadSemiScores)
        self.finalSave.clicked.connect(self.loadFinalScores)

    # go back to home page (stack widget)
    def goback(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

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

    # create a list of group teams with 0 points --->(insertTables & groupGames)
    def createGroupTeams(self):
        for i in range(8):
            self.sorted_groups += [[self.tier1[i], self.tier2[i], self.tier3[i], self.tier4[i]]]
        self.insertTables()
        self.groupGames()

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

    # create a 96-element list each representing a match
    def groupGames(self):
        for i in range(8):
            for j in range(4):
                for k in range(4):
                    if k != j:
                        team1 = self.sorted_groups[i][j][0]
                        team2 = self.sorted_groups[i][k][0]
                        self.groups_teams += [[team1, '0', team2, '0']]
        # create new matches (without scores) just Initialising using (createFrame)
        self.createWidget(self.groups_teams, self.matchesLayout, self.matchesSave, homeAway=True)

    # sorting each group in descending order (points) ---> (insertTables)
    def sortGroups(self):
        for grp in self.sorted_groups:
            grp.sort(reverse=True, key=lambda x: int(x[1]))
        self.insertTables()

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

        # loading score of the main group games from the gui into the (groups_teams) list ----> (gameResult)

    def loadScores(self):
        self.loadScore(self.MatchesWidget, self.groups_teams, self.gameResult, draw_allowance=True)

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
        self.qualifiedTeams()

    # selection
    def qualifiedTeams(self):
        self.qualified_teams = []
        self.round16_matches = []
        for grp in self.sorted_groups:
            for team in grp[:2]:
                self.qualified_teams += [team]
        for i in range(0, len(self.qualified_teams), 4):
            self.round16_matches += [[self.qualified_teams[i][0], '0', self.qualified_teams[i + 3][0], '0']]
            self.round16_matches += [[self.qualified_teams[i + 1][0], '0', self.qualified_teams[i + 2][0], '0']]
        self.editRound16()

    def editRound16(self):
        if self.round16Flag:
            self.createWidget(self.round16_matches, self.round16Layout, self.round16Save)
            self.round16Flag = False
        else:
            j = 0
            for i in range(0, len(self.round16Widget.findChildren(QLabel)), 3):
                self.round16Widget.findChildren(QLabel)[i].setText(str(self.round16_matches[j][0]))
                self.round16Widget.findChildren(QLabel)[i + 1].setText(str(self.round16_matches[j][2]))
                j += 1

    def load16Scores(self):
        self.loadScore(self.round16Widget, self.round16_matches, self.editQuarter, round_winner=self.quarter_winners,
                       nxt_round_matches=self.quarter_matches)

    def editQuarter(self):
        if self.quarterFlag:
            self.createWidget(self.quarter_matches, self.quarterLayout, self.quarterSave)
            self.quarterFlag = False
        else:
            j = 0
            for i in range(0, len(self.quarterWidget.findChildren(QLabel)), 3):
                self.quarterWidget.findChildren(QLabel)[i].setText(str(self.quarter_matches[j][0]))
                self.quarterWidget.findChildren(QLabel)[i + 1].setText(str(self.quarter_matches[j][2]))
                j += 1

    def loadQuarterScores(self):
        self.loadScore(self.quarterWidget, self.quarter_matches, self.editSemi, round_winner=self.quarter_winners,
                       nxt_round_matches=self.semi_matches)

    def editSemi(self):
        if self.semiFlag:
            self.createWidget(self.semi_matches, self.semiLayout, self.semiSave)
            self.semiFlag = False
        else:
            j = 0
            for i in range(0, len(self.semiWidget.findChildren(QLabel)), 3):
                self.semiWidget.findChildren(QLabel)[i].setText(str(self.semi_matches[j][0]))
                self.semiWidget.findChildren(QLabel)[i + 1].setText(str(self.semi_matches[j][2]))
                j += 1

    def loadSemiScores(self):
        self.loadScore(self.semiWidget, self.semi_matches, self.createFinalMatches, round_winner=self.semi_winners,
                       semi=True, round_loser=self.semi_losers)

    def createFinalMatches(self):
        self.first_place_match = [[self.semi_winners[0], '0', self.semi_winners[1], '0']]
        self.third_place_match = [[self.semi_losers[0], '0', self.semi_losers[1], '0']]
        self.final_matches = self.first_place_match + self.third_place_match
        self.editFinal()

    def editFinal(self):
        if self.finalFlag:
            self.createWidget(self.final_matches, self.finalLayout, self.finalSave)
            self.finalFlag = False
        else:
            j = 0
            for i in range(0, len(self.finalWidget.findChildren(QLabel)), 3):
                self.finalWidget.findChildren(QLabel)[i].setText(str(self.final_matches[j][0]))
                self.finalWidget.findChildren(QLabel)[i + 1].setText(str(self.final_matches[j][2]))
                j += 1

    def loadFinalScores(self):
        self.loadScore(self.finalWidget, self.final_matches, self.showWinners, round_winner=self.final_winners,
                       semi=True, round_loser=self.final_losers)

    def showWinners(self):
        print(f'First place {self.final_winners[0]} \nSecond place {self.final_losers[0]}')
        print(f'Third place {self.final_winners[1]} \nfourth place {self.final_losers[1]}')

    def createWidget(self, matches_list, Layout, Btn, homeAway=False):
        for match in matches_list:
            self.createFrames(match[0], match[2], Layout, homeAway)
        Btn.setEnabled(True)

    def editWidget(self):
        if self.finalFlag:
            self.createFinal()
            self.finalFlag = False
        else:
            j = 0
            for i in range(0, len(self.finalWidget.findChildren(QLabel)), 3):
                self.finalWidget.findChildren(QLabel)[i].setText(str(self.final_matches[j][0]))
                self.finalWidget.findChildren(QLabel)[i + 1].setText(str(self.final_matches[j][2]))
                j += 1

    def loadScore(self, widget, matches_list, nxt_round_func, round_winner=None, nxt_round_matches=None, semi=False,
                  round_loser=None, draw_allowance=False):
        counter = 0
        semiCounter = 0
        for lineEdit in widget.findChildren(QLineEdit):
            if counter % 2 == 0:
                if lineEdit.text().isdigit():
                    matches_list[semiCounter][1] = lineEdit.text()
                else:
                    rand = randint(0, 5)
                    matches_list[semiCounter][1] = str(rand)
                    lineEdit.setText(str(rand))
                counter += 1
            else:
                if lineEdit.text().isdigit():
                    matches_list[semiCounter][3] = lineEdit.text()
                else:
                    rand = randint(0, 5)
                    matches_list[semiCounter][3] = str(rand)
                    lineEdit.setText(str(rand))
                if matches_list[semiCounter][3] == matches_list[semiCounter][1] and not draw_allowance:
                    rand1 = randint(0, 5)
                    rand2 = randint(0, 5)
                    while abs(rand1 - rand2) < 3 and rand1 == rand2:
                        rand1 = randint(0, 5)
                        rand2 = randint(0, 5)
                    matches_list[semiCounter][1] = rand1
                    matches_list[semiCounter][3] = rand2
                    lineEdit.setText(f'{lineEdit.text()} ({rand2})')
                    widget.findChildren(QLineEdit)[counter-1].setText(
                        f'{widget.findChildren(QLineEdit)[counter-1].text()} ({rand1})')
                counter += 1
                semiCounter += 1
        if not draw_allowance:
            round_winner[:] = self.koWinner(matches_list)
            if semi:
                round_loser[:] = self.koLosers(matches_list)
            else:
                nxt_round_matches[:] = self.creatKoMatches(round_winner)
        nxt_round_func()

    def koWinner(self, matches_list):
        winners = []
        for match in matches_list:
            if match[1] > match[3]:
                winners += [match[0]]
            elif match[3] > match[1]:
                winners += [match[2]]
        return winners

    def koLosers(self, matches_list):
        losers = []
        for match in matches_list:
            if match[1] > match[3]:
                losers += [match[2]]
            elif match[3] > match[1]:
                losers += [match[0]]
        return losers

    def creatKoMatches(self, winner_list):
        matches = []
        for i in range(0, len(winner_list), 2):
            matches += [[winner_list[i], '0', winner_list[i+1], '0']]
        return matches

    # creating gui frame for 1 match
    def createFrames(self, team1, team2, widget, homeAway=False):
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
        self.label_17 = QLabel(self.frame)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(480, 10, 111, 41))
        self.label_17.setStyleSheet(u"font: 75 12pt \"Unispace\";\n"
                                    "color:rgb(255, 255, 255);\n"
                                    "")
        if homeAway:
            self.team1.setText(f'(H) {team1}')
            self.team2.setText(f'{team2} (A)')
        else:
            self.team1.setText(f'{team1}')
            self.team2.setText(f'{team2}')

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
        self.team1_score.setText('-')
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
        self.team2_score.setText('-')
        self.team2_score.setAlignment(Qt.AlignCenter)

        widget.addWidget(self.frame)
        widget.setSpacing(50)


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
