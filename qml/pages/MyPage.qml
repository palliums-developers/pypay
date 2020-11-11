import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Control {
    signal goBack
    topInset: 0
    leftInset: 0
    rightInset: 0
    bottomInset: 0

    signal sendClicked
    signal receiveClicked
    signal walletManageClicked
    
    contentItem: Rectangle {
        color: "#501BA2"

        Rectangle {
            id: totalRec
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.top: parent.top
            anchors.topMargin: 8
            color: "#FFFFFF"
            height: 57
            radius: 4
            Column {
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 12
                spacing: 5
                Text {
                    text: qsTr("总资产子和")
                    font.pointSize: 10
                    color: "#999999"
                }
                Text {
                    text: appSettings.eyeIsOpen ? qsTr("$ ") + server.value_total : "******"
                    font.pointSize: 18
                }
            }
        }

        Row {
            id: sendAndReceiveRow
            spacing: 8
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: totalRec.bottom
            anchors.topMargin: 16
            // Send
            MyButton4 {
                icon.source: "../icons/send.svg"
                text: qsTr("转账")
                width: 69
                height: 26
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        sendClicked()
                    }
                }
            }
            // Receive
            MyButton4 {
                id: receiveBtn
                icon.source: "../icons/receive.svg"
                text: qsTr("收款")
                width: 69
                height: 26
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        receiveClicked()
                    }
                }
            }
        }

        Row {
            id: walletMgrRow
            spacing: 10
            anchors.top: sendAndReceiveRow.bottom
            anchors.topMargin: 15
            anchors.left: sendAndReceiveRow.left
            anchors.leftMargin: 5
            Image {
                source: "../icons/wallet.svg"
                fillMode: Image.PreserveAspectFit
                width: 16
                anchors.verticalCenter: walletText.verticalCenter
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        walletManageClicked()
                    }
                }
            }
            Text {
                id: walletText
                text: qsTr("钱包管理")
                color: "#FFFFFF"
                font.pointSize: 13
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        walletManageClicked()
                    }
                }
            }
        }

        Row {
            id: helpRow
            spacing: 10
            anchors.top: walletMgrRow.bottom
            anchors.topMargin: 15
            anchors.left: walletMgrRow.left
            Image {
                source: "../icons/help.svg"
                fillMode: Image.PreserveAspectFit
                width: 16
                anchors.verticalCenter: helpText.verticalCenter
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        server.open_url("https://violas.io")
                    }
                }
            }
            Text {
                id: helpText
                text: qsTr("帮助中心")
                color: "#FFFFFF"
                font.pointSize: 13
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        server.open_url("https://violas.io")
                    }
                }
            }
        }

        Row {
            spacing: 10
            anchors.top: helpRow.bottom
            anchors.topMargin: 15
            anchors.left: helpRow.left
            Image {
                source: "../icons/quit.svg"
                fillMode: Image.PreserveAspectFit
                width: 16
                anchors.verticalCenter: quitText.verticalCenter
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        appWindow.close()
                    }
                }
            }
            Text {
                id: quitText
                text: qsTr("退出")
                color: "#FFFFFF"
                font.pointSize: 13
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        appWindow.close()
                    }
                }
            }
        }
    }
}
