#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Gamble game with lot of variation and customization to fit most streamers"""
# ---------------------------------------
# Libraries and references
# ---------------------------------------
from fractions import Fraction
import codecs
import json
import os
import winsound
import ctypes
import re
import codecs
import time
import math
import sys
import random
import csv


# ---------------------------------------
# [Required] Script information
# ---------------------------------------
ScriptName = "QueueClicker"
Website = "twitch.tv/QueueSS"
Creator = "goeticThunder"
Version = "2.0.0a"
Description = "Queue Clicker 2.0"

# ---------------------------------------
# Variables
# ---------------------------------------
settingsfile = os.path.join(os.path.dirname(__file__), "settings.json")
jackpotFile = os.path.join(os.path.dirname(__file__), "jackpot.txt")
MessageBox = ctypes.windll.user32.MessageBoxW
MB_YES = 6
RegBet = re.compile(r"^100$|^\d{0,3}? *%?$", re.U)
m_ConfigFile = os.path.join(os.path.dirname(__file__), "Settings/settings.json")
m_ConfigFileJs = os.path.join(os.path.dirname(__file__), "Settings/settings.js")
m_jackpotFile = os.path.join(os.path.dirname(__file__), "jackpot.txt")

millnames = ['', 'K', 'M', 'B', 'T', 'Qu']


