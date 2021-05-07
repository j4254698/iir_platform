# Name: RunDll32 with .inf Callback
# rta: rundll32_inf_callback.py
# ATT&CK: T1105
# Description: Loads RunDll32 with a suspicious .inf file that makes a local http GET

# Ref. about RunDLL32
#       - http://blog.naver.com/PostView.nhn?blogId=koromoon&logNo=220079686444
# Ref. about squiblydoo attack
#       - https://www.rocketcyber.com/blog-cyber-cases-from-the-soc-squiblydoo-attack
import time
import common

INF_FILE = common.get_path("bin", "script_launch.inf")


@common.dependencies(INF_FILE)
def main():
    # http server will terminate on main thread exit
    # if daemon is True
    common.log("RunDLL32 with Script Object and Network Callback")
    server, ip, port = common.serve_web()
    callback = "http://%s:%d" % (ip, port)
    common.clear_web_cache()

    common.patch_regex(INF_FILE, common.CALLBACK_REGEX, callback)

    rundll32 = "rundll32.exe"
	# Ref. https://docs.microsoft.com/en-us/windows/win32/api/setupapi/nf-setupapi-installhinfsectiona
	# Ref. UnregisterDlls Directive in .inf
	#       - https://docs.microsoft.com/en-us/windows-hardware/drivers/install/inf-unregisterdlls-directive
    dll_entrypoint = "setupapi.dll,InstallHinfSection"
    common.execute([rundll32, dll_entrypoint, "DefaultInstall", "128", INF_FILE], shell=False)

    time.sleep(1)
    common.log("Cleanup", log_type="-")
    common.execute("taskkill /f /im notepad.exe")
    server.shutdown()


if __name__ == "__main__":
    exit(main())
