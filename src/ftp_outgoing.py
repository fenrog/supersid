#!/usr/bin/env python3

"""
Send data to FTP server from local_tmp ftp_directory.

Any .csv files in the local_tmp directory will be sent to the FTP server.
Once they are successfully transfered, the file will be deleted.
The idea is that this program will run periodically (hourly?), and make sure
that all the files are transfered, even if there are Internet or power outages.

Name: ftp_outgoing.py
Author: Steve Berl

Created: 2022-01-03

Module can be run from the command line, or invoked programmatically
Command line argument:

-c|--config supersid.cfg : the configuration file for its [FTP]
   and [PARAMETERS] sections

"""

import sys
import os
import ftplib
import glob
from socket import gaierror
import argparse
from supersid_common import exist_file
from supersid_config import read_config, CONFIG_FILE_NAME


def create_file_list(config):
    """Create a list of files to send to FTP server."""
    local_tmp = config.get('local_tmp')
    print(f"local_tmp: {local_tmp}")

    if not os.path.isdir(local_tmp):
        print(f"the 'local_tmp' folder '{local_tmp}' does not exist")
        sys.exit(1)

    pattern = f"{config.get('local_tmp')}{config.get('site_name')}*.csv"
    file_list = [file for file in glob.glob(pattern) if os.path.isfile(file)]

    return file_list


def ftp_send(config, files_to_send):
    """
    FTP the files to the server destination specified in the config.

    It is assumed that the current working directory is the directory
    containing the files in the list.
    """
    error_count = 0
    if files_to_send:
        print("Opening FTP session with", config.get('ftp_server'))

        try:
            ftp = ftplib.FTP(config.get('ftp_server'))
        except (gaierror, ConnectionRefusedError) as ex:
            print(ex)
            print("Check ftp_server in .cfg file")
            error_count = 1
            return error_count

        try:
            ftp.login(config.get('ftp_login'), config.get('ftp_password'))
            ftp.cwd(config.get('ftp_directory'))
            print("putting files to ", config.get('ftp_directory'))
            for file_name in files_to_send:
                print(f"Sending {file_name}")
                print("STOR " + os.path.basename(file_name))
                with open(file_name, 'rb') as file_desc:
                    res = ftp.storlines(f"STOR {os.path.basename(file_name)}", file_desc)
                if not res.lower().startswith('226 transfer complete'):
                    print(f"Upload of {file_name} failed: {res}")
                    error_count += 1
                else:
                    # Success, delete the files
                    print(f"Deleting: {file_name}")
                    os.remove(file_name)

        except ftplib.all_errors as err:
            print(err)
            error_count += 1
            # Dont delete file if there is an error.
            # We will try again another time.

        ftp.quit()
        print("FTP session closed.")
    return error_count


def main():
    """ the main function 
    - parses the command line,
    - reads the configuration file
    - creates the file list
    - sends the files to the ftp server
    - deletes the sent files on success
    """
    parser = argparse.ArgumentParser(description="Upload data files to server")
    parser.add_argument("-c", "--config", dest="cfg_filename",
                        type=exist_file,
                        default=CONFIG_FILE_NAME,
                        help="Supersid configuration file")

    args = parser.parse_args()

    # read the configuration file or exit
    cfg = read_config(args.cfg_filename)
    # read_config will check if local_tmp is configured and points to a
    # directory. It does check if the directory is writeable.

    files_to_send = create_file_list(cfg)
    error_count = ftp_send(cfg, files_to_send)

    print(f"Exit with {error_count} errors")
    sys.exit(0)


if __name__ == '__main__':
    main()
