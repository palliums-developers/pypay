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
    signal sendClicked
    signal receiveClicked
    signal exchangeClicked

    Image {       
        id: bankImage
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 200
        source: "../icons/walletbackground.svg"

        Text {
            id: totalText
            text: qsTr("存款总额($)")
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
            text: appSettings.eyeIsOpen ? qsTr("$ ") + payController.totalBalance : "******"
            font.pointSize: 20
            color: "#FFFFFF"
        }
    }

    Rectangle {
        id: whiteRec
        anchors.top: bankImage.bottom
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
            text: qsTr("存款市场")
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

        // Bank list
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
                        anchors.right: parent.right
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
                        if (tokenEntry.chain == 'libra') {
                            payController.requestLBRHistory(tokenEntry.addr, tokenEntry.name, -1, 0, 100)
                        } else if (tokenEntry.chain == 'violas') {
                            payController.requestVLSHistory(tokenEntry.addr, tokenEntry.name, -1, 0, 100)
                        } else {
                            console.log("invalid")
                        }
                        coinDetailPage.open()
                    }
                }
            }
        }
    }
}
