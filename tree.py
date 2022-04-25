import os
from typing import Optional

import requests
from collections import namedtuple

FileLink = namedtuple('FileLink', 'web local')


class Tree:

    def __init__(self, default_config, user_config: Optional[dict]):
        """
        The __init__ function is called when a new instance of the class is created.
        It initializes the attributes of an object, and it can take arguments that
        are passed through to __init__ as variables. In this case, we are setting up
        the tree_ attribute with an empty dictionary. It will be filled with the
        folder and file names.
        
        :param self: Used to Refer to an instance of a class.
        :param default_config: Used to Store the configuration of the class.
        :return: The object of the class.
        """
        self.default_config = default_config
        self.user_config = user_config
        self.tree_ = dict()
        self.download_list = []
        self.download_folder = os.path.realpath(self.getconfig('download_dir'))

    def getconfig(self, key):
        return self.user_config.get(
            key,
            self.default_config.get(
                key, ""
            )
        )

    def add(self, new_url: str):
        """
        The add function adds a new url to the tree.
        It takes in a string, and splits it into its domain, path and filename components.
        If the domain is not already in the tree's keys, it adds it as such with an empty dictionary as its value.
        If the path is not already in that dictionary's keys, then it adds that key with an empty list as its value.
        Finally  we add our file name to this list.
        
        :param self: Used to Access variables that belongs to the class.
        :param new_url: Used to Pass in the url that is being added to the tree.
        :return: The number of nodes in the tree.
        
        """
        # new_url = new_url.replace("://", "__", 1)

        protocol__domain, url__ = new_url.replace("://", "__", 1).split('/', 1)
        parameter_ = url__.split("?")[1] if len(url__.split("?")) == 2 else ""
        url_ = url__.split("?")[0].split("/")

        domain_, path_, filename_ = protocol__domain, "/".join(url_[0:-1]), url_[-1]

        # filename_ = filename_.split("?")[0] if len(filename_.split("?")) > 1 else filename_
        # prepare a List for Downloading
        web = os.path.join(
            domain_.replace("__", "://"),
            path_,
            filename_
        )
        local = os.path.join(
            self.download_folder,
            web.replace("://", "__")
        ).split("?")[0]

        self.download_list += [FileLink(web=web, local=local)]

        if domain_ not in self.tree_.keys():
            self.tree_[domain_] = {path_: [filename_.split("?")[0]]}
        elif path_ not in self.tree_[domain_].keys():
            self.tree_[domain_][path_] = [filename_.split("?")[0]]
        else:
            self.tree_[domain_][path_] += [filename_.split("?")[0]]

    def get_domain_names(self):
        """
        The get_domain_names function returns a list of all the domain names in the database.
        
        :param self: Used to Access variables that belongs to the class.
        :return: A list of the domain names that are associated with the account.
        
        """
        return self.tree_.keys()

    def get_domain_paths(self, domain):
        """
        The get_domain_paths function returns a list of paths for the given domain.
        Sorted by most nested folders to lesseror none.

        :param self: Used to Access the class attributes.
        :param domain: Used to Specify the domain of the paths.
        :return: A list of all the paths in a domain.

        """
        pathnames = list(self.tree_[domain].keys())
        pathnames.sort(key=lambda s: s.count("/"), reverse=True)
        return pathnames

    def __call__(self):
        """
        The __call__ function is a special method that allows instances of the class to be called as functions.
        The __call__ function is called when an instance of the class is used like a function, i.e. with brackets:
        
            foo()
        
        :param self: Used to Reference the object itself.
        :return: The tree_ dictionary
        """
        return self.tree_

    def check_for_or_create_folders(self):

        """
        The check_for_or_create_folders function checks to see if the folders in the pathname exist. If they don't, it creates them.
        
        :param self: Used to Access the attributes and methods of the class in a method.
        :return: A dictionary of the domains and their paths.
        """

        for domain in self.tree_.keys():
            self.process_mkdir(domain)
            for pathname in self.get_domain_paths(domain):
                self.process_mkdir(f'{domain}/{pathname}')

    def process_mkdir(self, folder):
        """
        The process_mkdir function creates a folder in the download directory.
        The function takes one argument, which is the name of the folder to be created.
        If that folder already exists, it will print a message and skip over that step.
        Otherwise, it will create the new directory.

        :param self: Used to Access the attributes and methods of the class in python.
        :param folder: Used to Create a folder in the download directory.
        :return: None.

        """

        folder = os.path.join(self.download_folder, folder)
        if os.path.exists(folder):
            return
        print(f'Folder: {folder}', end="")
        try:
            os.makedirs(folder, exist_ok=True)
        except OSError as error:
            print('\t -> Error: ', error)
            return
        if os.path.exists(folder):
            print("\t... created.")

    def download_files(self):
        for file in self.download_list:
            response = requests.get(file.web, )
            if response.status_code != 200:
                fname = file.local.split("/")[-1]
                print("_" * 5, end="")
                print("|", fname, "|", end="")
                print("_" * (80-5-4-len(fname)))

                print(f"[!] Error (Status code: {response.status_code}) with file: ")
                print("[!]", file.web, "[!]", sep="\t")
                print("_" * 80)
            else:
                with open(file.local, 'wb') as localfile:
                    localfile.write(response.content)
