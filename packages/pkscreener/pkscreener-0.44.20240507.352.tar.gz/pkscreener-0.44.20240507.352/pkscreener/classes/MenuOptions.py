"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""
from enum import Enum

from PKDevTools.classes.ColorText import colorText
from PKDevTools.classes.log import default_logger
from PKDevTools.classes.OutputControls import OutputControls
import pkscreener.classes.ConfigManager as ConfigManager
from pkscreener.classes.OtaUpdater import OTAUpdater
from pkscreener.classes import VERSION

configManager = ConfigManager.tools()
MENU_SEPARATOR = ""
LINE_SEPARATOR = "\n"

level0MenuDict = {
    "X": "Scanners",
    "M": "Monitor Intraday",
    "S": "Strategies",
    "B": "Backtests",
    "G": "Growth of 10k",
    "C": "Analyse morning vs close outcomes",
    "T": "~",
    "D": "Download Daily OHLC Data for the Past Year",
    "I": "Download Intraday OHLC Data for the Last Trading Day",
    "E": "Edit user configuration",
    "Y": "View your user configuration",
    "U": "Check for software update",
    "L": "Collect Logs for Debugging",
    "H": "Help / About Developer",
    "Z": "Exit (Ctrl + C)",
}
level1_S_MenuDict = {
    "S": "Summary",
    "M": "Back to the Top/Main menu",
    "Z": "Exit (Ctrl + C)",
}
level1_X_MenuDict = {
    "W": "Screen stocks from my own Watchlist",
    "N": "Nifty Prediction using Artifical Intelligence (Use for Gap-Up/Gap-Down/BTST/STBT)",
    "E": "Live Index Scan : 5 EMA for Intraday",
    "0": "Screen stocks by the stock names (NSE Stock Code)",
    "1": "Nifty 50          ",
    "2": "Nifty Next 50     ",
    "3": "Nifty 100         ",
    "4": "Nifty 200         ",
    "5": "Nifty 500         ",
    "6": "Nifty Smallcap 50 ",
    "7": "Nifty Smallcap 100",
    "8": "Nifty Smallcap 250",
    "9": "Nifty Midcap 50   ",
    "10": "Nifty Midcap 100",
    "11": "Nifty Midcap 150 ",
    "12": "Nifty (All Stocks)",
    "13": "Newly Listed (IPOs in last 2 Year)           ",
    "14": "F&O Stocks Only",
    "15": "NASDAQ",
    "M": "Back to the Top/Main menu",
    "Z": "Exit (Ctrl + C)",
}
level2_X_MenuDict = {
    "0": "Full Screening (Shows Technical Parameters without any criterion)",
    "1": "Probable Breakouts/Breakdowns   ",
    "2": "Today's Breakouts/Breakdowns",
    "3": "Consolidating stocks            ",
    "4": "Lowest Volume in last N-days (Early Breakout Detection)",
    "5": "RSI screening                   ",
    "6": "Reversal Signals",
    "7": "Stocks making Chart Patterns    ",
    "8": "CCI outside of the given range",
    "9": "Volume gainers                  ",
    "10": "Closing at least 2% up since last 3 days",
    "11": "Short term bullish (Ichimoku)  ",
    "12": "N-Minute Price & Volume breakout(Intraday)",
    "13": "Bullish RSI & MACD             ",
    "14": "NR4 Daily Today",
    "15": "52 week low breakout(today)(Sell)",
    "16": "10 days low breakout(Sell)",
    "17": "52 week high breakout(today)     ",
    "18": "Bullish Aroon(14) Crossover",
    "19": "MACD Histogram x below 0 (Sell) ",
    "20": "Bullish for next day",
    "21": "MF/FIIs Popular Stocks         ",
    "22": "View Stock Performance         ",
    "23": "Breaking out now               ",
    "24": "Higher Highs,Lows & Close (SuperTrend)",
    "25": "Lower Highs,Lows (Watch for Rev.)",
    "26": "Stocks with stock-split/bonus/dividends",
    "27": "ATR Cross                      ",
    "28": "Bullish Higher Opens           ",
    # "27": "Intraday Momentum Build-up      ",
    # "28": "Extremely bullish daily close      ",
    # "29": "Rising RSI                      ",
    # "30": "RSI entering bullish territory",
    "42": "Show Last Screened Results",
    "M": "Back to the Top/Main menu",
    "Z": "Exit (Ctrl + C)",
}
level3_X_Reversal_MenuDict = {
    "1": "Buy Signals (Bullish Reversal)",
    "2": "Sell Signals (Bearish Reversal)",
    "3": "Momentum Gainers (Rising Bullish Momentum)",
    "4": "Reversal at Moving Average (Bullish Reversal)",
    "5": "Volume Spread Analysis (Bullish VSA Reversal)",
    "6": "Narrow Range (NRx) Reversal",
    "7": "Lorentzian Classifier (Machine Learning based indicator)",
    "8": "PSAR and RSI reversal",
    "9": "Rising RSI",
    "10": "RSI MA Reversal",
    "0": "Cancel",
}
level3_X_ChartPattern_MenuDict = {
    "1": "Bullish Inside Bar (Flag) Pattern",
    "2": "Bearish Inside Bar (Flag) Pattern(Sell)",
    "3": "The Confluence (50 & 200 MA/EMA)",
    "4": "VCP (Volatility Contraction Pattern)",
    "5": "Buying at Trendline (Ideal for Swing/Mid/Long term)",
    "6": "Bollinger Bands (TTM) Squeeze",
    "7": "Candle-stick Patterns",
    "0": "Cancel",
}

