import os
import git
from colorama import Fore, Style


class GitDriver:
    def __init__(self):
        cwd = os.getcwd()

        if not os.path.exists(os.path.join(cwd, ".git")):
            raise RuntimeError("GitLazy must be invoked from root forlder of the repository (where .git is)")
        
        self.repo = git.Repo(cwd)

    def get_current_diff(self, verbose=False):
        if "nothing to commit, working tree clean" in self.repo.git.status():
            raise RuntimeError("Repo is clean, no diff detected")
        
        self.raw_diff = ""

        git_status = self.repo.git.status()

        if "Changes not staged for commit" in git_status:
            self.raw_diff += self.repo.git.diff()

        if "Changes to be committed" in git_status:
            self.raw_diff += "\n"
            self.raw_diff += self.repo.git.diff(cached=True)
        
        if "Untracked files" in git_status:
            self.raw_diff += "\n"
            self.raw_diff += git_status

        if verbose:
            width = int(os.get_terminal_size().columns)
            header = ">" * 10 + " CURRENT GIT DIFF " + ">" * (width - 28)
            print(Fore.GREEN + header)
            print(Fore.WHITE + Style.DIM + self.raw_diff + Style.RESET_ALL + Fore.RESET)
            width = int(os.get_terminal_size().columns)

        return self.raw_diff
    
    def commit_with_comment(self, comment, ask_before_commit):
        if ask_before_commit:
            response = None
            width = int(os.get_terminal_size().columns)
            header = ">" * 10 + " USE SUGGESTED COMMENT? " + ">" * (width - 34)
            print(Fore.YELLOW + header + Fore.RESET)
            while response not in ["Y", "n"]:
                response = input("Are you sure you want to use this generated comment? Y/n")
            
            if response == "n":
                return
        
        self.stage()
        self.commit(comment)
    
    def stage(self):
        
        self.repo.git.add(all=True)

    def commit(self, comment):
        self.repo.git.commit(message=comment)

