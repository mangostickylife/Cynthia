import praw
import re
import datetime
import sqlite3  
import time
from columnar import columnar
client_id="MhhcADFvm4V1Vw"
client_secret="1HuWl3H-riu_bUZtCNaX3QIe6VThlw"
username="AmbitiousExternal922"
password="DWUT2nesh2nuld_juk"
user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/5311 (KHTML, like Gecko) Chrome/36.0.870.0 Mobile Safari/5311"


# for submission in subreddit.new(limit=100000):
#     matches = re.search("\$[a-zA-Z]+", submission.title)  
#     if matches is not None:
#         print(matches.group(0))
#         print(datetime.datetime.fromtimestamp(submission.created))


def query_subreddit_by_new(subreddit=str, limit=1000):
    reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent,
    )

    
    matches = []
    for submission in reddit.subreddit(subreddit).new(limit=limit):

        stocks = re.search("\$[a-zA-Z]+", submission.title)  

        if stocks is not None:
            localtime_epoch = time.localtime(submission.created_utc)
            localtime_formatted = time.strftime('%c', localtime_epoch)
            entry = [submission.name, submission.author.name, stocks.group(0), submission.title,  localtime_formatted, submission.created_utc]
            matches.append(entry)


    # headers = ["ID", "Author", "Symbol", "Title", "Local Time", "Epoch Time"]
    # table = columnar(matches, headers, no_borders=True)
    # print(table)

    return matches

def init_reddit():
    reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=user_agent,
    )
    return reddit

def init_table(subreddit):
    conn = sqlite3.connect('Cynthia.db')
    c = conn.cursor()
    c.execute("CREATE TABLE ? (ID text Primary Key, Author text, Symbol text, Title text, LocalTime text, EpochTime INTEGER)", subreddit)
    conn.close()

def add_row(subreddit, matches):
    conn = sqlite3.connect('Cynthia.db')
    c = conn.cursor()

    for match in matches:
        output = c.execute("SELECT * FROM ? WHERE ID=?", (subreddit, match[0]))
        print(output)


def check_table(subreddit, sumbission_id):
    conn = sqlite3.connect('Cynthia.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ? WHERE ID=?", (subreddit, sumbission_id))


def main():
    init_table("wallstreetbets")
    matches = query_subreddit_by_new("wallstreetbets", limit=1000)
    print(matches)


main()


     