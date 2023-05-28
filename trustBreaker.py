import datetime
import json
import os
import time
from git_faker import _pull_shark, _pair_extraordinaire, fake_readme, get_user_email, github_add_contributors_to_repository, github_add_fake_commits_to_repository, github_open_issue, github_close_issue
from simple_term_menu import TerminalMenu as tm
import click
import dotenv

import datetime


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'

dotenv.load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USER = None
EMAIL = None
REPO = None

SLEEP_TIME = 5

OPTIONS = ['Celeb Cameo', 'Fake Activity', "Spoof Achievements", "Fake Profile Stats"]
DONE = []

TOTAL_MERGED_PRS = 0

LOGO = """

      ^~~~~~~~~~^ .~~~~~^:.    .~~^     ^~~.   .^!7!~:..~~~~~~~~~~:                                 
      P&##@@@##&P :&@@##&&#Y.  !@@5     B@@^  ?#@###&&~.###&@@&##&7                                 
      ...:&@&:... :@@B. .P@@J  !@@5     B@@^ ^@@#:  .^  .. !@@P ..                                  
         .#@#.    :@@#!!7B@&~  !@@5     B@@^  Y@@#57:      !@@5                                     
         .#@#.    :@@@B&@@Y.   !@@5     B@@^   :75#@@G^    !@@5                                     
         .#@#.    :@@B .5@&7   ~@@B.   ^&@&: .:    7@@G    !@@5                                     
         .&@&.    :@@#   ?@@P:  ?#@&GGB@@B!  !@#GPG#@#~    !@@P                                     
          777     .77!    ^7?~   .~7JJJ7^    .~7JJJ7~.     :77~                                     
                                                                                                    
        ......       ......       ........      ...       ...     ...  ........   ......            
       7&######GJ.  ~&&####B5~   7&#####&Y     5&&&5     .B&B.  ^G&B! :#&####&B. ^#&####BP!         
       7@@5:^~G@@J  !@@G^^!#@@~  ?@@5:^^^:    ?@@J@@?    .&@# .Y@@5:  :&@#^^^^^  ^@@#^^!B@@7        
       7@@P77?B@B^  !@@P.:^B@&^  7@@P7777:   ~@@Y Y@@^   .&@#7#@B^    :&@#7777~  ^@@B:.^G@@!        
       7@@#GGB&&P^  !@@@#@@@Y:   7@@#GBBB^  .#@&~:~&@B.  .&@@&&@B^    :&@@BBBBJ  ^@@@#&@@5^         
       7@@J   !@@#  !@@P:!&@P:   7@@J       5@@&&&&&@@5  .&@&^^B@@?   :&@B       ^@@B:~#@G^         
       ?@@BYY5#@@J  !@@P  :G@&7  ?@@BYYY57 ?@@P.:::.P@@? .&@#. .Y@@P: :@@@YYYYJ. ^@@B  .P@@J        
       ~555555Y7^   ^557    J55~ ~555555P7 Y55:     :55Y..Y5J    755? .Y55555PY. :55J    ?55!   
       
       
       
"""


@click.command()
def trustBreaker():
    global GITHUB_TOKEN, OPTIONS, DONE, USER, EMAIL, REPO
    OPTIONS = [option for option in OPTIONS if option not in DONE]

    print(LOGO)

    selection = init_fun()
    if selection == 'Celeb Cameo':
        _celeb_cameo()
        DONE.append(selection)
    elif selection == 'Fake Activity':
        _fakeActivity()
        print(f"You were busy! - https://github.com/{USER}/")
        DONE.append(selection)
    elif selection == "Spoof Achievements":
        _spoof_achievements()
        print(f"Achievements spoofed! - https://github.com/{USER}")
        DONE.append(selection)
    elif selection == "Fake Profile Stats":
        _fake_profile_stats()
        print(f"Profile stats faked! - https://github.com/{USER}")
        DONE.append(selection)
    trustBreaker()


