#! python3

import sys
import os

from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtCore import QUrl, Qt, QCoreApplication

from pypay.paycontroller import PayController
from pypay.tokenmodel import TokenEntry, TokenModel
from pypay.depositmodel import DepositEntry, DepositModel
from pypay.borrowmodel import BorrowEntry, BorrowModel
from pypay.borrowordermodel import BorrowOrderEntry, BorrowOrderModel
from pypay.historymodel import HistoryEntry, HistoryModel
from pypay.bittransactionmodel import BitTransactionEntry, BitTransactionModel
from pypay.addrbookmodel import AddrBookEntry, AddrBookModel

application_path = (
    os.path.dirname(sys.executable)
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

if __name__ == '__main__':
    print("starting pypay ...")

    QCoreApplication.setApplicationName("PyPay")
    QCoreApplication.setOrganizationName("Palliums")
    QCoreApplication.setOrganizationDomain("palliums.org")
    QCoreApplication.setApplicationVersion("0.0.1")

    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

    app = QGuiApplication(sys.argv)

    file = os.path.join(application_path, "qml/icons/pypay.png")
    QGuiApplication.setWindowIcon(QIcon(file));

    qmlRegisterType(TokenEntry, "PyPay", 1, 0, "TokenEntry")
    qmlRegisterType(TokenModel, "PyPay", 1, 0, "TokenModel")
    qmlRegisterType(BitTransactionEntry, "PyPay", 1, 0, "BitTransactionEntry")
    qmlRegisterType(BitTransactionModel, "PyPay", 1, 0, "BitTransactionModel")
    qmlRegisterType(AddrBookEntry, "PyPay", 1, 0, "AddrBookEntry")
    qmlRegisterType(AddrBookModel, "PyPay", 1, 0, "AddrBookModel")
    qmlRegisterType(HistoryEntry, "PyPay", 1, 0, "HistoryEntry")
    qmlRegisterType(HistoryModel, "PyPay", 1, 0, "HistoryModel")
    qmlRegisterType(DepositEntry, "PyPay", 1, 0, "DepositEntry")
    qmlRegisterType(DepositModel, "PyPay", 1, 0, "DepositModel")
    qmlRegisterType(BorrowEntry, "PyPay", 1, 0, "BorrowEntry")
    qmlRegisterType(BorrowModel, "PyPay", 1, 0, "BorrowModel")
    qmlRegisterType(BorrowOrderEntry, "PyPay", 1, 0, "BorrowOrderEntry")
    qmlRegisterType(BorrowOrderModel, "PyPay", 1, 0, "BorrowOrderModel")

    payController = PayController()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("payController", payController)
    file = os.path.join(application_path, "qml/main.qml")
    engine.load(QUrl.fromLocalFile(file))
    if not engine.rootObjects():
        print("not engine.rootObjects()")
        sys.exit(-1)

    try:
        exitCode = app.exec_()

        del engine
        del payController
        
        sys.exit(exitCode)
    except:
        print("exiting")

