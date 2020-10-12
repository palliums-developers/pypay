import QtQuick 2.14
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"
import "../models/ViolasServer.js" as Server

//import PyPay 1.0

Page {
    id: root

    property var bankBorrowInfo: ({})
    property int topMargin: 79      // top to borrowBtn
    property int bottomMargin: 49   // bottom to borrowBtn   
    property bool isSelected: false

    signal backArrowClicked

    function getBorrowInfo(id) {
        if (payController.addr) {
            Server.request('GET', '/1.0/violas/bank/borrow/info?id='+ id + '&address=' + payController.addr,
                null, function(resp) {
                    bankBorrowInfo = resp.data;
                    for (var i=0; i<resp.data.intor.length; i++) {
                        intorModel.append({"title":resp.data.intor[i].title, "content":resp.data.intor[i].text})
                    }
                    for (var i=0; i<resp.data.question.length; i++) {
                        questionModel.append({"title":resp.data.question[i].title, "content":resp.data.question[i].text})
                    }
                    console.log(JSON.stringify(bankBorrowInfo))
                });
        }
    }

    ListModel {
        id: intorModel
    }

    ListModel {
        id: questionModel
    }

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
        text: qsTr("Bank > <b><b>Borrow</b></b>")
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
        contentHeight: contentColumn.height + root.topMargin + borrowBtn.height + root.bottomMargin + contentColumn2.height

        Column {
            id: contentColumn
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            spacing: 10

            Rectangle {
                id: conRec
                width: parent.width
                height: 32 + borrowText.contentHeight + 40 + conRow.height + 32
                color: "#FFFFFF"
                Text {
                    id: borrowText
                    text: qsTr("Borrow")
                    color: "#5C5C5C"
                    font.pointSize: 12
                    anchors.left: parent.left
                    anchors.leftMargin: 50
                    anchors.top: parent.top
                    anchors.topMargin: 32
                }
                TextFieldLine {
                    id: inputLine
                    anchors.left: borrowText.right
                    anchors.leftMargin: 8
                    anchors.right: tokenText.left
                    anchors.rightMargin: 8
                    anchors.verticalCenter: borrowText.verticalCenter
                    placeholderText: qsTr("minimum_amount: ") + (bankBorrowInfo.minimum_amount / 1000000).toFixed(6) + ",  " + qsTr("minimum_step: ") + (bankBorrowInfo.minimum_step / 1000000).toFixed(6)
                }
                Text {
                    id: tokenText
                    text: bankBorrowInfo.token_show_name
                    anchors.right: parent.right
                    anchors.rightMargin: 50
                    anchors.verticalCenter: borrowText.verticalCenter
                }
                Row {
                    id: conRow
                    anchors.left: borrowText.left
                    anchors.top: borrowText.bottom
                    anchors.topMargin: 40
                    spacing: 8
                    Image {
                        id: avaImage
                        width: 20
                        fillMode: Image.PreserveAspectFit
                        source: "../icons/availablebank.svg"
                    }
                    Text {
                        text: qsTr("avaliable borrow: ")
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
            }

            Rectangle {
                id: con2Rec
                width: parent.width
                height: 32 + rateText.contentHeight + 20 + 1 + 20 + con2Column.height + 20 + 1 + 20 + con2Column2.height + 32
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
                    text: bankBorrowInfo.rate * 100 + "%" + "/" + qsTr("Day")
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
                        text: qsTr("pledge rate = borrow amount / deposit amount")
                        color: "#5C5C5C"
                    }
                }
                Text {
                    anchors.right: rateText2.right
                    anchors.verticalCenter: con2Column.verticalCenter
                    text: bankBorrowInfo.pledge_rate * 100 + "%"
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
                Column {
                    id: con2Column2
                    anchors.left: rateText.left
                    anchors.top: con2Line2.bottom
                    anchors.topMargin: 20
                    Text {
                        text: qsTr("Borrow account")
                        color: "#5C5C5C"
                        font.pointSize: 12
                    }
                    Text {
                        text: qsTr("liquidation part will Deduction from deposit account")
                        color: "#5C5C5C"
                    }
                }
                Text {
                    id: payTypeText2
                    text: qsTr("Bank")
                    anchors.verticalCenter: con2Column2.verticalCenter
                    anchors.right: rateText2.right
                }
            }
        }

        Row {
            anchors.top: contentColumn.bottom
            anchors.topMargin: 40
            anchors.horizontalCenter: parent.horizontalCenter
            spacing: 5
            Image {
                anchors.verticalCenter: checkText.verticalCenter
                width: 14
                height: 14
                source: root.isSelected ? "../icons/xuanze-2.svg" : "../icons/xuanze.svg"
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        root.isSelected = !root.isSelected
                    }
                }
            }
            Text {
                id: checkText
                text: qsTr("<font color="#999999">I read and agree</font><font color="#7038FD"><b>《Borrow agreement》</b></font>")
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        payController.openUrl("https://violas.io")
                    }
                }
            }
        }

        MyButton3 {
            id: borrowBtn
            anchors.top: contentColumn.bottom
            anchors.topMargin: root.topMargin
            anchors.horizontalCenter: parent.horizontalCenter
            text: qsTr("Borrow Now")
            width: 200
            height: 40
        }

        Column {
            id: contentColumn2
            anchors.top: borrowBtn.bottom
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
