from os import path
import sys
import configparser
from tree import Tree
from banner import banner as help_msg
import time


class Timestamps:
    def __init__(self, comment: str = "---"):
        self.i = 0
        self.stamps = []
        self.ping('__init__')

    def ping(self, comment: str = "---"):
        self.i += 1
        self.stamps += [(time.perf_counter(), f'{self.i}-{comment}')]

    def printout(self):
        table = "-> {:>6} sec. <-> {:<40} <-"
        print(table.format("<>" * 3, "<>" * 20))
        print(table.format(round(self.stamps[-1][0] - self.stamps[0][0], 4), "<Application runtime>"))
        print(table.format("<>" * 3, "<>" * 20))
        if not I_am_developing:
            return
        # detailed Timetable
        for i in range(0, len(self.stamps) - 1):
            print(table.format(
                round(self.stamps[i + 1][0] - self.stamps[i][0], 4),
                self.stamps[i][1] + " => " + self.stamps[i+1][1]
            )
            )


timestamps = Timestamps()
config = configparser.ConfigParser()

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print(help_msg())
        exit()

    if not path.isfile(sys.argv[1]):
        print(f"File not found: {sys.argv[1]}")
        exit()
    with open(sys.argv[1], "r") as urlfile:
        urls = urlfile.read().splitlines()

    print(f"Load settings: {config.read('settings.ini')}... ", end="")
    print(f"{len(config.defaults())} keys loaded.")
    print(f"{len(config.sections())} other sections loaded.")
    timestamps.ping('Sorting')
    urls.sort(key=lambda s: len(s))

    timestamps.ping('Config')
    defaults_dict = config.defaults()
    # if there is a user defined section in the settings.ini file
    # specified key=value pairs will be overwritten with no need to change default settings
    # Todo: accept CLI arguments to overwrite setting
    # Todo: make using auth/cookie/headers work

    use_custom_section = defaults_dict.get('use_section', 'user')
    if use_custom_section in config.sections():
        users_dict = dict(config.items(use_custom_section, False))  # get(use_custom_section,)
        print(users_dict)
    else:
        users_dict = dict()

    tree = Tree(defaults_dict, users_dict)
    I_am_developing = tree.getconfig('I_am_developing')

    timestamps.ping('Adding URLs')
    for url in urls:
        tree.add(url)

    timestamps.ping('Make folders')
    tree.check_for_or_create_folders()

    timestamps.ping('Downloading files')
    tree.download_files()

    timestamps.ping('End')
    timestamps.printout()