level4_X_ChartPattern_BBands_SQZ_MenuDict = {
    "1": "TTM Squeeze-Buy",
    "2": "TTM In-Squeeze",
    "3": "TTM Squeeze-Sell",
    "4": "All/Any",
    "0": "Cancel",
}

level4_X_ChartPattern_Confluence_MenuDict = {
    "1": "Confluence up / GoldenCrossOver / DMA50 / DMA200",
    "2": "Confluence Down / DeadCrossOver",
    "3": "Any/All",
    "0": "Cancel",
}

level3_X_PopularStocks_MenuDict = {
    "1": "Shares bought/sold by Mutual Funds/FIIs (M*)",
    "2": "Shareholding by number of Mutual Funds/FIIs (M*)",
    "3": "MF/FIIs Net Ownership Increased",
    "4": "Dividend Yield (M*)",
    "5": "Only MF Net Ownership Increased",
    "6": "Only MF Net Ownership Decreased",
    "7": "MF/FIIs Net Ownership Decreased",
    "8": "Fair Value Buy Opportunities",
    "9": "Fair Value Sell Opportunities",
    "0": "Cancel",
}

level3_X_StockPerformance_MenuDict = {
    "1": "Short term",
    "2": "Medium term",
    "3": "Long term",
    "0": "Cancel",
}

level4_X_Lorenzian_MenuDict = {
    "1": "Buy",
    "2": "Sell",
    "3": "Any/All",
    "0": "Cancel",
}


class MenuRenderStyle(Enum):
    STANDALONE = 1
    TWO_PER_ROW = 2
    THREE_PER_ROW = 3


class menu:
    def __init__(self):
        self.menuKey = ""
        self.menuText = ""
        self.submenu = None
        self.level = 0
        self.isException = None
        self.hasLeftSibling = False
        self.parent = None
        self.line = 0
        self.lineIndex = 0

    def create(self, key, text, level=0, isException=False, parent=None):
        self.menuKey = str(key)
        self.menuText = text
        self.level = level
        self.isException = isException
        self.parent = parent
        self.line = 0
        self.lineIndex = 0
        return self

    def keyTextLabel(self):
        return f"{MENU_SEPARATOR}{self.menuKey} > {self.menuText}"

    def commandTextKey(self, hasChildren=False):
        cmdText = ""
        if self.parent is None:
            cmdText = f"/{self.menuKey}"
            return cmdText
        else:
            cmdText = f"{self.parent.commandTextKey(hasChildren=True)}_{self.menuKey}"
            return cmdText

    def commandTextLabel(self, hasChildren=False):
        cmdText = ""
        if self.parent is None:
            cmdText = f"{self.menuText}" if hasChildren else f"{self.menuText}"
            return cmdText
        else:
            cmdText = (
                f"{self.parent.commandTextLabel(hasChildren=True)} > {self.menuText}"
            )
            return f"{cmdText}"

    def render(self,coloredValues=[]):
        t = ""
        if self.isException:
            if self.menuText.startswith("~"):
                self.menuText = self.renderSpecial(self.menuKey)
            t = f"\n\n     {self.keyTextLabel()}"
        elif not self.menuKey.isnumeric():
            t = f"\n     {self.keyTextLabel()}"
        else:
            # 9 to adjust an extra space when 10 becomes a 2 digit number
            spaces = "     " if int(self.menuKey) <= 9 else "    "
            if not self.hasLeftSibling:
                t = f"\n{spaces}{self.keyTextLabel()}"
            else:
                t = f"\t{self.keyTextLabel()}"
        if coloredValues is not None and str(self.menuKey) in coloredValues:
            t = f"{colorText.FAIL}{t}{colorText.END}"
        return t

    def renderSpecial(self, menuKey):
        configManager.getConfig(ConfigManager.parser)
        menuText = "~"
        if self.level == 0 and menuKey == "T":
            menuText = (
                "Toggle between long-term (Default)"
                + colorText.WARN
                + " [Current]"
                + colorText.END
                + " and Intraday user configuration\n"
                if not configManager.isIntradayConfig()
                else "Toggle between long-term (Default) and Intraday"
                + colorText.WARN
                + " [Current]"
                + colorText.END
                + " user configuration"
            )
        return menuText


