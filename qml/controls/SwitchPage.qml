import QtQuick 2.15
import QtQuick.Controls 2.15

import "../controls"

Item {
    id: root
    property int pageCount: 1
    property int pageIndex: 0
    signal pageClicked(int index)

    Component {
        id: repCom
        Row {
            spacing: 4
            Repeater {
                id: rep
                model: pageCount
                RecButton {
                    width: 24
                    height: 24
                    radius: 1
                    isSelected: index == pageIndex
                    Text {
                        anchors.centerIn: parent
                        text: index + 1
                    }
                    onClickedSignal: {
                        pageIndex = index
                        pageClicked(index)
                        recLoader.sourceComponent = undefined
                        sourceComponent = repCom
                    }
                }
            }
        }
    }

    Row {
        spacing: 4
        RecButton {
            width: 18
            height: 24
            isEnabled: pageIndex != 0
            Text {
                anchors.centerIn: parent
                text: "<"
            }
        }
        Loader {
            id: recLoader
            sourceComponent: repCom
        }
        RecButton {
            width: 18
            height: 24
            isEnabled: pageIndex != pageCount - 1
            Text {
                anchors.centerIn: parent
                text: ">"
            }
        }
    } 
}
