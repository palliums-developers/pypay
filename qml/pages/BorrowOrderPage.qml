import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"

import PyPay 1.0

Page {
    id: root
    signal backArrowClicked

    background: Rectangle {
        color: "#F7F7F9"
    }

    ImageButton {
        id: backBtn
        anchors.top: parent.top
        anchors.topMargin: 72
        anchors.left: parent.left
        anchors.leftMargin: 72
        width: 24
        height: 24
        source: "../icons/backarrow3.svg"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                backArrowClicked()
            }
        }
    }

    Text {
        id: titleText
        text: qsTr("Bank> <b><b>Borrow Order</b></b>")
        font.pointSize: 14
        color: "#5C5C5C"
        anchors.verticalCenter: backBtn.verticalCenter
        anchors.left: backBtn.right
        anchors.leftMargin: 8
    }

    Rectangle {
        anchors.left: parent.left
        anchors.leftMargin: 50
        anchors.right: parent.right
        anchors.rightMargin: 50
        anchors.top: backBtn.bottom
        anchors.topMargin: 24
        anchors.bottom: parent.bottom
        color: "#FFFFFF"
        
        TabBar {
            id: tabBar
            anchors.top: parent.top
            anchors.topMargin: 40
            anchors.left: parent.left
            anchors.leftMargin: 54
            width: 500

            TabButton {
                text: qsTr("Current Borrow")
                width: 200
                leftPadding: 0
                contentItem: Text {
                        text: parent.text
                        color: tabBar.currentIndex == 0 ? "#333333" : "#999999"
                        font.pointSize: tabBar.currentIndex == 0 ? 16 : 12
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
            }

            TabButton {
                text: qsTr("Borrow Detail")
                width: 200
                leftPadding: 0
                contentItem: Text {
                    text: parent.text
                    color: tabBar.currentIndex == 1 ? "#333333" : "#999999"
                    font.pointSize: tabBar.currentIndex == 1 ? 16 : 12
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: "#FFFFFF"
                }
            }
        }
        Rectangle {
            anchors.left: tabBar.left
            anchors.leftMargin: tabBar.currentIndex == 0 ? 0 : 200
            anchors.top: tabBar.bottom
            anchors.topMargin: 8
            width: 40
            height: 3
            color: "blue"
        }

        StackLayout {
            id: stackView
            anchors.top: tabBar.bottom
            anchors.topMargin: 32
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 80
            currentIndex: tabBar.currentIndex

            ListView {
                id: currentBorrowView
                model: server.currentBorrowModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                header: Rectangle {
                    z: 2
                    width: parent.width
                    height: 50
                    Text {
                        id: tokenText
                        anchors.left: parent.left
                        anchors.leftMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Token")
                    }
                    Text {
                        id: amountText
                        anchors.left: tokenText.left
                        anchors.leftMargin: (28 + 100) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Amount")
                    }
                    Text {
                        id: availableBorrowText
                        anchors.left: tokenText.left
                        anchors.leftMargin: (28 + 296) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Available Borrow")
                    }
                    Text {
                        id: operationText
                        anchors.left: tokenText.left
                        anchors.leftMargin: (28 + 690) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Operation")
                    }
                    Rectangle {
                        anchors.left: parent.left
                        anchors.leftMargin: 27
                        anchors.right: parent.right
                        anchors.rightMargin: 27
                        anchors.bottom: parent.bottom
                        height: 1
                        color: "#DEDEDE"
                        opacity: 0.5
                    }
                }
                headerPositioning: ListView.OverlayHeader
                delegate: Rectangle {
                    width: currentBorrowView.width
                    height: 50
                    Text {
                        id: tokenText
                        anchors.left: parent.left
                        anchors.leftMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: currency
                    }
                    Text {
                        id: amountText
                        anchors.left: tokenText.left
                        anchors.leftMargin: (28 + 100) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: amount.toFixed(2)
                    }
                    Text {
                        id: availableBorrowText
                        anchors.left: tokenText.left
                        anchors.leftMargin: (28 + 296) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: available_borrow.toFixed(2)
                    }
                    Text {
                        id: repaymentOperationText
                        anchors.left: tokenText.left
                        anchors.leftMargin: (28 + 690) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Repayment")
                    }
                    Text {
                        id: borrowOperationText
                        anchors.left: tokenText.left
                        anchors.leftMargin: (28 + 774) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Borrow")
                    }
                    Text {
                        id: detailOperationText
                        anchors.left: borrowOperationText.right
                        anchors.leftMargin: (28 + 860) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Detail")
                    }
                }
            }

            ListView {
                id: borrowDetailView
                model: server.borrowDetailModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                header: Rectangle {
                    z: 2
                    width: parent.width
                    height: headCol.height
                    Column {
                        id: headCol
                        spacing: 8
                        Rectangle {
                            width: borrowDetailView.width
                            height: 30
                            color: "blue"
                            visible: false
                        }
                        Rectangle {
                            width: borrowDetailView.width
                            height: 50
                            //color: "red"
                            Text {
                                id: dateText
                                anchors.left: parent.left
                                anchors.leftMargin: 54
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Date")
                            }
                            Text {
                                id: tokenText
                                anchors.left: dateText.left
                                anchors.leftMargin: (28 + 180) / 1070 * parent.width
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Token")
                            }
                            Text {
                                id: amountText
                                anchors.left: dateText.left
                                anchors.leftMargin: (28 + 388) / 1070 * parent.width
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Amount")
                            }
                            Text {
                                id: feeText
                                anchors.left: dateText.left
                                anchors.leftMargin: (28 + 690) / 1070 * parent.width
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Fee")
                            }
                            Text {
                                id: statusText
                                anchors.left: dateText.left
                                anchors.leftMargin: (28 + 860) / 1070 * parent.width
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Status")
                            }
                            Rectangle {
                                anchors.left: parent.left
                                anchors.leftMargin: 27
                                anchors.right: parent.right
                                anchors.rightMargin: 27
                                anchors.bottom: parent.bottom
                                height: 1
                                color: "#DEDEDE"
                                opacity: 0.5
                            }
                        }
                    }
                }
                headerPositioning: ListView.OverlayHeader
                delegate: Rectangle {
                    width: borrowDetailView.width
                    height: 50
                    Text {
                        id: dateText
                        anchors.left: parent.left
                        anchors.leftMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: date
                    }
                    Text {
                        id: tokenText
                        anchors.left: dateText.left
                        anchors.leftMargin: (28 + 180) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: currency
                    }
                    Text {
                        id: amountText
                        anchors.left: dateText.left
                        anchors.leftMargin: (28 + 388) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: amount
                    }
                    Text {
                        id: feeText
                        anchors.left: dateText.left
                        anchors.leftMargin: (28 + 690) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: fee
                    }
                    Text {
                        id: statusText
                        anchors.left: dateText.left
                        anchors.leftMargin: (28 + 860) / 1070 * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: status
                    }
                }
            }
        }

        SwitchPage {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: stackView.bottom
            anchors.topMargin: 16
            visible: tabBar.currentIndex == 0 && server.currentBorrowModel.count != 0
            pageCount: server.currentBorrowModel.get(0).total_count / 10 + (server.currentBorrowModel.get(0).total_count % 10 == 0 ? 0 : 1)
            onPageClicked: {
                var params = { "address": payController.addr, "offset": index * 10, "limit": 10 }
                server.getBorrowOrder(params)
            }
        }

        SwitchPage {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: stackView.bottom
            anchors.topMargin: 16
            visible: tabBar.currentIndex == 1 && server.borrowDetailModel.count != 0
            pageCount: server.borrowDetailModel.get(0).total_count / 10 + (server.borrowDetailModel.get(0).total_count % 10 == 0 ? 0 : 1)
            onPageClicked: {
                var params = { "address": payController.addr, "offset": index * 10, "limit": 10 }
                server.getBorrowOrderList(params)
            }
        }


        Column {
            visible: tabBar.currentIndex == 0 ? server.currentBorrowModel.count == 0 : server.borrowDetailModel.count == 0
            anchors.centerIn: parent
            spacing: 8
            Image {
                source: "../icons/bank_no_data.svg"
                width: 196
                fillMode: Image.PreserveAspectFit
            }
            Text {
                text: qsTr("No Data")
                anchors.horizontalCenter: parent.horizontalCenter
                color: "#BABABA"
            }
        }
    }
}
