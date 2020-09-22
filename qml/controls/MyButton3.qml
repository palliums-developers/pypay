// common button eg: Create wallet button.
import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Button {
    id: control
    text: qsTr("MyButton3")
    hoverEnabled: true
    display: AbstractButton.TextBesideIcon
    opacity: hovered? 0.8 : 1

    property bool selected: false

    background: Rectangle {
        width: control.width
        height: control.height
        color: control.hovered ? "#60429E" : "#876CC0"
        radius: 0.5 * height
    }

    contentItem: Text {
        text: control.text
        font: control.font
        color: "#FFFFFF"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}
