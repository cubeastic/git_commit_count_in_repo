from requests import get    # Import the function to talk with the API
from time import mktime, strptime   # Import the function for time conversion
from os import path, system     # Import the function to check for the existence of config files
from sys import exit    # Import the function for future uses
import xml.etree.ElementTree as Et  # Import the function for xml handling
from beautifultable import BeautifulTable   # Import the function to make the final table


# A class that talks with GitHub API and receives the number of commits and new brances according to the dates
class GitCounter:
    
    def __init__(self):
        self.config_file = "config.xml"
        if path.exists(self.config_file):
            self.token = self.get_config("git_token")   # GitHubs API Personal Token
            self.repos_file = self.get_config("repos_file")     # The file that holds the repositories
            self.from_date = int(mktime(strptime(self.get_config("from_date"), "%d/%m/%Y")))    # Convert to Unix
            self.to_date = int(mktime(strptime(self.get_config("to_date"), "%d/%m/%Y")))        # Convert to Unix
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

    # Parse the list and extract the owner and the repo name
    def get_list(self):
        if path.exists(self.repos_file):
            with open(self.repos_file) as f:
                for i in f:
                    # { owner: [name, commits] }
                    self.repositories[i.split("/")[3]] = [i.split("/")[4].replace("\n", ""), 0]
            return True
        else:
            print("ERROR: {0} was not found".format(self.repos_file))
            exit()

    # Count the commits using the given owner and repo name and counter
    def count_commits(self, owner, repo):
        if get("https://api.github.com", headers=self.headers).status_code not in self.errors:
            json_obj = get(self.commit_url.format(owner, repo[0]), headers=self.headers).json()
            try:
                if json_obj["message"] == "Not Found":
                    print("ERROR: please check the repository name, {0} was not found".format(repo[0]))
                    exit()
            except TypeError:
                pass
            for o in json_obj:
                if self.from_date < o["week"] < self.to_date:
                    repo[1] += o["total"]
            return repo[1]
        else:
            print("ERROR: please enter a valid token key")

    # Count the number of new branches between the dates that were provided
    def branch_check(self, owner, repo):
        if get("https://api.github.com", headers=self.headers).status_code not in self.errors:
            json_obj = get(self.branches_url.format(owner, repo[0]), headers=self.headers).json()
            # Only if there are more than one branches, check for new ones. 1 = master
            if len(json_obj) > 1:
                cnt = 0
                for o in json_obj:
                    b = get(self.branch_url.format(owner, repo[0], o["name"]), headers=self.headers).json()
                    # Before checking, convert the given time zone time to unix
                    bd = int(mktime(strptime(str(b["commit"]["commit"]["author"]["date"]), "%Y-%m-%dT%H:%M:%SZ")))
                    if self.from_date < bd < self.to_date:
                        cnt += 1
                return cnt

    # Build the table for the use to see the results
    def build_table(self):
        if self.get_list():
            table = BeautifulTable()
            # According to the users request
            table.column_headers = ["Name", "Commits", "New Branches"]
            for owner, repo in self.repositories.items():
                table.append_row([repo[0], self.count_commits(owner, repo), self.branch_check(owner, repo)])
                yield table


if __name__ == "__main__":
    a = GitCounter()
    # Print the table with the results
    for row in a.build_table():
        print("\033[H\033[J")
        print(row)
