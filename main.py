#       Team 14 - Tournament Gui
#       team members
#       1- Ahmed Amin Ahmedsamy 2
#       2- Ahmed Alaa el-din    13
#       3- Ehab Tarek Shokri    34
#       4- Ziad Mosaad El-sayed 48
#       python version python 3.10.1
#       you must first type "pip install PyQt5" and "pip install PyQt5-tools "in the cmd
import math
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QTableWidget, QMessageBox, QFrame, \
    QSizePolicy, QLabel, QLineEdit, QAbstractScrollArea, QAbstractItemView
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
        self.initTeams = [{'name': 'Brazil', 'rank': 1}, {'name': 'Belgium', 'rank': 4},
                          {'name': 'Argentina', 'rank': 2}, {'name': 'France', 'rank': 3},
                          {'name': 'England', 'rank': 5}, {'name': 'Spain', 'rank': 10},
                          {'name': 'Netherlands', 'rank': 6}, {'name': 'Portugal', 'rank': 9},
                          {'name': 'Denmark', 'rank': 18}, {'name': 'Germany', 'rank': 14},
                          {'name': 'Croatia', 'rank': 7}, {'name': 'Mexico', 'rank': 15},
                          {'name': 'Uruguay', 'rank': 16}, {'name': 'Switzerland', 'rank': 12},
                          {'name': 'USA', 'rank': 13}, {'name': 'Senegal', 'rank': 19},
                          {'name': 'Wales', 'rank': 28}, {'name': 'Austria', 'rank': 34},
                          {'name': 'Serbia', 'rank': 29}, {'name': 'Morocco', 'rank': 11},
                          {'name': 'Japan', 'rank': 20}, {'name': 'Poland', 'rank': 22},
                          {'name': 'South Korea', 'rank': 25}, {'name': 'Tunisia', 'rank': 30},
                          {'name': 'Costa Rica', 'rank': 32}, {'name': 'Australia', 'rank': 27},
                          {'name': 'Canada', 'rank': 53}, {'name': 'Cameroon', 'rank': 33},
                          {'name': 'Ecuador', 'rank': 44}, {'name': 'Qatar', 'rank': 60},
                          {'name': 'Ghana', 'rank': 58}, {'name': 'Saudi Arabia', 'rank': 49},
                          {'name': 'Italy', 'rank': 8}, {'name': 'Colombia', 'rank': 17},
                          {'name': 'Peru', 'rank': 21}, {'name': 'Sweden', 'rank': 23},
                          {'name': 'IR Iran', 'rank': 24}, {'name': 'Ukraine', 'rank': 26},
                          {'name': 'Jamaica', 'rank': 64}, {'name': 'Chile', 'rank': 31},
                          {'name': 'Nigeria', 'rank': 35}, {'name': 'Hungary', 'rank': 36},
                          {'name': 'Russia', 'rank': 37}, {'name': 'Czechia', 'rank': 38},
                          {'name': 'Egypt', 'rank': 39}, {'name': 'Algeria', 'rank': 40},
                          {'name': 'Scotland', 'rank': 42}, {'name': 'Norway', 'rank': 43},
                          {'name': 'Turkey', 'rank': 44}, {'name': 'Mali', 'rank': 45},
                          {'name': 'Paraguay', 'rank': 46}, {'name': 'Côte d\'Ivoire', 'rank': 47},
                          {'name': 'Republic of Ireland', 'rank': 48}, {'name': 'Burkina Faso', 'rank': 50},
                          {'name': 'Greece', 'rank': 51}, {'name': 'Romania', 'rank': 52},
                          {'name': 'Costa Rica', 'rank': 53}, {'name': 'Venezuela', 'rank': 55},
                          {'name': 'Slovakia', 'rank': 54}, {'name': 'Finland', 'rank': 56},
                          {'name': 'Bosnia and Herzegovina', 'rank': 57}, {'name': 'Qatar', 'rank': 58},
                          {'name': 'Northern Ireland', 'rank': 59}, {'name': 'Panama', 'rank': 61},
                          {'name': 'Slovenia', 'rank': 62}, {'name': 'Iceland', 'rank': 63}]
        self.teams = []
        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.tier4 = []
        self.next_btn = False
        self.row = 0
        self.createGroupsButton.clicked.connect(self.gotosort)
        self.createLeagueButton.clicked.connect(self.createLeague)
        self.nextButton.clicked.connect(self.gotoNextPage)
        self.pointer = 0

    # insert data into list and dictionary
    def insert(self):
        name = self.teamNameField.text()
        rank = self.teamRankField.text()
        self.teamNameField.setText('')
        self.teamRankField.setText('')
        if len(name) == 0 or len(rank) == 0:
            self.teamError.setText('Please enter all the fields')
        else:
            if self.row == 64:
                self.teamError.setText('MAX is 64 teams')
            else:
                if rank.isdigit():
                    int_rank = int(rank)
                    self.teamError.setText('')
                    self.team_dict += [{"name": name, "rank": rank}]
                    self.teams += [[name, 0, 0, int_rank]]
                    self.loadData()
                else:
                    self.teamError.setText('rank must be integer')

    # load date into the GUI table
    def loadData(self):
        curr = self.row + 1
        self.teamsTable.setRowCount(curr)
        self.teamsTable.setItem(self.row, 0, QtWidgets.QTableWidgetItem(self.team_dict[self.pointer]['name']))
        self.teamsTable.setItem(self.row, 1, QtWidgets.QTableWidgetItem(self.team_dict[self.pointer]['rank']))
        self.row = curr
        self.pointer += 1       # a variable to iterate through team_dict

    # insert predefined into the list and loading it into the GUI table
    def autofillData(self):
        if self.row < 64:
            self.teamsTable.setRowCount(self.row + 1)
            for i in range(1):
                self.teamsTable.setItem(self.row+i, 0, QtWidgets.QTableWidgetItem(self.initTeams[self.row+i]['name']))
                self.teamsTable.setItem(self.row+i, 1, QtWidgets.QTableWidgetItem(str(self.initTeams[self.row+i]['rank'])))
                self.teams += [[self.initTeams[self.row + i]['name'], 0, 0, self.initTeams[self.row + i]['rank']]]
            self.row += 1
        else:
            self.autofillButton.setEnabled(False)

    # sorting the list : 'teams' and redirecting into the Groups GUI
    def gotosort(self):
        if self.row < 4:
            self.groupError.setText('Number of teams must be at least 4')
        else:
            self.teams.sort(key=lambda x: x[3])  # sorting the list depending on its 3rd element (rank)
            self.showWarning()
            self.groupError.setText('')
            self.gotoNextPage()

    # trans
    def goToLeague(self):
        self.groupError.setText('')
        self.gotoNextPage()

    # Creates a group object
    def createGroups(self):
        if self.next_btn:
            widget.removeWidget(widget.widget(1))
        self.next_btn = True
        groups = GroupStage()
        groups.teams = self.teams
        for team in groups.teams:
            team[1] = 0     # clearing old points
            team[2] = 0     # clearing old goals
        groups.createTiers()
        widget.addWidget(groups)

    # Creates a League object
    # Creates a group object
    def createLeague(self):
        self.teams.sort(key=lambda x: x[3])
        if self.next_btn:
            widget.removeWidget(widget.widget(1))
        self.next_btn = True
        league = League()
        league.teams = self.teams
        league.setTeamList()
        widget.addWidget(league)
        self.gotoNextPage()

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
    def gotoNextPage(self):
        if not self.next_btn:
            self.groupError.setText('create groups or League First')
        else:
            widget.setCurrentIndex(widget.currentIndex() + 1)
            self.groupError.setText('')


