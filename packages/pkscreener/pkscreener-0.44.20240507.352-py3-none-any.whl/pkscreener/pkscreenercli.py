#!/usr/bin/python3
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
# Pyinstaller compile Windows: pyinstaller --onefile --icon=screenshots\icon.ico pkscreener\pkscreenercli.py  --hidden-import cmath --hidden-import talib.stream --hidden-import numpy --hidden-import pandas --hidden-import alive-progress
# Pyinstaller compile Linux  : pyinstaller --onefile --icon=screenshots/icon.ico pkscreener/pkscreenercli.py  --hidden-import cmath --hidden-import talib.stream --hidden-import numpy --hidden-import pandas --hidden-import alive-progress
import warnings
warnings.simplefilter("ignore", UserWarning,append=True)
import argparse
import builtins
import logging
import json
import traceback
import datetime
# Keep module imports prior to classes
import os
import sys
import tempfile
os.environ["PYTHONWARNINGS"]="ignore::UserWarning"
import multiprocessing

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    logging.getLogger("tensorflow").setLevel(logging.ERROR)
except Exception:# pragma: no cover
    pass

from time import sleep
import time

from PKDevTools.classes import log as log
from PKDevTools.classes.ColorText import colorText
from PKDevTools.classes.log import default_logger
from PKDevTools.classes.PKDateUtilities import PKDateUtilities
from pkscreener import Imports
from PKDevTools.classes.OutputControls import OutputControls
from pkscreener.classes.MarketMonitor import MarketMonitor
import pkscreener.classes.ConfigManager as ConfigManager

if __name__ == '__main__':
    multiprocessing.freeze_support()
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["AUTOGRAPH_VERBOSITY"] = "0"

printenabled=False
originalStdOut=None
original__stdout=None
cron_runs=0

def decorator(func):
    def new_func(*args, **kwargs):
        if printenabled:
            try:
                func(*args,**kwargs)
            except Exception as e:# pragma: no cover
                default_logger().debug(e, exc_info=True)
                pass

    return new_func


# print = decorator(print) # current file
def disableSysOut(input=True, disable=True):
    global printenabled
    printenabled = not disable
    if disable:
        global originalStdOut, original__stdout
        if originalStdOut is None:
            builtins.print = decorator(builtins.print)  # all files
            if input:
                builtins.input = decorator(builtins.input)  # all files
            originalStdOut = sys.stdout
            original__stdout = sys.__stdout__
        sys.stdout = open(os.devnull, "w")
        sys.__stdout__ = open(os.devnull, "w")
    else:
        try:
            sys.stdout.close()
            sys.__stdout__.close()
        except Exception as e:# pragma: no cover
            default_logger().debug(e, exc_info=True)
            pass
        sys.stdout = originalStdOut
        sys.__stdout__ = original__stdout

