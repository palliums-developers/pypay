import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Controls.Material 2.4
import QtQuick.Window 2.14
import Qt.labs.settings 1.0

import "controls"
import "pages"

ApplicationWindow {
    id: appWindow
    width: 1440
    height: 1024
    minimumWidth: 1024
    minimumHeight: 768
    visible: true
    title: qsTr("桌面支付钱包")

    property bool userIsLogin: false

    property double leftRecWidth1 : 200
    property double leftRecWidth2 : 300
    property double topRecHeight : 64
    property double fMargin: 8

    function showWalletPage() {
        walletMenuBtn.selected = true
        marketMenuBtn.selected = false
        walletStack.visible = true
        marketStack.visible = false
    }

    function showMarketPage() {
        walletMenuBtn.selected = false
        marketMenuBtn.selected = true
        walletStack.visible = false
        marketStack.visible = true
    }

    function showCreatePage(b) {
        createStack.visible = b
    }

    function showImportPage(b) {
        importStack.visible = b
    }

    Settings {
        id: appSettings
        fileName: "pypay.ini"
        property alias x: appWindow.x
        property alias y: appWindow.y
        property alias width: appWindow.width
        property alias height: appWindow.height
        property bool eyeIsOpen: false
        property bool walletIsCreate: false
        property bool mnemonicIsBackup: false
        property string password: ""    // TODO
    }

    Component.onCompleted: {
        if (appSettings.walletIsCreate) {   // TODO load
            payController.createWallet()
        }
    }

    //onClosing: {
    //    payController.shutdown()
    //}
    
    Rectangle {
        anchors.fill: parent
        color: "#F7F7F9"
        
        // Left rectangle
        Rectangle {
            id: leftRec
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            width: parent.width > 1920 ? leftRecWidth2 : leftRecWidth1
            color: "#501BA2"
            z: 999
            // logo
            Item {
                anchors.top: parent.top
                anchors.left: parent.left
                width: parent.width
                height: topRecHeight
                Image {
                    anchors.centerIn: parent
                    height: 0.7 * parent.height
                    source: "icons/logo.svg"
                    fillMode: Image.PreserveAspectFit
                }
            }

            MenuButton {
                id: walletMenuBtn
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.topMargin: 140
                height: 80
                icon.source: "icons/walleticon.svg"
                text: qsTr("钱包")
                selected: true
                onClicked: {
                    showWalletPage()
                }
            }
            MenuButton {
                id: marketMenuBtn
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: walletMenuBtn.bottom
                anchors.topMargin: 10
                height: 80
                icon.source: "icons/marketicon.svg"
                text: qsTr("市场")
                onClicked: {
                    showMarketPage()
                }
            }
        }

        // Top rectangle
        Rectangle {
            id: topRec
            anchors.top: parent.top
            anchors.left: leftRec.right
            anchors.right: parent.right
            height: topRecHeight
            color: "#FFFFFF"

            Row {
                spacing: 43
                anchors.right: parent.right
                anchors.rightMargin: 43
                anchors.verticalCenter: parent.verticalCenter
                // 我的
                ImageButton {
                    id: myButton
                    source: "./icons/me.svg"
                    height: 24
                    anchors.verticalCenter: parent.verticalCenter
                    fillMode: Image.PreserveAspectFit
                    visible: appSettings.walletIsCreate
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (appWindow.userIsLogin) {
                                myPopupPage.open()
                            }
                        }
                    }
                    Popup {
                        id: myPopupPage
                        x: parent.x
                        y: parent.y + parent.height + 5
                        width: 170
                        height: 220
                        padding: 0
                        MyPage {
                            id: myPage
                            anchors.fill: parent
                        }
                    }
                }

                // Import button
                MyButton {
                    id: importBtn
                    text: qsTr("导入")
                    anchors.verticalCenter: parent.verticalCenter
                    background.implicitWidth: 29
                    background.implicitHeight: 14
                    visible: !appSettings.walletIsCreate
                    onClicked: {
                        showImportPage(true)
                    }
                }

                // Create button
                MyButton {
                    id: createBtn
                    text: qsTr("创建")
                    anchors.verticalCenter: parent.verticalCenter
                    background.implicitWidth: 29
                    background.implicitHeight: 14
                    visible: !appSettings.walletIsCreate
                    onClicked: {
                        showCreatePage(true)
                    }
                }

                // Download button
                MyButton {
                    id: downloadBtn
                    text: qsTr("下载")
                    anchors.verticalCenter: parent.verticalCenter
                    background.implicitWidth: 29
                    background.implicitHeight: 14
                }

                // Transaction MyComboBox
                MyComboBox {
                    id: tsComboBox               
                    width: 150
                    anchors.verticalCenter: parent.verticalCenter
                }
            }
        }

        // Right bottom center area
        Rectangle {
            anchors.top: topRec.bottom
            anchors.topMargin: fMargin
            anchors.bottom: parent.bottom
            anchors.left: leftRec.right
            anchors.leftMargin: fMargin
            anchors.right: parent.right
            color: "#FFFFFF"

            // Wallet stack view
            StackView {
                id: walletStack
                anchors.fill: parent
                initialItem: walletPage
            }

            // Wallet page
            Component {
                id: walletPage
                WalletPage {
                    onBackupMnemonicClicked: {
                        createStack.clear()
                        createStack.push(backupMnemonic)
                        showCreatePage(true)
                    }
                    onReceiveClicked: {
                        walletStack.push(receivePage)
                    }
                    onSendClicked: {
                        walletStack.push(sendPage)
                    }
                }
            }

            // 收款
            Component {
                id: receivePage
                ReceivePage {
                    onBackArrowClicked: {
                        walletStack.pop()
                    }
                }
            }

            // 转账
            Component {
                id: sendPage
                SendPage {
                    onBackArrowClicked: {
                        walletStack.pop()
                    }
                    onSendClicked: {
                    }
                }
            }

            // Market stack view
            StackView {
                id: marketStack
                anchors.fill: parent
                initialItem: marketPage
                visible: false
            }

            // Market page
            Component {
                id: marketPage
                MarketPage {
                }
            }

            EnterPasswordPage {
                id: enterPasswordPage
                anchors.fill: parent
                visible: appSettings.walletIsCreate
                onEnterClicked: {
                    enterPasswordPage.visible = false
                }
            }

            // Create stack view
            StackView {
                id: createStack
                anchors.fill: parent
                initialItem: setPasswordPage
                visible: false
            }

            // Set password
            Component {
                id: setPasswordPage
                SetPasswordPage {
                    onBackArrowClicked: {
                        showCreatePage(false)
                    }
                    onCreateClicked: {
                        createStack.push(getMnemonic)
                    }
                }
            }

            // Get Mnemonic
            Component {
                id: getMnemonic
                GetMnemonicPage {
                    onBackArrowClicked: {
                        createStack.pop()
                    }
                    onBackupClicked: {
                        createStack.push(backupMnemonic)
                    }
                    onLaterBackupClicked: {
                        showCreatePage(false)
                        enterPasswordPage.visible = false
                        appWindow.userIsLogin = true
                    }
                }
            }

            // Backup Mnemonic
            Component {
                id: backupMnemonic
                BackupMnemonicPage {
                    onBackArrowClicked: {
                        createStack.pop()
                    }
                    onNextBtnClicked: {
                        createStack.push(confirmMnemonic)
                    }
                }
            }

            // Confirm Mnemonic
            Component {
                id: confirmMnemonic
                ConfirmMnemonicPage {
                    onBackArrowClicked: {
                        createStack.pop()
                    }
                    onCompleteBtnClicked: {
                        showCreatePage(false)
                        enterPasswordPage.visible = false
                        appWindow.userIsLogin = true
                    }
                }
            }

            // Import wallet stack view
            StackView {
                id: importStack
                anchors.fill: parent
                initialItem: importPage
                visible: false
            }

            // Import
            Component {
                id: importPage
                ImportPage {
                    onBackArrowClicked: {
                        showImportPage(false)
                    }
                    onImportClicked: {
                        showImportPage(false)
                        enterPasswordPage.visible = false
                        appWindow.userIsLogin = true
                    }
                }
            }
        }

        // 币种详情
        Popup {
            id: coinDetailPage
            x: parent.width - width
            y: topRec.height
            width: 436
            height: parent.height - topRec.height
            background: Rectangle {
                border.color: "lightsteelblue"
            }
            contentItem: Item {
                CoinDetailPage {
                    id: coinDetail
                    anchors.fill: parent
                    onGoBack: {
                        coinDetailPage.close()
                    }
                    onTransactionDetailOpened: {
                        coinDetail.visible = false
                        transactionDetail.visible = true
                    }
                }
                TransactionDetailPage {
                    id: transactionDetail
                    anchors.fill: parent
                    visible: false
                    onGoBack: {
                        coinDetail.visible = true
                        transactionDetail.visible = false
                    }
                }
            }
            onOpened: {
                coinDetail.visible = true
                transactionDetail.visible = false
            }
        }

        // 添加币种
        Popup {
            id: addCoinPage
            x: parent.width - width
            y: topRec.height
            width: 436
            height: parent.height - topRec.height
            background: Rectangle {
                border.color: "lightsteelblue"
            }
            contentItem: AddCoinPage {
                id: addCoin
                anchors.fill: parent
                onGoBack: {
                    addCoinPage.close()
                }
            }
        }

        // 地址薄
        Popup {
            id: addrBookPage
            x: parent.width - width
            y: topRec.height
            width: 436
            height: parent.height - topRec.height
            background: Rectangle {
                border.color: "lightsteelblue"
            }
            contentItem: Item {
                AddrBookPage {
                    id: addrBook
                    anchors.fill: parent
                    onGoBack: {
                        addrBookPage.close()
                    }
                    onAddAddrClicked: {
                        addrBook.visible = false
                        addAddrPage.visible = true
                        console.log("main add addr")
                    }
                }
                AddAddrPage {
                    id: addAddrPage
                    anchors.fill: parent
                    visible: false
                    onGoBack: {
                        addrBook.visible = true
                        addAddrPage.visible = false
                    }
                }
            }
            onOpened: {
                addrBook.visible = true
                addAddrPage.visible = false
            }
        }
    }
}
