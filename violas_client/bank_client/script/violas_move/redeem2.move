script {
use 0x1::ViolasBank;

fun main<Token>(account: &signer, amount: u64, data: vector<u8>) {
    if(ViolasBank::is_published(account) == false) {
	ViolasBank::publish(account, x"00");
    };
    ViolasBank::redeem<Token>(account, amount, data);
    ViolasBank::exit_bank<Token>(account, amount);
}
}
