import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Button {
    id: control
    flat: true
    text: qsTr("MenuButton")
    hoverEnabled: true
    display: AbstractButton.TextBesideIcon
    opacity: hovered? 0.8 : 1

    property bool selected: false

    background: Image {
        width: control.width
        height: control.height
        source: control.selected? "../icons/menubuttonbackground.svg" : ""
    }

    contentItem: RowLayout {
        spacing: 8
        Image {
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            source: control.icon.source
        }
        Text {
            text: control.text
            font: control.font
            color: "#FFFFFF"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
        }
    }
}
