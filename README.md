# DownloadHelperTool
Helper tool to download a list of urls provided by simple text file. Saves the files in the same folder structure as it is on the server.
```
+----------------------------------------------------------+
|     ___                  _              _                |
|    |   \ _____ __ ___ _ | |___  __ _ __| |  _ __ _  _    |
|    | |) / _ \ V  V / ' \| / _ \/ _` / _` |_| '_ \ || |   |
|    |___/\___/\_/\_/|_||_|_\___/\__,_\__,_(_) .__/\_, |   |
|                                            |_|   |__/    |
|                         _                                |
|                        | |__ _  _                        |
|                        | '_ \ || |                       |
|                        |_.__/\_, |                       |
|                              |__/                        |
|        _               _  _                              |
|     _ | |___ _ _  ___ | || |__ _ ___ _  _ ___ ___ _ _    |
|    | || / -_) ' \(_-< | __ / _` / -_) || (_-</ -_) '_|   |
|     \__/\___|_||_/__/ |_||_\__,_\___|\_,_/__/\___|_|     |
+----------------------------------------------------------+
|                          Usage:                          |
|          python3 download.py file_with_urls.txt          |
|                                                          |
|        This will download all files in the list.         |
|  The folder structure will be the same as in the list.   |
|        First folder will be the (sub)domain name.        |
+----------------------------------------------------------+
```

I wrote this little python helper after i saw jbeers11 downloading / copying js files and creating folders by hand.
Might be helpfull :-)
