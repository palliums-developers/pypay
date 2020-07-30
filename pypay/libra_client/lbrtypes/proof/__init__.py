from libra_client.canoser import Struct
from libra_client.crypto.hash import HashValue, SparseMerkleInternalHasher, TransactionAccumulatorHasher, EventAccumulatorHasher

class MerkleTreeInternalNode(Struct):
    _fields = [
        ("left_child", HashValue),
        ("right_child", HashValue),
    ]

class SparseMerkleInternalNode(MerkleTreeInternalNode):
    hasher = SparseMerkleInternalHasher

class TransactionAccumulatorInternalNode(MerkleTreeInternalNode):
    hasher = TransactionAccumulatorHasher

class EventAccumulatorInternalNode(MerkleTreeInternalNode):
    hasher = EventAccumulatorHasher

class SparseMerkleLeafNode(Struct):
    _fields = [
        ("key", HashValue),
        ("value_hash", HashValue),
    ]