# GroupStageUi class
class GroupStage(QDialog):
    def __init__(self):
        super(GroupStage, self).__init__()
        loadUi('GroupStage.ui', self)
        self.tables_number = 0
        self.nog = 0
        self.extra = 0
        self.qualifiers = 0
        self.teams = []  # list with the  teams will be using it for making tiers
        self.groups_teams = []  # a temporary list help to slice the games of each group separately
        self.games_result = []  # # of elements (game) each element has 2 value (team1 points - team2 points)
        self.tier1 = []  # temp list to have the first tier shuffled
        self.tier2 = []  # temp list to have the second tier shuffled
        self.tier3 = []  # temp list to have the third tier shuffled
        self.tier4 = []  # temp list to have the fourth tier shuffled
        self.sorted_groups = []  # group based list (8 groups) each group has 4 teams (sorted)
        self.qualified_teams = []  # qualified to Round of 16
        self.teams_struggling = []
        self.matchesFlag = True
        self.qualFlag = True
        self.round32Flag = True
        self.round32_winners = []
        self.round32_matches = []
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
        self.qualificationSave.clicked.connect(self.loadQualScores)
        self.round32Save.clicked.connect(self.load32Scores)
        self.round16Save.clicked.connect(self.load16Scores)
        self.quarterSave.clicked.connect(self.loadQuarterScores)
        self.semiSave.clicked.connect(self.loadSemiScores)
        self.finalSave.clicked.connect(self.loadFinalScores)
        # setting All tabs to be visible
        for i in range(2, 8):
            self.Groups.setTabVisible(i, False)


    # go back to home page (stack widget)
    def goback(self):
        widget.setCurrentIndex(widget.currentIndex() - 1)

    # input : team list
    # output : slice the team list, then shuffle it and append it into one suitable list --->(createGroupTeams)
    def createTiers(self):
        self.nog = int(len(self.teams)/4)
        self.qualifiers = self.nog*2
        self.extra = len(self.teams) % 4
        temp = self.nog
        self.tier1 = self.teams[0:temp]
        self.tier2 = self.teams[temp:(2*temp)]
        self.tier3 = self.teams[(2*temp):(3*temp)]
        self.tier4 = self.teams[(3*temp):]
        shuffle(self.tier1)
        shuffle(self.tier2)
        shuffle(self.tier3)
        shuffle(self.tier4)
        self.createGroupTeams()

    # create a list of group teams with 0 points --->(insertTables & groupGames)
    def createGroupTeams(self):
        for i in range(self.nog):
            self.sorted_groups += [[self.tier1[i], self.tier2[i], self.tier3[i], self.tier4[i]]]
        for i in range(self.extra):
            self.sorted_groups[0] += [self.tier4[self.nog + i]]
        self.createGroupsTable()
        self.insertTables()
        self.groupGames()

    # create tables for groups
    def createGroupsTable(self):
        for x in range(int(math.ceil(self.nog/4))):
            temp = (self.nog - ((x+1) * 4)) % 4
            if temp == 0:
                temp += 4
            for y in range(temp):
                self.createTable(x, y)

    # a function to automatically insert data into the group tables
    def insertTables(self):
        for grp, tables in zip(self.sorted_groups, self.GroupsWidget.findChildren(QTableWidget)):
            row_index = 0
            for team in grp:
                if self.matchesFlag:
                    tables.setRowCount(tables.rowCount() + 1)
                col_index = 0
                for info in team[:3]:
                    item = QTableWidgetItem(str(info))
                    tables.setItem(row_index, col_index, item)
                    col_index += 1
                row_index += 1
        self.matchesFlag = False

    # create  x-element list each representing a match
    def groupGames(self):
        for i in range(self.nog):
            for j in range(len(self.sorted_groups[i])):
                for k in range(len(self.sorted_groups[i])):
                    if k != j:
                        team1 = self.sorted_groups[i][j][0]
                        team2 = self.sorted_groups[i][k][0]
                        self.groups_teams += [[team1, '0', team2, '0']]
        # create new matches (without scores) just Initialising using (createFrame)
        self.createWidget(self.groups_teams, self.matchesLayout, self.matchesSave, homeAway=True)

    # sorting each group in descending order (points) ---> (insertTables)
    def sortGroups(self):
        for grp in self.sorted_groups:
            grp.sort(reverse=True, key=lambda x: int(x[2]))
            grp.sort(reverse=True, key=lambda x: int(x[1]))
        self.insertTables()

    # clear points ---> (sortAfterClear)
    def clearPoints(self):
        for grp in self.sorted_groups:
            for team in grp:
                team[1] = '0'
                team[2] = '0'
        self.sortAfterClear()
        self.loadScores()

    # getting teams in it is first order to keep having the same matches
    def sortAfterClear(self):
        for grp in self.sorted_groups:
            grp.sort(key=lambda x: int(x[3]))

        # loading score of the main group games from the gui into the (groups_teams) list ----> (gameResult)

    def loadScores(self):
        self.loadScore(self.MatchesWidget, self.groups_teams, self.gameResult, 1,
                       draw_allowance=True)

    # updates [overwrites] (games_result) list depending on matches results (group_games) ---> (updatePoints)
    def gameResult(self):
        self.games_result = []
        for match in self.groups_teams:
            points1 = 0
            points2 = 0
            goals1 = 0
            goals2 = 0
            if int(match[1]) > int(match[3]):
                points1 += 3
                goals1 += (int(match[1]) - int(match[3]))
                goals2 += (int(match[3]) - int(match[1]))
            elif int(match[3]) > int(match[1]):
                points2 += 3
                goals1 += (int(match[1]) - int(match[3]))
                goals2 += (int(match[3]) - int(match[1]))
            else:
                points1 += 1
                points2 += 1
                goals1 += (int(match[1]) - int(match[3]))
                goals2 += (int(match[3]) - int(match[1]))

            self.games_result += [[points1, goals1, points2, goals2]]
        self.updatePoints()

    # update points list to be used in filling the group table's data  ---> (sortGroups)
    def updatePoints(self):
        self.sortAfterClear()
        game_counter = 0  # starts at game 0 , ends at game 96 (to iterate the games result list)
        for i in range(self.nog):
            for j in range(len(self.sorted_groups[i])):
                for k in range(len(self.sorted_groups[i])):
                    if k != j:
                        # adding point1 to team 1
                        self.sorted_groups[i][j][1] = str(int(self.sorted_groups[i][j][1]) +
                                                          self.games_result[game_counter][0])
                        # adding goal difference
                        self.sorted_groups[i][j][2] = str(int(self.sorted_groups[i][j][2]) +
                                                          self.games_result[game_counter][1])

                        # adding point2 to team 2
                        self.sorted_groups[i][k][1] = str(int(self.sorted_groups[i][k][1]) +
                                                          self.games_result[game_counter][2])
                        # adding goal difference
                        self.sorted_groups[i][k][2] = str(int(self.sorted_groups[i][k][2]) +
                                                          self.games_result[game_counter][3])

                        game_counter += 1
        self.sortGroups()
        self.qualifiedTeams()

    # selection
    def qualifiedTeams(self):
        self.qualified_teams = []
        self.round16_matches = []
        for grp in self.sorted_groups:
            for team in grp[:2]:
                self.qualified_teams += [team[0]]
        if self.qualifiers == 2:
            print(f'Tournament Winner is {self.qualified_teams[0]}')
        if self.qualifiers == 4:
            self.matches_after_grp(self.semi_matches)
            self.Groups.setTabVisible(6, True)
            self.editSemi()
        elif self.qualifiers == 8:
            self.matches_after_grp(self.quarter_matches)
            self.Groups.setTabVisible(5, True)
            self.editQuarter()
        elif self.qualifiers == 16:
            self.matches_after_grp(self.round16_matches)
            self.Groups.setTabVisible(4, True)
            self.editRound16()
        elif self.qualifiers == 32:
            self.matches_after_grp(self.round32_matches)
            self.Groups.setTabVisible(2, True)

        else:
            self.Groups.setTabVisible(3, True)
            self.qualifications()

    def qualifications(self):
        number_base2 = math.pow(2, math.floor(math.log2(self.qualifiers)))
        temp = int(-2 * (self.qualifiers - number_base2))
        self.teams_struggling = self.qualified_teams[temp:]
        self.teams_struggling = self.creatKoMatches(self.teams_struggling)
        self.editQualifications()


    def editQualifications(self):
        if self.qualFlag:
            self.createWidget(self.teams_struggling, self.qualificationLayout, self.qualificationSave)
            self.qualFlag = False
        else:
            j = 0
            for i in range(0, len(self.qualificationWidget.findChildren(QLabel)), 3):
                self.qualificationWidget.findChildren(QLabel)[i].setText(str(self.teams_struggling[j][0]))
                self.qualificationWidget.findChildren(QLabel)[i + 1].setText(str(self.teams_struggling[j][2]))
                j += 1

    def loadQualScores(self):
        self.loadScore(self.qualificationWidget, self.teams_struggling, self.qual_nxt_stage, 3,
                       round_winner=self.teams_struggling, qualifications=True)

    def qual_nxt_stage(self):
        number_base2 = math.pow(2, math.floor(math.log2(self.qualifiers)))
        temp = int(-2 * (self.qualifiers - number_base2))
        self.qualified_teams = self.qualified_teams[:temp] + self.teams_struggling
        self.qualifiers = len(self.qualified_teams)
        if self.qualifiers == 4:
            self.matches_after_grp(self.semi_matches)
            self.Groups.setTabVisible(6, True)
            self.editSemi()
        elif self.qualifiers == 8:
            self.matches_after_grp(self.quarter_matches)
            self.Groups.setTabVisible(5, True)
            self.editQuarter()
        elif self.qualifiers == 16:
            self.matches_after_grp(self.round16_matches)
            self.Groups.setTabVisible(4, True)
            self.editRound16()

    def editRound32(self):
        if self.round32Flag:
            self.createWidget(self.round32_matches, self.round32Layout, self.round32Save)
            self.round32Flag = False
        else:
            j = 0
            for i in range(0, len(self.round32Widget.findChildren(QLabel)), 3):
                self.round32Widget.findChildren(QLabel)[i].setText(str(self.round32_matches[j][0]))
                self.round32Widget.findChildren(QLabel)[i + 1].setText(str(self.round32_matches[j][2]))
                j += 1

    def load32Scores(self):
        self.loadScore(self.round32Widget, self.round32_matches, self.editRound16, 4,
                       round_winner=self.round16_winners, nxt_round_matches=self.round16_matches)

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
        self.loadScore(self.round16Widget, self.round16_matches, self.editQuarter, 5,
                       round_winner=self.quarter_winners, nxt_round_matches=self.quarter_matches)

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
        self.loadScore(self.quarterWidget, self.quarter_matches, self.editSemi, 6,
                       round_winner=self.quarter_winners, nxt_round_matches=self.semi_matches)

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
        self.loadScore(self.semiWidget, self.semi_matches, self.createFinalMatches, 7,
                       round_winner=self.semi_winners, semi=True, round_loser=self.semi_losers)

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
        self.loadScore(self.finalWidget, self.final_matches, self.showWinners, 7,
                       round_winner=self.final_winners, semi=True, round_loser=self.final_losers)

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

    def loadScore(self, widget, matches_list, nxt_round_func, nxt_tab_index, round_winner=None, nxt_round_matches=None, semi=False,
                  round_loser=None, draw_allowance=False, qualifications = False):
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
            elif not qualifications:
                nxt_round_matches[:] = self.creatKoMatches(round_winner)
        self.Groups.setTabVisible(nxt_tab_index, True)
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

    def matches_after_grp(self, nxt_round_matches):
        nxt_round_matches[:] = []
        for i in range(0, len(self.qualified_teams), 4):
            nxt_round_matches[:] += [[self.qualified_teams[i], '0', self.qualified_teams[i + 3], '0']]
            nxt_round_matches[:] += [[self.qualified_teams[i + 1], '0', self.qualified_teams[i + 2], '0']]
        print(nxt_round_matches)

    def creatKoMatches(self, winner_list):
        matches = []
        for i in range(0, len(winner_list), 2):
            matches += [[winner_list[i], '0', winner_list[i+1], '0']]
        return matches

    # creating table
    def createTable(self, row, col):
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        grp_name = 'Group ' + alpha[self.tables_number]
        self.tables_number += 1
        self.frame = QFrame(self.groupLayout)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(265, 300))
        self.frame.setMaximumSize(QSize(265, 300))
        self.frame.setGeometry(QRect(20, 80, 271, 321))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 30, 241, 51))
        self.label.setStyleSheet(u"font: 75 20pt \"Unispace\";\n"
                                 "color:rgb(52, 77, 189);\n"
                                 "")
        self.label.setAlignment(Qt.AlignCenter)
        self.Table = QTableWidget(self.frame)
        if (self.Table.columnCount() < 3):
            self.Table.setColumnCount(3)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.Table.setHorizontalHeaderItem(0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        __qtablewidgetitem15.setTextAlignment(Qt.AlignLeading | Qt.AlignTop)
        self.Table.setHorizontalHeaderItem(1, __qtablewidgetitem15)
        __qtablewidgetitem500 = QTableWidgetItem()
        __qtablewidgetitem500.setTextAlignment(Qt.AlignLeading | Qt.AlignTop)
        self.Table.setHorizontalHeaderItem(2, __qtablewidgetitem500)
        self.Table.setObjectName(u"Table")
        self.Table.setGeometry(QRect(0, 80, 265, 190))
        self.Table.setStyleSheet(u"QTableWidget{	\n"
                                 "border: 3px solid #803CE0;\n"
                                 "border-radius: 10px;\n"
                                 "color:rgb(255, 255, 255);\n"
                                 "font-family: Arial;\n"
                                 "font: 11pt;\n"
                                 "background-color:rgb(71, 142, 210);\n"
                                 "alternate-background-color:rgb(44, 94, 212);\n"
                                 "}")
        self.Table.setFrameShape(QFrame.Box)
        self.Table.setFrameShadow(QFrame.Raised)
        self.Table.setLineWidth(2)
        self.Table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.Table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.Table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table.setGridStyle(Qt.SolidLine)
        self.Table.setRowCount(0)
        self.Table.horizontalHeader().setCascadingSectionResizes(True)
        self.Table.horizontalHeader().setMinimumSectionSize(40)
        self.Table.horizontalHeader().setDefaultSectionSize(40)
        self.Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.Table.horizontalHeader().setProperty("showSortIndicator", False)
        self.Table.horizontalHeader().setStretchLastSection(False)
        self.Table.verticalHeader().setStretchLastSection(False)
        self.label.setText(QCoreApplication.translate("GroupStage", grp_name, None))
        ___qtablewidgetitem = self.Table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("GroupStage", u"Team", None))
        ___qtablewidgetitem1 = self.Table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("GroupStage", u"Pts", None))
        ___qtablewidgetitem2 = self.Table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("GroupStage", u"GD", None))
        self.groupsLayout.addWidget(self.frame, row, col, 1, 1)

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


