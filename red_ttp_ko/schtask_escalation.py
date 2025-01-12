# Name: Scheduled Task Privilege Escalation
# rta: schtask_escalation.py
# ATT&CK: T1053

import time
import os
import common

# Ref. Using schtasks
#     - https://ychcom.tistory.com/entry/schtasks-%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC-%EC%9E%91%EC%97%85-%EC%8A%A4%EC%BC%80%EC%A4%84%EB%9F%AC-%EC%82%AC%EC%9A%A9%EB%B2%95


def schtasks(*args, **kwargs):
    return common.execute(['schtasks.exe'] + list(args), **kwargs)


def main():
    common.log("Scheduled Task Privilege Escalation")

    task_name = 'test-task-rta'
    file_path = os.path.abspath('task.log')
    command = "cmd.exe /c whoami.exe > " + file_path

    # Delete the task if it exists
    code, output = schtasks('/query', '/tn', task_name)
    if code == 0:
        schtasks('/delete', '/tn', task_name, '/f')

    code, output = schtasks('/create',  '/tn', task_name, '/ru', 'system', '/tr', command, '/sc', 'onlogon')
    if code != 0:
        common.log("Error creating task", log_type="!")
        return

    # Run the task and grab the file
    code, output = schtasks('/run', '/tn', task_name)
    if code == 0:
        time.sleep(2)
        common.print_file(file_path)
        time.sleep(1)
        common.remove_file(file_path)

    schtasks('/delete', '/tn', task_name, '/f')


if __name__ == "__main__":
    main()
