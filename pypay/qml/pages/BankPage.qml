import QtQuick 2.14
import QtQuick.Controls 2.14
import "../controls"
import PyPay 1.0

Page {
    id: root
    leftPadding: 134
    rightPadding: 134
    topPadding: 77

    Rectangle {       
        id: bankRec
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        height: 226
        color: "#501BA2"
        radius: 24

        Text {
            id: totalText
            text: qsTr("存款总额($)")
            anchors.top: parent.top
            anchors.topMargin: 16
            anchors.left: parent.left
            anchors.leftMargin: 42
            color: "#FFFFFF"
            font.pointSize: 12
            verticalAlignment: Text.AlignVCenter
        }
        Image {
            id: eyesImage
            anchors.left: totalText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: totalText.verticalCenter
            anchors.topMargin: 10
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
            id: depositText
            anchors.top: totalText.bottom
            anchors.topMargin: 16
            anchors.left: totalText.left
            text: appSettings.eyeIsOpen ? qsTr("≈") + payController.deposit: "******"
            font.pointSize: 20
            color: "#FFFFFF"
            verticalAlignment: Text.AlignVCenter
        }

        // 可借总额
        Image {
            id: borrowImage
            anchors.left: depositText.left
            anchors.top: depositText.bottom
            anchors.topMargin: 16
            source: "../icons/borrow.svg"
            fillMode: Image.PreserveAspectFit
        }
        Text {
            id: borrowText
            text: qsTr("可借总额 ($)    ")
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: borrowImage.right
            anchors.leftMargin: 8
            anchors.verticalCenter: borrowImage.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }
        Text {
            text: appSettings.eyeIsOpen ? qsTr("≈") + payController.borrow: "******"
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: borrowText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: borrowText.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }

        // 累计收益
        Image {
            id: incomeImage
            anchors.left: depositText.left
            anchors.top: borrowImage.bottom
            anchors.topMargin: 16
            source: "../icons/borrow.svg"
            fillMode: Image.PreserveAspectFit
        }
        Text {
            id: incomeText
            text: qsTr("累计收益 ($)    ")
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: incomeImage.right
            anchors.leftMargin: 8
            anchors.verticalCenter: incomeImage.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }
        Text {
            id: incomeDataText
            text: appSettings.eyeIsOpen ? qsTr("≈") + payController.income: "******"
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: incomeText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: incomeText.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }

        // 昨日收益
        Image {
            id: lastdayincomeImage
            anchors.left: incomeDataText.right
            anchors.leftMargin: 50
            anchors.verticalCenter: incomeDataText.verticalCenter
            source: "../icons/lastdayincome.svg"
            fillMode: Image.PreserveAspectFit
        }
        Text {
            id: lastdayincomeText
            text: qsTr("昨日收益: ")
            anchors.left: lastdayincomeImage.right
            anchors.leftMargin: 8
            anchors.verticalCenter: lastdayincomeImage.verticalCenter
            color: "#FFFFFF"
            font.pointSize: 12
            verticalAlignment: Text.AlignVCenter
        }

        Text {
            text: appSettings.eyeIsOpen ? qsTr("≈") + payController.lastdayincome: "******"
            color: "#FFFFFF"
            font.pointSize: 12
            anchors.left: lastdayincomeText.right
            anchors.leftMargin: 8
            anchors.verticalCenter: lastdayincomeText.verticalCenter
            verticalAlignment: Text.AlignVCenter
        }

        // 右上角的"..."
        Image {
            anchors.right: parent.right
            anchors.rightMargin: 42
            anchors.top: parent.top
            anchors.topMargin: 32
            fillMode: Image.PreserveAspectFit
            source: "../icons/more.svg"
        }
    }

    Rectangle {
        id: whiteRec
        anchors.top: bankRec.bottom
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

        // TODO 借款市场

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
            model: payController.depositModel
            spacing: 12
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                property var entry: modelData
                anchors.left: parent.left
                anchors.right: parent.right
                height: Entry.isShow ? 60 : -12
                visible: entry.isShow
                color: "#EBEBF1"
                radius: 14
                MyImage {
                    id: itemImage
                    source: {
                        if (entry.chain == "bitcoin") {
                            return "../icons/bitcoin.svg"
                        } else if (entry.chain == "violas") {
                            return "../icons/violas.svg"
                        } else if (entry.chain == "libra") {
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
                    text: entry.name
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
                        id: rateText
                        text: appSettings.eyeIsOpen ? entry.rate: "******"
                        color: "#333333"
                        font.pointSize: 16
                        anchors.right: parent.right
                    }
                    Text {
                        text: qsTr("年化收益率")
                        color: "#ADADAD"
                        font.pointSize: 12
                        anchors.right: amountText.right
                    }
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                    }
                }
            }
        }
    }
}
