import QtQuick 2.14
import QtQuick.Controls 2.14

Button {
    id: control
    flat: true
    text: qsTr("MyButton")
    hoverEnabled: true

    contentItem: Text {
        text: control.text
        font: control.font
        color: control.down || hovered? "#FFFFFF" : "#501BA2"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 30
        implicitHeight: 15
        color: control.down || hovered? "#501BA2" : "#FFFFFF"
        radius: 4
    }
}
