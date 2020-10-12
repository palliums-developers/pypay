import QtQuick 2.14
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

import PyPay 1.0

Page {
    id: root

    property int topMargin: 43
    property int bottomMargin: 49      

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
        text: qsTr("Bank > <b><b>Deposit</b></b>")
        font.pointSize: 14
        color: "#5C5C5C"
        anchors.verticalCenter: backBtn.verticalCenter
        anchors.left: backBtn.right
        anchors.leftMargin: 8
    }

    Flickable {
        clip: true
        anchors.top: parent.top
        anchors.topMargin: 140
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 40
        anchors.horizontalCenter: parent.horizontalCenter
        width: 716
        contentHeight: contentColumn.height + root.topMargin + depositBtn.height + root.bottomMargin + contentColumn2.height

        Column {
            id: contentColumn
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            spacing: 10

            Rectangle {
                id: conRec
                width: parent.width
                height: 32 + storeText.contentHeight + 40 + conRow.height + 16 + conRow2.height + 32
                color: "#FFFFFF"
                Text {
                    id: storeText
                    text: qsTr("Store")
                    color: "#5C5C5C"
                    font.pointSize: 12
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: parent.top
                    anchors.topMargin: 32
                }
                TextFieldLine {
                    id: inputLine
                    anchors.left: storeText.right
                    anchors.leftMargin: 8
                    anchors.right: tokenText.left
                    anchors.rightMargin: 8
                    anchors.verticalCenter: storeText.verticalCenter
                    placeholderText: qsTr("minimum_amount: ") + (server.bankDepositInfo.minimum_amount / 1000000).toFixed(6) + ",  " + qsTr("minimum_step: ") + (server.bankDepositInfo.minimum_step / 1000000).toFixed(6)
                }
                Text {
                    id: tokenText
                    text: server.bankDepositInfo.token_show_name
                    anchors.right: parent.right
                    anchors.rightMargin: 50
                    anchors.verticalCenter: storeText.verticalCenter
                }
                Row {
                    id: conRow
                    anchors.left: storeText.left
                    anchors.top: storeText.bottom
                    anchors.topMargin: 40
                    spacing: 8
                    Image {
                        id: avaImage
                        width: 20
                        fillMode: Image.PreserveAspectFit
                        source: "../icons/availablebank.svg"
                    }
                    Text {
                        text: qsTr("avaliable balance: ")
                        font.pointSize: 12
                        color: "#5C5C5C"
                        anchors.verticalCenter: avaImage.verticalCenter
                    }
                    Text {
                        text: qsTr("All")
                        color: "#7038FD"
                        font.pointSize: 12
                        anchors.verticalCenter: avaImage.verticalCenter
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                            }
                        }
                    }
                }

                Row {
                    id: conRow2
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: conRow.bottom
                    anchors.topMargin: 16
                    spacing: 8
                    Image {
                        id: limitImage
                        width: 20
                        fillMode: Image.PreserveAspectFit
                        source: "../icons/limitbank.svg"
                    }
                    Text {
                        text: qsTr("limit of day: ") + (server.bankDepositInfo.quota_limit / 1000000).toFixed(6)
                        font.pointSize: 12
                        color: "#5C5C5C"
                        anchors.verticalCenter: limitImage.verticalCenter
                    }
                }
            }

            Rectangle {
                id: con2Rec
                width: parent.width
                height: 32 + rateText.contentHeight + 20 + 1 + 20 + con2Column.height + 20 + 1 + 20 + payTypeText.contentHeight + 32
                color: "#FFFFFF"
                Text {
                    id: rateText
                    text: qsTr("Rate")
                    color: "#5C5C5C"
                    font.pointSize: 12
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: parent.top
                    anchors.topMargin: 32
                }
                Text {
                    id: rateText2
                    text: server.bankDepositInfo.rate * 100 + "%"
                    anchors.verticalCenter: rateText.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 50
                    color: "#13B788"
                }
                Rectangle {
                    id: con2Line
                    anchors.top: rateText.bottom
                    anchors.topMargin: 20
                    anchors.left: rateText.left
                    anchors.right: rateText2.right
                    height: 1
                    color: "#DEDEDE"
                }
                Column {
                    id: con2Column
                    anchors.top: con2Line.bottom
                    anchors.topMargin: 20
                    anchors.left: con2Line.left
                    Text {
                        text: qsTr("pledge rate")
                        color: "#5C5C5C"
                    }
                    Text {
                        text: qsTr("pledge rate = deposit amount / borrow amount")
                        color: "#5C5C5C"
                    }
                }
                Text {
                    anchors.right: rateText2.right
                    anchors.verticalCenter: con2Column.verticalCenter
                    text: server.bankDepositInfo.pledge_rate * 100 + "%"
                }
                Rectangle {
                    id: con2Line2
                    anchors.top: con2Column.bottom
                    anchors.topMargin: 20
                    anchors.left: rateText.left
                    anchors.right: rateText2.right
                    height: 1
                    color: "#DEDEDE"
                }
                Text {
                    id: payTypeText
                    text: qsTr("Pay type")
                    color: "#5C5C5C"
                    font.pointSize: 12
                    anchors.left: rateText.left
                    anchors.top: con2Line2.bottom
                    anchors.topMargin: 20
                }
                Text {
                    id: payTypeText2
                    text: qsTr("Wallet")
                    anchors.verticalCenter: payTypeText.verticalCenter
                    anchors.right: rateText2.right
                }
            }
        }

        MyButton3 {
            id: depositBtn
            anchors.top: contentColumn.bottom
            anchors.topMargin: root.topMargin
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("Deposit Now")
            width: 200
            height: 40
        }

        Column {
            id: contentColumn2
            anchors.top: depositBtn.bottom
            anchors.topMargin: root.bottomMargin
            anchors.left: parent.left
            anchors.right: parent.right
            spacing: 10

            Rectangle {
                id: intorRec
                width: parent.width
                height: 32 + intorText.contentHeight + 32 + con3Column.height + (intorRec.isShowMore ? 32 : 0)
                color: "#FFFFFF"
                property bool isShowMore: false
                Text {
                    id: intorText
                    text: qsTr("Intor")
                    color: "#5C5C5C"
                    font.pointSize: 14
                    font.bold: true
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: parent.top
                    anchors.topMargin: 32
                }
                Image {
                    anchors.right: parent.right
                    anchors.rightMargin: 50
                    anchors.verticalCenter: intorText.verticalCenter
                    source: intorRec.isShowMore ? "../icons/arrow_down.svg" : "../icons/arrow_right.svg"
                    width: 12
                    fillMode: Image.PreserveAspectFit
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            intorRec.isShowMore = !intorRec.isShowMore
                        }
                    }
                }
                Column {
                    id: con3Column
                    anchors.left: intorText.left
                    anchors.top: intorText.bottom
                    anchors.topMargin: 32
                    spacing: 8
                    Repeater {
                        model: intorRec.isShowMore ? intorModel : 0
                        Text {
                            text: title + "  "  + content
                        }
                    }
                }
            }

            Rectangle {
                id: questionRec
                width: parent.width
                height: 32 + questionText.contentHeight + 32 + con4Column.height + (questionRec.isShowMore ? 32 : 0)
                color: "#FFFFFF"
                property bool isShowMore: false
                Text {
                    id: questionText
                    text: qsTr("Question")
                    color: "#5C5C5C"
                    font.pointSize: 14
                    font.bold: true
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: parent.top
                    anchors.topMargin: 32
                }
                Image {
                    anchors.right: parent.right
                    anchors.rightMargin: 50
                    anchors.verticalCenter: questionText.verticalCenter
                    source: questionRec.isShowMore ? "../icons/arrow_down.svg" : "../icons/arrow_right.svg"
                    width: 12
                    fillMode: Image.PreserveAspectFit
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            questionRec.isShowMore = !questionRec.isShowMore
                        }
                    }
                }
                Column {
                    id: con4Column
                    anchors.left: questionText.left
                    anchors.top: questionText.bottom
                    anchors.topMargin: 32
                    spacing: 8
                    Repeater {
                        model: questionRec.isShowMore ? questionModel : 0
                        Column {
                            spacing: 16
                            Text {
                                text: title
                                font.pointSize: 12
                            }
                            Text {
                                text: content
                                font.pointSize: 10
                            }
                        }
                    }
                }
            }
        }
    }
}
