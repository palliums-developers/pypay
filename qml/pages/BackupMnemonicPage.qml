import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked
    signal nextBtnClicked

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
        text: qsTr("备份助记词")
        font.pointSize: 20
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 48
    }
    Text {
        id: title2Text
        text: qsTr("请将这些词按顺序写在纸上")
        font.pointSize: 16
        color: "#3B3847"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: titleText.bottom
        anchors.topMargin: 3
    }

    Grid {
        id: mnemonicGrid
        columns: 3
        anchors.top: title2Text.bottom
        anchors.topMargin: 24
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 16
        Repeater {
            //model: payController.mnemonic.split(" ")
            Rectangle {
                border.color: "#3C3848"
                width: 90
                height: 32
                Text {
                    anchors.centerIn: parent
                    text: modelData
                    font.pointSize: 15
                }
            }
        }
    }

    Row {
        id: tipRow
        anchors.left: mnemonicGrid.left
        anchors.right: mnemonicGrid.right
        anchors.top: mnemonicGrid.bottom
        anchors.topMargin: 24
        spacing: 10
        Image {
            id: noPictureImage
            source: "../icons/nopicture.svg"
            width: 40
            fillMode: Image.PreserveAspectFit
        }
        Text {
            anchors.verticalCenter: noPictureImage.verticalCenter
            text: qsTr("不要截屏或复制到剪切板，这将可能被第三方恶意软件收集，造成资产损失")
            color: "#3B3847"
            font.pointSize: 12
            width: mnemonicGrid.width - 40 - 10
            wrapMode: Text.WordWrap
        }
    }

    

    // 按钮
    MyButton3 {
        id: nextBtn
        anchors.top: tipRow.bottom
        anchors.topMargin: 8
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("下一步")
        width: 200
        height: 40
        onClicked: {
            //payController.genMnemonicRandom()
            root.nextBtnClicked()
        }
    }
}
