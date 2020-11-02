import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: control
    width: 316
    height: 24
    border.color: startTextField.activeFocus || endTextField.activeFocus ? "#FD6565" : "#979797"

    property string startPlaceholderText: "Start time"
    property string endPlaceholderText: "End time"
    property alias startText: startTextField.text
    property alias endText: endTextField.text

    RowLayout {
        Layout.margins: 2
        anchors.fill: parent
        TextInput {
            id: startTextField
            placeholderText: control.startPlaceholderText
            background: Rectangle {
                border.color: "#FFFFFF"
            }
            selectByMouse: true
            echoMode: TextInput.Normal
        }

        Text {
            text: "---"
        }

        TextInput {
            id: endTextField
            placeholderText: control.endPlaceholderText
            background: Rectangle {
                border.color: "#FFFFFF"
            }
            selectByMouse: true
            echoMode: TextInput.Normal
        }
    }
}