# This Class manages application menus
class menus:
    
    @staticmethod
    def allMenus(topLevel="X",index=12):
        menuOptions = [topLevel]
        indexOptions =[index]
        scanOptions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,23,24,25,27,28]
        scanSubOptions = {
                            6:[1,2,3,4,5,6,{7:[1,2]},8,9],
                            7:[1,2,{3:[1,2]},4,5,{6:[1,3]},7],
                            # 21:[3,5,6,7,8,9]
                         }
        runOptions = []
        for menuOption in menuOptions:
            for indexOption in indexOptions:
                for scanOption in scanOptions:
                    if scanOption in scanSubOptions.keys():
                        for scanSubOption in scanSubOptions[scanOption]:
                            if isinstance(scanSubOption, dict):
                                for childLevelOption in scanSubOption.keys():
                                    for value in scanSubOption[childLevelOption]:
                                        runOption = f"{menuOption}:{indexOption}:{scanOption}:{childLevelOption}:{value}:D:D:D:D:D"
                                        runOptions.append(runOption)
                            else:
                                runOption = f"{menuOption}:{indexOption}:{scanOption}:{scanSubOption}:D:D:D:D:D"
                                runOptions.append(runOption)
                    else:
                        runOption = f"{menuOption}:{indexOption}:{scanOption}:D:D:D:D:D"
                        runOptions.append(runOption)
        return runOptions

    def __init__(self):
        self.level = 0
        self.menuDict = {}
        self.strategyNames = []

    def fromDictionary(
        self,
        rawDictionary={},
        renderStyle=MenuRenderStyle.STANDALONE,
        renderExceptionKeys=[],
        skip=[],
        parent=None,
    ):
        tabLevel = 0
        self.menuDict = {}
        line = 0
        lineIndex = 1
        for key in rawDictionary:
            if skip is not None and key in skip:
                continue
            m = menu()
            m.create(
                str(key).upper(), rawDictionary[key], level=self.level, parent=parent
            )
            if key in renderExceptionKeys:
                m.isException = True
                line += 2
                lineIndex = 1
                m.line = line
                m.lineIndex = lineIndex
            elif str(key).isnumeric():
                m.hasLeftSibling = False if tabLevel == 0 else True
                if tabLevel == 0:
                    line += 1
                lineIndex = tabLevel + 1
                m.line = line
                m.lineIndex = lineIndex
                tabLevel = tabLevel + 1
                if tabLevel >= renderStyle.value:
                    tabLevel = 0
            else:
                line += 1
                lineIndex = 1
                m.line = line
                m.lineIndex = lineIndex
            self.menuDict[str(key).upper()] = m
        return self

    def render(self, asList=False, coloredValues=[]):
        menuText = [] if asList else ""
        for k in self.menuDict.keys():
            m = self.menuDict[k]
            if asList:
                menuText.append(m)
            else:
                menuText = menuText + m.render(coloredValues=([] if asList else coloredValues))
        return menuText

    def renderForMenu(self, selectedMenu=None, skip=[], asList=False, renderStyle=None):
        if selectedMenu is None and self.level == 0:
            # Top level Application Main menu
            return self.renderLevel0Menus(
                skip=skip, asList=asList, renderStyle=renderStyle, parent=selectedMenu
            )
        elif selectedMenu is not None:
            if selectedMenu.menuKey == "S":
                    return self.renderLevel1_S_Menus(
                    skip=skip,
                    asList=asList,
                    renderStyle=renderStyle,
                    parent=selectedMenu,
                )
            if selectedMenu.level == 0:
                self.level = 1
                # sub-menu of the top level main selected menu
                return self.renderLevel1_X_Menus(
                    skip=skip,
                    asList=asList,
                    renderStyle=renderStyle,
                    parent=selectedMenu,
                )
            elif selectedMenu.level == 1:
                self.level = 2
                # next levelsub-menu of the selected sub-menu
                return self.renderLevel2_X_Menus(
                    skip=skip,
                    asList=asList,
                    renderStyle=renderStyle,
                    parent=selectedMenu,
                )
            elif selectedMenu.level == 2:
                self.level = 3
                # next levelsub-menu of the selected sub-menu
                if selectedMenu.menuKey == "6":
                    return self.renderLevel3_X_Reversal_Menus(
                        skip=skip,
                        asList=asList,
                        renderStyle=renderStyle,
                        parent=selectedMenu,
                    )
                elif selectedMenu.menuKey == "7":
                    return self.renderLevel3_X_ChartPattern_Menus(
                        skip=skip,
                        asList=asList,
                        renderStyle=renderStyle,
                        parent=selectedMenu,
                    )
                elif selectedMenu.menuKey == "21":
                    return self.renderLevel3_X_PopularStocks_Menus(
                        skip=skip,
                        asList=asList,
                        renderStyle=renderStyle,
                        parent=selectedMenu,
                    )
                elif selectedMenu.menuKey == "22":
                    return self.renderLevel3_X_StockPerformance_Menus(
                        skip=skip,
                        asList=asList,
                        renderStyle=renderStyle,
                        parent=selectedMenu,
                    )
            elif selectedMenu.level == 3:
                self.level = 4
                # next levelsub-menu of the selected sub-menu
                if selectedMenu.parent.menuKey == "6" and selectedMenu.menuKey in ["7","10"]:
                    return self.renderLevel4_X_Lorenzian_Menus(
                        skip=skip,
                        asList=asList,
                        renderStyle=renderStyle,
                        parent=selectedMenu,
                    )
                if selectedMenu.parent.menuKey == "7" and selectedMenu.menuKey == "3":
                    return self.renderLevel4_X_ChartPattern_Confluence_Menus(
                        skip=skip,
                        asList=asList,
                        renderStyle=renderStyle,
                        parent=selectedMenu,
                    )
                if selectedMenu.parent.menuKey == "7" and selectedMenu.menuKey == "6":
                    return self.renderLevel4_X_ChartPattern_BBands_SQZ_Menus(
                        skip=skip,
                        asList=asList,
                        renderStyle=renderStyle,
                        parent=selectedMenu,
                    )
                

    def find(self, key=None):
        if key is not None:
            try:
                return self.menuDict[str(key).upper()]
            except Exception as e:  # pragma: no cover
                default_logger().debug(e, exc_info=True)
                return None
        return None

    def renderLevel0Menus(self, asList=False, renderStyle=None, parent=None, skip=None):
        menuText = self.fromDictionary(
            level0MenuDict,
            renderExceptionKeys=["T", "E", "U", "Z", "L", "D"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select a menu option:"
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

    Enter your choice > (default is """
                    + colorText.WARN
                    + self.find("X").keyTextLabel()
                    + ") "
                    "" + colorText.END
                )
                try:
                    OTAUpdater.checkForUpdate(VERSION, skipDownload=True)
                except:
                    pass
            return menuText

    def renderLevel1_S_Menus(
        self, skip=[], asList=False, renderStyle=None, parent=None
    ):
        strategies = self.strategyNames
        counter = 1
        menuDict = {}
        for strategyName in strategies:
            menuDict[f"{counter}"] = strategyName.ljust(20)
            counter += 1
        for key in level1_S_MenuDict.keys():
            menuDict[key] = level1_S_MenuDict[key]

        menuText = self.fromDictionary(
            menuDict,
            renderExceptionKeys=level1_S_MenuDict.keys(),
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.THREE_PER_ROW,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select a Strategy for Screening:"
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

    Enter your choice > """
                    ""
                )
            return menuText
        
    def renderLevel1_X_Menus(
        self, skip=[], asList=False, renderStyle=None, parent=None
    ):
        menuText = self.fromDictionary(
            level1_X_MenuDict,
            renderExceptionKeys=["W", "0", "M", "15"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.THREE_PER_ROW,
            skip=skip,
            parent=parent,
        ).render(asList=asList, coloredValues=["15"])
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an Index for Screening:"
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

    Enter your choice > (default is """
                    + colorText.WARN
                    + self.find(str(configManager.defaultIndex)).keyTextLabel()
                    + ")  "
                    "" + colorText.END
                )
            return menuText

    def renderLevel2_X_Menus(
        self, skip=[], asList=False, renderStyle=None, parent=None
    ):
        menuText = self.fromDictionary(
            level2_X_MenuDict,
            renderExceptionKeys=["0", "42", "M"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.TWO_PER_ROW,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select a Criterion for Stock Screening: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText

    def renderLevel3_X_Reversal_Menus(
        self, skip=[], asList=False, renderStyle=None, parent=None
    ):
        menuText = self.fromDictionary(
            level3_X_Reversal_MenuDict,
            renderExceptionKeys=["0"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an option: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText

    def renderLevel3_X_ChartPattern_Menus(
        self, skip=[], asList=False, renderStyle=MenuRenderStyle.STANDALONE, parent=None
    ):
        menuText = self.fromDictionary(
            level3_X_ChartPattern_MenuDict,
            renderExceptionKeys=["0"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an option: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText

    def renderLevel3_X_PopularStocks_Menus(
        self, skip=[], asList=False, renderStyle=MenuRenderStyle.STANDALONE, parent=None
    ):
        menuText = self.fromDictionary(
            level3_X_PopularStocks_MenuDict,
            renderExceptionKeys=["0"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an option: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText

    def renderLevel3_X_StockPerformance_Menus(
        self, skip=[], asList=False, renderStyle=MenuRenderStyle.STANDALONE, parent=None
    ):
        menuText = self.fromDictionary(
            level3_X_StockPerformance_MenuDict,
            renderExceptionKeys=["0"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an option: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText

    def renderLevel4_X_Lorenzian_Menus(
        self, skip=[], asList=False, renderStyle=MenuRenderStyle.STANDALONE, parent=None
    ):
        menuText = self.fromDictionary(
            level4_X_Lorenzian_MenuDict,
            renderExceptionKeys=["0"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an option: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText


    def renderLevel4_X_ChartPattern_BBands_SQZ_Menus(
        self, skip=[], asList=False, renderStyle=MenuRenderStyle.STANDALONE, parent=None
    ):
        menuText = self.fromDictionary(
            level4_X_ChartPattern_BBands_SQZ_MenuDict,
            renderExceptionKeys=["0"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an option: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText


    def renderLevel4_X_ChartPattern_Confluence_Menus(
        self, skip=[], asList=False, renderStyle=MenuRenderStyle.STANDALONE, parent=None
    ):
        menuText = self.fromDictionary(
            level4_X_ChartPattern_Confluence_MenuDict,
            renderExceptionKeys=["0"],
            renderStyle=renderStyle
            if renderStyle is not None
            else MenuRenderStyle.STANDALONE,
            skip=skip,
            parent=parent,
        ).render(asList=asList)
        if asList:
            return menuText
        else:
            if OutputControls().enableMultipleLineOutput:
                OutputControls().printOutput(
                    colorText.BOLD
                    + colorText.WARN
                    + "[+] Select an option: "
                    + colorText.END
                )
                OutputControls().printOutput(
                    colorText.BOLD
                    + menuText
                    + """

            """
                    + colorText.END
                )
            return menuText
        
# Fundamentally good compnaies but nearing 52 week low
# https://www.tickertape.in/screener/equity/prebuilt/SCR0005

# Dividend Gems
# https://www.tickertape.in/screener/equity/prebuilt/SCR0027

# Cash rich small caps
# https://www.tickertape.in/screener/equity/prebuilt/SCR0017
