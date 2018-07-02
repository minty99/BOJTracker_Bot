import requests
from irc import *
import time
from twitter import *
from bs4 import BeautifulSoup

def get_AC_List(username):
    resp = requests.get('https://www.acmicpc.net/user/' + username)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    all_prob = soup.select("div.col-md-9 > div > div.panel-body")
    prob_ac = all_prob[0].select("span.problem_number > a")
    ret = []
    for t in prob_ac:
        ret += [ int(t.text) ]
    return ret

def get_Update(username):
    print("get_Update: Database for " + username)
    now = get_AC_List(username)
    for p in now:
        if p not in current[username]:
            irc.send(channel[username], "\x02\x03" + "03" + "Accepted: https://boj.kr/" + str(p))
#           if username == "mhkim4886": twitter.tweet("Accepted! https://boj.kr/" + str(p))
    current[username] = now[:]

server = "moe.uriirc.org"
port = 16664
nickname = "minty_BOJbot"
db = open("DB.txt", "r")
channel = dict()
current = dict()
users = list()
irc = IRC()

while True:
    line = db.readline().split()
    if not line: break
    ID = line[0]
    chan = line[1]
    channel[ID] = chan
    current[ID] = get_AC_List(ID)
    users += [ ID ]
    if len(users) == 1: irc.connect(server, chan, port, nickname)
    else: irc.join(chan)
db.close()

# twitter = Twitter()

while True:
    for username in users:
        try:
            for i in range(4):
                text = irc.get_text()
                time.sleep(1)
            get_Update(username)
        except Exception as ex: pass
