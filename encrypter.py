# Module imports
from io import BufferedReader
from typing import Optional

class ImageEncrypter:
    """Handle writing and reading of an image"""
    def __init__(self):
        pass

    @property
    @staticmethod
    def file_contents(filename) -> bytes:
        return open(filename, "rb").read()

    @staticmethod
    def get_offset(data: bytes):
        return data.index(bytes.fromhex("FFD9")) + 2

    def overwrite_message(self,msg:str):
        # Remove message from file
        self.reset_image()

        # Write message to file
        self.write_message(msg)

    def write_message(self, filename:str, msg:str, print_message:bool=False):
        if filename is None:
            return

        # Open file for appending
        with open(filename, "ab") as file:
            # Write encoded message to file
            file.write(bytes(msg, encoding="utf-8"))

        if print_message:
            print(f"Written message: '{msg}'")

    def message_length(self, filename):
        file_contents = open(filename, "rb").read()
        file_length = len(file_contents)
        offset = self.get_offset(file_contents)

        return file_length - offset

    def read_message(self, filename:str, print_message:bool=False) -> str:
        if filename is None:
            return ''

        # Open file for reading
        with open(filename, "rb") as file:
            try:
                # Move cursor to start of message
                file.seek(self.get_offset(file.read()))
                contents = file.read().decode('utf-8')
            except Exception as e:
                print(e)
                contents =  ''

        if print_message:
            print(f"Read Message: {contents}")

        return contents

    def reset_image(self, filename):
        if filename is None:
            return

        # Open file for writing
        file = open(filename, "rb+")

        # Truncate file to len(file) - n bytes
        file.truncate(len(file.read())- self.message_length(filename))

        file.close()
        del file


def main():
    galaxy = ImageEncrypter()
    galaxy.reset_image()
    galaxy.read_message(print_message=True)

if __name__ == "__main__":
    main()

    # print(open("galaxy.jpg", "rb").read().index(bytes.fromhex("FFD9")))