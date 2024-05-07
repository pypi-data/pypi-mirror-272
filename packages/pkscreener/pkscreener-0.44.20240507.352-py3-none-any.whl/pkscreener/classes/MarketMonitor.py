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
import os
import sys
import pandas as pd
import numpy as np
from PKDevTools.classes.Singleton import SingletonType, SingletonMixin
from PKDevTools.classes.OutputControls import OutputControls
from PKDevTools.classes.ColorText import colorText
from PKDevTools.classes import Archiver
from PKDevTools.classes.SuppressOutput import SuppressOutput

class MarketMonitor(SingletonMixin, metaclass=SingletonType):
    def __init__(self,monitors=[], maxNumResultsPerRow=3,maxNumColsInEachResult=6,maxNumRowsInEachResult=10,maxNumResultRowsInMonitor=2):
        super(MarketMonitor, self).__init__()
        if monitors is not None and len(monitors) > 0:
            
            self.monitors = monitors[:maxNumResultRowsInMonitor*maxNumResultsPerRow]
            self.monitorIndex = 0
            self.monitorPositions = {}
            # self.monitorNames = {}
            # We are going to present the dataframes in a 3x3 matrix with limited set of columns
            rowIndex = 0
            colIndex = 0
            self.maxNumResultRowsInMonitor = maxNumResultRowsInMonitor
            self.maxNumRowsInEachResult = maxNumRowsInEachResult
            self.maxNumColsInEachResult = maxNumColsInEachResult
            self.maxNumResultsPerRow = maxNumResultsPerRow
            maxColIndex = self.maxNumColsInEachResult * self.maxNumResultsPerRow - 1
            self.lines = 0
            for monitorKey in self.monitors:
                self.monitorPositions[monitorKey] = [rowIndex,colIndex]
                # self.monitorNames[monitorKey] = ""
                colIndex += self.maxNumColsInEachResult
                if colIndex > maxColIndex:
                    colIndex = 0
                    rowIndex += self.maxNumRowsInEachResult
            columns = []
            colNameIndex = 0
            maxColIndex = min(maxColIndex,len(self.monitorPositions)*self.maxNumColsInEachResult -1)
            while colNameIndex <= maxColIndex:
                columns.append(f"A{colNameIndex +1}")
                colNameIndex += 1
            self.monitor_df = pd.DataFrame(columns=columns)

    def currentMonitorOption(self):
        try:
            option = None
            maxIndex = len(self.monitors) -1
            option = str(self.monitors[self.monitorIndex:self.monitorIndex+1][0])
            self.monitorIndex += 1
            if self.monitorIndex > maxIndex:
                self.monitorIndex = 0
        except:
            pass
        return option

    def refresh(self, screen_df:pd.DataFrame=None, screenOptions=None, chosenMenu=None, dbTimestamp="", telegram=False):
        highlightRows = []
        highlightCols = []
        if screen_df is None or screen_df.empty:
            return

        screen_monitor_df = screen_df.copy()
        screen_monitor_df.reset_index(inplace=True)
        screen_monitor_df = screen_monitor_df[["Stock", "LTP", "%Chng","52Wk H","RSI/i" if "RSI/i" in screen_monitor_df.columns else "RSI","Volume"]].head(self.maxNumRowsInEachResult-1)
        # Import Utility here since Utility has dependency on PKScheduler which in turn has dependency on 
        # multiprocessing, which behaves erratically if imported at the top.
        from pkscreener.classes import Utility
        screen_monitor_df.loc[:, "%Chng"] = screen_monitor_df.loc[:, "%Chng"].apply(
                    lambda x: Utility.tools.roundOff(str(x).split("% (")[0] + colorText.END,0)
                )
        screen_monitor_df.loc[:, "52Wk H"] = screen_monitor_df.loc[:, "52Wk H"].apply(
            lambda x: Utility.tools.roundOff(x,0)
        )
        screen_monitor_df.loc[:, "Volume"] = screen_monitor_df.loc[:, "Volume"].apply(
            lambda x: Utility.tools.roundOff(x,0)
        )
        screen_monitor_df.rename(columns={"%Chng": "Ch%","Volume":"Vol","52Wk H":"52WkH", "RSI":"RSI/i"}, inplace=True)
        if telegram:
            telegram_df = screen_monitor_df[["Stock", "LTP", "Ch%", "Vol"]]
            try:
                telegram_df.loc[:, "Stock"] = telegram_df.loc[:, "Stock"].apply(
                    lambda x: x.split('\x1b')[3].replace('\\','') if 'http' in x else x
                )
                cols = ["LTP", "Ch%", "Vol"]
                for col in cols:
                    telegram_df.loc[:, col] = telegram_df.loc[:, col].apply(
                        lambda x: x.replace(colorText.FAIL,"").replace(colorText.GREEN,"").replace(colorText.WARN,"").replace(colorText.BOLD,"").replace(colorText.END,"")
                    )
                telegram_df.loc[:, "LTP"] = telegram_df.loc[:, "LTP"].apply(
                    lambda x: str(int(round(float(x),0)))
                )
                telegram_df.loc[:, "Ch%"] = telegram_df.loc[:, "Ch%"].apply(
                    lambda x: f'{int(round(float(x.replace("%","")),0))}%'
                )
                telegram_df.loc[:, "Vol"] = telegram_df.loc[:, "Vol"].apply(
                    lambda x: f'{int(round(float(x.replace("x","")),0))}x'
                )
                with SuppressOutput(suppress_stderr=True, suppress_stdout=True):
                    for col in telegram_df.columns:
                        telegram_df[col] = telegram_df[col].astype(str)
            except:
                pass
        monitorPosition = self.monitorPositions.get(screenOptions)
        if monitorPosition is not None:
            startRowIndex, startColIndex = monitorPosition
            if not self.monitor_df.empty:
                for _ in range(self.lines):
                    sys.stdout.write("\x1b[1A")  # cursor up one line
                    sys.stdout.write("\x1b[2K")  # delete the last line

            firstColIndex = startColIndex
            rowIndex = 0
            colIndex = 0
            highlightRows = [startRowIndex]
            highlightCols = []
            while rowIndex <= len(screen_monitor_df):
                for col in screen_monitor_df.columns:
                    if rowIndex == 0:
                        # Column names to be repeated for each refresh in respective headers
                        cleanedScreenOptions = screenOptions.replace(":D","")
                        widgetHeader = ":".join(cleanedScreenOptions.split(":")[:4])
                        if "i " in screenOptions:
                            widgetHeader = f'{":".join(widgetHeader.split(":")[:3])}:i:{cleanedScreenOptions.split("i ")[-1]}'
                        self.monitor_df.loc[startRowIndex,[f"A{startColIndex+1}"]] = colorText.BOLD+colorText.HEAD+(widgetHeader if startColIndex==firstColIndex else col)+colorText.END
                        highlightCols.append(startColIndex)
                    else:
                        self.monitor_df.loc[startRowIndex, [f"A{startColIndex+1}"]] = screen_monitor_df.iloc[rowIndex-1,colIndex]
                        colIndex += 1
                    startColIndex += 1
                _, startColIndex= monitorPosition
                rowIndex += 1
                colIndex = 0
                highlightRows.append(startRowIndex+1)
                startRowIndex += 1

        self.monitor_df = self.monitor_df.replace(np.nan, "-", regex=True)
        # self.monitorNames[screenOptions] = f"(Dashboard) > {chosenMenu}"
        latestScanMenuOption = f"{dbTimestamp} (Dashboard) > " + f"{chosenMenu} [{screenOptions}]"
        OutputControls().printOutput(
            colorText.BOLD
            + colorText.FAIL
            + f"[+] {latestScanMenuOption}"
            + colorText.END
            , enableMultipleLineOutput=True
        )
        tabulated_results = colorText.miniTabulator().tabulate(
            self.monitor_df, tablefmt=colorText.No_Pad_GridFormat,
            highlightCharacter=colorText.HEAD+"="+colorText.END,
            showindex=False,
            highlightedRows=highlightRows,
            highlightedColumns=highlightCols,
            maxcolwidths=Utility.tools.getMaxColumnWidths(self.monitor_df)
        )
        self.lines = len(tabulated_results.splitlines()) + 1 # 1 for the progress bar at the bottom and 1 for the chosenMenu option
        OutputControls().printOutput(tabulated_results, enableMultipleLineOutput=True)
        if telegram:
            STD_ENCODING=sys.stdout.encoding if sys.stdout is not None else 'utf-8'
            
            telegram_df_tabulated = colorText.miniTabulator().tabulate(
                            telegram_df,
                            headers="keys",
                            tablefmt=colorText.No_Pad_GridFormat,
                            showindex=False,
                            maxcolwidths=[None,None,4,3]
                        ).encode("utf-8").decode(STD_ENCODING).replace("-K-----S-----C-----R","-K-----S----C---R").replace("%  ","% ").replace("=K=====S=====C=====R","=K=====S====C===R").replace("Vol  |","Vol|").replace("x  ","x")
            telegram_df_tabulated = telegram_df_tabulated.replace("-E-----N-----E-----R","-E-----N----E---R").replace("=E=====N=====E=====R","=E=====N====E===R")
            result_output = f"{latestScanMenuOption}\n<pre>{telegram_df_tabulated}</pre>"
            try:
                filePath = os.path.join(Archiver.get_user_outputs_dir(), "monitor_outputs.txt")
                f = open(filePath, "w")
                f.write(result_output)
                f.close()
            except:
                pass

