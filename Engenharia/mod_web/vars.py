import os

from os import path


defUserDir = path.expanduser("~")
defProfileDir = path.join(defUserDir, "AppData", "Local",
                          "Google", "Chrome", "User Data")
defDownloadDir = path.join(defUserDir, "Downloads")