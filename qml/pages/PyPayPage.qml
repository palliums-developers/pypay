import QtQuick 2.15
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.15

import "../controls"

import PyPay 1.0

Page {
    id: root
    property bool isShowHeader: false
    property string tipText: qsTr("Server request error!")
    signal backArrowClicked

    function startBusy() {
        timer.running = true
        busy.running = true
        maskRec.visible = true
    }

    function stopBusy() {
        timer.running = false
        busy.running = false
        maskRec.visible = false
    }

    background: Rectangle {
        id: backRec
        color: "#F7F7F9"
    }

    Row {
        z: 1000
        visible: isShowHeader
        anchors.left: parent.left
        anchors.leftMargin: 72
        anchors.top: parent.top
        anchors.topMargin: 72
        spacing: 8
        ImageButton {
            id: backBtn
            width: 24
            height: 24
            source: "../icons/backarrow3.svg"
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    root.backArrowClicked()
                }
            }
        }

        Text {
            text: root.title
            font.pointSize: 14
            color: "#5C5C5C"
            anchors.verticalCenter: backBtn.verticalCenter
        }
    }

    BusyIndicator {
        z: 1000
        id: busy
        anchors.centerIn: parent
        running: false
    }

    Rectangle {
        z: 999
        id: maskRec
        color: backRec.color
        anchors.fill: parent
        visible: false
    }

    Text {
        id: tip
        z: 1000
        text: tipText
        anchors.centerIn: parent
        visible: false
    }

    Timer {
        id: timer
        interval: 3000
        repeat: false
        running: false
        onTriggered: {
            busy.running = false
            tip.visible = true
        }
    }
}
