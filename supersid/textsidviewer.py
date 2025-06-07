"""SuperSID text mode viewer.

Minimal output for SuperSID in text mode i.e. within terminal window.

Each Viewer must implement:
- __init__(): all initializations
- run(): main loop to get user input
- close(): cleaning up
- status_display(): display a message in a status bar or equivalent
"""
import sys
import readchar
from threading import Timer
from time import sleep

from config import FILTERED, RAW, print_config


class textSidViewer:
    def __init__(self, controller):
        self.version = "1.3.1 20150421 (text)"
        print("SuperSID initialization")
        self.controller = controller
        self.MAXLINE = 70
        self.print_menu()
        self.timer = Timer(0.5, self.check_keyboard)
        self.timer.start()

    def run(self):
        """Loop waiting for keyboard interrupt.

        i.e. do nothing until user press 'X' or CTRL-C
        """
        try:
            while self.controller.__class__.running:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            pass

    def status_display(self, msg):
        print(("\r" + msg + " "*self.MAXLINE)[:self.MAXLINE],  end='')
        sys.stdout.flush()

    def update_psd(self, Pxx, freqs):
        pass

    def close(self):
        self.timer.cancel()

    def print_menu(self):
        print("\n" + "-" * self.MAXLINE)
        print("Site:", self.controller.config['site_name'], " " * 20, end='')
        print("Monitor:", self.controller.config['monitor_id'])
        print("-" * self.MAXLINE)
        print(" F) save Filtered buffers")
        print(" R) save Raw buffers")
        print(" E) save Extended raw buffers")
        print("-" * self.MAXLINE)
        print(" C) list the Config file(s) parameters")
        print(" V) Version")
        print(" ?) display this menu")
        if self.controller.config['hourly_save'] == 'YES':
            print(" X) eXit (with saving)")
        else:
            print(" X) eXit (without saving)")
        print("-" * self.MAXLINE)

    def check_keyboard(self):
        s = readchar.readkey().lower()
        if s == "x":
            self.controller.close()
        elif s in ("f", "r", "e"):
            print("\n\n")
            for fname in self.controller.save_current_buffers(
                    log_type=FILTERED if s == "f" else RAW,
                    log_format='both_extended' if s == "e" else 'both'):
                print(fname, "saved")
            self.print_menu()
        elif s == "?":
            self.print_menu()
        elif s == "c":
            print_config(self.controller.config)
            self.print_menu()
        elif s == "v":
            print("\n")
            print(self.controller.about_app())
            self.print_menu()
        else:
            sys.stdout.write('\a')  # terminal bell
        # call again in half a second to check if a new key has been pressed
        if s != "x":
            self.timer = Timer(0.5, self.check_keyboard)
            self.timer.start()
