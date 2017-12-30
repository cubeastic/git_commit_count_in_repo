from requests import get
from time import ctime, strftime, localtime
from os import path
from sys import exit
import xml.etree.ElementTree as Et  # Import the function for xml handling
import time


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
        return strftime("%Y-%m-%d", localtime(int(t)))

    def count_commits(self):
        if self.repositories:
            for owner, repo in self.repositories.items():
                json_obj = get(self.api_addr.format(owner, repo)).json()
                for elem in json_obj:
                    try:
                        if self.last_X_months(elem["week"]):
                            print self.unix_to_time(elem["week"])
                    except:
                        print json_obj["message"]

    def last_X_months(self, t):
        return abs(t - time.time()) < (2592000 * self.time_frame)


a = GitCounter()
a.get_list()
a.count_commits()
