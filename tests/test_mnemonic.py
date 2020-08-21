from mnemonic import Mnemonic

# Initialize class instance
mnemo = Mnemonic("english")

# Generate word list given the strength
words = mnemo.generate(strength=256)
print(words)

# Given the word list and custom passphrase (empty in example), generate seed
seed = mnemo.to_seed(words, passphrase="")
print(seed)

# Given the word list, calculate original entropy
entropy = mnemo.to_entropy(words)
print(seed)
