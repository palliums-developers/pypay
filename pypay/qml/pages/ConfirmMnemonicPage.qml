import QtQuick 2.14
import QtQuick.Controls 2.5
import "../controls"

Page {
    id: root
    signal backArrowClicked
    signal completeBtnClicked
    property var mnemonicList: ["","","","","","","","","","","",""]

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
        text: qsTr("确认助记词")
        font.pointSize: 20
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 48
    }
    Text {
        id: title2Text
        text: qsTr("请顺序点击助记词，以确认您正确备份")
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
                model: mnemonicList
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
                model: payController.mnemonicRandom.split(" ")
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
                                payController.addMnemonicWord(modelData)
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
        visible: payController.mnemonicConfirm.length != 0
        Repeater {
            model: payController.mnemonicConfirm.split(" ")
            Rectangle {
                color: "#504ACB"
                width: 90
                height: 32
                Text {
                    anchors.centerIn: parent
                    text: modelData
                    font.pointSize: 15
                    color: "#FFFFFF"
                }
            }
        }
    }

    // 按钮
    MyButton3 {
        id: nextBtn
        anchors.top: gridRow.bottom
        anchors.topMargin: 82 / 952 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("完成")
        width: 200
        height: 40
        onClicked: {
            //if (payController.mnemonic != payController.mnemonicConfirm) {
            //    tipText.visible = true
            //    tipTimer.running = true
            //    payController.genMnemonicRandom()
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
        text: qsTr("助记词顺序不正确，请校对")
    }

    Timer {
        id: tipTimer
        interval: 3000
        onTriggered: tipText.visible = false
    }
}
