import sys
from controllers.menu_controller import Menu
from PyQt5 import QtWidgets


def main():
    try:
        app = QtWidgets.QApplication(sys.argv)
        menu = Menu()
        window = menu
        window.show()
        app.exec_()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
