import QtQuick 2.15
import QtQuick.Controls 2.15

import "../controls"

Row {
    id: control
    property int pageCount: 1
    property int pageIndex: 0

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
                rep.itemAt(pageIndex).isSelected = false
                isSelected = true
                pageIndex = index
                console.log("pageIndex: ", pageIndex)
            }
        }
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
