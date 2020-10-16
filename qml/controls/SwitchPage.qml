import QtQuick 2.15
import QtQuick.Controls 2.15

import "../controls"

Item {
    id: root
    property int pageCount: 1
    property int pageIndex: 0
    property int spacing: 4
    property int oneRecWidth: 24
    signal pageClicked(int index)

    function refresh() {
        loader.sourceComponent = undefined
        loader.sourceComponent = pageNumComponent
    }

    Component {
        id: pageNumComponent
        Row {
            spacing: root.spacing
            Repeater {
                model: pageCount
                RecButton {
                    width: oneRecWidth
                    height: oneRecWidth
                    radius: 1
                    isSelected: index == pageIndex
                    Text {
                        anchors.centerIn: parent
                        text: index + 1
                    }
                    onClicked: {
                        root.pageClicked(index)
                    }
                }
            }
        }
    }

    Row {
        spacing: root.spacing
        RecButton {
            width: oneRecWidth * 2 / 3
            height: oneRecWidth
            radius: 1
            isEnabled: pageIndex != 0
            Text {
                anchors.centerIn: parent
                text: "<"
            }
            onClicked: {
                root.pageClicked(pageIndex - 1)
            }
        }
        Loader {
            id: loader
            sourceComponent: pageNumComponent
        }
        RecButton {
            width: oneRecWidth * 2 / 3
            height: oneRecWidth
            radius: 1
            isEnabled: pageIndex != pageCount - 1
            Text {
                anchors.centerIn: parent
                text: ">"
            }
            onClicked: {
                root.pageClicked(pageIndex + 1)
            }
        }
    } 
}
