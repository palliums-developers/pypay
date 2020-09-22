import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../controls"

import PyPay 1.0

Control {
    id: root
    padding: 8

    signal goBack
    signal transactionDetailOpened

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
            text: qsTr("币种详情")
            color: "#333333"
            font.pointSize: 16
            font.weight: Font.Medium
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Image {
            id: ima
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.top: titleText.bottom
            anchors.topMargin: 25
            height: 140
            source: "../icons/coindetailbackground.svg"
            Item {
                anchors.fill: parent
                ColumnLayout {
                    id: colLayout
                    anchors.fill: parent
                    Row {
                        spacing: 8
                        MyImage {
                            source: {
                                if (payController.currentTokenEntry.chain == "bitcoin") {
                                    return "../icons/bitcoin.svg"
                                } else if (payController.currentTokenEntry.chain == "violas") {
                                    return "../icons/violas.svg"
                                } else if (payController.currentTokenEntry.chain == "libra") {
                                    return "../icons/libra.svg"
                                } else {
                                    return ""
                                }
                            }
                            width: height
                            height: 14
                            radius: 0.5 * width
                            anchors.verticalCenter: nameText.verticalCenter
                        }
                        Text {
                            id: nameText
                            text: payController.currentTokenEntry.name
                            color: "#999999"
                            font.weight: Font.Normal
                            font.pointSize: 12
                        }
                    }
                    Text {
                        text: appSettings.eyeIsOpen ? payController.currentTokenEntry.amount : "******"
                        color: "#333333"
                        font.weight: Font.Bold
                        font.pointSize: 18
                    }
                    Text {
                        text: appSettings.eyeIsOpen ? "≈$" + payController.currentTokenEntry.totalPrice : "******"
                        color: "#999999"
                        font.weight: Font.Normal
                        font.pointSize: 12
                    }
                    Row {
                        spacing: 4
                        Text {
                            id: addrText
                            text: payController.currentTokenEntry.addr
                            color: "#5C5C5C"
                            font.weight: Font.Medium
                            font.pointSize: 14
                            width: colLayout.width - 8 * 2 - 4 - copyImgBtn.width
                            elide: Text.ElideMiddle
                            verticalAlignment: Text.AlignVCenter
                        }
                        ImageButton {
                            id: copyImgBtn
                            source: "../icons/copy.svg"
                            width: 10
                            height: 12
                            anchors.verticalCenter: addrText.verticalCenter
                            MouseArea {
                                anchors.fill: parent
                                onClicked: payController.copy(payController.currentTokenEntry.addr)
                            }
                        }
                    }
                }
            }
        }

        Row {
            id: rowBar
            anchors.left: ima.left
            anchors.leftMargin: 16
            anchors.top: ima.bottom
            anchors.topMargin: 32
            spacing: 40

            function disableSelect() {
                allText.isSelected = false
                inText.isSelected = false
                outText.isSelected = false
            }

            Text {
                id: allText
                text: qsTr("全部")
                property bool isSelected: true
                color: isSelected? "#7038FD" : "#C2C2C2"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rowBar.disableSelect()
                        parent.isSelected = !parent.isSelected
                        if (payController.currentTokenEntry.chain == "libra") {
                            payController.requestLBRHistory(payController.currentTokenEntry.addr, payController.currentTokenEntry.name, -1, 0, 100)
                        } else if (payController.currentTokenEntry.chain == "violas") {
                            payController.requestVLSHistory(payController.currentTokenEntry.addr, payController.currentTokenEntry.name, -1, 0, 100)
                        } else {
                            console.log("invaild")
                        }
                    }
                }
            }
            Text {
                id: inText
                text: qsTr("转入")
                property bool isSelected: false
                color: isSelected? "#7038FD" : "#C2C2C2"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rowBar.disableSelect()
                        parent.isSelected = !parent.isSelected
                        if (payController.currentTokenEntry.chain == "libra") {
                            payController.requestLBRHistory(payController.currentTokenEntry.addr, payController.currentTokenEntry.name, 1, 0, 100)
                        } else if (payController.currentTokenEntry.chain == "violas") {
                            payController.requestVLSHistory(payController.currentTokenEntry.addr, payController.currentTokenEntry.name, 1, 0, 100)
                        } else {
                            console.log("invaild")
                        }
                    }
                }
            }
            Text {
                id: outText
                text: qsTr("转出")
                property bool isSelected: false
                color: isSelected? "#7038FD" : "#C2C2C2"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        rowBar.disableSelect()
                        parent.isSelected = !parent.isSelected
                        if (payController.currentTokenEntry.chain == "libra") {
                            payController.requestLBRHistory(payController.currentTokenEntry.addr, payController.currentTokenEntry.name, 0, 0, 100)
                        } else if (payController.currentTokenEntry.chain == "violas") {
                            payController.requestVLSHistory(payController.currentTokenEntry.addr, payController.currentTokenEntry.name, 0, 0, 100)
                        } else {
                            console.log("invaild")
                        }
                    }
                }
            }
        }

        ListView {
            id: listView
            anchors.top: rowBar.bottom
            anchors.topMargin: 22
            anchors.left: rowBar.left
            anchors.right: ima.right
            anchors.rightMargin: 16
            anchors.bottom: parent.bottom
            model: payController.historyModel
            spacing: 8
            clip: true
            ScrollIndicator.vertical: ScrollIndicator { }
            delegate: Rectangle {
                width: listView.width
                height: 40
                color: "#EBEBF1"
                Image {
                    id: itemImage
                    source: "../icons/history.svg"
                    width: 24
                    fillMode: Image.PreserveAspectFit
                    anchors.left: parent.left
                    anchors.leftMargin: 8
                    anchors.verticalCenter: parent.verticalCenter
                }
                Text {
                    id: versionText
                    text: historyEntry.version
                    anchors.left: itemImage.right
                    anchors.leftMargin: 16
                    anchors.verticalCenter: parent.verticalCenter
                    color: "#333333"
                    font.pointSize: 12
                }
                Text {
                    id: amountText
                    text: historyEntry.amount
                    anchors.right: parent.right
                    anchors.rightMargin: 8
                    anchors.verticalCenter: parent.verticalCenter   
                    color: "#333333"
                    font.pointSize: 12
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        //payController.currentBitTransactionEntry = bitTransactionEntry
                        transactionDetailOpened()
                    }
                }
            }
        }
    }
}
