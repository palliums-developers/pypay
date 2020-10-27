import QtQuick 2.15 
import QtQuick.Controls 2.15 

import "../controls" 

Item {
    id: root
    property int numOfPerPage: 10
    property int pageIndex: 0
    property int spacing: 4
    property int oneRecWidth: 24
    property alias listModel: listModel
    signal pageClicked(int index)
    width: oneRecWidth * 2 / 3 + oneRecWidth * listModel.count + spacing * (listModel.count - 1) + oneRecWidth * 2 / 3
    height: oneRecWidth

    ListModel {
        id: listModel
    }

    ListView {
        id: listView
        anchors.fill: parent
        model: listModel
        orientation: ListView.Horizontal
        spacing: root.spacing
        highlight: Rectangle { color: "lightsteelblue"; radius: 1 }
        header: Item {
            width: headerRecBtn.width + spacing
            height: headerRecBtn.height
            RecButton {
                id: headerRecBtn
                anchors.left: parent.left
                width: oneRecWidth * 2 / 3
                height: oneRecWidth
                radius: 1
                isEnabled: pageIndex != 0
                Text {
                    anchors.centerIn: parent
                    text: "<"
                }
                onClicked: {
                    if (isEnabled) {
                        root.pageClicked(pageIndex - 1)
                        pageIndex -= 1
                    }
                }
            }
        }
        delegate: RecButton {
            width: oneRecWidth
            height: oneRecWidth
            isSelected: index == pageIndex
            Text {
                anchors.centerIn: parent
                text: index + 1
            }
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    root.pageClicked(index)
                    pageIndex = index
                }
            }
        }
        footer: Item {
            width: footerRecBtn.width + spacing
            height: footerRecBtn.height
            RecButton {
                id: footerRecBtn
                anchors.right: parent.right
                width: oneRecWidth * 2 / 3
                height: oneRecWidth
                radius: 1
                isEnabled: pageIndex != listModel.count - 1
                Text {
                    anchors.centerIn: parent
                    text: ">"
                }
                onClicked: {
                    if (isEnabled) {
                        root.pageClicked(pageIndex + 1)
                        pageIndex += 1
                    }
                }
            }
        }
    }
}