def _fake_profile_stats():
    workplace = input("Please enter your desired workplace: ")
    profession = input("Please enter your desired profession: ")
    fake_readme(GITHUB_TOKEN, USER, profession, workplace)


def init_fun():
    global GITHUB_TOKEN, USER, EMAIL, REPO, OPTIONS
    print("Lets start by setting up your credentials...")
    while not GITHUB_TOKEN:
        GITHUB_TOKEN = input("Please enter your GitHub token: ")
        if not GITHUB_TOKEN.startswith("ghp_"):
            print("Invalid token!")
            GITHUB_TOKEN = None
    while not USER and not EMAIL:
        if USER and not EMAIL:
            print("did not find user mail, try a different one")
        USER = input("Please enter your desired GitHub username: ")
        EMAIL = get_user_email(GITHUB_TOKEN, USER)
    if not REPO:
        REPO = input("Please enter the name of the repository you want to manipulate (CASE SENSITIVE!)")
    mainMenu = tm(OPTIONS, title="Trust Breaker")
    optionsIndex = mainMenu.show()
    selection = OPTIONS[optionsIndex]
    return selection


def _celeb_cameo():
    print("\n\nselect the celebrities you want to add to your repository...\n\npress SPACE to choose, ENTER to confirm")
    celebs_list = ['Linus Torvalds [Linux Kernel]', 'Guido van Rossum [Python]', 'Joel Spolsky [Trello, Stack Overflow]', 'Markus Persson [Minecraft]', 'Kenneth Reitz [Requests]']
    celebsMenu = tm(celebs_list, title="Celebrities", multi_select=True)
    celebsIndex = celebsMenu.show()
    celebs = [celebs_list[idx] for idx in celebsIndex]
    print("spoofing up the celebs...")
    celebs_map = {
        'Linus Torvalds [Linux Kernel]': {'username': 'torvalds', 'email': 'joel@spolsky.com'},
        'Guido van Rossum [Python]': {'username': 'gvanrossum', 'email': 'guido@python.org'},
        'Joel Spolsky [Trello, Stack Overflow]': {'username': 'jspolsky', 'email': 'joel@spolsky.com'},
        'Markus Persson [Minecraft]': {'username': 'xNotch', 'email': 'markus@mojang.com'},
        'Kenneth Reitz [Requests]': {'username': 'kennethreitz', 'email': 'me@kennethreitz.org'}
    }
    celebs = [celebs_map[celeb] for celeb in celebs]
    github_add_contributors_to_repository(GITHUB_TOKEN, USER, REPO, celebs)
    celebs = [celeb["username"] for celeb in celebs]
    print(f"{' & '.join(celebs)} contributed to {REPO}! - https://github.com/{USER}/{REPO}\n\n")


def _fakeActivity():
    start_date = datetime.datetime(2022, 1, 1)
    end_date = datetime.datetime.now()
    print("Faking activity...")
    github_add_fake_commits_to_repository(GITHUB_TOKEN, REPO, EMAIL, USER, start_date, end_date)
    print(f"Activity faked! - https://github.com/{USER}")


