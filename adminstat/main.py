import requests, antiddos, adminparser as parser, datetime
from admins import AdminDaemon as AD

def sortAdmins(admin):
    return admin.get_all()

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
mon = datetime.datetime(2021, 12, 1)
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
