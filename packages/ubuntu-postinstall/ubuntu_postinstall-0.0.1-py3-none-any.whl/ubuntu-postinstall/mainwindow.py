import os
from PySide6.QtWidgets import QMainWindow, QMessageBox
from concurrent.futures import ThreadPoolExecutor
from utils.gnome_utils import install_extension
from views.ui_main_window import Ui_MainWindow
from models.system_action import SystemAction
from time import sleep


class MainWindow(QMainWindow):
    def __init__(self, actions):
        super(MainWindow, self).__init__()
        self.actions = actions
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.pageCount = self.ui.stackedWidget.count()

        self.pageIndex = 0
        self.ui.stackedWidget.setCurrentIndex(self.pageIndex)

        self.ui.backButton.setEnabled(False)
        self.ui.exitButton.clicked.connect(self.close)
        self.ui.nextButton.clicked.connect(self.next_page)
        self.ui.backButton.clicked.connect(self.previous_page)

        self.ui.justPerfectionButton.clicked.connect(lambda: install_extension("just-perfection-desktop@just-perfection"))
        self.ui.gnome4xButton.clicked.connect(lambda: install_extension("gnome-ui-tune@itstime.tech"))

    def next_page(self):
        if self.pageIndex == self.pageCount - 4:
            self.ui.nextButton.setText("Proceed")
        elif self.pageIndex == self.pageCount - 3:
            msgBox = QMessageBox()
            msgBox.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
            msgBox.setText("Are you sure you want to make these modifications?\n" +
                           "NOTE: You are doing this at your own risk.")
            response = msgBox.exec()
            if response == QMessageBox.StandardButton.No:
                return

            self.ui.nextButton.setText("Finish")
            self.ui.nextButton.setEnabled(False)
            self.ui.backButton.setEnabled(False)
            self.ui.exitButton.setEnabled(False)
            executor = ThreadPoolExecutor(max_workers=1)  # Adjust max_workers as needed

            future = executor.submit(self.execute_actions)
            # Attach the callback to the future object
            future.add_done_callback(self.modifications_completed)
        elif self.pageIndex < self.pageCount - 3:
            self.ui.backButton.setEnabled(True)

        self.pageIndex = max(0, min(self.pageIndex + 1, self.pageCount - 1))
        self.ui.stackedWidget.setCurrentIndex(self.pageIndex)

    def previous_page(self):
        self.pageIndex = max(0, min(self.pageIndex - 1, self.pageCount-1))

        if self.pageIndex == 0:
            self.ui.backButton.setEnabled(False)

        self.ui.stackedWidget.setCurrentIndex(self.pageIndex)

    def is_checked(self, key):
        return getattr(self.ui, key).isChecked()

    def execute_actions(self):
        # if not linux
        if os.name != 'posix':
            print("This script is only for Linux systems.")
            sleep(3)
            return

        system_command = ""

        for key, action in self.actions.items():
            if not self.is_checked(key):
                continue

            if (isinstance(action, SystemAction)):
                for command in action.commands:
                    system_command += command.command + " && "
                continue

            print("Executing action: " + key)
            action.execute()

        if system_command != "":
            system_command += "echo System modifications completed."
            os.system(f"pkexec sh -c '{system_command}'")

    def modifications_completed(self, _):
        self.ui.applyTitle.setText(self.ui.finishLabel.text())
        self.ui.progressBar.setParent(None)

        self.ui.nextButton.setEnabled(True)
        self.ui.nextButton.setText("Finish")
        self.ui.nextButton.clicked.connect(self.close)
