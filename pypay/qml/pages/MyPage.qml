import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14
import "../controls"
import "../model"
import PyPay 1.0

Control {
    signal goBack
    topInset: 0
    leftInset: 0
    rightInset: 0
    bottomInset: 0

    signal sendClicked
    signal receiveClicked
    
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
                    font.pointSize: 12
                    color: "#999999"
                }
                Text {
                    text: appSettings.eyeIsOpen ? qsTr("$ 0.00") : "******"
                    font.weight: Font.Blod
                    font.pointSize: 18
                }
            }
        }

        Row {
            id: sendAndReceiveRow
            spacing: 8
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: totalRec.bottom
            anchors.topMargin: 8
            // Send
            MyButton2 {
                icon.source: "../icons/send.svg"
                text: qsTr("转账")
                width: 69
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        sendClicked()
                        payController.currentSelectedAddr = ""
                    }
                }
            }
            // Receive
            MyButton2 {
                id: receiveBtn
                icon.source: "../icons/receive.svg"
                text: qsTr("收款")
                width: 69
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
            spacing: 5
            anchors.top: sendAndReceiveRow.bottom
            anchors.topMargin: 15
            anchors.left: sendAndReceiveRow.left
            anchors.leftMargin: 5
            Image {
                source: "../icons/wallet.svg"
                fillMode: Image.PreserveAspectFit
                width: 16
            }
            Text {
                text: qsTr("钱包管理")
                color: "#FFFFFF"
                font.pointSize: 14
            }
        }

        Row {
            id: helpRow
            spacing: 5
            anchors.top: walletMgrRow.bottom
            anchors.topMargin: 15
            anchors.left: walletMgrRow.left
            Image {
                source: "../icons/help.svg"
                fillMode: Image.PreserveAspectFit
                width: 16
            }
            Text {
                text: qsTr("帮助中心")
                color: "#FFFFFF"
                font.pointSize: 14
            }
        }

        Row {
            spacing: 5
            anchors.top: helpRow.bottom
            anchors.topMargin: 15
            anchors.left: helpRow.left
            Image {
                source: "../icons/help.svg"
                fillMode: Image.PreserveAspectFit
                width: 16
            }
            Text {
                text: qsTr("退出")
                color: "#FFFFFF"
                font.pointSize: 14
            }
        }
    }
}
