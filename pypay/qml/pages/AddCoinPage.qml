import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14
import "../controls"
import "../model"
import PyPay 1.0

Control {
    padding: 8

    signal goBack

    contentItem: Item {
        Image {
            source: "../icons/backarrow.svg"
            anchors.left: parent.left
            anchors.verticalCenter: titleText.verticalCenter
            width: 16
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    goBack()
                }
            }
        }
        Text {
            id: titleText
            text: qsTr("添加币种")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }

        ListView {
            id: listView
            anchors.top: titleText.bottom
            anchors.topMargin: 22
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.bottom: parent.bottom
            model: payController.tokenModel
            spacing: 12
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                anchors.left: parent.left
                anchors.right: parent.right
                height: 60
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
                    radius: 20
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
                MySwitch {
                    visible: !tokenEntry.isDefault
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    checkable: true
                    checked: tokenEntry.isShow
                    onClicked: {
                        tokenEntry.isShow = !tokenEntry.isShow
                        payController.updateTokenShow(tokenEntry.name, tokenEntry.isShow)
                    }
                }
            }
        }
    }
}
