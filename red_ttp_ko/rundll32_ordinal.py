# Name: Rundll32 Loading by Ordinal
# rta: rundll32_ordinal.py
# ATT&CK: T1085
# Description: Executes "dsquery.dll" as mock malware through ordinal loading.

# Ref. about dsquery
#       - https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc732952(v=ws.11)

import subprocess
import time
import shutil
import common
import os

RUNDLL32 = "rundll32.exe"


def run_dll(dll, entry_point):
    common.log("Running %s with %s and entrypoint %s" % (RUNDLL32, dll, entry_point))
    common.execute([RUNDLL32, dll, entry_point], timeout=3, kill=True, )


def main():
    common.log("RunDLL32 with Ordinals")
    run_dll("dsquery.dll", "#258")
    dat_file = os.path.abspath("dsquery.dat")

    common.copy_file("C:\\Windows\\System32\\dsquery.dll", dat_file)
	# Ref. https://strontic.github.io/xcyclopedia/library/dsquery.dll-13DDA8DFDFF33BF5A2393EF4EE959620.html
	#      #258: OpenQueryWindow
    run_dll(dat_file, "#258")
    time.sleep(2)
    common.remove_file(dat_file)


if __name__ == "__main__":
    exit(main())
