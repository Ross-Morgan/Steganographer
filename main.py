# I am entirely aware this code has nowhere near enough comments :)

# Stdlib imports
import getpass
import os
import pathlib
import sys
from queue import Queue

# Module imports
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

# File imports
from assets import Assets
from encrypter import ImageEncrypter

WINDOW_TITLE = "Steganographer"
WINDOW_ICON =  Assets.image_icon
WIDTH, HEIGHT = 640, 480

USER = getpass.getuser()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QWidget=None):
        super(MainWindow, self).__init__(parent)
        self._filetypes = (("JPEG Images","*.jpg"), ("All Files", "*.*"))
        self._qfont = QtGui.QFont()
        self._qfont.setPointSize(20)
        self._opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        self._opacity_effect.setOpacity(0)

        self.encrypter = ImageEncrypter()
        self.current_image = None
        self.image_queue = Queue()

        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))
        self.setFixedSize(WIDTH, HEIGHT)

        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(0, 0, WIDTH, HEIGHT)
        self.background.setPixmap(QtGui.QPixmap(Assets.background))

        self.logo = QtWidgets.QLabel(self)
        self.logo.setGeometry(10, 0, 300, 50)
        self.logo.setPixmap(QtGui.QPixmap(Assets.logo))

        self.image_preview = QtWidgets.QLabel(self)
        self.image_preview.setGeometry(350, 10, 250, 250)
        self.image_preview.setStyleSheet("background-color: rgb(100, 100, 100); border: 4px solid black;")
        self.image_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.image_preview.setFont(self._qfont)
        self.image_preview.setText("No Image Selected")

        self.image_preview_button = QtWidgets.QPushButton(self)
        self.image_preview_button.setGeometry(350, 10, 250, 250)
        self.image_preview_button.setGraphicsEffect(self._opacity_effect)
        self.image_preview_button.clicked.connect(self.open_current_image)

        self.image_name_label = QtWidgets.QLabel(self)
        self.image_name_label.setGeometry(350, 270, 250, 50)
        self.image_name_label.setFont(self._qfont)
        self.image_name_label.setText(self.current_image)

        self.next_image_button = QtWidgets.QPushButton(self)
        self.next_image_button.setGeometry(500, 330, 100, 50)
        self.next_image_button.setFont(self._qfont)
        self.next_image_button.setText("Next")
        self.next_image_button.clicked.connect(self.load_next_image)

        self.queue_length_counter = QtWidgets.QTextEdit(self)
        self.queue_length_counter.setGeometry(435, 330, 50, 50)
        self.queue_length_counter.setFont(self._qfont)
        self.queue_length_counter.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.queue_length_counter.setText("0")
        self.queue_length_counter.setReadOnly(True)

        self.open_file_button = QtWidgets.QPushButton(self)
        self.open_file_button.setGeometry(20, 70, 175, 50)
        self.open_file_button.setFont(self._qfont)
        self.open_file_button.setText("Select Image")
        self.open_file_button.clicked.connect(self.select_file)

        self.open_files_button = QtWidgets.QPushButton(self)
        self.open_files_button.setGeometry(20, 130, 180, 50)
        self.open_files_button.setFont(self._qfont)
        self.open_files_button.setText("Select Images")
        self.open_files_button.clicked.connect(self.select_files)

        self.open_dir_button = QtWidgets.QPushButton(self)
        self.open_dir_button.setGeometry(20, 190, 200, 50)
        self.open_dir_button.setFont(self._qfont)
        self.open_dir_button.setText("Select Directory")
        self.open_dir_button.clicked.connect(self.select_directory)

        self.write_message_button = QtWidgets.QPushButton(self)
        self.write_message_button.setGeometry(20, 290, 140, 50)
        self.write_message_button.setFont(self._qfont)
        self.write_message_button.setStyleSheet("text-align: left;")
        self.write_message_button.setText("Write Data")
        self.write_message_button.clicked.connect(self.write_message)

        self.read_message_button = QtWidgets.QPushButton(self)
        self.read_message_button.setGeometry(20, 350, 140, 50)
        self.read_message_button.setFont(self._qfont)
        self.read_message_button.setStyleSheet("text-align: left;")
        self.read_message_button.setText("Read Data")
        self.read_message_button.clicked.connect(self.read_message)

        self.reset_file_button = QtWidgets.QPushButton(self)
        self.reset_file_button.setGeometry(20, 410, 175, 50)
        self.reset_file_button.setFont(self._qfont)
        self.reset_file_button.setStyleSheet("text-align: left;")
        self.reset_file_button.setText("Remove Data")
        self.reset_file_button.clicked.connect(self.remove_message)

    def write_message(self):
        message, ok = QtWidgets.QInputDialog.getText(None, "Message", "Input Message:")
        if message:
            self.encrypter.write_message(self.current_image, message)
        else:
            print("Error - Message Invalid")

    def read_message(self):
        message = self.encrypter.read_message(self.current_image)

        if message:
            print(message)
        else:
            print("Error - No message within file")

    def remove_message(self):
        self.encrypter.reset_image(self.current_image)

    def setup_shortcuts(self):
        self.open_file_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("ctrl+o"), self)
        self.open_file_shortcut.activated.connect(self.select_file)

        self.open_files_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("ctrl+shift+o"), self)
        self.open_files_shortcut.activated.connect(self.select_files)

        self.open_dir_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("ctrl+shift+alt+o"), self)
        self.open_dir_shortcut.activated.connect(self.select_directory)

    def open_current_image(self):
        if self.current_image:
            os.system(f'"{pathlib.Path(self.current_image)!s}"')

    def update_counter(self):
        self.queue_length_counter.setText(str(self.image_queue.qsize()))

    def update_image(self):
        self.image_name_label.setText(self.current_image.split("/")[-1])
        pixmap = QtGui.QPixmap(self.current_image)
        image_width, image_height = Image.open(self.current_image).size

        if image_width > image_height:
            pixmap = pixmap.scaledToWidth(self.image_preview.width())
        elif image_width < image_height:
            pixmap = pixmap.scaledToHeight(self.image_preview.height())
        else:
            pixmap = pixmap.scaled(self.image_preview.height(), self.image_preview.width())

        self.image_preview.setPixmap(pixmap)

    def load_next_image(self):
        if self.image_queue.empty():
            return

        next_image = self.image_queue.get()
        self.update_counter()

        if next_image:
            self.current_image = next_image
            self.update_image()

    def fill_queue(self, files):
        for file in files:
            self.image_queue.put(file)
        self.update_counter()

    def select_file(self):
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Image")

        if not image_path:
            return

        self.current_image = image_path
        self.update_image()

    def select_files(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "Open Images")

        if not files:
            return

        self.current_image = files[0]
        self.update_image()

        files.remove(self.current_image)
        self.fill_queue(files)

    def select_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")

        if not directory:
            return

        print(directory)

        files = list(filter(lambda s:s.endswith((".jpg", ".jpeg")), os.listdir(directory)))

        print(files)

        files = list(map(lambda file: f"{directory}/{file}", files))

        print(files)

        self.current_image = files[0]
        self.update_image()

        files.remove(self.current_image)
        self.fill_queue(files)


def main():
    app = QtWidgets.QApplication(sys.argv)

    ui = MainWindow()
    ui.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
