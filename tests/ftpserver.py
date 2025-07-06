"""
twisted based ftp server that allows
anonymos login with read only access
user:pass logn with write access
"""
from twisted.cred.checkers import AllowAnonymousAccess, InMemoryUsernamePasswordDatabaseDontUse
from twisted.cred.portal import Portal
from twisted.internet import reactor
from twisted.protocols.ftp import FTPFactory, FTPRealm

db = InMemoryUsernamePasswordDatabaseDontUse()
db.addUser("user", "pass")

p = Portal(FTPRealm('./', userHome='.'), (AllowAnonymousAccess(), db))

f = FTPFactory(p)

reactor.listenTCP(21, f)
reactor.run()
