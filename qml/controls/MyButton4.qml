import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Button {
    id: control
    text: qsTr("MyButton4")
    hoverEnabled: true
    display: AbstractButton.TextBesideIcon
    opacity: hovered? 0.8 : 1

    property bool selected: false

    background: Rectangle {
        width: control.width
        height: control.height
        radius: width / 2
        color: "#694d9f"
    }

    contentItem: RowLayout {
        anchors.fill: parent
        spacing: 4
        Image {
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
            source: control.icon.source
            Layout.preferredHeight: 20
            fillMode: Image.PreserveAspectFit 
        }
        Text {
            text: control.text
            font.pointSize: 10
            color: "#FFFFFF"
            Layout.alignment: Qt.AlignVCenter
            elide: Text.ElideRight
        }
    }
}