# League Ui Class
class League(QDialog):
    def __init__(self):
        super(League, self).__init__()
        loadUi("League.ui", self)
        self.Table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.teams = []  # list with the  teams will be using it for making tiers
        self.teams_matches = []
        self.games_result = []  # # of elements (game) each element has 2 value (team1 points - team2 points)
        self.matchesFlag = True
        self.matchesSave.clicked.connect(self.clearPoints)


    def setTeamList(self):
        self.Table.setRowCount(len(self.teams))
        for team in self.teams:
            temp = team.pop()                      # removing the rank
            team += [0, 0, 0, 0, 0, 0, temp]         # team['name' , MP, W, D, L, GF, GA, GD, PTS]
        self.loadTable()
        self.groupGames()

    def loadTable(self):
        row = 0
        for team in self.teams:
            column = 0
            for col in team[:9]:
                temp_item = QtWidgets.QTableWidgetItem(str(col))
                self.Table.setItem(row, column, temp_item)
                column += 1
            row += 1

    def groupGames(self):
        for j in range(len(self.teams)):
            for k in range(len(self.teams)):
                if k != j:
                    team1 = self.teams[j][0]
                    team2 = self.teams[k][0]
                    self.teams_matches += [[team1, '0', team2, '0']]
        self.editTable()

    def editTable(self):
        if self.matchesFlag:
            # create new matches (without scores) just Initialising using (createFrame)
            self.createWidget(self.teams_matches, self.matchesLayout, self.matchesSave, homeAway=True)
            self.matchesFlag = False

    # clear points ---> (sortAfterClear)
    def clearPoints(self):
        for team in self.teams:
            for col in range(1, 9):
                team[col] = 0
        self.sortAfterClear()
        self.loadScores()

    def sortAfterClear(self):
            self.teams.sort(key=lambda x: int(x[9]))

    def loadScores(self):
        self.loadScore(self.MatchesWidget, self.teams_matches, self.gameResult, draw_allowance=True)

    def gameResult(self):
        self.games_result = []
        for match in self.teams_matches:
            points1 = 0
            points2 = 0
            goals1 = int(match[1])
            goals2 = int(match[3])
            if goals1 > goals2:
                points1 += 3
            elif goals2 > goals1:
                points2 += 3
            else:
                points1 += 1
                points2 += 1
            self.games_result += [[points1, goals1, points2, goals2]]
        self.updateTable()

    # update points list to be used in filling the group table's data  ---> (sortGroups)
    def updateTable(self):
        self.sortAfterClear()
        game_counter = 0  # starts at game 0 , ends at game 96 (to iterate the games result list)
        for j in range(len(self.teams)):
            for k in range(len(self.teams)):
                if k != j:
                    # increasing match played
                    self.teams[j][1] += 1
                    # updating Wins & Draws & loses & points
                    if self.games_result[game_counter][0] == 3:
                        self.teams[j][2] += 1
                        self.teams[j][8] += 3
                    elif self.games_result[game_counter][0] == 1:
                        self.teams[j][3] += 1
                        self.teams[j][8] += 1
                    elif self.games_result[game_counter][0] == 0:
                        self.teams[j][4] += 1
                    # update GF & GA & GD
                    self.teams[j][5] += self.games_result[game_counter][1]
                    self.teams[j][6] += self.games_result[game_counter][3]
                    self.teams[j][7] += self.games_result[game_counter][1] - self.games_result[game_counter][3]
                    # increasing match played
                    self.teams[k][1] += 1
                    # updating Wins & Draws & loses & points
                    if self.games_result[game_counter][2] == 3:
                        self.teams[k][2] += 1
                        self.teams[k][8] += 3
                    elif self.games_result[game_counter][2] == 1:
                        self.teams[k][3] += 1
                        self.teams[k][8] += 1
                    elif self.games_result[game_counter][2] == 0:
                        self.teams[k][4] += 1
                    # update GF & GA & GD
                    self.teams[k][5] += self.games_result[game_counter][3]
                    self.teams[k][6] += self.games_result[game_counter][1]
                    self.teams[k][7] += self.games_result[game_counter][3] - self.games_result[game_counter][1]
                    game_counter += 1
        self.sortTable()

    def sortTable(self):
        self.teams.sort(key=lambda pts: int(pts[7]), reverse=True)
        self.teams.sort(key=lambda pts: int(pts[8]), reverse=True)
        self.loadTable()

    def loadScore(self, widget, matches_list, nxt_func, draw_allowance=False):
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
        nxt_func()

    def createWidget(self, matches_list, Layout, Btn, homeAway=False):
        for match in matches_list:
            self.createFrames(match[0], match[2], Layout, homeAway)
        Btn.setEnabled(True)

        # creating gui frame for 1 match

    def createFrames(self, team1, team2, widget, homeAway=False):
        self.frame = QFrame(self.MatchesWidget)
        self.frame.setObjectName(u'frame')
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