# Argument Parsing for test purpose
argParser = argparse.ArgumentParser()
argParser.add_argument(
    "-a",
    "--answerdefault",
    help="Pass default answer to questions/choices in the application. Example Y, N",
    required=False,
)
argParser.add_argument(
    "--backtestdaysago",
    help="Run scanner for -b days ago from today.",
    required=False,
)
argParser.add_argument(
    "--barometer",
    action="store_true",
    help="Send global market barometer to telegram channel or a user",
    required=False,
)
argParser.add_argument(
    "--bot",
    action="store_true",
    help="Run only in telegram bot mode",
    required=False,
)
argParser.add_argument(
    "-c",
    "--croninterval",
    help="Pass interval in seconds to wait before the program is run again with same parameters",
    required=False,
)
argParser.add_argument(
    "-d",
    "--download",
    action="store_true",
    help="Only download Stock data in .pkl file (No analysis will be run)",
    required=False,
)
argParser.add_argument(
    "-e",
    "--exit",
    action="store_true",
    help="Exit right after executing just once",
    required=False,
)
argParser.add_argument(
    "--forceBacktestsForZeroResultDays",
    help="Force run the backtests even for those days when we already have zero results saved in the repo",
    action=argparse.BooleanOptionalAction,
)
argParser.add_argument(
    "-i",
    "--intraday",
    help="Use Intraday configurations and use the candlestick duration that is passed. Acceptable values 1m, 5m, 10m, 15m, 1h etc.",
    required=False,
)
argParser.add_argument(
    "-m",
    "--monitor",
    help="Monitor for intraday scanners and their results.",
    required=False,
)
argParser.add_argument(
    "--maxdisplayresults",
    help="Maximum number of results to display.",
    required=False,
)
argParser.add_argument(
    "--maxprice",
    help="Maximum Price for the stock to be considered.",
    required=False,
)
argParser.add_argument(
    "--minprice",
    help="Minimum Price for the stock to be considered.",
    required=False,
)
argParser.add_argument(
    "-o",
    "--options",
    help="Pass selected options in the <MainMenu>:<SubMenu>:<SubMenu>:etc. format. For example: ./pkscreenercli.py -a Y -o X:12:10 -e will run the screener with answer Y as default choice to questions and scan with menu choices: Scanners > Nifty (All Stocks) > Closing at least 2%% up since last 3 day",
    required=False,
)
argParser.add_argument(
    "-p",
    "--prodbuild",
    action="store_true",
    help="Run in production-build mode",
    required=False,
)
argParser.add_argument(
    "--runintradayanalysis",
    action="store_true",
    help="Run analysis for morning vs EoD LTP values",
    required=False,
)
argParser.add_argument(
    "--simulate",
    type=json.loads, # '{"isTrading":true,"currentDateTime":"2024-04-29 09:35:38"}'
    help="Simulate various conditions",
    required=False,
)
argParser.add_argument(
    "-t",
    "--testbuild",
    action="store_true",
    help="Run in test-build mode",
    required=False,
)
argParser.add_argument(
    "--telegram",
    action="store_true",
    help="Run with an assumption that this instance is launched via telegram bot",
    required=False,
)
argParser.add_argument(
    "-u",
    "--user",
    help="Telegram user ID to whom the results must be sent.",
    required=False,
)
argParser.add_argument(
    "-l",
    "--log",
    action="store_true",
    help="Run with full logging enabled",
    required=False,
)
argParser.add_argument("-v", action="store_true")  # Dummy Arg for pytest -v
argsv = argParser.parse_known_args()
args = argsv[0]
results = None
resultStocks = None
plainResults = None
start_time = None
dbTimestamp = None
elapsed_time = None
configManager = ConfigManager.tools()

def removeMonitorFile():
    from PKDevTools.classes import Archiver
    filePath = os.path.join(Archiver.get_user_outputs_dir(), "monitor_outputs.txt")
    try:
        os.remove(filePath)
    except:
        pass

def logFilePath():
    try:
        from PKDevTools.classes import Archiver

        filePath = os.path.join(Archiver.get_user_outputs_dir(), "pkscreener-logs.txt")
        f = open(filePath, "w")
        f.write("Logger file for pkscreener!")
        f.close()
    except Exception:# pragma: no cover
        filePath = os.path.join(tempfile.gettempdir(), "pkscreener-logs.txt")
    return filePath


def setupLogger(shouldLog=False, trace=False):
    if not shouldLog:
        del os.environ['PKDevTools_Default_Log_Level']
        return
    log_file_path = logFilePath()

    if os.path.exists(log_file_path):
        try:
            os.remove(log_file_path)
        except Exception:# pragma: no cover
            pass
    OutputControls().printOutput(colorText.FAIL + "\n[+] Logs will be written to:"+colorText.END)
    OutputControls().printOutput(colorText.GREEN + f"[+] {log_file_path}"+colorText.END)
    OutputControls().printOutput(colorText.FAIL + "[+] If you need to share, open this folder, copy and zip the log file to share.\n" + colorText.END)
    # logger = multiprocessing.log_to_stderr(log.logging.DEBUG)
    log.setup_custom_logger(
        "pkscreener",
        log.logging.DEBUG,
        trace=trace,
        log_file_path=log_file_path,
        filter=None,
    )
    os.environ["PKDevTools_Default_Log_Level"] = str(log.logging.DEBUG)

