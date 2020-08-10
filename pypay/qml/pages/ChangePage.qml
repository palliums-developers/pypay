import QtQuick 2.14
import QtQuick.Controls 2.14
import "../controls"

Page {

    // Rate
    Text {
        text: qsTr("费率:") + "0.100%"
        font.pointSize: 12
        color: "#5C5C5C"
        anchors.right: changeInRec.right
        anchors.bottom: changeInRec.top
        anchors.bottomMargin: 5
    }
    
    // In
    Rectangle {
        id: changeInRec
        anchors.top: parent.top
        anchors.topMargin: 118.0 / 1024 * parent.height
        anchors.horizontalCenter: parent.horizontalCenter
        width: 635.0 / 1160 * parent.width
        height: 64
        border.color: inText.activeFocus ? "red" : "#C2C2C2"
        Text {
            id: inT
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: parent.top
            anchors.topMargin: 2
            text: qsTr("输入")
            font.pointSize: 12
            color: "#333333"
        }
        TextField {
            id: inText
            anchors.left: inT.left
            anchors.top: inT.bottom
            anchors.topMargin: 2
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 2
            width: parent.width - inTokenComboBox.width - 4 * 2
            background: Rectangle {
                border.color: "#FFFFFF"
            }
        }
        TokenComboBox {
            id: inTokenComboBox
            anchors.right: parent.right
            anchors.rightMargin: 4
            anchors.verticalCenter: inText.verticalCenter
        }
    }

    Image {
        id: changeImage
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: changeInRec.bottom
        anchors.topMargin: 4
        height: 24
        fillMode: Image.PreserveAspectFit
        source: "../icons/change.svg"
    }

    // Out
    Rectangle {
        id: changeOutRec
        anchors.top: changeImage.bottom
        anchors.topMargin: 5
        anchors.horizontalCenter: parent.horizontalCenter
        width: 635.0 / 1160 * parent.width
        height: 64
        border.color: outText.activeFocus ? "red" : "#C2C2C2"
        Text {
            id: outT
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: parent.top
            anchors.topMargin: 2
            text: qsTr("输出")
            font.pointSize: 12
            color: "#333333"
        }
        TextField {
            id: outText
            anchors.left: outT.left
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 2
            anchors.top: outT.bottom
            anchors.topMargin: 2
            width: parent.width - outTokenComboBox.width - 4 * 2
            background: Rectangle {
                border.color: "#FFFFFF"
            }
        }
        TokenComboBox {
            id: outTokenComboBox
            anchors.right: parent.right
            anchors.rightMargin: 4
            anchors.verticalCenter: outText.verticalCenter
        }
    }
    
    // Change Rate and Fee
    Column {
        id: rateColumn
        anchors.left: changeOutRec.left
        anchors.leftMargin: 8
        anchors.top: changeOutRec.bottom
        anchors.topMargin: 8
        Text {
            text: qsTr("兑换率: ") + "--"
            font.pointSize: 12
            color: "#5C5C5C"
        }
        Text {
            text: qsTr("矿工费用: ") + "--"
            font.pointSize: 12
            color: "#5C5C5C"
        }
    }

    // Change button
    MyButton3 {
        id: changeButton
        text: qsTr("兑换")
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: rateColumn.bottom
        anchors.topMargin: 8
        width: 200
        height: 46
    }

    // Change history
    Text {
        id: changeHistoryText
        anchors.left: changeOutRec.left
        anchors.top: changeButton.bottom
        anchors.topMargin: 24 / 952 * parent.height
        text: qsTr("兑换记录")
        color: "#3D3949"
        font.pointSize: 16
    }
    Rectangle {
        width: 15
        height: 2
        color: "#7038FD"
        anchors.left: changeHistoryText.left
        anchors.top: changeHistoryText.bottom
        anchors.topMargin: 2
    }
}
