script {
use 0x1::ViolasBank2;

fun main(account: &signer, tokenidx: u64, borrower: address, amount: u64, collateral_tokenidx: u64, data: vector<u8>) {
    ViolasBank2::liquidate_borrow_index(account, 0x1::Vector::empty(), 0x1::Vector::empty(), tokenidx, borrower, amount, collateral_tokenidx, data);
}
}

