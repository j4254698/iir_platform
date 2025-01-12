# Name: Powershell with Suspicious Arguments
# RTA: powershell_args.py
# ATT&CK: T1140
# Description: Calls PowerShell with suspicious command line arguments.

import os
import common
import base64


def encode(command):
    return base64.b64encode(command.encode('utf-16le'))


def main():
    common.log("PowerShell Suspicious Commands")
    temp_script = os.path.abspath("tmp.ps1")

    # Create an empty script     
    with open(temp_script, "wb") as f:
        f.write("whoami.exe\n")

    # powershell -encodedCommand: can use base64 encoding string
	#         > encodedCommand == encoded == ec
	# powershell -ExecutionPolicy: execution policy, byass: Nothing is blocked and there are no warnings or prompts.
	# iex(invoke-execute): run the string on the local computer
	#           Ref. https://sacstory.tistory.com/entry/PowerShell-IEX
	# u can find command alias by using powershell command:  get-alias -definition *
    powershell_commands = [
        'powershell -encoded %s' % encode('ping google.com'),
        'powershell.exe -ExecutionPol Bypass %s' % temp_script,
        'powershell.exe iex Get-Process',
        'powershell.exe -ec %s' % encode('Get-Process' + ' ' * 1000),
    ]

    for command in powershell_commands:
        common.execute(command)

    common.remove_file(temp_script)


if __name__ == "__main__":
    exit(main())
