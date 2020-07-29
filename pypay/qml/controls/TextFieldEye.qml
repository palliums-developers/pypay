import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.14

Rectangle {
    id: control
    width: 642
    height: 50
    border.color: textField.activeFocus ? "#FD6565" : "#979797"

    property string placeholderText: ""
    property alias text: textField.text
    property string imageSource: ""
    property bool eyeIsClose: true
    signal returnKeyPressed

    RowLayout {
        anchors.fill: parent
        TextField {
            id: textField
            Layout.fillWidth: true
            Layout.margins: 2
            placeholderText: control.placeholderText
            background: Rectangle {
                border.color: "#FFFFFF"
            }
            selectByMouse: true
            echoMode: control.eyeIsClose ? TextInput.Password : TextInput.Normal
            Keys.onPressed: {
                if (event.key == Qt.Key_Return) {
                    returnKeyPressed()
                }
            }
        }

        Image {
            Layout.preferredWidth: 15
            Layout.margins: 2
            Layout.rightMargin: 5
            source: control.imageSource
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    control.eyeIsClose = !control.eyeIsClose
                }
            }
        }
    }
}
