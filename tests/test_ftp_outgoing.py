r"""
test for ftp_outgoing.py
"""
import os
import sys
import glob
import shutil
import unittest
import readchar

from test_common import script_relative_to_cwd_relative as relpath

sys.path.append(relpath(r"../src"))
from supersid_config import read_config, CONFIG_FILE_NAME # pylint: disable=wrong-import-order, wrong-import-position, import-error
import ftp_outgoing                                       # pylint: disable=wrong-import-order, wrong-import-position, import-error


class TestFtpOutgoing(unittest.TestCase):
    """ tests ftp_outgoing.py """

    config = {}
    server_error = True

    def setUp(self):
        self.incoming = relpath("." + self.config["ftp_directory"]) + os.sep
        self.outgoing = self.config["local_tmp"]
        csv_files = glob.glob(self.incoming + "*.csv")
        csv_files += glob.glob(self.outgoing + "*.csv")
        for file in csv_files:
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                os.rmdir(file)

    def ftp_send(self, files_to_send):
        """ common subfunction """
        error_count = ftp_outgoing.ftp_send(self.config, files_to_send)
        if self.server_error:
            if len(files_to_send) == 0:
                # immediate return of ftp_outgoing.ftp_send) if the list is empty
                self.assertEqual(error_count, 0)
            else:
                self.assertNotEqual(error_count, 0)
            expected_incoming_files = []
            expected_remaining_files = files_to_send
        else:
            self.assertEqual(error_count, 0)
            expected_incoming_files = [f.replace(r"..\outgoing", "incoming") for f in files_to_send]
            expected_remaining_files = []
        print(self.incoming + "*.csv")
        incoming_files = glob.glob(self.incoming + "*.csv")
        self.assertEqual(incoming_files, expected_incoming_files)
        remaining_files = ftp_outgoing.create_file_list(self.config)
        self.assertEqual(remaining_files, expected_remaining_files)

    def test_outgoing_is_empty(self):
        """
        1) test ftp_outgoing.create_file_list()
        with an empty outgoing folder
        note: setUp() deleted all *.csv files and folders in the outgoing folder
        files_to_send shall be an empty list

        2) test ftp_outgoing.ftp_send()
        no files shall be incoming at the ftp server
        """
        # 1)
        outgoing_files = []
        files_to_send = ftp_outgoing.create_file_list(self.config)
        self.assertEqual(files_to_send, outgoing_files)

        # 2)
        self.ftp_send(files_to_send)

    def test_outgoing_contains_folder(self):
        """
        1) test ftp_outgoing.create_file_list()
        ../outgoing/folder.csv is a folder that shall be ignored
        files_to_send shall be an empty list

        2) test ftp_outgoing.ftp_send()
        no files shall be incoming at the ftp server
        """
        # 1)
        outgoing_files = []
        folder_name = os.path.join(self.outgoing, f"{self.config['site_name']}.csv")
        os.makedirs(folder_name)
        self.assertTrue(os.path.isdir(folder_name))
        files_to_send = ftp_outgoing.create_file_list(self.config)
        self.assertEqual(files_to_send, outgoing_files)
        os.rmdir(folder_name)
        self.assertFalse(os.path.isdir(folder_name))

        # 2)
        self.ftp_send(files_to_send)

    def test_outgoing_contains_one_file(self):
        """
        1) test ftp_outgoing.create_file_list() 
        ../outgoing/file1.csv is a file that shall be found
        files_to_send shall contain the created file

        2) test ftp_outgoing.ftp_send()
        the created file shall be incoming at the ftp server
        """
        # 1)
        outgoing_files = []
        file_name =  os.path.join(self.outgoing, f"{self.config['site_name']}1.csv")
        outgoing_files.append(file_name)
        with open(file_name, "wt", encoding="utf-8") as file_desc:
            file_desc.write("")
        self.assertTrue(os.path.isfile(file_name))
        files_to_send = ftp_outgoing.create_file_list(self.config)
        self.assertEqual(files_to_send, outgoing_files)

        # 2)
        self.ftp_send(files_to_send)

    def test_outgoing_contains_two_files(self):
        """
        1) test ftp_outgoing.create_file_list() 
        ../outgoing/file1.csv is a file that shall be found
        ../outgoing/file2.csv is a file that shall be found
        files_to_send shall contain the created files

        2) test ftp_outgoing.ftp_send()
        the created files shall be incoming at the ftp server
        """
        # 1)
        outgoing_files = []
        for name in [f"{self.config['site_name']}1.csv", f"{self.config['site_name']}2.csv"]:
            file_name =  os.path.join(self.outgoing, name)
            outgoing_files.append(file_name)
            with open(file_name, "wt", encoding="utf-8") as file_desc:
                file_desc.write("")
            self.assertTrue(os.path.isfile(file_name))
        files_to_send = ftp_outgoing.create_file_list(self.config)
        self.assertEqual(files_to_send, outgoing_files)

        # 2)
        self.ftp_send(files_to_send)


def setup(ftp_server, ftp_login, ftp_password):
    """ generic setup for all tests """
    if os.path.isfile(CONFIG_FILE_NAME):
        os.remove(CONFIG_FILE_NAME)
    shutil.copy2(relpath("test_ftp_outgoing.cfg"), CONFIG_FILE_NAME)
    TestFtpOutgoing.config = read_config(CONFIG_FILE_NAME)
    if ftp_server is not None:
        TestFtpOutgoing.config["ftp_server"] = ftp_server
    if ftp_login is not None:
        TestFtpOutgoing.config["ftp_login"] = ftp_login
    if ftp_password is not None:
        TestFtpOutgoing.config["ftp_password"] = ftp_password


def main():
    """ the main function """
    batch = "True" == os.environ.get('UNITTEST_BATCH')
    TestFtpOutgoing.server_error = "True" == os.environ.get('UNITTEST_SERVER_ERROR')
    ftp_server = os.environ.get('UNITTEST_FTP_SERVER')
    ftp_login = os.environ.get('UNITTEST_FTP_LOGIN')
    ftp_password = os.environ.get('UNITTEST_FTP_PASSWORD')

    if not batch:
        warning = "This test will modify and/or delete the content of " \
                  "'Config' and 'outgoing' folders.\n" \
                  "It is up to you to take backups.\n" \
                  "Do you want to continue (Y|n)?"
        print(warning)

        while True:
            ch = readchar.readkey().lower()
            if ch in ['y', chr(0x0D), chr(0x0A)]:
                break
            if 'n' == ch:
                sys.exit()
            else:
                print(warning)

    setup(ftp_server, ftp_login, ftp_password)
    print(TestFtpOutgoing.config["ftp_server"])
    unittest.main()


if __name__ == '__main__':
    main()
