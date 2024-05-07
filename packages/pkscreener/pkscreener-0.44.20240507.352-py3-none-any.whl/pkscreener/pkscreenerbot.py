#!/usr/bin/env python
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
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Application class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
import os
import html
import json
import logging
import re
import sys
import traceback
from datetime import datetime
from time import sleep
from telegram import __version__ as TG_VER
from telegram.constants import ParseMode

start_time = datetime.now()
MINUTES_5_IN_SECONDS = 300

from PKDevTools.classes.Telegram import get_secrets
from PKDevTools.classes.PKDateUtilities import PKDateUtilities
from PKDevTools.classes.ColorText import colorText
from pkscreener.classes.MenuOptions import MenuRenderStyle, menu, menus
from pkscreener.classes.WorkflowManager import run_workflow
from pkscreener.globals import showSendConfigInfo, showSendHelpInfo
monitor_proc = None

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackContext
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)

m0 = menus()
m1 = menus()
m2 = menus()
m3 = menus()

TOP_LEVEL_SCANNER_MENUS = ["X", "B", "MI"]
TOP_LEVEL_SCANNER_SKIP_MENUS = ["M", "S", "G", "C", "T", "D", "I", "E", "U", "L", "Z"]
INDEX_SKIP_MENUS = ["W","E","M","Z","0","2","3","4","6","7","9","10","13"]
SCANNER_SKIP_MENUS_1_TO_6 = ["0","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","42","M","Z"]
SCANNER_SKIP_MENUS_7_TO_12 = ["0","1","2","3","4","5","6","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","42","M","Z"]
SCANNER_SKIP_MENUS_13_TO_18 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","19","20","21","22","23","24","25","26","27","28","29","30","42","M","Z"]
SCANNER_SKIP_MENUS_19_TO_25 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","22","26","27","28","29","30","42","M","Z"]
SCANNER_SKIP_MENUS_26_TO_31 = ["0","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","29","30","42","M","Z"]
SCANNER_MENUS_WITH_NO_SUBMENUS = ["1","2","3","10","11","12","13","14","15","16","17","18","19","20","21","23","24","25","26","27","28"]
SCANNER_MENUS_WITH_SUBMENU_SUPPORT = ["6", "7", "21"]

