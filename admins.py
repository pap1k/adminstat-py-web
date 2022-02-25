import actiontypes as AT

class Admin:
    warns:int = 0
    bans:dict
    nick:str
    namebans: int = 0
    jails:int = 0

    def __init__(self, nick) -> None:
        self.nick = nick
        self.bans  = {"R" : 0, "HR" : 0, "C" : 0, "HC" : 0 }
        self.warns = 0
        self.namebans = 0
        self.jails = 0
    def add_warn(self) -> int:
        self.warns += 1
        return self.warns
    def add_ban(self, category) -> list:
        self.bans[category] += 1
        return self.bans
    def add_nameban(self) -> int:
        self.namebans += 1
        return self.namebans
    def add_jail(self) -> int:
        self.jails += 1
        return self.jails
    def get_all(self) -> int:
        bans = self.bans["C"] + self.bans["HC"] + self.bans["R"] + self.bans["HR"]
        return bans + self.warns + self.namebans + self.jails
    
class AdminDaemon:
    admins : list
    def __init__(self) -> None:
        self.admins = []

    def add(self, nick, action, param = "") -> Admin:
        #print(nick, action, param)
        admin_ref = self._search(nick)
        if not admin_ref:
            admin_ref = self._create(nick)

        if action == AT.TYPE_BAN:
            admin_ref.add_ban(param)
        elif action == AT.TYPE_BANNAME:
            admin_ref.add_nameban()
        elif action == AT.TYPE_WARN:
            admin_ref.add_warn()
        elif action == AT.TYPE_JAIL:
            admin_ref.add_jail()
        return admin_ref

    def get(self, nick) -> Admin:
        admin_ref = self._search(nick)
        if not admin_ref:
            return None
        return admin_ref

    def _create(self, nick) -> Admin:
        ref = Admin(nick)
        self.admins.append(ref)
        return ref

    def _search(self, nick) -> Admin:
        for adm in self.admins:
            if adm.nick.lower() == nick.lower():
                return adm
        return None