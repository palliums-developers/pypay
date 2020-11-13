import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    signal completeBtnClicked

    ListModel {
        id: mnemonicModel
    }

    ImageButton {
        anchors.top: parent.top
        anchors.topMargin: 24
        anchors.left: parent.left
        anchors.leftMargin: 24
        width: 32
        source: "../icons/backarrow2.svg"
        MouseArea {
            anchors.fill: parent
            onClicked: {
                backArrowClicked()
            }
        }
    }

    Text {
        id: titleText
        text: qsTr("Confirm mnemonic")
        font.pointSize: 20
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 48
    }
    Text {
        id: title2Text
        text: qsTr("Click mnemonic on order")
        font.pointSize: 16
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: titleText.bottom
        anchors.topMargin: 4
    }

    Row {
        id: gridRow
        anchors.top: title2Text.bottom
        anchors.topMargin: 48 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 68
        
        Grid {
            id: mnemonicGrid
            columns: 3
            spacing: 8
            Repeater {
                model: 12
                Rectangle {
                    color: "#F6F6FC"
                    width: 90
                    height: 32
                }
            }
        }
        Grid {
            id: mnemonicGrid2
            columns: 3
            spacing: 8
            Repeater {
                model: server.mnemonic_random.split(" ")
                Rectangle {
                    id: mneRec
                    border.color: "#3C3848"
                    width: 90
                    height: 32
                    Text {
                        id: mneText
                        anchors.centerIn: parent
                        text: modelData
                        font.pointSize: 15
                        color: "#3C3848"
                    }
                    MouseArea {
                        anchors.fill: parent
                        property bool isClicked: false
                        onClicked: {
                            if (!isClicked) {
                                mnemonicModel.append({"word": modelData})
                                mneRec.border.color = "#FFFFFF"
                                mneText.color = "#FFFFFF"
                                isClicked = true
                            }
                        }
                    }
                }
            }
        }
    }

    Grid {
        id: mnemonicConfirmGrid
        anchors.left: gridRow.left
        anchors.top: gridRow.top
        columns: 3
        spacing: 8
        visible: mnemonicModel.count != 0
        Repeater {
            model: mnemonicModel
            Rectangle {
                color: "#504ACB"
                width: 90
                height: 32
                Text {
                    anchors.centerIn: parent
                    text: word
                    font.pointSize: 15
                    color: "#FFFFFF"
                }
            }
        }
    }

    MyButton3 {
        id: nextBtn
        anchors.top: gridRow.bottom
        anchors.topMargin: 82 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("Complited")
        width: 200
        height: 40
        onClicked: {
            //if (payController.mnemonic != payController.mnemonicConfirm) {
            //    tipText.visible = true
            //    tipTimer.running = true
            //    server.gen_random_mnemonic()
            //} else {
                root.completeBtnClicked()
                appSettings.mnemonicIsBackup = true
            //}
        }
    }

    Text {
        id: tipText
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: nextBtn.bottom
        anchors.topMargin: 3
        visible: false
        font.pointSize: 14
        color: "#FD6565"
        text: qsTr("Mnemonic order is not right")
    }

    Timer {
        id: tipTimer
        interval: 3000
        onTriggered: tipText.visible = false
    }
}
