from requests import get
from time import ctime, strftime, localtime
from os import path
from sys import exit
import xml.etree.ElementTree as Et  # Import the function for xml handling


class GitCounter:
    
    def __init__(self):
        self.config_file = "config.xml"
        if path.exists(self.config_file):
            self.repos_file = self.get_config("repos_file")
            self.time_frame = self.get_config("last_X_months")
            self.repositories = dict()
            self.api_addr = "https://api.github.com/repos/{0}/{1}/stats/commit_activity"
        else:
            print("ERROR: {0} was not found".format(self.config_file))
            exit()

    # Loop through the config file and return the requested value from the requested tag
    def get_config(self, field):
        t = Et.parse(self.config_file)
        for i in t.getroot():
            if i.tag == field:
                return i.text

    def get_list(self):
        if path.exists(self.repos_file):
            with open(self.repos_file) as f:
                for i in f:
                    self.repositories[i.split("/")[3]] = i.split("/")[4].replace("\n", "")
        else:
            print("ERROR: {0} was not found".format(self.repos_file))
            exit()

    def unix_to_time(self, t):
        return strftime("%d/%m/%y", localtime(int(t)))

    def count_commits(self):
        if self.repositories:
            for owner, repo in self.repositories.items():
                print(get(self.api_addr.format(owner, repo))).json()

    def last_X_months(self):
        if abs(now - self.unix_to_time(time)) < X

a = GitCounter()
a.get_list()
a.count_commits()
