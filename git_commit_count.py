from requests import get
from time import strftime, localtime, mktime, strptime
from datetime import datetime
from os import path
from sys import exit
import xml.etree.ElementTree as Et  # Import the function for xml handling
from beautifultable import BeautifulTable


class GitCounter:
    
    def __init__(self):
        self.config_file = "config.xml"
        if path.exists(self.config_file):
            self.token = self.get_config("git_token")
            self.repos_file = self.get_config("repos_file")
            self.from_date = int(mktime(strptime(self.get_config("from_date"), "%d/%m/%Y")))
            self.to_date = int(mktime(strptime(self.get_config("to_date"), "%d/%m/%Y")))
            self.repositories = dict()
            self.commit_url = "https://api.github.com/repos/{0}/{1}/stats/commit_activity"
            self.branches_url = "https://api.github.com/repos/{0}/{1}/branches"
            self.branch_url = "https://api.github.com/repos/{0}/{1}/branches/{2}"
            self.headers = {'Authorization': 'token {}'.format(self.token)}
            self.errors = (401, 400, 403, 404)

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
                    self.repositories[i.split("/")[3]] = [i.split("/")[4].replace("\n", ""), 0]
            return True
        else:
            print("ERROR: {0} was not found".format(self.repos_file))
            exit()

    def count_commits(self):
        if get("https://api.github.com", headers=self.headers).status_code not in self.errors:
            if self.repositories:
                for owner, repo in self.repositories.items():
                    json_obj = get(self.commit_url.format(owner, repo[0]), headers=self.headers).json()
                    for o in json_obj:
                        if self.from_date < o["week"] < self.to_date:
                            repo[1] += o["total"]
                return True
        else:
            print("ERROR: please enter a valid token key")

    def branch_check(self):
        if get("https://api.github.com", headers=self.headers).status_code not in self.errors:
            if self.repositories:
                for owner, repo in self.repositories.items():
                    json_obj = get(self.branches_url.format(owner, repo[0]), headers=self.headers).json()
                    if len(json_obj) >= 1:
                        for o in json_obj:
                            sjson_obj = get(self.branch_url.format(owner, repo[0], o["name"]), headers=self.headers).json()
                            for so in sjson_obj:
                                print(so)

                return True

    def build_table(self):
        if self.count_commits() and self.branch_check():
            table = BeautifulTable()
            table.column_headers = ["Name", "Commits", "New Branches"]
            for owner, repo in self.repositories.items():
                table.append_row([repo[0], repo[1], "test"])
            return table


if __name__ == "__main__":
    a = GitCounter()
    if a.get_list():
        print(a.build_table())

        # Convert from timestamp
        # value = datetime.fromtimestamp(timestamp)
        # print(value.strftime('%d-%m-%Y'))