INDEX_COMMANDS_SKIP_MENUS_SCANNER = ["W", "E", "M", "Z"]
INDEX_COMMANDS_SKIP_MENUS_BACKTEST = ["W", "E", "M", "Z", "N", "0", "15"]
UNSUPPORTED_COMMAND_MENUS =["22","29","30","42","M","Z"]
SUPPORTED_COMMAND_MENUS = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, updatedResults=None) -> int:
    """Send message on `/start`."""
    updateCarrier = None
    if update is None:
        return
    else:
        if update.callback_query is not None:
            updateCarrier = update.callback_query
        if update.message is not None:
            updateCarrier = update.message
        if updateCarrier is None:
            return
    # Get user that sent /start and log his name
    user = updateCarrier.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    mns = m0.renderForMenu(asList=True)
    if (PKDateUtilities.isTradingTime() and not PKDateUtilities.isTodayHoliday()[0]) or ("PKDevTools_Default_Log_Level" in os.environ.keys()):
        mns.append(menu().create("MI", "Int. Monitor", 2))
    inlineMenus = []
    for mnu in mns:
        if mnu.menuKey in TOP_LEVEL_SCANNER_MENUS:
            inlineMenus.append(
                InlineKeyboardButton(
                    mnu.menuText.split("(")[0],
                    callback_data="C" + str(mnu.menuKey),
                )
            )
    keyboard = [inlineMenus]
    reply_markup = InlineKeyboardMarkup(keyboard)
    cmds = m0.renderForMenu(
        selectedMenu=None,
        skip=TOP_LEVEL_SCANNER_SKIP_MENUS,
        asList=True,
        renderStyle=MenuRenderStyle.STANDALONE,
    )
    chosenBotMenuOption = ""
    if updatedResults is None:
        cmdText = ""
        for cmd in cmds:
            cmdText = f"{cmdText}\n\n{cmd.commandTextKey()} for {cmd.commandTextLabel()}"
        menuText = f"Welcome {user.first_name}, {(user.username)}! Please choose a menu option by selecting a button from below.\n\nYou can also explore a wide variety of all other scanners by typing in \n{cmdText}\n\n OR just use the buttons below to choose."
    else:
        chosenBotMenuOption = "Int. Monitor"
        menuText = updatedResults
    # Send message with text and appended InlineKeyboard
    if update.callback_query is not None:
        await sendUpdatedMenu(
            menuText=menuText, update=update, context=context, reply_markup=reply_markup, replaceWhiteSpaces=(updatedResults is None)
        )
    elif update.message is not None:
        await update.message.reply_text(
            menuText,
            reply_markup=reply_markup,
        )
    await context.bot.send_message(
        chat_id=int(f"-{Channel_Id}"),
        text=f"Name: {user.first_name}, Username:@{user.username} with ID: {str(user.id)} started using the bot!\n{chosenBotMenuOption}",
        parse_mode=ParseMode.HTML,
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def XScanners(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    data = query.data.upper().replace("CX", "X").replace("CB", "B").replace("CG", "G").replace("CMI", "MI")
    if data not in TOP_LEVEL_SCANNER_MENUS:
        return start(update, context)
    if data == "MI":
        from PKDevTools.classes import Archiver
        filePath = os.path.join(Archiver.get_user_outputs_dir(), "monitor_outputs.txt")
        appLogsEnabled = ("PKDevTools_Default_Log_Level" in os.environ.keys())
        # User wants an Int. Monitor
        launcher = "/home/runner/work/PKScreener/PKScreener/pkscreenercli.bin" if "MONITORING_BOT_RUNNER" in os.environ.keys() else "pkscreener"
        launcher = f"python3.11 {launcher}" if launcher.endswith(".py") else launcher
        result_outputs = "Starting up the monitor for this hour. Please try again after 30-40 seconds."
        try:
            from subprocess import Popen
            global monitor_proc
            if monitor_proc is None or monitor_proc.poll() is not None: # Process finished from an earlier launch
                if os.path.exists(filePath):
                    # Let's remove the old file so that the new app can begin to run
                    # If we don't remove, it might just exit assuming that there's another instance
                    # already running.
                    os.remove(filePath)
                appArgs = [f"{launcher}","-a","Y","-m","X","--telegram",]
                if appLogsEnabled:
                    appArgs.append("-l")
                else:
                    appArgs.append("-p")
                monitor_proc = Popen(appArgs)
                logger.info(f"{launcher} -a Y -m 'X' -p --telegram launched")
            else:
                result_outputs = "Monitor is running, but the results are being prepared. Try again in next few seconds."
                logger.info(f"{launcher} -a Y -m 'X' -p --telegram already running")
        except Exception as e:
            result_outputs = "Hmm...It looks like you caught us taking a break! Try again later :-)"
            logger.info(f"{launcher} -a Y -m 'X' -p --telegram could not be launched")
            logger.info(e)
            pass
        try:
            if os.path.exists(filePath):
                f = open(filePath, "r")
                result_outputs = f.read()
                f.close()
            await start(update, context, updatedResults=result_outputs)
            return START_ROUTES
        except Exception as e:
            result_outputs = "Hmm...It looks like you caught us taking a break! Try again later :-)"
            logger.info(e)
            logger.info(f"{launcher} -a Y -m 'X' -p --telegram could not read {filePath}")
            await start(update, context, updatedResults=result_outputs)
            return START_ROUTES

    midSkip = "1" if data == "X" else "N"
    skipMenus = [midSkip]
    skipMenus.extend(INDEX_SKIP_MENUS)
    menuText = (
        m1.renderForMenu(
            m0.find(data),
            skip=skipMenus,
            renderStyle=MenuRenderStyle.STANDALONE,
        )
        .replace("     ", "")
        .replace("    ", "")
        .replace("\t", "")
        .replace(colorText.FAIL,"").replace(colorText.END,"")
    )
    menuText = menuText + "\n\nH > Home"
    mns = m1.renderForMenu(
        m0.find(data),
        skip=skipMenus,
        asList=True,
    )
    mns.append(menu().create("H", "Home", 2))
    inlineMenus = []
    await query.answer()
    for mnu in mns:
        inlineMenus.append(
            InlineKeyboardButton(
                mnu.menuKey, callback_data=str(f"{query.data}_{mnu.menuKey}")
            )
        )
    keyboard = [inlineMenus]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=menuText, reply_markup=reply_markup)
    return START_ROUTES


async def Level2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    inlineMenus = []
    menuText = "Hmm...It looks like you caught us taking a break! Try again later :-)"
    mns = []
    query = update.callback_query
    await query.answer()
    preSelection = (
        query.data.upper().replace("CX", "X").replace("CB", "B").replace("CG", "G")
    )
    selection = preSelection.split("_")
    preSelection = f"{selection[0]}_{selection[1]}"
    if (selection[0].upper() not in TOP_LEVEL_SCANNER_MENUS):
        await start(update, context)
        return START_ROUTES
    if selection[len(selection)-1].upper() == "H":
        await start(update, context)
        return START_ROUTES
    if len(selection) == 2 or (len(selection) == 3 and selection[2] == "P"):
        if str(selection[1]).isnumeric():
            # It's only level 2
            menuText = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_1_TO_6,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            menuText = menuText + "\n\nN > More options"
            menuText = menuText + "\nH > Home"
            mns = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_1_TO_6,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            mns.append(menu().create("N", "More Options", 2))
            mns.append(menu().create("H", "Home", 2))
        elif selection[1] == "N":
            selection.extend(["", ""])
    elif len(selection) == 3:
        if selection[2] == "N":
            menuText = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_7_TO_12,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            menuText = menuText + "\n\nM > More Options"
            menuText = menuText + "\nH > Home"
            mns = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_7_TO_12,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            mns.append(menu().create("M", "More Options", 2))
            mns.append(menu().create("H", "Home", 2))
        elif selection[2] == "M":
            menuText = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_13_TO_18,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            menuText = menuText + "\n\n>> More Options"
            menuText = menuText + "\nH > Home"
            mns = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_13_TO_18,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            mns.append(menu().create(">>", "More Options", 2))
            mns.append(menu().create("H", "Home", 2))
        elif selection[2] == ">>":
            menuText = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_19_TO_25,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            menuText = menuText + "\n\nR > More Options"
            menuText = menuText + "\nH > Home"
            mns = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_19_TO_25,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            mns.append(menu().create("R", "More Options", 2))
            mns.append(menu().create("H", "Home", 2))
        elif selection[2] == "R":
            menuText = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_26_TO_31,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            menuText = menuText + "\n\nH > Home"
            mns = m2.renderForMenu(
                m1.find(selection[1]),
                skip=SCANNER_SKIP_MENUS_26_TO_31,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            mns.append(menu().create("H", "Home", 2))
        elif str(selection[2]).isnumeric():
            preSelection = f"{selection[0]}_{selection[1]}_{selection[2]}"
            if selection[2] in SCANNER_MENUS_WITH_SUBMENU_SUPPORT:
                menuText = m3.renderForMenu(
                    m2.find(selection[2]),
                    renderStyle=MenuRenderStyle.STANDALONE,
                    skip=["0"],
                )
                mns = m3.renderForMenu(
                    m2.find(selection[2]),
                    asList=True,
                    renderStyle=MenuRenderStyle.STANDALONE,
                    skip=["0"],
                )
            else:
                if selection[2] == "4":  # Last N days
                    selection.extend(["D", ""])
                elif selection[2] == "5":  # RSI range
                    selection.extend(["D", "D"])
                elif selection[2] == "8":  # CCI range
                    selection.extend(["D", "D"])
                elif selection[2] == "9":  # Vol gainer ratio
                    selection.extend(["D", ""])
                elif selection[2] in SCANNER_MENUS_WITH_NO_SUBMENUS:  # Vol gainer ratio
                    selection.extend(["", ""])
    elif len(selection) == 4:
        preSelection = (
            query.data.upper().replace("CX", "X").replace("CB", "B").replace("CG", "G")
        )
    optionChoices = ""
    if len(selection) <= 3:
        for mnu in mns:
            inlineMenus.append(
                InlineKeyboardButton(
                    mnu.menuKey,
                    callback_data="C" + str(f"{preSelection}_{mnu.menuKey}"),
                )
            )
        keyboard = [inlineMenus]
        reply_markup = InlineKeyboardMarkup(keyboard)
    elif len(selection) >= 4:
        optionChoices = (
            f"{selection[0]} > {selection[1]} > {selection[2]} > {selection[3]}"
        )
        expectedTime = f"{'10 to 15' if '> 15' in optionChoices else '1 to 2'}"
        menuText = f"Thank you for choosing {optionChoices}. You will receive the notification/results in about {expectedTime} minutes. It generally takes 1-2 minutes for NSE (2000+) stocks and 10-15 minutes for NASDAQ (7300+).\n\nPKScreener is free and will always remain so for everyone. Consider donating to help cover the basic server costs:\n\nUPI (India): 8007162973@APL \n\nor\nhttps://github.com/sponsors/pkjmesra?frequency=one-time&sponsor=pkjmesra"

        reply_markup = default_markup(inlineMenus)
        options = ":".join(selection)
        await launchScreener(
            options=options,
            user=query.from_user,
            context=context,
            optionChoices=optionChoices,
            update=update,
        )
    try:
        if optionChoices != "":
            await context.bot.send_message(
                chat_id=int(f"-{Channel_Id}"),
                text=f"Name: <b>{query.from_user.first_name}</b>, Username:@{query.from_user.username} with ID: <b>@{str(query.from_user.id)}</b> submitted scan request <b>{optionChoices}</b> to the bot!",
                parse_mode=ParseMode.HTML,
            )
    except Exception:# pragma: no cover
        await start(update, context)
    if not str(optionChoices.upper()).startswith("B"):
        await sendUpdatedMenu(
            menuText=menuText, update=update, context=context, reply_markup=reply_markup
        )
    return START_ROUTES

def default_markup(inlineMenus):
    mns = m0.renderForMenu(asList=True)
    for mnu in mns:
        if mnu.menuKey in TOP_LEVEL_SCANNER_MENUS:
            inlineMenus.append(
                    InlineKeyboardButton(
                        mnu.menuText.split("(")[0],
                        callback_data="C" + str(mnu.menuKey),
                    )
                )
    keyboard = [inlineMenus]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def sendUpdatedMenu(menuText, update: Update, context, reply_markup, replaceWhiteSpaces=True):
    try:
        if update.callback_query.message.text == menuText:
            menuText = f"{PKDateUtilities.currentDateTime()}:\n{menuText}"
        await update.callback_query.edit_message_text(
            text=menuText.replace("     ", "").replace("    ", "").replace("\t", "").replace(colorText.FAIL,"").replace(colorText.END,"") if replaceWhiteSpaces else menuText,
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
    except Exception as e:# pragma: no cover
        logger.log(e)
        await start(update, context)


async def launchScreener(options, user, context, optionChoices, update):
    try:
        if str(optionChoices.upper()).startswith("B"):
            optionChoices = optionChoices.replace(" ", "").replace(">", "_").replace(":","_").replace("_D","")
            while optionChoices.endswith("_"):
                optionChoices = optionChoices[:-1]
            if str(optionChoices).split("_")[2] == "6" and str(optionChoices).split("_")[3] == "7":
                optionChoices = f"{optionChoices}_3" # Lorenzian Any/All
            responseText = f"Thank you for choosing {optionChoices}!\n\nHere are the results:\n\nInsights: https://pkjmesra.github.io/PKScreener/Backtest-Reports/PKScreener_{optionChoices}_Insights_DateSorted.html"
            responseText = f"{responseText}\n\nSummary: https://pkjmesra.github.io/PKScreener/Backtest-Reports/PKScreener_{optionChoices}_Summary_StockSorted.html"
            responseText = f"{responseText}\n\nStock-wise: https://pkjmesra.github.io/PKScreener/Backtest-Reports/PKScreener_{optionChoices}_backtest_result_StockSorted.html"
            responseText = f"{responseText}\n\nOther Reports: https://pkjmesra.github.io/PKScreener/BacktestReports.html"
            if update is not None and update.message is not None:
                await update.message.reply_text(responseText)
            else:
                await update.callback_query.edit_message_text(
                    text=responseText,
                    reply_markup=default_markup([]),
                )
            await shareUpdateWithChannel(
                update=update, context=context, optionChoices=optionChoices
            )
            # run_workflow(optionChoices, str(user.id), str(options.upper()))
        elif str(optionChoices.upper()).startswith("X"):
            optionChoices = optionChoices.replace(" ", "").replace(">", "_")
            while optionChoices.endswith("_"):
                optionChoices = optionChoices[:-1]
            run_workflow(
                optionChoices, str(user.id), str(options.upper()), workflowType="X"
            )
        elif str(optionChoices.upper()).startswith("G"):
            optionChoices = optionChoices.replace(" ", "").replace(">", "_")
            while optionChoices.endswith("_"):
                optionChoices = optionChoices[:-1]
            options = options.upper().replace("G", "G:3").replace("::", ":D:D:D")
            run_workflow(
                optionChoices, str(user.id), str(options.upper()), workflowType="G"
            )
            # Popen(
            #     [
            #         "pkscreener",
            #         "-a",
            #         "Y",
            #         "-e",
            #         "-p",
            #         "-o",
            #         str(options.upper()),
            #         "-u",
            #         str(user.id),
            #     ]
            # )
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(e)
        await start(update, context)


async def BBacktests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Try Scanners", callback_data=str("CX")),
            # InlineKeyboardButton("Growth of 10k", callback_data=str("CG")),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Backtesting NOT implemented yet in this Bot!\n\n\nYou can use backtesting by downloading the software from https://github.com/pkjmesra/PKScreener/",
        reply_markup=reply_markup,
    )
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        text="See https://github.com/pkjmesra/PKScreener/ for more details or join https://t.me/PKScreener. \n\n\nSee you next time!"
    )
    return ConversationHandler.END


# This can be your own ID, or one for a developer group/channel.
# You can use the /start command of this bot to see your chat id.
chat_idADMIN = 123456789
Channel_Id = 12345678
GROUP_CHAT_ID = 1001907892864


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error("Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    global start_time
    timeSinceStarted = datetime.now() - start_time
    if (
        "telegram.error.Conflict" in tb_string
    ):  # A newer 2nd instance was registered. We should politely shutdown.
        if (
            timeSinceStarted.total_seconds() >= MINUTES_5_IN_SECONDS
        ):  # shutdown only if we have been running for over 5 minutes
            print(
                f"Stopping due to conflict after running for {timeSinceStarted.total_seconds()/60} minutes."
            )
            try:
                context.application.stop()
                sys.exit(0)
            except RuntimeError:
                context.application.shutdown()
            sys.exit(0)
        else:
            print("Other instance running!")
            # context.application.run_polling(allowed_updates=Update.ALL_TYPES)
    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    try:
        # Finally, send the message
        if "telegram.error.Conflict" not in message:
            await context.bot.send_message(
                chat_id=int(f"-{Channel_Id}"), text=message, parse_mode=ParseMode.HTML
            )
    except Exception:# pragma: no cover
        try:
            if "telegram.error.Conflict" not in tb_string:
                await context.bot.send_message(
                    chat_id=int(f"-{Channel_Id}"),
                    text=tb_string,
                    parse_mode=ParseMode.HTML,
                )
        except Exception:# pragma: no cover
            print(tb_string)


async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _shouldAvoidResponse(update):
        return
    msg = update.effective_message
    m = re.match("\s*/([0-9a-zA-Z_-]+)\s*(.*)", msg.text)
    cmd = m.group(1).lower()
    args = [arg for arg in re.split("\s+", m.group(2)) if len(arg)]
    if cmd.startswith("cx_") or cmd.startswith("cb_") or cmd.startswith("cg_"):
        await Level2(update=update, context=context)
        return START_ROUTES
    if cmd.startswith("cx") or cmd.startswith("cb") or cmd.startswith("cg"):
        await XScanners(update=update, context=context)
        return START_ROUTES
    if cmd.startswith("cz"):
        await end(update=update, context=context)
        return END_ROUTES

    if cmd == "start":
        await start(update=update, context=context)
        return START_ROUTES
    if cmd == "help":
        await help_command(update=update, context=context)
        return START_ROUTES
    if cmd.upper() in TOP_LEVEL_SCANNER_MENUS:
        await shareUpdateWithChannel(update=update, context=context)
        m0.renderForMenu(
            selectedMenu=None,
            skip=TOP_LEVEL_SCANNER_SKIP_MENUS,
            renderStyle=MenuRenderStyle.STANDALONE,
        )
        selectedMenu = m0.find(cmd.upper())
        cmdText = ""
        cmds = m1.renderForMenu(
            selectedMenu=selectedMenu,
            skip=(INDEX_COMMANDS_SKIP_MENUS_SCANNER  if cmd in ["x"] else INDEX_COMMANDS_SKIP_MENUS_BACKTEST),
            asList=True,
            renderStyle=MenuRenderStyle.STANDALONE,
        )
        for cmd in cmds:
            if cmd in ["N", "0"]:
                continue
            cmdText = (
                f"{cmdText}\n\n{cmd.commandTextKey()} for {cmd.commandTextLabel()}"
            )
        if cmd in ["x"]:
            cmdText = f"{cmdText}\n\nFor option 0 <Screen stocks by the stock name>, please type in the command in the following format\n/X_0 SBIN\n or \n/X_0_0 SBIN\nand hit send where SBIN is the NSE stock code.For multiple stocks, you can type in \n/X_0 SBIN,ICICIBANK,OtherStocks\nYou can put in any number of stocks separated by space or comma(,)."
        """Send a message when the command /help is issued."""
        await update.message.reply_text(f"Choose an option:\n{cmdText}")
        return START_ROUTES

    if update.message is None:
        await help_command(update=update, context=context)
        return START_ROUTES
    if "x_0" in cmd or "x_0_0" in cmd or "b_0" in cmd or "g_0" in cmd:
        await shareUpdateWithChannel(update=update, context=context)
        shouldScan = False
        if len(args) > 0:
            shouldScan = True
            selection = [
                cmd.split("_")[0].upper(),
                "0",
                "0",
                f"{','.join(args)}".replace(" ", ""),
            ]
        if shouldScan:
            options = ":".join(selection)
            await launchScreener(
                options=options,
                user=update.message.from_user,
                context=context,
                optionChoices=cmd.upper(),
                update=update,
            )
            await sendRequestSubmitted(cmd.upper(), update=update, context=context)
            return START_ROUTES
        else:
            if cmd in ["x"]:
                cmdText = "For option 0 <Screen stocks by the stock name>, please type in the command in the following format\n/X_0 SBIN or /X_0_0 SBIN and hit send where SBIN is the NSE stock code.For multiple stocks, you can type in /X_0 SBIN,ICICIBANK,OtherStocks . You can put in any number of stocks separated by space or comma(,)."
            """Send a message when the command /help is issued."""
            await update.message.reply_text(f"Choose an option:\n{cmdText}")
            return START_ROUTES

    if "x_" in cmd or "b_" in cmd or "g_" in cmd:
        await shareUpdateWithChannel(update=update, context=context)
        selection = cmd.split("_")
        if len(selection) == 2:
            m0.renderForMenu(
                selectedMenu=None,
                skip=TOP_LEVEL_SCANNER_SKIP_MENUS,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            selectedMenu = m0.find(selection[0].upper())
            m1.renderForMenu(
                selectedMenu=selectedMenu,
                skip=(
                    INDEX_COMMANDS_SKIP_MENUS_SCANNER
                    if "x_" in cmd
                    else INDEX_COMMANDS_SKIP_MENUS_BACKTEST
                ),
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            selectedMenu = m1.find(selection[1].upper())
            if "x_" in cmd and selectedMenu.menuKey == "N":  # Nifty prediction
                options = ":".join(selection)
                await launchScreener(
                    options=options,
                    user=update.message.from_user,
                    context=context,
                    optionChoices=cmd.upper(),
                    update=update,
                )
                await sendRequestSubmitted(cmd.upper(), update=update, context=context)
                return START_ROUTES
            elif (
                "x_" in cmd and selectedMenu.menuKey == "0"
            ):  # a specific stock by name
                cmdText = "For option 0 <Screen stocks by the stock name>, please type in the command in the following format\n/X_0 SBIN or /X_0_0 SBIN and hit send where SBIN is the NSE stock code.For multiple stocks, you can type in /X_0 SBIN,ICICIBANK,OtherStocks. You can put in any number of stocks separated by space or comma(,)."
                """Send a message when the command /help is issued."""
                await update.message.reply_text(f"Choose an option:\n{cmdText}")
                return START_ROUTES
            cmds = m2.renderForMenu(
                selectedMenu=selectedMenu,
                skip=UNSUPPORTED_COMMAND_MENUS,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            cmdText = ""
            for cmd in cmds:
                cmdText = (
                    f"{cmdText}\n\n{cmd.commandTextKey()} for {cmd.commandTextLabel()}"
                )
            await update.message.reply_text(f"Choose an option:\n{cmdText}")
            return START_ROUTES
        elif len(selection) == 3:
            m0.renderForMenu(
                selectedMenu=None,
                skip=TOP_LEVEL_SCANNER_SKIP_MENUS,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            selectedMenu = m0.find(selection[0].upper())
            m1.renderForMenu(
                selectedMenu=selectedMenu,
                skip=(
                    INDEX_COMMANDS_SKIP_MENUS_SCANNER
                    if "x_" in cmd
                    else INDEX_COMMANDS_SKIP_MENUS_BACKTEST
                ),
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            selectedMenu = m1.find(selection[1].upper())
            m2.renderForMenu(
                selectedMenu=selectedMenu,
                skip=UNSUPPORTED_COMMAND_MENUS,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            if selection[2] in SCANNER_MENUS_WITH_SUBMENU_SUPPORT:
                selectedMenu = m2.find(selection[2].upper())
                cmds = m3.renderForMenu(
                    selectedMenu=selectedMenu,
                    asList=True,
                    renderStyle=MenuRenderStyle.STANDALONE,
                    skip=["0"],
                )
                cmdText = ""
                for cmd in cmds:
                    cmdText = f"{cmdText}\n\n{cmd.commandTextKey()} for {cmd.commandTextLabel()}"
                await update.message.reply_text(f"Choose an option:\n{cmdText}")
                return START_ROUTES
            else:
                if selection[2] == "4":  # Last N days
                    selection.extend(["D", ""])
                elif selection[2] == "5":  # RSI range
                    selection.extend(["D", "D"])
                elif selection[2] == "8":  # CCI range
                    selection.extend(["D", "D"])
                elif selection[2] == "9":  # Vol gainer ratio
                    selection.extend(["D", ""])
                elif selection[2] in SUPPORTED_COMMAND_MENUS:
                    selection.extend(["", ""])
        if len(selection) >= 4:
            options = ":".join(selection)
            await launchScreener(
                options=options,
                user=update.message.from_user,
                context=context,
                optionChoices=cmd.upper(),
                update=update,
            )
            await sendRequestSubmitted(cmd.upper(), update=update, context=context)
            return START_ROUTES
    if cmd == "y" or cmd == "h":
        await shareUpdateWithChannel(update=update, context=context)
        if cmd == "y":
            showSendConfigInfo(defaultAnswer='Y',user=str(update.message.from_user.id))
        elif cmd == "h":
            showSendHelpInfo(defaultAnswer='Y',user=str(update.message.from_user.id))
        # await launchScreener(
        #     options=f"{cmd.upper()}:",
        #     user=update.message.from_user,
        #     context=context,
        #     optionChoices=cmd.upper(),
        #     update=update,
        # )
        # await sendRequestSubmitted(cmd.upper(), update=update, context=context)
        return START_ROUTES
    await update.message.reply_text(f"{cmd.upper()} : Not implemented yet!")
    await help_command(update=update, context=context)


async def sendRequestSubmitted(optionChoices, update, context):
    menuText = f"Thank you for choosing {optionChoices}. You will receive the notification/results in about 5 minutes! \n\nConsider donating to help keep this project going:\nUPI: 8007162973@APL \nor\nhttps://github.com/sponsors/pkjmesra?frequency=one-time&sponsor=pkjmesra"
    await update.message.reply_text(menuText)
    await help_command(update=update, context=context)
    await shareUpdateWithChannel(
        update=update, context=context, optionChoices=optionChoices
    )


async def shareUpdateWithChannel(update, context, optionChoices=""):
    query = update.message or update.callback_query
    message = f"Name: <b>{query.from_user.first_name}</b>, Username:@{query.from_user.username} with ID: <b>@{str(query.from_user.id)}</b> began using ({optionChoices}) the bot!"
    await context.bot.send_message(
        chat_id=int(f"-{Channel_Id}"), text=message, parse_mode=ParseMode.HTML
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if _shouldAvoidResponse(update):
        return

    cmds = m0.renderForMenu(
        selectedMenu=None,
        skip=TOP_LEVEL_SCANNER_SKIP_MENUS,
        asList=True,
        renderStyle=MenuRenderStyle.STANDALONE,
    )
    cmdText = ""
    for cmd in cmds:
        cmdText = f"{cmdText}\n\n{cmd.commandTextKey()} for {cmd.commandTextLabel()}"
    """Send a message when the command /help is issued."""
    if update is not None and update.message is not None:
        await update.message.reply_text(
            f"You can begin by typing in /start and hit send!\n\nOR\n\nChoose an option:\n{cmdText}"
        )  #  \n\nThis bot restarts every hour starting at 5:30am IST until 10:30pm IST to keep it running on free servers. If it does not respond, please try again in a minutes to avoid the restart duration!
        query = update.message
        message = f"Name: <b>{query.from_user.first_name}</b>, Username:@{query.from_user.username} with ID: <b>@{str(query.from_user.id)}</b> began using the bot!"
        await context.bot.send_message(
            chat_id=int(f"-{Channel_Id}"), text=message, parse_mode=ParseMode.HTML
        )


def _shouldAvoidResponse(update):
    sentFrom = []
    if update.callback_query is not None:
        sentFrom.append(abs(update.callback_query.from_user.id))
    if update.message is not None and update.message.from_user is not None:
        sentFrom.append(abs(update.message.from_user.id))
        if update.message.from_user.username is not None:
            sentFrom.append(update.message.from_user.username)
    if update.channel_post is not None:
        if update.channel_post.chat is not None:
            sentFrom.append(abs(update.channel_post.chat.id))
            if update.channel_post.chat.username is not None:
                sentFrom.append(update.channel_post.chat.username)
        if update.channel_post.sender_chat is not None:
            sentFrom.append(abs(update.channel_post.sender_chat.id))
            sentFrom.append(update.channel_post.sender_chat.username)
    if update.edited_channel_post is not None:
        sentFrom.append(abs(update.edited_channel_post.sender_chat.username))

    if (
        abs(int(Channel_Id)) in sentFrom
        or abs(int(GROUP_CHAT_ID)) in sentFrom
        or "GroupAnonymousBot" in sentFrom
        or "PKScreener" in sentFrom
        or "PKScreeners" in sentFrom
    ):
        # We want to avoid sending any help message back to channel
        # or group in response to our own messages
        return True
    return False


def addCommandsForMenuItems(application):
    cmds0 = m0.renderForMenu(
        selectedMenu=None,
        skip=TOP_LEVEL_SCANNER_SKIP_MENUS,
        asList=True,
        renderStyle=MenuRenderStyle.STANDALONE,
    )
    for mnu0 in cmds0:
        p0 = mnu0.menuKey.upper()
        application.add_handler(CommandHandler(p0, command_handler))
        selectedMenu = m0.find(p0)
        cmds1 = m1.renderForMenu(
            selectedMenu=selectedMenu,
            skip=(
                INDEX_COMMANDS_SKIP_MENUS_SCANNER if p0 == "X" else INDEX_COMMANDS_SKIP_MENUS_BACKTEST
            ),
            asList=True,
            renderStyle=MenuRenderStyle.STANDALONE,
        )
        for mnu1 in cmds1:
            p1 = mnu1.menuKey.upper()
            if p1 in ["N", "0"]:
                if p1 in ["N"]:
                    application.add_handler(
                        CommandHandler(f"{p0}_{p1}", command_handler)
                    )
                continue
            application.add_handler(CommandHandler(f"{p0}_{p1}", command_handler))
            selectedMenu = m1.find(p1)
            cmds2 = m2.renderForMenu(
                selectedMenu=selectedMenu,
                skip=UNSUPPORTED_COMMAND_MENUS,
                asList=True,
                renderStyle=MenuRenderStyle.STANDALONE,
            )
            for mnu2 in cmds2:
                p2 = mnu2.menuKey.upper()
                application.add_handler(
                    CommandHandler(f"{p0}_{p1}_{p2}", command_handler)
                )
                if p2 in SCANNER_MENUS_WITH_SUBMENU_SUPPORT:
                    selectedMenu = m2.find(p2)
                    cmds3 = m3.renderForMenu(
                        selectedMenu=selectedMenu,
                        asList=True,
                        renderStyle=MenuRenderStyle.STANDALONE,
                        skip=["0"],
                    )
                    for mnu3 in cmds3:
                        p3 = mnu3.menuKey.upper()
                        application.add_handler(
                            CommandHandler(f"{p0}_{p1}_{p2}_{p3}", command_handler)
                        )

# def send_stuff(context: CallbackContext):
#   job = context.job

#   keyboard = [ 
#     [   
#         InlineKeyboardButton("NEVER", callback_data="NEVER"),
#         InlineKeyboardButton("UNLIKELY", callback_data="UNLIKELY")
#     ],  
#     [   
#         InlineKeyboardButton("MEH", callback_data="MEH"),
#         InlineKeyboardButton("MAYBE", callback_data="MAYBE")
#     ],  
#     [   
#         InlineKeyboardButton("YES", callback_data="YES"),
#         InlineKeyboardButton("ABSOLUTELY", callback_data="ABSOLUTELY")
#     ],  
#     [   
#         InlineKeyboardButton("RATHER NOT SAY", callback_data="UNKNOWN")
#     ]   
#   ]

#   reply_markup = InlineKeyboardMarkup(keyboard)

#   context.bot.send_photo(job.context, photo=open(PATH+thefile, 'rb'))
#   # return values of send_message are saved in the 'msg' var
#   msg = context.bot.send_message(job.context, text='RATE', reply_markup=reply_markup)

#   # the following job is created every time the send_stuff function is called
#   context.job_queue.run_once(
#     callback=cleanup,
#     when=5,
#     context=msg,
#     name='cleanup'
#   )

# # the function called by the job
# def cleanup(context: CallbackContext):
#   job = context.job

#   context.bot.edit_message_text(
#     chat_id=job.context.chat.id,
#     text='NO ANSWER PROVIDED',
#     message_id=job.context.message_id
#   )


def runpkscreenerbot() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    global chat_idADMIN, Channel_Id
    Channel_Id, TOKEN, chat_idADMIN, GITHUB_TOKEN = get_secrets()
    # TOKEN = '1234567'
    # Channel_Id = 1001785195297
    application = Application.builder().token(TOKEN).build()
    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(XScanners, pattern="^" + str("CX") + "$"),
                CallbackQueryHandler(XScanners, pattern="^" + str("CB") + "$"),
                CallbackQueryHandler(XScanners, pattern="^" + str("CMI") + "$"),
                # CallbackQueryHandler(XScanners, pattern="^" + str("CG") + "$"),
                CallbackQueryHandler(Level2, pattern="^" + str("CX_")),
                CallbackQueryHandler(Level2, pattern="^" + str("CB_")),
                CallbackQueryHandler(Level2, pattern="^" + str("CMI_")),
                # CallbackQueryHandler(Level2, pattern="^" + str("CG_")),
                CallbackQueryHandler(end, pattern="^" + str("CZ") + "$"),
                CallbackQueryHandler(start, pattern="^"),
            ],
            END_ROUTES: [],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, help_command)
    )
    # application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, command_handler))
    # application.add_handler(MessageHandler(filters.COMMAND, command_handler))
    # Add ConversationHandler to application that will be used for handling updates
    addCommandsForMenuItems(application)
    application.add_handler(conv_handler)
    # ...and the error handler
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    runpkscreenerbot()
