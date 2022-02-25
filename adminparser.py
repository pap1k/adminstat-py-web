import re, actiontypes as AT, datetime

class ParsedString:
    date : datetime
    action: int
    admin: str
    category : str
    reason: str
    def __init__(self, date : datetime, action: int, admin : str, category : str, reason : str):
        self.date = date
        self.action = action
        self.admin = admin
        self.category = category
        self.reason = reason
    def print(self):
        print(f"Parsed string\n--date: {self.date}\n--action: {self.action}\n--admin: {self.admin}\n--categoty: {self.category}\n--reason: {self.reason}\n\n")

class Parser:
    raw_data : str
    parsed_data : list = []

    def __init__(self, document) -> None:
        self.raw_data = document.split("</span>\n<br>")[1]
    
    def _show_raw(self):
        open("_output.txt", "w", encoding="utf-8").write(self.raw_data)
        print("Saved to _output.txt")

    def _show_parsed(self):
        for v in self.parsed_data:
            v.print()

    def parse(self, count : int = 0):
        subarray = self.raw_data.split("<br>") if count == 0 else self.raw_data.split("<br>")[0:count]
        for string in subarray:
            if (not ("Комментарий" in string)) and (not ("превышено допустимое количество предупреждений" in string)) and (not ("разбанил") in string):
                self.parsed_data.append(self.parse_string(string))

    def parse_string(self, string) -> ParsedString:
        string = string.replace("\n", "")
        redate = re.findall(r"\[(\d\d):(\d\d):(\d{4})\]", string)[0]
        date = None
        if len(redate) == 3 :
            date = datetime.datetime(int(redate[2]), int(redate[1]), int(redate[0]))
        
        action = re.findall(r"\] (\w): ", string)[0]
        act = AT.TYPE_UNKNOWN

        if action == "B":
            act = AT.TYPE_BAN
        elif action == "U":
            act = AT.TYPE_UNABN
        elif action == "W":
            act = AT.TYPE_UNWARN if "снял" in string else AT.TYPE_WARN
        elif action == "J":
            act = AT.TYPE_UNJAIL if "освобожден" in string else AT.TYPE_JAIL
        elif action == "M":
            act = AT.TYPE_UNMUTE if "снял" in string else AT.TYPE_MUTE
        elif action == "N":
            act = AT.TYPE_UNBANNAME if "снял" in string else AT.TYPE_BANNAME
        else:
            act = AT.TYPE_UNKNOWN

        rename = re.findall(r"дминистрат\w+\b (\w+)\b[,\s]", string)
        aname = rename[0] if len(rename) > 0 else "ANON"

        category = None
        if act == AT.TYPE_BAN: category = re.findall(r"причина: \[(.*) -", string)[0]

        reason = None
        if act == AT.TYPE_JAIL: reason = re.findall(r"тюрьму.*за (.*)\.", string)[0]
        if act == AT.TYPE_BAN: reason = re.findall(r"причина:.*\] (.*)", string)[0]
        if act == AT.TYPE_WARN: reason = re.findall(r"причина:\s(.*)", string)[0]

        #error check
        _basic = date == None or act == None or aname == None
        _rc = reason == None and category == None
        if _basic:
            print("=============\nERROR WHILE PARSING (basic)\nRaw string: "+string+"\n==============")
        # if _rc:
        #     print("=============\nERROR WHILE PARSING (rc)\nRaw string: "+string+"\n==============")
        if act == 1 and aname == "ANON" and category == "W":
            print(string)
        return ParsedString(date, act, aname, category, reason)