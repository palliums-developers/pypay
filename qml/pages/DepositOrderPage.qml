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
        text: qsTr("Bank> <b><b>Deposit Order</b></b>")
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
                id: depositTabBtn
                text: qsTr("Current Deposit")
                width: 200
                leftPadding: 0
                contentItem: Text {
                        id: depositBtnText
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
                text: qsTr("Deposit Detail")
                width: 200
                leftPadding: 0
                contentItem: Text {
                    id: depositDetailText
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
            anchors.top: tabBar.bottom
            anchors.topMargin: 55
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 80
            currentIndex: tabBar.currentIndex

            ListView {
                id: currentDepositView
                model: server.currentDepositModel
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
                        id: principalText
                        anchors.left: tokenText.left
                        anchors.leftMargin: 100 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Principal")
                    }
                    Text {
                        id: incomeText
                        anchors.left: principalText.left
                        anchors.leftMargin: 206 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Income")
                    }
                    Text {
                        id: rateText
                        anchors.left: incomeText.left
                        anchors.leftMargin: 192 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Rate")
                    }
                    Text {
                        id: statusText
                        anchors.left: rateText.left
                        anchors.leftMargin: 150 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Status")
                    }
                    Text {
                        id: operationText
                        anchors.right: parent.right
                        anchors.rightMargin: 54
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
                    width: currentDepositView.width
                    height: 50
                    Text {
                        id: tokenText
                        anchors.left: parent.left
                        anchors.leftMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: currency
                    }
                    Text {
                        id: principalText
                        anchors.left: tokenText.left
                        anchors.leftMargin: 100 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: principal.toFixed(2)
                    }
                    Text {
                        id: incomeText
                        anchors.left: principalText.left
                        anchors.leftMargin: 206 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: earnings.toFixed(2)
                    }
                    Text {
                        id: rateText
                        anchors.left: incomeText.left
                        anchors.leftMargin: 192 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: rate * 100 + "%"
                        color: "#13B788"
                    }
                    Text {
                        id: statusText
                        anchors.left: rateText.left
                        anchors.leftMargin: 150 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: {
                            if (status == 0) {
                                return qsTr("Deposited")
                            } else if (status == 1) {
                                return qsTr("Extraction")
                            } else if (status == -1) {
                                return qsTr("Extraction failed")
                            } else if (status == -2) {
                                return qsTr("Deposition failed")
                            } else {
                                return qsTr("Unknown, ") + status
                            }
                        }
                        color: "#13B788"
                    }
                    Text {
                        id: operationText
                        anchors.right: parent.right
                        anchors.rightMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: qsTr("Extraction")
                        color: "#7038FD"
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                            }
                        }
                    }
                }
            }

            ListView {
                id: borrowDetailView
                model: server.depositDetailModel
                spacing: 12
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                header: Rectangle {
                    z: 2
                    width: parent.width
                    Column {
                        anchors.fill: parent
                        spacing: 8
                        Rectangle {
                            width: parent.width
                            height: 30
                            color: "blue"
                            visible: false
                        }
                        Rectangle {
                            width: parent.width
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
                                anchors.leftMargin: 200 / (1070 - 54*2) * parent.width
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Token")
                            }
                            Text {
                                id: amountText
                                anchors.left: tokenText.left
                                anchors.leftMargin: 250 / (1070 - 54*2) * parent.width
                                anchors.verticalCenter: parent.verticalCenter
                                text: qsTr("Amount")
                            }
                            Text {
                                id: statusText
                                anchors.right: parent.right
                                anchors.rightMargin: 54
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
                        anchors.leftMargin: 200 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: currency
                    }
                    Text {
                        id: amountText
                        anchors.left: tokenText.left
                        anchors.leftMargin: 250 / (1070 - 54*2) * parent.width
                        anchors.verticalCenter: parent.verticalCenter
                        text: value
                    }
                    Text {
                        id: statusText
                        anchors.right: parent.right
                        anchors.rightMargin: 54
                        anchors.verticalCenter: parent.verticalCenter
                        text: status
                    }
                }
            }
        }

        Column {
            visible: tabBar.currentIndex == 0 ? server.currentDepositModel.count == 0 : server.depositDetailModel.count == 0
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
