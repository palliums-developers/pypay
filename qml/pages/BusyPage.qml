import QtQuick 2.14
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../controls"

Page {
    id: root
    signal backArrowClicked

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

    BusyIndicator {
        id: busy
        anchors.centerIn: parent
        running: true
    }

    Timer {
        interval: 3000
        repeat: false
        running: true
        onTriggered: {
            busy.running = false
            tip.visible = true
        }
    }

    Text {
        id: tip
        text: qsTr("Server request error!")
        anchors.centerIn: parent
        visible: false
    }
}
