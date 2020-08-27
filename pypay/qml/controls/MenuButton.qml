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

    contentItem: Row {
        anchors.left: parent.left
        anchors.leftMargin: 50
        anchors.verticalCenter: parent.verticalCenter
        spacing: 8
        Image {
            id: conImage
            source: control.icon.source
            anchors.verticalCenter: parent.verticalCenter
            width: 24
            fillMode: Image.PreserveAspectFit
        }
        Text {
            text: control.text
            font: control.font
            color: "#FFFFFF"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            elide: Text.ElideRight
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
