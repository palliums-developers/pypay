import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Control {
    id: root
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
        radius: 4

        Rectangle {
            id: totalRec
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.top: parent.top
            anchors.topMargin: 12
            color: "#FFFFFF"
            height: 57
            radius: 4
            Column {
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 12
                spacing: 5
                Text {
                    text: qsTr("Total balance($)")
                    font.pointSize: 10
                    color: "#999999"
                }
                Text {
                    text: appSettings.eyeIsOpen ? server.value_total : "******"
                    font.pointSize: 18
                }
            }
            ImageButton {
                source: "../icons/arrow_right.svg"
                fillMode: Image.PreserveAspectFit
                height: 10
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 12
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
                text: qsTr("Send")
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
                text: qsTr("Receive")
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

        Image {
            id: mineRewardImage
            anchors.top: sendAndReceiveRow.bottom
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.leftMargin: 4
            anchors.right: parent.right
            anchors.rightMargin: 4
            source: "../icons/mine_reward.svg"
            fillMode: Image.PreserveAspectFit
            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 32
                color: "#FFFFFF"
                font.pointSize: 16
                text: qsTr("挖矿奖励")
            }
        }

        Column {
            id: menuColumn
            spacing: 24
            anchors.top: mineRewardImage.bottom
            anchors.topMargin: 20
            anchors.left: parent.left
            anchors.leftMargin: 24
            Row {
                id: walletMgrRow
                spacing: 10
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
                    text: qsTr("Wallet manage")
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
                id: inviteRewardRow
                spacing: 10
                Image {
                    source: "../icons/invite_reward.svg"
                    fillMode: Image.PreserveAspectFit
                    width: 16
                    anchors.verticalCenter: inviteRewardText.verticalCenter
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            console.log("invite reward button clicked")
                        }
                    }
                }
                Text {
                    id: inviteRewardText
                    text: qsTr("Invite reward")
                    color: "#FFFFFF"
                    font.pointSize: 13
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            console.log("invite reward button clicked")
                        }
                    }
                }
            }

            Row {
                id: helpRow
                spacing: 10
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
                    text: qsTr("Help center")
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
                id: quitRow
                spacing: 10
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
                    text: qsTr("Quit")
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
}