def _spoof_achievements():
    print("\n\nselect the achievements you want to add to your profile...\n\npress ENTER to choose")
    achievements_list = ['Quickdraw (closed an issue / pull request within 5 minutes of opening)', 'Pair Extraordinaire (Coauthored commits on merged pull request)', 'Pull Shark (Opened a pull request that has been merged)', 'Code Explorer (pushed to 100 repositories)', 'Code Ninja (pushed to 1000 repositories)', 'Exit']
    is_finished = False
    finished = []
    while not is_finished and len(achievements_list) > 1:
        achievements_list = [achievement for achievement in achievements_list if achievement not in finished]
        achievementsMenu = tm(achievements_list, title="Achievements", multi_select=False)
        achievementsIndex = achievementsMenu.show()
        selection = achievements_list[achievementsIndex]
        if selection == 'Exit':
            is_finished = True
            print("Exiting...")
            break
        if selection == 'Quickdraw (closed an issue / pull request within 5 minutes of opening)':
            quickdraw()
            finished.append(selection)
        if selection == 'Pair Extraordinaire (Coauthored commits on merged pull request)':
            levels = ['1 [1 commit]', '2 [10 commits]', '3 [24 commits]', '4 [48 commits]']
            print("\n\nselect the level of Pair Extraordinaire you want to achieve...\n\npress SPACE to choose, ENTER to confirm")
            levelsMenu = tm(levels, title="Pair Extraordinaire", multi_select=False)
            levelsIndex = levelsMenu.show()
            lvl = levels[levelsIndex]
            lvl = int(lvl[0])
            pair_extraordinaire(lvl)
            finished.append(selection)
        if selection == 'Pull Shark (Opened a pull request that has been merged)':
            levels = ['1 [2 pull requests]', '2 [16 pull requests]', '3 [128 pull requests]', '4 [1024 pull requests - THIS WILL CONSUME ALOT OF API CALLS]']
            print("\n\nselect the level of Pull Shark you want to achieve...\n\npress SPACE to choose, ENTER to confirm")
            levelsMenu = tm(levels, title="Pull Shark", multi_select=False)
            levelsIndex = levelsMenu.show()
            lvl = levels[levelsIndex]
            lvl = int(lvl[0])
            pull_shark(lvl)
            finished.append(selection)


def quickdraw():
    issue_number = github_open_issue(REPO, USER, GITHUB_TOKEN)
    time.sleep(5)
    github_close_issue(issue_number, REPO, USER, GITHUB_TOKEN)
    print(f"Quickdraw done!")


def pair_extraordinaire(lvl=2):
    global TOTAL_MERGED_PRS
    if lvl == 1:
        _pair_extraordinaire(REPO, USER, GITHUB_TOKEN, EMAIL)
        TOTAL_MERGED_PRS += 1
    if lvl == 2:
        for i in range(10):
            _pair_extraordinaire(REPO, USER, GITHUB_TOKEN, EMAIL)
            TOTAL_MERGED_PRS += 1
            print(f"coauthored {i}/10 commits")
    if lvl == 3:
        for i in range(24):
            _pair_extraordinaire(REPO, USER, GITHUB_TOKEN, EMAIL)
            TOTAL_MERGED_PRS += 1
            print(f"coauthored {i}/24 commits")
    if lvl == 4:
        for i in range(48):
            _pair_extraordinaire(REPO, USER, GITHUB_TOKEN, EMAIL)
            TOTAL_MERGED_PRS += 1
            print(f"coauthored {i}/48 commits")
    print(f"Pair Extraordinaire done!")


def pull_shark(lvl=2):
    global TOTAL_MERGED_PRS
    if lvl == 1:
        while TOTAL_MERGED_PRS < 2:
            _pull_shark(REPO, USER, GITHUB_TOKEN, EMAIL)
            TOTAL_MERGED_PRS += 1
            time.sleep(SLEEP_TIME)
    if lvl == 2:
        while TOTAL_MERGED_PRS < 16:
            _pull_shark(REPO, USER, GITHUB_TOKEN, EMAIL)
            TOTAL_MERGED_PRS += 1
            time.sleep(SLEEP_TIME)
            print(f"merged {TOTAL_MERGED_PRS}/16 pull requests")
    if lvl == 3:
        while TOTAL_MERGED_PRS < 128:
            _pull_shark(REPO, USER, GITHUB_TOKEN, EMAIL)
            TOTAL_MERGED_PRS += 1
            time.sleep(SLEEP_TIME)
            print(f"merged {TOTAL_MERGED_PRS}/128 pull requests")
    if lvl == 4:
        while TOTAL_MERGED_PRS < 1024:
            _pull_shark(REPO, USER, GITHUB_TOKEN, EMAIL)
            TOTAL_MERGED_PRS += 1
            time.sleep(SLEEP_TIME)
            print(f"merged {TOTAL_MERGED_PRS}/1024 pull requests")
    print(f"Pull Shark done!")