def warnAboutDependencies():
    if not Imports["talib"]:
        OutputControls().printOutput(
                colorText.BOLD
                + colorText.FAIL
                + "[+] TA-Lib is not installed. Looking for pandas_ta."
                + colorText.END
            )
        sleep(1)
        if Imports["pandas_ta"]:
            OutputControls().printOutput(
                colorText.BOLD
                + colorText.GREEN
                + "[+] Found and falling back on pandas_ta.\n[+] For full coverage(candle patterns), you may wish to read the README file in PKScreener repo : https://github.com/pkjmesra/PKScreener \n[+] or follow instructions from\n[+] https://github.com/ta-lib/ta-lib-python"
                + colorText.END
            )
            sleep(1)
        else:
            OutputControls().printOutput(
                colorText.BOLD
                + colorText.FAIL
                + "[+] Neither ta-lib nor pandas_ta was located. You need at least one of them to continue! \n[+] Please follow instructions from README file under PKScreener repo: https://github.com/pkjmesra/PKScreener"
                + colorText.END
            )
            input("Press any key to try anyway...")

def runApplication():
    from pkscreener.globals import main, sendQuickScanResult,sendMessageToTelegramChannel, sendGlobalMarketBarometer, updateMenuChoiceHierarchy, isInterrupted, refreshStockData, closeWorkersAndExit
    # From a previous call to main with args, it may have been mutated.
    # Let's stock to the original args passed by user
    argsv = argParser.parse_known_args()
    args = argsv[0]
    if args.runintradayanalysis:
        from pkscreener.classes.MenuOptions import menus
        runOptions = menus.allMenus(topLevel="C", index=12)
        optionalFinalOutcome_df = None
        import pkscreener.classes.Utility as Utility
        import pandas as pd
        # Delete any existing data from the previous run.
        configManager.deleteFileWithPattern(pattern="stock_data_*.pkl")
        for runOption in runOptions:
            args.options = runOption
            try:
                optionalFinalOutcome_df,_ = main(userArgs=args,optionalFinalOutcome_df=optionalFinalOutcome_df)
                if "EoDDiff" not in optionalFinalOutcome_df.columns:
                    # Somehow the file must have been corrupted. Let's re-download
                    configManager.deleteFileWithPattern(pattern="stock_data_*.pkl")
                    configManager.deleteFileWithPattern(pattern="intraday_stock_data_*.pkl")
                if isInterrupted():
                    break
            except Exception as e:
                OutputControls().printOutput(e)
                if args.log:
                    traceback.print_exc()
        if optionalFinalOutcome_df is not None:
            final_df = None
            optionalFinalOutcome_df.drop('FairValue', axis=1, inplace=True, errors="ignore")
            df_grouped = optionalFinalOutcome_df.groupby("Stock")
            for stock, df_group in df_grouped:
                if stock == "PORTFOLIO":
                    if final_df is None:
                        final_df = df_group[["Pattern","LTP","SqrOffLTP","SqrOffDiff","EoDLTP","EoDDiff","DayHigh","DayHighDiff","%Chng"]]
                    else:
                        final_df = pd.concat([final_df, df_group[["Pattern","LTP","SqrOffLTP","SqrOffDiff","EoDLTP","EoDDiff","DayHigh","DayHighDiff","%Chng"]]], axis=0)
            final_df.rename(
                columns={
                    "LTP": "Morning Portfolio",
                    "SqrOffLTP": "SqrOff Portfolio",
                    "EoDLTP": "EoD Portfolio",
                    "%Chng": "EoD %Chng",
                    },
                    inplace=True,
                )
            mark_down = colorText.miniTabulator().tabulate(
                                final_df,
                                headers="keys",
                                tablefmt=colorText.No_Pad_GridFormat,
                                showindex = False
                            ).encode("utf-8").decode(Utility.STD_ENCODING)
            OutputControls().printOutput(mark_down)
            sendQuickScanResult(menuChoiceHierarchy="IntradayAnalysis",
                                user="-1001785195297",
                                tabulated_results=mark_down,
                                markdown_results=mark_down,
                                caption="IntradayAnalysis - Morning alert vs Market Close",
                                pngName= f"PKS_IA_{PKDateUtilities.currentDateTime().strftime('%Y-%m-%d_%H:%M:%S')}",
                                pngExtension= ".png"
                                )
    else:
        if args.barometer:
            sendGlobalMarketBarometer(userArgs=args)
        else:
            global results, resultStocks, plainResults, dbTimestamp, elapsed_time, start_time
            monitorOption_org = ""
            # args.monitor = configManager.defaultMonitorOptions
            if args.monitor:
                args.answerdefault = args.answerdefault or 'Y'
                if MarketMonitor().monitorIndex == 0:
                    dbTimestamp = PKDateUtilities.currentDateTime().strftime("%H:%M:%S")
                    elapsed_time = 0
                    if start_time is None:
                        start_time = time.time()
                    else:
                        elapsed_time = round(time.time() - start_time,2)
                        start_time = time.time()
                monitorOption_org = MarketMonitor().currentMonitorOption()
                monitorOption = monitorOption_org
                lastComponent = monitorOption.split(":")[-1]
                # previousCandleDuration = configManager.duration
                if "i" in lastComponent:
                    # We need to switch to intraday scan
                    monitorOption = monitorOption.replace(lastComponent,"")
                    args.intraday = lastComponent.replace("i","").strip()
                    configManager.toggleConfig(candleDuration=args.intraday, clearCache=False)
                else:
                    # We need to switch to daily scan
                    args.intraday = None
                    configManager.toggleConfig(candleDuration='1d', clearCache=False)
                if monitorOption.startswith("|"):
                    monitorOption = monitorOption.replace("|","")
                    # We need to pipe the output from previous run into the next one
                    if resultStocks is not None:
                        resultStocks = ",".join(resultStocks)
                        monitorOption = f"{monitorOption}:{resultStocks}"
                args.options = monitorOption.replace("::",":")
                # (previousCandleDuration != configManager.duration) or 
                if (MarketMonitor().monitorIndex == 1 and args.options is not None and plainResults is not None):
                    # Load the stock data afresh for each cycle
                    refreshStockData(args.options)
            try: 
                results = None
                plainResults = None
                resultStocks = None
                results, plainResults = main(userArgs=args)
                if isInterrupted():
                    closeWorkersAndExit()
                    removeMonitorFile()
                    sys.exit(0)
                while pipeResults(plainResults,args):
                    results, plainResults = main(userArgs=args)
            except SystemExit:
                closeWorkersAndExit()
                removeMonitorFile()
                sys.exit(0)
            except Exception as e:
                default_logger().debug(e, exc_info=True)
                # Probably user cancelled an operation by choosing a cancel sub-menu somewhere
                pass
            if plainResults is not None and not plainResults.empty:
                plainResults = plainResults[~plainResults.index.duplicated(keep='first')]
                results = results[~results.index.duplicated(keep='first')]
                resultStocks = plainResults.index
            if results is not None and args.monitor and len(monitorOption_org) > 0:
                MarketMonitor().refresh(screen_df=results,screenOptions=monitorOption_org, chosenMenu=updateMenuChoiceHierarchy(),dbTimestamp=f"{dbTimestamp} | CycleTime:{elapsed_time}s",telegram=args.telegram)


