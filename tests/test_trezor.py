# https://trezor.io/
# https://pypi.org/project/trezor/
# https://github.com/trezor/trezor-firmware/tree/master/python


# pip install trezor

from trezorlib.client import get_default_client
from trezorlib.tools import parse_path
from trezorlib import btc

def test_get_bitcoin_address():
    # Use first connected device
    client = get_default_client()

    # Print out Trezor's features and settings
    print(client.features)

    # Get the first address of first BIP44 account
    # (should be the same address as shown in wallet.trezor.io)
    bip32_path = parse_path("44'/0'/0'/0/0")
    address = btc.get_address(client, "Bitcoin", bip32_path, True)
    print("Bitcoin address:", address)

def test_generate_entropy(strength, internal_entropy, external_entropy):
    '''
    strength - length of produced seed. One of 128, 192, 256
    random - binary stream of random data from external HRNG
    '''
    if strength not in (128, 192, 256):
        raise ValueError("Invalid strength")

    if not internal_entropy:
        raise ValueError("Internal entropy is not provided")

    if len(internal_entropy) < 32:
        raise ValueError("Internal entropy too short")

    if not external_entropy:
        raise ValueError("External entropy is not provided")

    if len(external_entropy) < 32:
        raise ValueError("External entropy too short")

    entropy = hashlib.sha256(internal_entropy + external_entropy).digest()
    entropy_stripped = entropy[:strength // 8]

    if len(entropy_stripped) * 8 != strength:
        raise ValueError("Entropy length mismatch")

    return entropy_stripped

def test_mnemonic_check():
    comp = bytes.fromhex(input("Please enter computer-generated entropy (in hex): ").strip())
    trzr = bytes.fromhex(input("Please enter Trezor-generated entropy (in hex): ").strip())
    word_count = int(input("How many words your mnemonic has? "))

    strength = word_count * 32 // 3

    entropy = generate_entropy(strength, trzr, comp)

    words = mnemonic.Mnemonic('english').to_mnemonic(entropy)
    if not mnemonic.Mnemonic('english').check(words):
        print("Mnemonic is invalid")
        return

    if len(words.split(' ')) != word_count:
        print("Mnemonic length mismatch!")
        return

    print("Generated mnemonic is:", words)


if __name__ == "__main__":
    get_bitcoin_address()
    mnemonic_check()
