from http.server import BaseHTTPRequestHandler

from server import run_server

import requests, adminstat.adminparser as parser, datetime
from adminstat.admins import AdminDaemon as AD
from adminstat import antiddos

def sortAdmins(admin):
    return admin.get_all()

def DO_STUFF():
    S = requests.Session()

    resp = S.get("https://gta-trinity.ru/")
    code = antiddos.get(resp.text)

    cookies = dict(
        name='REACTLABSPROTECTION',
        value=code,
        path='/',
        domain='gta-trinity.ru',
        expires=2145916555,
        rest = {'hostOnly':True}
    )
    S.cookies.set(**cookies)

    data = S.get("https://gta-trinity.ru/rpgmon/bans.php").text
    #data = open("testdata.htm", "r", encoding="utf-8").read()
    P = parser.Parser(data)
    P.parse(1000)

    daemon = AD()
    mon = datetime.datetime.today()
    tocount = 0
    skipped = 0
    for string in P.parsed_data:
        #Смотрим за текущий месяц
        if mon.strftime("%m") == string.date.strftime("%m"):
            daemon.add(string.admin, string.action, string.category)
            tocount += 1
        else:
            skipped += 1
    daemon.admins.sort(key = sortAdmins, reverse=True)
    return daemon


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        info = DO_STUFF()
        print(info)
        #####
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        #####
        self.wfile.write('<html><head><meta charset="utf-8">'.encode())
        self.wfile.write('<title>Админ стата</title></head><body>'.encode())

        self.printStat(info)
        
        self.wfile.write('</body></html>'.encode())

    def printStat(self, daemon):
        i = 1
        total = 0
        for admin in daemon.admins:
            self.wfile.write(f"[{i}] {admin.nick}: {admin.get_all()}<br>".encode())
            total += admin.get_all()
            i += 1
        self.wfile.write(f"===================<br>Всего наказаний: {total}<br>".encode())


run_server(handler_class=HttpGetHandler)
