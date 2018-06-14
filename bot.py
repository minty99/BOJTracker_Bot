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

channel = "#minty99"
server = "moe.uriirc.org"
port = 16664
nickname = "minty_BOJbot"

current = get_AC_List("mhkim4886")
irc = IRC()
irc.connect(server, channel, port, nickname)
twitter = Twitter()

while True:
    now = get_AC_List("mhkim4886")
    print("UPDATE: Database")
    for p in now:
        if p not in current:
            irc.send(channel, "minty99 solved https://boj.kr/" + str(p))
            twitter.send("#Solved: https://boj.kr/" + str(p))
    current = now[:]
    time.sleep(10)