# ---------------------------------------
# Classes
# ---------------------------------------
class Settings:
    """" Loads settings from file if file is found if not uses default values"""

    # The 'default' variable names need to match UI_Config
    def __init__(self, settingsfile=None):
        if settingsfile and os.path.isfile(settingsfile):
            with codecs.open(settingsfile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else:  # set variables if no custom settings file is found
            self.OnlyLive = False
            self.Enabled = True
            self.Interval = 10
            self.BasePayout = 1
            self.Command = "!gamble"
            self.Permission = "Everyone"
            self.PermissionInfo = ""
            self.VoteStartPermission = "Moderator"
            self.Mode = "Revlo"
            self.Usage = "Stream Chat"
            self.AllWord = "all"
            self.BetCommand = "!vote"
            self.StartBets = "!start"
            self.StopBets = "!stop"
            self.PayOutCommand = "!payout"
            self.AbortCommand = "!abort"
            self.AdminPermission = "Moderator"
            self.ForceAll = False
            self.UseRandom = False
            self.RandomMax = 1
            self.RandomMin = 100
            self.Jackpot = 500
            self.JackpotEnabled = False
            self.JackpotNumber = 150
            self.JackpotPercentage = 50
            self.JackpotBase = 500
            self.JackpotCheck = True
            self.JackpotWord = "jackpot"
            self.UseCD = True
            self.Cooldown = 5
            self.OnCooldown = "{0} the command is still on cooldown for {1} seconds!"
            self.UserCooldown = 10
            self.OnUserCooldown = "{0} the command is still on user cooldown for {1} seconds!"
            self.CasterCD = True
            self.BaseResponse = "Rolled {0}. "
            self.NotEnoughResponse = "{0} you don't have that much {1} to gamble! "
            self.WinResponse = "{0} won {1} {3} and now has {2} {3} "
            self.LoseResponse = "{0} lost {1} {3} and now has {2} {3} "
            self.TooMuchResponse = "{0} you can't gamble more than {1} {2}"
            self.TooLowResponse = "{0} you can't gamble less than {1} {2}"
            self.InfoResponse = "To gamble use !gamble <amount>"
            self.PermissionResp = "$user -> only $permission ($permissioninfo) and higher can use this command"
            self.JackpotWin = "{0} won the jackpot of {1} {3} and now has a total of {2} {3}"
            self.JackpotResponse = "There's currently {0} {1} in the jackpot!"
            self.MinValue = 0
            self.MaxValue = 150
            self.WinChance = 40
            self.TripleWinEnabled = True
            self.TripleChance = 2
            self.MinBet = 5
            self.MaxBet = 9999
            self.RMinValue = 1
            self.RMaxValue = 100
            self.RWinChance = 40
            self.RMinBet = 1
            self.RMaxBet = 9999
            self.PMinValue = 0
            self.PMaxValue = 100
            self.PMinBet = 1
            self.PMaxBet = 9999
            self.SMinValue = 0
            self.SMaxValue = 100
            self.SMinBet = 1
            self.SMaxBet = 9999
            self.SWinNumbers = "42 69 100"
            self.SMultiplier = 30
            self.NoZero = "{0} -> You are not allowed to roll anything less than 1!"
            self.NoCurrency = "{0} -> You don't have any currency to gamble!"
            self.BetsOpenResponse = "Bets opened"
            self.BetsCloseResponse = "Bets closed"
            self.AbortResponse = "Something happened - aborting bets, you have been refunded."
            self.PayOutResponse = "Payout {0}"
            self.CurrencyResponse = "You have to bet at least {0} {1}"
            self.NotEnoughResponse = "{0} you don't have that many {1} to bet"
            self.CommandResponse = "Betting is used by {0} [Yes/No] [Amount] - Minimum bet varies by player level."
            self.NoWinnerResponse = "Sadly no one won"
            self.alreadyResponse = "You bet already"
            self.BetPermission = "Everyone"
            self.BasePot = 10
            self.DismissBasePot = 2000
            self.BettingTime = 60


    # Reload settings on save through UI
    def Reload(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')

    def Save(self, settingsfile):
        """ Save settings contained within to .json and .js settings files. """
        try:
            with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
            with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
                f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
        except ValueError:
            Parent.Log(ScriptName, "Failed to save settings to file.")


class Player:

    def __init__(self, username, exp):
        self.username = username
        self.level = 1
        self.prestige = 0
        self.level_cap = 100
        self.exp = exp
        if not os.path.exists("..\Streamlabs Chatbot\Services\Games\QueueClicker2\Users\{}.txt".format(self.username)):
            self.playerSave()

    def read_file(self, string_to_find):
        user_file = open("..\Streamlabs Chatbot\Services\Games\QueueClicker2\Users\{}.txt".format(self.username), "a+")
        user_file.seek(0)
        lines = user_file.readlines()
        for line in lines:
            if string_to_find in line:
                string = line.split()
                level_of_string = int(string[1])
                user_file.close()
                return level_of_string
        user_file.close()
        return 0

    def playerLoad(self):
        self.level = self.read_file("Level")
        self.prestige = self.read_file("Prestige")
        self.level_cap = self.read_file("LevelCap")

    def playerSave(self):
        user_file = open("..\Streamlabs Chatbot\Services\Games\QueueClicker2\Users\{}.txt".format(self.username), "w")
        print_statement = "Level {}\nPrestige {}\nLevelCap {}".format(self.level, self.prestige, self.level_cap)
        user_file.write(print_statement)
        user_file.close()

    def levelUp(self):
        self.level += 1

    def pointsToLevelUp(self):
        return 100 * self.level**2

    def prestigeUp(self):
        self.level = 1
        self.prestige += 1
        point_reset = Parent.GetPoints(self.username) * -1
        Parent.AddPoints(self.username, self.username, point_reset)
        self.level_cap = int(100*1.25**(self.prestige))

    def getPointModifier(self):
        prestige_mod = self.prestige*1.2
        level_mod = (1 + self.level)**1.1
        return prestige_mod + level_mod

    def levelUpCheck(self):
        if self.exp >= self.pointsToLevelUp():
            while self.exp > self.pointsToLevelUp():
                self.levelUp()
            if self.level < 3:
                return "{0} has leveled up! They're now level {1}.".format(self.username, self.level)
            elif self.level % 5 == 0:
                return "{0} has leveled up! They're now level {1}.".format(self.username, self.level)
        if self.level >= self.level_cap:
            self.prestigeUp()
            return "{0} has PRESTIGED! {0} is now prestige rank {1}.".format(self.username, self.prestige)
        return ""

    def getMinBet(self):
        if self.level <= 5:
            min_bet_value = MySet.MinBet
        else:
            #old value
            #min_bet_value = ((self.level - 1) * 150)

            #testing?
            min_bet_value = int((((self.level - 5) * 300) * (self.prestige * 1.2)))
        return min_bet_value

class nonPublic:

    def __init__(self):

        self.Pot = 0
        self.Bets = {}
        self.Win = {}
        self.WinPot = 0
        self.Loss = {}
        self.LossPot = 0
        self.PayedOut = False
        self.isBetOpen = False
        self.TimeToClose = 0

# ---------------------------------------
# Settings functions
# ---------------------------------------
def SetDefaults():
    """Set default settings function"""
    global MySettings
    winsound.MessageBeep()
    returnValue = MessageBox(0, u"You are about to reset the settings, "
                                "are you sure you want to continue?"
                             , u"Reset settings file?", 4)
    if returnValue == MB_YES:
        returnValue = MessageBox(0, u"Settings successfully restored to default values"
                                 , u"Reset complete!", 0)
        global MySet
        MyNonPublic = nonPublic()
        Settings.Save(MySet, settingsfile)


def ReloadSettings(jsonData):
    """Reload settings on pressing the save button"""
    global MySet
    MySet.Reload(jsonData)
    global jackpot
    jackpot = MySet.Jackpot


def SaveSettings():
    """Save settings on pressing the save button"""
    Settings.Save(MySet, settingsfile)
    jackpot = MySet.Jackpot

    with open(jackpotFile, "w+") as f:
        f.write(str(jackpot))


MySettings = Settings()


# ---------------------------------------
# Optional functions
# ---------------------------------------
def OpenReadMe():
    """Open the readme.txt in the scripts folder"""
    location = os.path.join(os.path.dirname(__file__), "README.txt")
    os.startfile(location)


def SendResp(data, Usage, Message):
    """Sends message to Stream or discord chat depending on settings"""
    Message = Message.replace("$user", data.UserName)
    Message = Message.replace("$currencyname", Parent.GetCurrencyName())
    Message = Message.replace("$target", data.GetParam(1))
    Message = Message.replace("$permissioninfo", MySet.PermissionInfo)
    Message = Message.replace("$permission", MySet.Permission)

    l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and (Usage in l) and not data.IsWhisper():
        Parent.SendStreamMessage(Message)

    l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
    if not data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendStreamWhisper(data.User, Message)

    l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
    if data.IsFromDiscord() and not data.IsWhisper() and (Usage in l):
        Parent.SendDiscordMessage(Message)

    l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
    if data.IsFromDiscord() and data.IsWhisper() and (Usage in l):
        Parent.SendDiscordDM(data.User, Message)


def IsFromValidSource(data, Usage):
    """Return true or false depending on the message is sent from
    a source that's in the usage setting or not"""
    if not data.IsFromDiscord():
        l = ["Stream Chat", "Chat Both", "All", "Stream Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Stream Whisper", "Whisper Both", "All", "Stream Both"]
        if data.IsWhisper() and (Usage in l):
            return True

    if data.IsFromDiscord():
        l = ["Discord Chat", "Chat Both", "All", "Discord Both"]
        if not data.IsWhisper() and (Usage in l):
            return True

        l = ["Discord Whisper", "Whisper Both", "All", "Discord Both"]
        if data.IsWhisper() and (Usage in l):
            return True
    return False


def ReportBug():
    """Open google form to report a bug"""
    os.system("explorer https://goo.gl/forms/wATNZWSkmmYhur9q2")


# ---------------------------------------
# [Required] functions
# ---------------------------------------
def Init():
    """data on Load, required function"""
    global MySettings
    global MySet
    global lastPayoutTime
    global vote_flag
    global MyNonPublic

    MySet = Settings(settingsfile)
    MySettings = Settings(m_ConfigFile)
    vote_flag = False
    lastPayoutTime = time.time()
    MyNonPublic = nonPublic()

    if MySet.Usage == "Twitch Chat":
        MySet.Usage = "Stream Chat"
        Settings.Save(MySet, settingsfile)

    elif MySet.Usage == "Twitch Whisper":
        MySet.Usage = "Stream Whisper"
        Settings.Save(MySet, settingsfile)

    elif MySet.Usage == "Twitch Both":
        MySet.Usage = "Stream Both"
        Settings.Save(MySet, settingsfile)

    global jackpot
    jackpot = MySet.Jackpot


def Execute(data):
    """Required Execute data function"""
    username = data.User

    player = Player(username, Parent.GetPoints(username))

    player.playerLoad()

    if data.GetParam(0).lower() == "!Profile".lower():
        show_statistics(player)

    if data.GetParam(0).lower() == "!StartNewVote".lower():
        test = data.GetParam()
        Parent.SendStreamMessage(test)

    """Gamble Execution"""
    if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():

        if not IsFromValidSource(data, MySet.Usage):
            return

        if Parent.GetPoints(data.User) == 0:
            message = MySet.NoCurrency.format(data.UserName)
            SendResp(data, MySet.Usage, message)
            return

        if not HasPermission(data):
            return

        if not MySet.OnlyLive or Parent.IsLive():

            if IsOnCooldown(data):
                return

            global gambleInt

            gambleInt = data.GetParam(1)

            if data.GetParam(1).lower() == "min".lower() or data.GetParam(1).lower() == "minimum".lower():
                gambleInt = player.getMinBet()

            if MySet.UseRandom:
                max_random = int(Parent.GetPoints(data.User) * MySet.RandomMax / 100 + 1)
                min_random = int(Parent.GetPoints(data.User) * MySet.RandomMin / 100)
                gambleInt = Parent.GetRandom(min_random, max_random)

            elif MySet.ForceAll:
                gambleInt = int(Parent.GetPoints(data.User))

            if RegBet.search(data.GetParam(1)) and "%" in data.GetParam(1):
                gambleInt = int(data.GetParam(1).replace("%", "")) * Parent.GetPoints(data.User) / 100
                if gambleInt < 1 or gambleInt > Parent.GetPoints(data.User):
                    return
                Parent.Log(ScriptName, str(gambleInt))

            if "/" in data.GetParam(1):
                gambleInt = int(Parent.GetPoints(data.User) * float(Fraction(data.GetParam(1))))
                if gambleInt < 1 or gambleInt > Parent.GetPoints(data.User):
                    return
                Parent.Log(ScriptName, str(gambleInt))

            try:
                gambleInt = int(gambleInt)

            except ValueError:
                set_bet = MySet.UseRandom or MySet.ForceAll

                if data.GetParam(1).lower() == MySet.AllWord.lower() and not set_bet:
                    gambleInt = Parent.GetPoints(data.User)

                elif data.GetParam(1).lower() == MySet.JackpotWord and MySet.JackpotCheck:

                    message = MySet.JackpotResponse.format(MakeHumanReadable(jackpot), Parent.GetCurrencyName())
                    SendResp(data, MySet.Usage, message)
                    return

                elif data.GetParam(1).lower() == "half".lower():
                    gambleInt = int(Parent.GetPoints(data.User)/2)

                elif data.GetParam(1).lower() == "random".lower():
                    randValue = Parent.GetPoints(data.User)
                    gambleInt = random.randint(player.getMinBet(),randValue)

                else:
                    return

            try:
                int(gambleInt)
                if int(gambleInt) < 1:
                    SendResp(data, MySet.Usage, MySet.NoZero.format(data.UserName))
                    return

            except ValueError:
                pass

            if MySet.Mode == "Revlo":
                Revlo(data)

            elif MySet.Mode == "Revlo Advanced":
                RevloAdvanced(data, player)

    """Betting"""
    if data.GetParam(0).lower() == MySettings.StartBets.lower():
        HasPerm = Parent.HasPermission(data.User, MySettings.AdminPermission, MySettings.PermissionInfo)
        if HasPerm:
            openBet(data)
    elif data.GetParam(0).lower() == MySettings.StopBets.lower():
        HasPerm = Parent.HasPermission(data.User, MySettings.AdminPermission, MySettings.PermissionInfo)
        if HasPerm:
            closeBet(data)
    elif data.GetParam(0).lower() == MySettings.PayOutCommand.lower():
        HasPerm = Parent.HasPermission(data.User, MySettings.AdminPermission, MySettings.PermissionInfo)
        if HasPerm:
            payOut(data)
        else:
            Parent.SendStreamMessage("You do not have permission to do that.")
    elif data.GetParam(0).lower() == MySettings.AbortCommand.lower():
        HasPerm = Parent.HasPermission(data.User, MySettings.AdminPermission, MySettings.PermissionInfo)
        if HasPerm:
            abort(data)
    elif data.GetParam(0).lower() == MySettings.BetCommand.lower():
        HasPerm = Parent.HasPermission(data.User, MySettings.BetPermission, MySettings.PermissionInfo)
        if HasPerm:
            placeBet(data, player)
    return

def Tick():
    """Required tick function"""
    if MySettings.Enabled is True and (Parent.IsLive() or not MySettings.OnlyLive):
        global lastPayoutTime, jackpot_tick
        if time.time() - lastPayoutTime > MySettings.Interval:
            lastPayoutTime = time.time()
            for viewers in Parent.GetViewerList():
                if os.path.exists(
                        "C:\Users\Owner\AppData\Roaming\Streamlabs\Streamlabs Chatbot\Services\Games\QueueClicker2\Users\{}.txt".format(
                            viewers)):
                    username = str(viewers)
                    player = Player(username, Parent.GetPoints(viewers))
                    player.playerLoad()
                    base_payout_tick = MySettings.BasePayout

                    point_output = player.getPointModifier() + base_payout_tick

                    Parent.AddPoints(viewers, viewers, point_output)

                    if Parent.GetPoints(viewers) < 0:
                        point_offset = Parent.GetPoints(viewers) * -1
                        Parent.AddPoints(viewers, viewers, point_offset)

                    level_up_message = player.levelUpCheck()
                    if level_up_message != "":
                        Parent.SendStreamMessage(level_up_message)

                    if player.exp < player.getMinBet():
                        point_minimum_offset = player.getMinBet() - player.exp
                        Parent.AddPoints(viewers, viewers, point_minimum_offset)

                    player.playerSave()


# ---------------------------------------
# Functions for all game modes
# ---------------------------------------
def Revlo(data):
    """Revlo game mode function"""
    global gambleInt
    if Parent.GetPoints(data.User) < int(gambleInt):
        NotEnoughResp(data)
        return

    roll_value = Parent.GetRandom(1, 101)

    Parent.RemovePoints(data.User, data.UserName, gambleInt)

    if int(roll_value) == int(MySet.JackpotNumber) and MySet.JackpotEnabled:
        HandleJackpot(data, roll_value, gambleInt)
        return

    if roll_value >= 99:
        HandleTripleWin(data, roll_value, gambleInt, player)

    elif roll_value >= 61:
        HandleWin(data, roll_value, gambleInt, player)

    else:
        HandleLoss(data, roll_value, gambleInt)

    AddCooldown(data)

def RevloAdvanced(data, player):
    """Revlo Advanced game mode function"""
    if MySet.MaxBet < gambleInt and MySet.MaxBet != 0:
        MaxBetResp(data, MySet.MaxBet)
        return

    if player.getMinBet() > gambleInt:
        MinBetResp(data, player.getMinBet())
        return

    if Parent.GetPoints(data.User) < gambleInt:
        NotEnoughResp(data)
        return

    roll_value = Parent.GetRandom(MySet.MinValue, MySet.MaxValue + 1)

    Parent.RemovePoints(data.User, data.UserName, gambleInt)

    triple_win = MySet.MaxValue - MySet.MaxValue * MySet.TripleChance / 100

    if int(roll_value) == int(MySet.JackpotNumber) and MySet.JackpotEnabled:
        HandleJackpot(data, roll_value, gambleInt)
        return

    if roll_value > triple_win and MySet.TripleWinEnabled:
        HandleTripleWin(data, roll_value, gambleInt, player)

    elif roll_value > int(MySet.MaxValue - MySet.MaxValue * MySet.WinChance / 100):
        HandleWin(data, roll_value, gambleInt, player)

    else:
        HandleLoss(data, roll_value, gambleInt)

    AddCooldown(data)

def MakeHumanReadable(n):
    millnames = ['', ' K', ' M', ' B', ' T', ' Qua', ' Qui', ' S', ' Sep', ' O', ' N', ' D', ' Ud', ' Dd', ' Td', ' Qd',
                 ' Qud', ' Sd', ' Spd', ' Od', ' Nd', ' V']
    n = float(n)
    millidx = max(0, min(len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    if n < 10000:
        return '{:,}'.format(int(n))
    return '{:.2f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

def MakeHumanReadableSecond(n):
    n = float(n)
    millnames = ['', ' K', ' M', ' B', ' T', ' Qua', ' Qui', ' S', ' Sep', ' O', ' N', ' D', ' Ud', ' Dd', ' Td', ' Qd',
                 ' Qud', ' Sd', ' Spd', ' Od', ' Nd', ' V']
    millidx = max(0, min(len(millnames) - 1, int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
    if n < 10000:
        return '{:.2f}'.format(float(n))
    return '{:.2f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

def openBet(data):
    global MySettings
    global MyNonPublic

    if(MyNonPublic.isBetOpen == False and MyNonPublic.Bets == {} and MyNonPublic.PayedOut == False):
        MyNonPublic.isBetOpen = True
        openBetMessage = MySettings.BetsOpenResponse.format()
        Parent.SendTwitchMessage(openBetMessage)
        MyNonPublic.TimeToClose = time.time() + MySettings.BettingTime;
    return

def closeBet(data):
    global MySettings
    global MyNonPublic

    if(MyNonPublic.isBetOpen == True):
        MyNonPublic.isBetOpen = False
        MyNonPublic.PayedOut = True
        if(MyNonPublic.Pot < MySettings.DismissBasePot):
            for key, value in MyNonPublic.Bets.iteritems():
                MyNonPublic.Pot += MySettings.BasePot * int(value)/100
        closeBetMessage = MySettings.BetsCloseResponse.format()
        Parent.SendTwitchMessage(closeBetMessage)

    return

def abort(data):
    global MyNonPublic

    if(data.GetParam(0) == MySettings.AbortCommand and (MyNonPublic.isBetOpen == True or MyNonPublic.PayedOut == True)):
        for key, value in MyNonPublic.Bets.iteritems():
            Parent.AddPoints(key, int(value))
        MyNonPublic.isBetOpen = False
        MyNonPublic.PayedOut = False
        MyNonPublic.Pot = 0
        MyNonPublic.WinPot = 0
        MyNonPublic.LossPot = 0
        MyNonPublic.Bets.clear()
        MyNonPublic.Win.clear()
        MyNonPublic.Loss.clear()
        abortMessage = MySettings.AbortResponse.format()
        Parent.SendTwitchMessage(abortMessage)
    return

def placeBet(data, player):
    global MySettings
    global MyNonPublic
    if player.level <= 5:
        min_bet_value = MySet.MinBet
    else:
        min_bet_value = ((player.level - 1) * 100)

    if(data.GetParam(1) != "yes" and data.GetParam(1) != "no"):
        commandMessage = MySettings.CommandResponse.format(MySettings.BetCommand)
        Parent.SendTwitchMessage(commandMessage)
    if(MyNonPublic.isBetOpen == True):
        if(data.GetParam(1) == "yes"):
            try:
                int(data.GetParam(2))
            except ValueError:
                commandMessage = MySettings.CommandResponse.format(MySettings.BetCommand)
                Parent.SendTwitchMessage(commandMessage)
            else:
                if(MyNonPublic.Bets.has_key(data.User) == False and Parent.GetPoints(data.User) >= int(data.GetParam(2))):
                    if(int(data.GetParam(2)) >= min_bet_value):
                        Parent.RemovePoints(data.User,int(data.GetParam(2)))
                        MyNonPublic.Win[data.User] = data.GetParam(2)
                        MyNonPublic.Bets[data.User] = data.GetParam(2)
                        MyNonPublic.WinPot = MyNonPublic.WinPot + int(data.GetParam(2))
                        MyNonPublic.Pot = MyNonPublic.Pot + int(data.GetParam(2))
                        Parent.SendStreamMessage("{0} bet {1} {2} on {3}! Good luck bud".format(Parent.GetDisplayName(player.username), MakeHumanReadable(data.GetParam(2)), Parent.GetCurrencyName(), data.GetParam(1)))
                    else:
                        btwMsg = MySettings.CurrencyResponse.format(min_bet_value, Parent.GetCurrencyName())
                        Parent.SendTwitchMessage(btwMsg)
                elif MyNonPublic.Bets.has_key(data.User) == True:
                    alreadyMessage = MySettings.alreadyResponse.format(data.User)
                    Parent.SendTwitchMessage(alreadyMessage)
                else:
                    notEnoughMessage = MySettings.NotEnoughResponse.format(data.User, Parent.GetCurrencyName(), MySettings.BetCommand)
                    Parent.SendTwitchMessage(notEnoughMessage)
        elif(data.GetParam(1) == "no"):
            try:
                int(data.GetParam(2))
            except ValueError:
                commandMessage = MySettings.CommandResponse.format(MySettings.BetCommand)
                Parent.SendTwitchMessage(commandMessage)
            else:
                if(MyNonPublic.Bets.has_key(data.User) == False and Parent.GetPoints(data.User) >= int(data.GetParam(2))):
                    if(int(data.GetParam(2)) >= min_bet_value):
                        Parent.RemovePoints(data.User,int(data.GetParam(2)))
                        MyNonPublic.Loss[data.User] = data.GetParam(2)
                        MyNonPublic.Bets[data.User] = data.GetParam(2)
                        MyNonPublic.LossPot = MyNonPublic.LossPot + int(data.GetParam(2))
                        MyNonPublic.Pot = MyNonPublic.Pot + int(data.GetParam(2))
                        Parent.SendStreamMessage(
                            "{0} bet {1} {2} on {3}! Good luck bud".format(Parent.GetDisplayName(player.username),
                                                                           MakeHumanReadable(data.GetParam(2)), Parent.GetCurrencyName(),
                                                                           data.GetParam(1)))
                    else:
                        btwMsg = MySettings.CurrencyResponse.format(min_bet_value, Parent.GetCurrencyName())
                        Parent.SendTwitchMessage(btwMsg)
                elif MyNonPublic.Bets.has_key(data.User) == True:
                    alreadyMessage = MySettings.alreadyResponse.format(data.User)
                    Parent.SendTwitchMessage(alreadyMessage)
                else:
                    notEnoughMessage = MySettings.NotEnoughResponse.format(data.User, Parent.GetCurrencyName(), MySettings.BetCommand)
                    Parent.SendTwitchMessage(notEnoughMessage)
    return


def payOut(data):
    global MySettings
    global MyNonPublic

    if (MyNonPublic.isBetOpen == False and MyNonPublic.PayedOut == True and data.GetParam(
            0) == MySettings.PayOutCommand) and (data.GetParam(1) == "yes" or data.GetParam(1) == "no"):
        if (data.GetParam(1) == "yes" and len(MyNonPublic.Win) > 0):
            winMessage = ""
            for key, value in MyNonPublic.Win.iteritems():
                player = Player(key, Parent.GetPoints(key))
                player.playerLoad()

                #give more points for prestiging
                prestige_buff = 0.2*player.prestige

                amount = int((int(value) / float(MyNonPublic.WinPot) * MyNonPublic.Pot)*(1+prestige_buff))

                #add points for winning
                Parent.AddPoints(key, amount)
                if (winMessage == ""):
                    winMessage += key + "( " + str(MakeHumanReadable(amount)) + " )"
                else:
                    winMessage += " ," + key + "( " + str(MakeHumanReadable(amount)) + " )"

            MyNonPublic.PayedOut = False

            POwinMessage = MySettings.PayOutResponse.format(winMessage)
            Parent.SendTwitchMessage(POwinMessage)
        elif (data.GetParam(1) == "no" and len(MyNonPublic.Loss) > 0):
            lossMessage = ""
            for key, value in MyNonPublic.Loss.iteritems():
                player = Player(key, Parent.GetPoints(key))
                player.playerLoad()

                #give more points for prestiging
                prestige_buff = 0.2*player.prestige

                #Allows players of low prestiges to still yield profit in the event of a solo vote
                if prestige_buff <= 0.6:
                    prestige_buff = 0.6

                amount = 2 * (int((int(value) / float(MyNonPublic.LossPot) * MyNonPublic.Pot)*(1 + prestige_buff)))

                #add points for winning
                Parent.AddPoints(key, amount)
                if (lossMessage == ""):
                    lossMessage += key + "( " + str(MakeHumanReadable(amount)) + " )"
                else:
                    lossMessage += " ," + key + "( " + str(MakeHumanReadable(amount)) + " )"

            MyNonPublic.PayedOut = False

            POlossMessage = MySettings.PayOutResponse.format(lossMessage)
            Parent.SendTwitchMessage(POlossMessage)
        elif ((data.GetParam(1) == "yes" or data.GetParam(1) == "no") and len(MyNonPublic.Bets) == 0):
            MyNonPublic.PayedOut = False
            NoWinnerMessage = MySettings.NoWinnerResponse.format()
            Parent.SendTwitchMessage(NoWinnerMessage)
        MyNonPublic.Pot = 0
        MyNonPublic.WinPot = 0
        MyNonPublic.LossPot = 0
        MyNonPublic.Bets.clear()
        MyNonPublic.Win.clear()
        MyNonPublic.Loss.clear()
    return



# ---------------------------------------
# Game functions
# ---------------------------------------
def show_statistics(player):
    EXP = player.exp
    level = player.level
    level_cap = player.level_cap
    prestige_in = level_cap - level
    points_per_second = float(player.getPointModifier()/10)
    points_to_level_up = player.pointsToLevelUp()
    prestige = player.prestige
    prestige_buff = (player.prestige*20)
    minimum_bet = player.getMinBet()

    Parent.SendStreamWhisper(
        player.username, "Prestige: {0} (+{1}%) | Lvl: {2} | EXP: {3} / {4} | Prestige in: {5} lvls | Minimum Bet: {6} | EXP/s: {7}".format(
                                                                 prestige, prestige_buff, level, MakeHumanReadable(EXP),
                              MakeHumanReadable(points_to_level_up), prestige_in, minimum_bet, points_per_second))
    return

def is_vote_active(data, vote_flag, yes_or_no, amount):
    if vote_flag:
        vote_execute(yes_or_no, amount)
    else:
        Parent.SendStreamMessage("Didn't make it")

def vote_execute(yes_or_no, amount):
    Parent.SendStreamMessage("We made it")

def MaxBetResp(data, maxbet):
    """Send message about maximum bet size"""
    currency = Parent.GetCurrencyName()
    maxBetMessage = MySet.TooMuchResponse.format(data.UserName, maxbet, currency)

    SendResp(data, MySet.Usage, maxBetMessage)


def MinBetResp(data, min_bet_value):
    """Send message about minimum bet size"""
    currency = Parent.GetCurrencyName()
    minBetMessage = MySet.TooLowResponse.format(data.UserName, min_bet_value, currency)

    SendResp(data, MySet.Usage, minBetMessage)


def NotEnoughResp(data):
    """Send message about not having enough currency"""
    currency = Parent.GetCurrencyName()
    notEnough = MySet.NotEnoughResponse.format(data.UserName, currency, MySet.Command)
    SendResp(data, MySet.Usage, notEnough)


def AddCooldown(data):
    """add cooldowns"""
    if Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD:
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)
        return

    else:
        Parent.AddUserCooldown(ScriptName, MySet.Command, data.User, MySet.UserCooldown)
        Parent.AddCooldown(ScriptName, MySet.Command, MySet.Cooldown)


def IsOnCooldown(data):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    cooldown = Parent.IsOnCooldown(ScriptName, MySet.Command)
    userCooldown = Parent.IsOnUserCooldown(ScriptName, MySet.Command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and MySet.CasterCD)

    if (cooldown or userCooldown) and caster is False:

        if MySet.UseCD:
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, MySet.Command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, MySet.Command, data.User)

            if cooldownDuration > userCDD:
                m_CooldownRemaining = cooldownDuration

                message = MySet.OnCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)

            else:
                m_CooldownRemaining = userCDD

                message = MySet.OnUserCooldown.format(data.UserName, m_CooldownRemaining)
                SendResp(data, MySet.Usage, message)
        return True
    return False


def HasPermission(data):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, MySet.Permission, MySet.PermissionInfo):
        message = MySet.PermissionResp.format(data.UserName, MySet.Permission, MySet.PermissionInfo)
        SendResp(data, MySet.Usage, message)
        return False
    return True

# ---------------------------------------
# Game outcomes
# ---------------------------------------
def HandleJackpot(data, roll, bet):
    """Handle jackpot"""
    global jackpot
    Parent.AddPoints(data.User, data.UserName, bet)
    Parent.AddPoints(data.User, data.UserName, jackpot)

    points = MakeHumanReadable(Parent.GetPoints(data.User))
    currency = Parent.GetCurrencyName()
    jackpot_human_readable = MakeHumanReadable(jackpot)

    jackpotMessage = MySet.JackpotWin.format(data.UserName, jackpot_human_readable, points, currency)
    message = MySet.BaseResponse.format(roll, data.UserName)
    SendResp(data, MySet.Usage, message + jackpotMessage)

    MySet.Jackpot = MySet.JackpotBase
    Settings.Save(MySet, settingsfile)
    jackpot = MySet.Jackpot

    with open(jackpotFile, "w+") as f:
        f.write(str(jackpot))


def HandleTripleWin(data, roll, bet, player):
    """Handle triple wins!"""

    prestige_buff = 1 + (player.prestige * 0.2)
    currency = Parent.GetCurrencyName()
    winnings = MakeHumanReadable(((bet * 2) + (bet * prestige_buff)))
    winnings_int = ((bet * 2) + (bet * prestige_buff))

    Parent.AddPoints(data.User, data.UserName, winnings_int)
    points = MakeHumanReadable(Parent.GetPoints(data.User))

    winMessage = MySet.WinResponse.format(data.UserName, winnings, points, currency)

    SendResp(data, MySet.Usage, MySet.BaseResponse.format(roll, data.UserName) + winMessage)


def HandleWin(data, roll, bet, player):
    """Handle wins, adding points and sending message"""

    prestige_buff = 1 + (player.prestige * 0.2)
    currency = Parent.GetCurrencyName()
    winnings_int = (bet + (bet * prestige_buff))
    winnings = MakeHumanReadable((bet + (bet * prestige_buff)))

    Parent.AddPoints(data.User, data.UserName, winnings_int)
    points = MakeHumanReadable(Parent.GetPoints(data.User))

    winMessage = MySet.WinResponse.format(data.UserName, winnings, points, currency)

    SendResp(data, MySet.Usage, MySet.BaseResponse.format(roll, data.UserName) + winMessage)


def HandleLoss(data, roll, bet):
    """Handle loss message"""
    global jackpot
    global MySet

    jackpot += int(bet * MySet.JackpotPercentage / 100)
    MySet.Jackpot = jackpot
    MySet.Save(settingsfile)

    with open(jackpotFile, "w+") as f:
        f.write(str(jackpot))

    points = MakeHumanReadable(Parent.GetPoints(data.User))
    currency = Parent.GetCurrencyName()
    losings = MakeHumanReadable(bet)

    loseMessage = MySet.LoseResponse.format(data.UserName, losings, points, currency, MySet.Jackpot)

    SendResp(data, MySet.Usage, MySet.BaseResponse.format(roll, data.UserName) + loseMessage)
