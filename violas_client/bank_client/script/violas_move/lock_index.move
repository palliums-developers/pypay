script {
use 0x1::ViolasBank2;

fun main(account: &signer, tokenidx: u64, amount: u64, data: vector<u8>) {
    ViolasBank2::lock_index(account, 0x1::Vector::empty(), tokenidx, amount, data);
}
}