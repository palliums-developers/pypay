#! /usr/bin/env python3

import sys
import os

from PyQt5.QtCore import QUrl, Qt, QCoreApplication
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtQml import QQmlApplicationEngine

from pypay.paycontroller import PayController


application_path = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)


def main():
    QCoreApplication.setApplicationName("PyPay")
    QCoreApplication.setOrganizationName("Palliums")
    QCoreApplication.setOrganizationDomain("palliums.org")
    QCoreApplication.setApplicationVersion("1.0.0")

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QGuiApplication(sys.argv)

    file = os.path.join(application_path, "qml/icons/pypay.png")
    QGuiApplication.setWindowIcon(QIcon(file));

    engine = QQmlApplicationEngine()
    payController = PayController(None, engine, application_path)
    engine.rootContext().setContextProperty("payController", payController)
    file = os.path.join(application_path, "qml/main.qml")
    engine.load(QUrl.fromLocalFile(file))
    if not engine.rootObjects():
        print("not engine.rootObjects()")
        sys.exit(1)

    exitCode = app.exec_()

    del engine
    del payController

    sys.exit(exitCode)


if __name__ == '__main__':
    main()
