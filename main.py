import sys
from PyQt5 import QtWidgets
from external_connections import ExternalConnections

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ExternalConnections()
    window.show()
    sys.exit(app.exec_())
