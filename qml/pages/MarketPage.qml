import QtQuick 2.14
import QtQuick.Controls 2.14

Page {
    property bool isChangeSelected: true

    ChangePage {
        anchors.fill: parent
        visible: isChangeSelected
    }

    PoolPage {
        anchors.fill: parent
        visible: !isChangeSelected
    }

    Rectangle {
        id: selectRec
        width: 200
        height: 34
        color: "#FFFFFF"
        radius:  100      
        border.color: "#7038FD"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 31.0 / 952 * parent.height

        Row {
            anchors.verticalCenter: selectRec.verticalCenter
            padding: 1
            Rectangle {
                id: changeRec
                width: 99
                height: 32
                radius: 100
                color: isChangeSelected ? "#7038FD" : "#FFFFFF"
                Text {
                    text: qsTr("兑换")
                    color: isChangeSelected ? "#FFFFFF" : "#7038FD"
                    anchors.centerIn: parent
                }   
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        isChangeSelected = true
                    }
                }
            }
            Rectangle {
                id: poolRec
                width: 99
                height: 32
                radius: 100
                color: isChangeSelected ? "#FFFFFF" : "#7038FD"
                Text {
                    text: qsTr("资金池")
                    color: isChangeSelected ? "#7038FD" : "#FFFFFF"
                    anchors.centerIn: parent
                }   
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        isChangeSelected = false
                    }
                }
            }
        }
    }
}