def pipeResults(prevOutput,args):
    nextOnes = args.options.split(";")
    if len(nextOnes) > 1:
        monitorOption = nextOnes[1]
        if len(monitorOption) == 0:
            return False
        lastComponent = monitorOption.split(":")[-1]
        if "i" in lastComponent:
            # We need to switch to intraday scan
            monitorOption = monitorOption.replace(lastComponent,"")
            args.intraday = lastComponent.replace("i","").strip()
            configManager.toggleConfig(candleDuration=args.intraday, clearCache=False)
        else:
            # We need to switch to daily scan
            args.intraday = None
            configManager.toggleConfig(candleDuration='1d', clearCache=False)
        if monitorOption.startswith("|"):
            monitorOption = monitorOption.replace("|","")
            # We need to pipe the output from previous run into the next one
            if prevOutput is not None and not prevOutput.empty:
                prevOutput_results = prevOutput[~prevOutput.index.duplicated(keep='first')]
                prevOutput_results = prevOutput_results.index
                prevOutput_results = ",".join(prevOutput_results)
                monitorOption = f"{monitorOption}:{prevOutput_results}"
        args.options = monitorOption.replace("::",":")
        args.options = args.options + ":D:;".join(nextOnes[2:])
        return True
    return False

def pkscreenercli():
    global originalStdOut
    if sys.platform.startswith("darwin"):
        try:
            multiprocessing.set_start_method("fork")
        except RuntimeError as e:# pragma: no cover
            if "RUNNER" not in os.environ.keys() and ('PKDevTools_Default_Log_Level' in os.environ.keys() and os.environ["PKDevTools_Default_Log_Level"] != str(log.logging.NOTSET)):
                OutputControls().printOutput(
                    "[+] RuntimeError with 'multiprocessing'.\n[+] Please contact the Developer, if this does not work!"
                )
                OutputControls().printOutput(e)
                traceback.print_exc()
            pass

    OutputControls(enableMultipleLineOutput=(args.monitor is None)).printOutput("",end="\r")
        
    configManager.getConfig(ConfigManager.parser)
    # configManager.restartRequestsCache()
    # args.monitor = configManager.defaultMonitorOptions
    if args.monitor is not None:
        MarketMonitor(monitors=args.monitor.split(",") if len(args.monitor)>5 else configManager.defaultMonitorOptions.split(","),maxNumResultsPerRow=configManager.maxDashboardWidgetsPerRow)

    if args.log or configManager.logsEnabled:
        setupLogger(shouldLog=True, trace=args.testbuild)
        if not args.prodbuild and args.answerdefault is None:
            input("Press <Enter> to continue...")
    else:
        if "PKDevTools_Default_Log_Level" in os.environ.keys():
            del os.environ['PKDevTools_Default_Log_Level']
            # os.environ["PKDevTools_Default_Log_Level"] = str(log.logging.NOTSET)
    if args.simulate:
        os.environ["simulation"] = json.dumps(args.simulate)
    elif "simulation" in os.environ.keys():
        del os.environ['simulation']
    # Import other dependency here because if we import them at the top
    # multiprocessing behaves in unpredictable ways
    import pkscreener.classes.Utility as Utility

    configManager.default_logger = default_logger()
    if originalStdOut is None:
        # Clear only if this is the first time it's being called from some
        # loop within workflowtriggers.
        Utility.tools.clearScreen(userArgs=args, clearAlways=True)
    warnAboutDependencies()
    if args.prodbuild:
        disableSysOut()

    if not configManager.checkConfigFile():
        configManager.setConfig(
            ConfigManager.parser, default=True, showFileCreatedText=False
        )
    if args.telegram:
        # Launched by bot for intraday monitor?
        if (PKDateUtilities.isTradingTime() and not PKDateUtilities.isTodayHoliday()[0]) or ("PKDevTools_Default_Log_Level" in os.environ.keys()):
            from PKDevTools.classes import Archiver
            filePath = os.path.join(Archiver.get_user_outputs_dir(), "monitor_outputs.txt")
            if os.path.exists(filePath):
                default_logger().info("monitor_outputs.txt already exists! This means an instance may already be running. Exiting now...")
                # Since the file exists, it means, there is another instance running
                sys.exit(0)
            import atexit
            atexit.register(removeMonitorFile)
        else:
            # It should have been launched only during the trading hours
            default_logger().info("--telegram option must be launched ONLY during NSE trading hours. Exiting now...")
            sys.exit(0)
    # Check and see if we're running only the telegram bot
    if args.bot:
        from pkscreener import pkscreenerbot
        pkscreenerbot.runpkscreenerbot()
        return
    
    if args.intraday:
        configManager.toggleConfig(candleDuration=args.intraday, clearCache=False)
    else:
        configManager.toggleConfig(candleDuration='1d', clearCache=False)
    if args.options is not None and str(args.options) == "0":
        # Must be from unit tests to be able to break out of loops via eventing
        args.options = None
    
    if args.maxprice:
        configManager.maxLTP = args.maxprice
        configManager.setConfig(ConfigManager.parser, default=True, showFileCreatedText=False)
    if args.minprice:
        configManager.minLTP = args.minprice
        configManager.setConfig(ConfigManager.parser, default=True, showFileCreatedText=False)
    if args.testbuild and not args.prodbuild:
        OutputControls().printOutput(
            colorText.BOLD
            + colorText.FAIL
            + "[+] Started in TestBuild mode!"
            + colorText.END
        )
        runApplication()
    elif args.download:
        OutputControls().printOutput(
            colorText.BOLD
            + colorText.FAIL
            + "[+] Download ONLY mode! Stocks will not be screened!"
            + colorText.END
        )
        if args.intraday is None:
            configManager.toggleConfig(candleDuration="1d", clearCache=False)
        runApplication()
        from pkscreener.globals import closeWorkersAndExit
        closeWorkersAndExit()
        removeMonitorFile()
        sys.exit(0)
    else:
        runApplicationForScreening()

