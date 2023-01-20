from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer, Qt
import psutil

class ExternalConnections(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('TCP manager')
        self.resize(500, 300)

        self.connections_list = QtWidgets.QListWidget()
        self.connections_list.itemDoubleClicked.connect(self.view_details)
        self.kill_button = QtWidgets.QPushButton('Kill Connection')
        self.kill_button.setCursor(Qt.PointingHandCursor)

        self.refresh_button = QtWidgets.QPushButton('Refresh')
        self.refresh_button.clicked.connect(self.refresh_connections)



        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.connections_list)
        layout.addWidget(self.kill_button)
        layout.addWidget(self.refresh_button)



        self.kill_button.clicked.connect(self.kill_connection)
        self.setStyleSheet("""
            QListWidget {
                background-color: #F0F0F0;
                font-size: 14px;
                color: #333;
                padding: 10px;
                border: 1px solid #CCC;
            }

            QPushButton {
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            }

            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)


        self.refresh_connections()

    def refresh_connections(self):
        self.connections_list.clear()
        self.connections = []
        for connection in psutil.net_connections():
            if connection.status == 'ESTABLISHED':
                if connection.laddr.ip != '127.0.0.1':
                    service_name = psutil.Process(connection.pid).name()
                    item = f'{connection.raddr.ip}:{connection.raddr.port} - {service_name}'
                    self.connections.append(connection)
                    self.connections_list.addItem(item)

    def view_details(self):
        selected_index = self.connections_list.currentRow()
        if selected_index != -1:
            connection = self.connections[selected_index]
            pid = connection.pid
            try:
                process = psutil.Process(pid)
                process_info = f'Process Name: {process.name()}\n' \
                               f'Process Status: {process.status()}\n' \
                               f'Source IP: {connection.laddr.ip}:{connection.laddr.port}\n' \
                               f'Destination IP: {connection.raddr.ip}:{connection.raddr.port}\n'

                QtWidgets.QMessageBox.information(self, 'Connection Details', process_info)
            except:
                pass
    def kill_connection(self):
        selected_index = self.connections_list.currentRow()
        if selected_index != -1:
            connection = self.connections[selected_index]
            pid = connection.pid
            psutil.Process(pid).kill()
            self.refresh_connections()
