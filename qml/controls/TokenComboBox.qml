import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

import "../controls"

Rectangle {
    id: root
    width: 100
    height: 32
    radius: 16
    color: isListPopOpen ? "#6131AB" : "#d3d3d3"
    property bool isListPopOpen: false

    property string chain: "bitcoin"
    property string name: "BTC"
    signal tokenSelected
    property bool isShowViolasCoin: true

    RowLayout {
        anchors.fill: parent
        spacing: 4
        MyImage {
            id: itemImage
            source: {
                if (chain == "bitcoin") {
                    return "../icons/bitcoin.svg"
                } else if (chain == "diem") {
                    return "../icons/diem.svg"
                } else if (chain == "violas") {
                    return "../icons/violas.svg"
                } else {
                    return ""
                }
            }
            width: root.height - 10
            height: width
            radius: width / 2
            Layout.preferredWidth: width
            Layout.leftMargin: 8
        }

        Text {
            id: curName
            color: root.isListPopOpen ? "#FFFFFF" : "#7038FD" 
            text: name
            font.pointSize: 12
            Layout.fillWidth: true
            Layout.leftMargin: 4
        }

        Canvas {
            id: canvas
            Layout.preferredWidth: 12
            Layout.preferredHeight: 8
            Layout.rightMargin: 8
            contextType: "2d"

            onPaint: {
                var ctx = getContext("2d")
                ctx.strokeStyle = root.isListPopOpen ? "#FFFFFF" : "#7038FD"
                ctx.beginPath()
                ctx.moveTo(2,2)
                ctx.lineTo(width/2,height - 2)
                ctx.lineTo(width - 2,2)
                ctx.stroke()
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            popup.open()
        }
    }

    Popup {
        id: popup
        x: parent.width / 2 - width / 2
        y: parent.height + 20
        width: 375
        height: 338
        onOpened: {
            root.isListPopOpen = true
            canvas.requestPaint()
        }
        onClosed: {
            root.isListPopOpen = false
            canvas.requestPaint()
        }
        background: Rectangle {
            border.color: "lightsteelblue"
            radius: 10
        }
        contentItem: Item {
            ListView {
                id: listView
                anchors.fill: parent
                model: server.model_tokens
                spacing: 8
                clip: true
                ScrollIndicator.vertical: ScrollIndicator { }
                delegate: Rectangle {
                    width: listView.width
                    height: appWindow.currencies_show.includes(show_name) ? 60 : -8
                    visible: appWindow.currencies_show.includes(show_name)
                    radius: 8
                    color: "#EBEBF1"
                    RowLayout {
                        anchors.fill: parent
                        MyImage {
                            id: itemImage
                            source: {
                                if (chain == "bitcoin") {
                                    return "../icons/bitcoin.svg"
                                } else if (chain == "diem") {
                                    return "../icons/diem.svg"
                                } else if (chain == "violas") {
                                    return "../icons/violas.svg"
                                } else {
                                    return ""
                                }
                            }
                            radius: 20
                            width: 40
                            height: width
                            Layout.preferredWidth: width
                            Layout.leftMargin: 8
                        }
                        Text {
                            text: name
                            Layout.fillWidth: true
                            Layout.leftMargin: 8
                        }
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            root.chain = chain
                            root.name = name
                            popup.close()
                            tokenSelected()
                        }
                    }
                }
            }
        }
    }
}