def runLoopOnScheduleOrStdApplication(hasCronInterval):
    if hasCronInterval:
        scheduleNextRun()
    else:
        runApplication()

def runApplicationForScreening():
    from pkscreener.globals import closeWorkersAndExit
    try:
        hasCronInterval = args.croninterval is not None and str(args.croninterval).isnumeric()
        shouldBreak = (args.exit and not hasCronInterval)or args.user is not None or args.testbuild
        runLoopOnScheduleOrStdApplication(hasCronInterval)
        while True:
            if shouldBreak:
                break
            runLoopOnScheduleOrStdApplication(hasCronInterval)
        if args.v:
            disableSysOut(disable=False)
            return
        closeWorkersAndExit()
        removeMonitorFile()
        sys.exit(0)
    except SystemExit:
        closeWorkersAndExit()
        removeMonitorFile()
        sys.exit(0)
    except (RuntimeError, Exception) as e:  # pragma: no cover
        default_logger().debug(e, exc_info=True)
        if args.prodbuild:
            disableSysOut(disable=False)
        OutputControls().printOutput(
            f"{e}\n[+] An error occurred! Please run with '-l' option to collect the logs.\n[+] For example, 'pkscreener -l' and then contact the developer!"
        )
        if "RUNNER" in os.environ.keys() or ('PKDevTools_Default_Log_Level' in os.environ.keys() and os.environ["PKDevTools_Default_Log_Level"] != str(log.logging.NOTSET)):
            traceback.print_exc()
        if args.v:
            disableSysOut(disable=False)
            return
        closeWorkersAndExit()
        removeMonitorFile()
        sys.exit(0)


