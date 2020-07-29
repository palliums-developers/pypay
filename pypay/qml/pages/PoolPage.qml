import QtQuick 2.14
import QtQuick.Controls 2.14

Page {
    Button {
        anchors.left: parent.left
        anchors.leftMargin: 68
        anchors.top: parent.top
        anchors.topMargin: 31
        text: qsTr("My pool")
    }

    // Rate
    Text {
        text: qsTr("Fee Rate: ") + "0.100%"
        font.pointSize: 14
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
        height: 94.0 / 952 * parent.height
        border.color: inText.activeFocus ? "red" : "#C2C2C2"
        Text {
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.top: parent.top
            anchors.topMargin: 8
            text: qsTr("Input")
            font.pointSize: 14
            color: "#333333"
        }
        TextField {
            id: inText
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 8
            width: 200
            background: Rectangle {
                border.color: "#FFFFFF"
            }
        }
        ComboBox {
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 12
            model: ["Select token", "token1", "token2", "token3"]
        }
    }

    Text {
        id: changeImage
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: changeInRec.bottom
        anchors.topMargin: 5
        height: 24
        text: "&"
    }

    // Out
    Rectangle {
        id: changeOutRec
        anchors.top: changeImage.bottom
        anchors.topMargin: 5
        anchors.horizontalCenter: parent.horizontalCenter
        width: 635.0 / 1160 * parent.width
        height: 94.0 / 952 * parent.height
        border.color: outText.activeFocus ? "red" : "#C2C2C2"
        Text {
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.top: parent.top
            anchors.topMargin: 8
            text: qsTr("Output")
            font.pointSize: 14
            color: "#333333"
        }
        TextField {
            id: outText
            anchors.left: parent.left
            anchors.leftMargin: 8
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 8
            width: 200
            background: Rectangle {
                border.color: "#FFFFFF"
            }
        }
        ComboBox {
            anchors.right: parent.right
            anchors.rightMargin: 8
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 12
            model: ["Select token", "token1", "token2", "token3"]
        }
    }
    
    // Change Rate and Fee
    Column {
        anchors.left: changeOutRec.left
        anchors.leftMargin: 8
        anchors.top: changeOutRec.bottom
        anchors.topMargin: 8
        Text {
            text: qsTr("Change rate: ") + "--"
            font.pointSize: 12
            color: "#5C5C5C"
        }
        Text {
            text: qsTr("Miner fee: ") + "--"
            font.pointSize: 12
            color: "#5C5C5C"
        }
    }

    // Change button
    Button {
        id: changeButton
        text: qsTr("Change")
        hoverEnabled: true
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: changeOutRec.bottom
        anchors.topMargin: 77.0 / 952 * parent.height
        width: 280
        height: 46

        contentItem: Text {
            text: changeButton.text
            font: changeButton.font
            color: "#FFFFFF"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }

        background: Rectangle {
            implicitWidth: changeButton.width
            implicitHeight: changeButton.height
            color: "#6131AB"
            radius: changeButton.height / 2
        }
    }

    // Change history
    Text {
        id: changeHistoryText
        anchors.left: changeOutRec.left
        anchors.top: changeButton.bottom
        anchors.topMargin: 74.0 / 952 * parent.height
        text: qsTr("Pool histrory")
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
