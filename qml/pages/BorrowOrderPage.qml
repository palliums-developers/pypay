import QtQuick 2.14
import QtQuick.Controls 2.5
import "../controls"

Page {
    id: root
    background: Rectangle {
        color: "#F7F7F9"
    }
    signal backArrowClicked

    function getBalance(chain, name) {
        payController.getCurBalance(chain, name)
    }

    background: Rectangle {
        color: "#F7F7F9"
    }

    Flickable {
        anchors.fill: parent
        contentHeight: 200000

        ImageButton {
            id: backBtn
            anchors.top: parent.top
            anchors.topMargin: 98
            anchors.left: parent.left
            anchors.leftMargin: 92
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
            text: qsTr("Bank> <b>Borrow Order</b>")
            font.pointSize: 14
            color: "#5C5C5C"
            anchors.verticalCenter: backBtn.verticalCenter
            anchors.left: backBtn.right
            anchors.leftMargin: 8
        }
    }
}