def scheduleNextRun():
    sleepUntilNextExecution = not PKDateUtilities.isTradingTime()
    while sleepUntilNextExecution:
        OutputControls().printOutput(
            colorText.BOLD
            + colorText.FAIL
            + (
                "SecondsAfterClosingTime[%d] SecondsBeforeMarketOpen [%d]. Next run at [%s]"
                % (
                    int(PKDateUtilities.secondsAfterCloseTime()),
                    int(PKDateUtilities.secondsBeforeOpenTime()),
                    str(
                        PKDateUtilities.nextRunAtDateTime(
                            bufferSeconds=3600,
                            cronWaitSeconds=int(args.croninterval),
                        )
                    ),
                )
            )
            + colorText.END
        )
        if (PKDateUtilities.secondsAfterCloseTime() >= 3600) and (
            PKDateUtilities.secondsAfterCloseTime() <= (3600 + 1.5 * int(args.croninterval))
        ):
            sleepUntilNextExecution = False
        if (PKDateUtilities.secondsBeforeOpenTime() <= -3600) and (
            PKDateUtilities.secondsBeforeOpenTime() >= (-3600 - 1.5 * int(args.croninterval))
        ):
            sleepUntilNextExecution = False
        sleep(int(args.croninterval))
    global cron_runs
    if cron_runs > 0:
        OutputControls().printOutput(
            colorText.BOLD + colorText.GREEN + f'=> Going to fetch again in {int(args.croninterval)} sec. at {(PKDateUtilities.currentDateTime() + datetime.timedelta(seconds=120)).strftime("%Y-%m-%d %H:%M:%S")} IST...' + colorText.END,
            end="\r",
            flush=True,
        )
        sleep(int(args.croninterval) if not args.testbuild else 3)
    runApplication()
    cron_runs += 1

if __name__ == "__main__":
    try:
        pkscreenercli()
    except KeyboardInterrupt:
        sys.exit(0)
