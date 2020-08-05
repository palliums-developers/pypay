import QtQuick 2.14
import QtQuick.Controls 2.14
import "../controls"
import PyPay 1.0

Page {
    id: root
    leftPadding: 125
    rightPadding: 138
    topPadding: 69
    signal backupMnemonicClicked
    signal receiveClicked
    signal sendClicked

    Image {       
        id: walletImage
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 200
        source: "../icons/walletbackground.svg"

        Text {
            id: totalText
            text: qsTr("总资产")
            anchors.top: parent.top
            anchors.topMargin: 42
            anchors.left: parent.left
            anchors.leftMargin: 29
            color: "#9A91BE"
            font.pointSize: 12
        }
        Image {
            id: eyesImage
            anchors.left: totalText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: totalText.verticalCenter
            fillMode: Image.PreserveAspectFit
            source: appSettings.eyeIsOpen ? "../icons/eyes_open.svg" : "../icons/eyes_close.svg"
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    appSettings.eyeIsOpen = !appSettings.eyeIsOpen
                }
            }
        }

        Text {
            id: amountText
            anchors.top: totalText.bottom
            anchors.topMargin: 20
            anchors.left: totalText.left
            text: appSettings.eyeIsOpen ? qsTr("$ 0.00") : "******"
            font.pointSize: 20
            color: "#FFFFFF"
        }

        // Send
        MyButton2 {
            icon.source: "../icons/send.svg"
            text: qsTr("转账")
            anchors.right: receiveBtn.left
            anchors.rightMargin: 30
            anchors.verticalCenter: amountText.verticalCenter
            width: 114
            visible: appSettings.walletIsCreate
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
            anchors.right: parent.right
            anchors.rightMargin: 60
            anchors.verticalCenter: amountText.verticalCenter
            width: 114
            visible: appSettings.walletIsCreate
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    receiveClicked()
                }
            }
        }
    }

    Rectangle {
        id: whiteRec
        anchors.top: walletImage.bottom
        anchors.topMargin: -65
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        border.color: "lightsteelblue"
        border.width: 1
        radius: 20

        Text {
            id: tokenText
            anchors.top: parent.top
            anchors.topMargin: 34
            anchors.left: whiteRec.left
            anchors.leftMargin: 29
            text: qsTr("资产")
            color: "#7D71AA"
        }
        ImageButton {
            id: addImage
            visible: appSettings.walletIsCreate
            anchors.verticalCenter: tokenText.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 32
            source: "../icons/add.svg"
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    addCoinPage.open()
                }
            }
        }

        Image {
            id: noImage
            anchors.centerIn: parent
            width: 100
            fillMode: Image.PreserveAspectFit
            source: "../icons/nowallet.svg"
            visible: !appSettings.walletIsCreate
        }
        Text {
            anchors.top: noImage.bottom
            anchors.topMargin: 10
            anchors.horizontalCenter: noImage.horizontalCenter
            text: qsTr("No Token")
            color: "#E0E0E0"
            visible: !appSettings.walletIsCreate
        }

        // Coins list
        ListView {
            id: walletListView
            anchors.top: tokenText.bottom
            anchors.topMargin: 22
            anchors.left: parent.left
            anchors.leftMargin: 20
            anchors.right: parent.right
            anchors.rightMargin: 20
            anchors.bottom: parent.bottom
            model: payController.tokenModel
            spacing: 12
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: tokenEntry.isShow ? 60 : -12
                visible: tokenEntry.isShow
                color: "#EBEBF1"
                radius: 14
                MyImage {
                    id: itemImage
                    source: {
                        if (tokenEntry.chain == "bitcoin") {
                            return "../icons/bitcoin.svg"
                        } else if (tokenEntry.chain == "violas") {
                            return "../icons/violas.svg"
                        } else if (tokenEntry.chain == "libra") {
                            return "../icons/libra.svg"
                        } else {
                            return ""
                        }
                    }
                    radius: 14
                    width: 41
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    text: tokenEntry.name
                    anchors.left: itemImage.right
                    anchors.leftMargin: 15
                    anchors.verticalCenter: parent.verticalCenter
                    color: "#333333"
                    font.pointSize: 16
                }
                Column {
                    anchors.right: parent.right
                    anchors.rightMargin: 15
                    anchors.verticalCenter: parent.verticalCenter
                    Text {
                        id: amountText
                        text: appSettings.eyeIsOpen ? tokenEntry.amount : "******"
                        color: "#333333"
                        font.pointSize: 16
                    }
                    Text {
                        text: appSettings.eyeIsOpen ? "≈$" + tokenEntry.totalPrice : "******"
                        color: "#ADADAD"
                        font.pointSize: 12
                        anchors.right: amountText.right
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        payController.currentTokenEntry = tokenEntry
                        payController.requestLBRHistory(tokenEntry.addr, tokenEntry.name, -1, 0, 10)
                        coinDetailPage.open()
                    }
                }
            }
        }
    }

    // 安全提醒
    Rectangle {
        anchors.left: walletImage.left
        anchors.leftMargin: 1
        anchors.right: walletImage.right
        anchors.rightMargin: 1
        anchors.bottom: parent.bottom
        height: 254
        visible: appSettings.walletIsCreate && !appSettings.mnemonicIsBackup
        Image {
            id: backgroundImage
            source: "../icons/warning_background.svg"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            height: 53
            Row {
                spacing: 5
                anchors.centerIn: parent
                Image {
                    id: warningIcon
                    source: "../icons/warning_icon.svg"
                    height: 34
                    fillMode: Image.PreserveAspectFit
                }
                Text {
                    text: qsTr("安全提醒")
                    font.pointSize: 20
                    color: "#FFFFFF"
                    anchors.verticalCenter: warningIcon.verticalCenter
                }
            }
        }
        Row {
            id: tipRow1
            anchors.left: tipRow2.left
            anchors.top: backgroundImage.bottom
            anchors.topMargin: 28
            Rectangle {
                color: "#3D3949"   
                width: 4
                height: 4
                radius: 2
                anchors.verticalCenter: tipText1.verticalCenter
            }
            spacing: 5
            Text {
                id: tipText1
                text: qsTr("您的身份助记词未备份，请务必备份助记词")
                font.pointSize: 14
                color: "#3D3949"
            }
        }
        Row {
            id: tipRow2
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: tipRow1.bottom
            anchors.topMargin: 5
            Rectangle {
                color: "#3D3949"   
                width: 4
                height: 4
                radius: 2
                anchors.verticalCenter: tipText2.verticalCenter
            }
            spacing: 5
            Text {
                id: tipText2
                text: qsTr("助记词可用于恢复身份下钱包资产，防止忘记密码、应用删除、手机丢失等情况导致资产损失")
                font.pointSize: 14
                color: "#3D3949"
            }
        }
        
        // 备份助记词按钮
        MyButton3 {
            id: backupBtn
            anchors.top: tipRow2.bottom
            anchors.topMargin: 46
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("立即备份")
            width: 200
            height: 40
            onClicked: {
                root.backupMnemonicClicked()
            }
        }
    }
}