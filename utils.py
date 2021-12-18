from datetime import datetime
import inspect
import sqlite3
from time import sleep
import yaml

from pyrogram import Client, filters

DIRECTION = r'/home/bot/HATE/'
CONFIG = yaml.safe_load(open(DIRECTION + 'config.yml', 'r'))
TOKEN = CONFIG['TOKEN']
BOT = Client("hatebot", CONFIG['API_ID'], CONFIG['API_HASH'], bot_token=TOKEN)
ADMINS = CONFIG['ADMINS']
LOGFILE = DIRECTION + CONFIG['downloader_logfile']

class Log():
    def __init__(self, file: str = LOGFILE) -> None:
        self.file = file
    
    def log(self, text: str, offset = 0, *, logfile = LOGFILE) -> None:
        now = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))[:-3] # [:-3] crops the extra milliseconds digits
        tab = '\t'*offset
        fmt = f"[{now}]{tab} {text}\n"

        print(fmt, end='')
        with open(self.file, 'a', encoding='utf-8') as f:
            f.write(fmt)

logger_ = Log()

def _dbgl() -> int:
    """
    Returns the line where this function
    was called
    """
    return inspect.currentframe().f_back.f_lineno

# def _log(file: str, text: str, tabbing = 0) -> None:
#     print("[{}]{} {}".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))[:-3], "\t"*tabbing, text))
#     with open(file, 'a', encoding='utf-8') as f:
#         f.write("[{}]{} {}\n".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))[:-3], "\t"*tabbing, text))

class ReachedMaxRetriesError(Exception):
    pass

def db_retry_until_unlocked(directory: str, cmd: str, sleep_time = 2, max_retries = 10, logfile = LOGFILE) -> list:
    """
    Handles the 'database is locked' exception
    and tries to execute the function until the db
    gets unlocked, and closes the connection afterwards.
    :param file: logfile
    :param directory: directory of the db
    :param cmd: sqlite command 
    :param time: sleep time between attempts in seconds (default = 2)
    :param max_retries: amounts of attempts allowed until breaking (default = 10)
    """
    _flag = False
    retry_count = 0
    con = sqlite3.connect(directory)
    cur = con.cursor()
    while not _flag:
        if retry_count < max_retries:
            try:
                cur.execute(cmd)
                con.commit()
                _flag = True
            except sqlite3.OperationalError:
                logger_.log(logfile, f"[{retry_count}]Database is locked, reattempting again in {sleep_time} seconds...", 2)
                retry_count += 1
                sleep(sleep_time)
        else:
            logger_.log(logfile, f"======Reached max retries ({max_retries}), breaking")
            raise ReachedMaxRetriesError("Reached max retries")
    fetched = cur.fetchall()
    con.close()
    return fetched

def notify_admins(text: str) -> None:
    """
    Notifies all admins with a text
    and logs it.
    :param text: text to send
    """
    for admin in ADMINS:
        BOT.send_message(admin, text)
    logger_.log(text)

if __name__ == '__main__':
    """Tests"""
    test_logger = Log("D:\\test\\bin\\bruhlog.txt")
    test_logger.log(_dbgl(), 2)
    test_logger.log(_dbgl(), 1)
    test_logger.log(2)
    test_logger.log(_dbgl(), 0)
