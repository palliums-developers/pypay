script {
use 0x7257c2417e4d1038e1817c8f283ace2e::ViolasBank;

fun main(account: &signer, userdata: vector<u8>) {
    ViolasBank::publish(account, userdata)
}
}
