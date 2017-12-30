from requests import get
from time import ctime, strftime

class GitQ:

    def __init__(self):
        self.owner

print(get("https://api.github.com/repos/cubeastic/sheets_to_slides/stats/commit_activity")).json()

print(ctime(int("1483833600")))
'Fri Sep 10 16:51:25 2010'
#time.strftime("%D %H:%M", time.localtime(int("1284101485")))
#'09/10/10 16:51'

