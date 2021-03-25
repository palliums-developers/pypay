from enum import IntEnum
from violas_client.move_core_types.account_address import AccountAddress
from violas_client.lbrtypes.bytecode import gen_hex_hash
from violas_client.lbrtypes.bytecode import CodeType as LibraCodeType

class CodeType(IntEnum):
    EXCHANGE = 1000
    ADD_CURRENCY = 1001
    ADD_LIQUIDITY = 1002
    CHANGE_REWARDER = 1003
    INITIALIZE = 1004
    REMOVE_LIQUIDITY = 1005
    SET_NEXT_REWARDPOOL = 1006
    SET_POOL_ALLOC_POINT = 1007
    SWAP = 1008
    WITHDRAW_MINE_REWARD = 1009

bytecodes = {
    "exchange": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x0b\x01\x00\x12\x02\x12U\x03g\xba\x02\x04\xa1\x03h\x05\x89\x04\xc8\x05\x07\xd1\t\xc5\x0b\x08\x96\x15\x10\x06\xa6\x15(\n\xce\x15\xb2\x01\x0c\x80\x17\xf8%\r\xf8<:\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04\x00\x05\x00\x06\x00\x07\x00\x08\x00\t\x02\x00\x00\x05\x02\x00\x00\n\x01\x00\x00\x0b\x02\x00\x00\x0c\x01\x00\x00\r\x02\x00\x00\x0e\x01\x00\x00\x0f\x01\x00\x00\x10\x01\x00\x00\x11\x01\x00\x00\x12\x01\x00\x00\x13\x02\x00\x00\x14\x01\x00\x00\x15\x02\x00\x00\x16\x01\x00\x00\x17\x01\x00\x00\x18\x02\x00\x00\x19\x01\x00\x03\x19\x01\x00\x07\x07\x02\x00\x05)\x01\x01\x02\x02\x1a\x00\x01\x01\x01\x03\x1b\x02\x03\x01\x01\x03\x1c\x04\x00\x01\x01\x03\x1d\x02\x05\x01\x01\x03\x1e\x04\x06\x00\x03\x1f\x07\x00\x01\x01\x03 \x06\x00\x00\x08!\x08\t\x01\x01\x08"\n\x0b\x01\x01\x08#\x0c\x03\x01\x01\x08$\x00\r\x01\x01\x08%\x0c\x0e\x01\x01\x08&\x0f\x05\x01\x01\x08\'\x10\x00\x01\x01\x06(\x04\x02\x00\x05*\x11\x00\x01\x02\x05+\x04\x12\x01\x02\x04,\x00\x05\x00\x01-\t\x01\x01\x01\x00\x1b\x00\x03\x01\x01\x00\x1c\x04\x00\x01\x01\x00.\x13\x00\x02\x01\x01\x00/\x14\x00\x00\x000\x00\x02\x00\x001\x15\x00\x00\x002\x16\x00\x00\x003\x17\x00\x01\x01\x004\x14\x05\x00\x005\x00\x05\x01\x01\x006\x00\x18\x00\x007\x02\x05\x02\x01\x01\x008\x19\x14\x00\x009\x1a\x1b\x00\x00:\x00\x1c\x02\x01\x01\x00;\x1d\x1e\x00\x00<\x00\x14\x02\x01\x01\x00=\x1f \x00\x00>!"\x00\x00?\x16\x00\x00\x00@#\x05\x00\x00A$\x14\x02\x01\x01\x00B\x15\x00\x00\x00C\x02\x05\x00\x00D\x14\x05\x00\x00E%\x00\x02\x01\x01\x00F\x1c\x00\x00\x00G&\x00\x00\x00H%\x00\x00\x00I\'\x00\x00\x00J\x1c\x05\x00\x00K(\x00\x02\x01\x01\x00L)\x00\x00\x00M\x00\x00\x00\x00N\'\x00\x00\x00O*\x00\x01\x01\x00P\x04\x00\x00\x1c+\x01+\x00+\t\x01\r\x01\x02+\x13+\x13.!/(/\r1\x123\x0f4\x05+\x0b\x01\x0c<\x08<\r<\x1c.\x07<\x03+\x03.\x0cA\x08A\rA\x0cC\x08C\rC\n1\nA\n\x01\x104\nC\x00.\x1a+\x1a.\x12F\x0c1\x0716+6.\x12K\x1aN\x081\x0cR\x07R\n\x05\r\x05\x07\x05\x12T\n<6N\x00\x01\n\x02\x01\x05\x01\x01\x01\x06\x0c\x01\x03\x01\x08\x12\x05\x06\x08\x12\x05\x03\n\x02\n\x02\x02\x06\n\t\x00\x03\x01\x06\t\x00\x02\x07\n\t\x00\x03\x01\x07\t\x00\x02\x06\n\t\x00\x06\t\x00\x01\n\t\x00\x02\x01\x03\x01\x06\n\t\x00\x02\x07\n\t\x00\t\x00\x02\x07\x0b\x14\x01\t\x00\t\x00\x01\x0b\x14\x01\t\x00\x05\x06\x0c\x03\x03\x03\x03\x03\x03\x03\x03\x05\n\x02\x03\n\x02\x03\x03\x02\x06\x0c\x05\x02\x06\x0c\x03\x01\n\n\x02\x07\x03\x03\x03\x03\x03\x03\x03\x02\x03\x07\x08\x06\x01\x07\x08\x10\x02\x03\x03\x02\x03\x05\x02\x01\x08\x10\x03\x03\x03\x07\x08\t\x01\x07\x08\x08\x02\x03\x07\x08\x0f\x01\x07\x08\x0e\x02\x04\x04\n\x06\x0c\x03\x03\x03\x03\x03\x03\x03\x03\x03\x04\x06\x0c\x03\x03\x03\x03\x06\x0c\x04\x04\x03\x06\x0c\x03\x03\x06\x06\x0c\x05\x03\x03\n\x02\n\x02\x05\n\x02\x03\n\x02\x03\n\x02\x02\x05\x03\x01\t\x00\x04\n\x02\x07\x08\x07\x01\x03\r\x03\x03\x03\x03\x07\x08\x08\x03\x03\x07\x08\t\x01\x03\x01\x03\x03\x01\t\x01\x02\t\x00\t\x01\x06\x03\x03\x07\n\x08\x04\x07\x08\x0c\x01\x03\x01\x08\x04\x07\x08\x00\n\x02\x08\x01\x07\x08\x02\x03\x03\n\x02\x01\x08\x00\x01\x08\x01\x03\x07\x08\n\x01\x03\x08\x04\x04\x07\x08\x02\x04\x01\x03\x01\x01\x06\n\x02\n\n\x02\x01\x03\x01\x03\x01\x07\x08\x07\x07\x03\x03\x03\x01\x03\x07\x08\x0e\x07\x08\x0f\x17\x03\x03\x03\x03\x04\x04\x04\x04\x04\x03\x01\x01\x03\x01\x03\x01\x03\x03\x03\x03\x03\x01\x03\x05\x03\x03\x07\x08\x05\x07\x08\x05\x07\n\x08\x05\x01\x08\x05\x04\x03\x03\x01\x03\x05\x03\x03\x06\x08\x05\x06\n\x08\x05\x06\x08\x06\t\x03\x03\x07\x08\x08\x07\x08\t\x01\x03\x01\x03\x03\x08\x03\x03\x07\x08\x08\x07\x08\x08\x07\n\x08\x08\x01\x03\x01\x01\x08\x08\x05\x03\x03\x07\x08\x0e\x07\x08\x0e\x07\n\x08\x0e\x01\x08\x0e\t\x03\x03\n\x02\n\x02\x03\x03\x05\x07\x08\x0e\x07\x08\x0f\x07\n\x02\x08\x01\x07\x08\x02\x08\x03\x03\x03\n\x02\x01\x08\x03\x0f\x04\x01\x03\x03\x03\x03\x03\x06\x08\x04\x06\n\x08\x04\x03\x06\x08\x0c\x03\x03\x08\x10\x04\x05\x03\x01\x03\x01\x01\x13\x03\x03\n\x02\n\x02\x03\x03\x03\x07\x08\x08\x03\x03\x07\x08\t\x01\x03\x01\x01\x03\x07\x08\x0e\x07\x08\x0f\x03\x07\n\x02\x08\x01\x07\x08\x02\x08\x0b\x03\x03\n\x02\x01\x08\x0b\x03\x07\x08\x02\x01\x03\x06\x07\x08\x0c\x07\x08\n\x01\x03\x01\x03\x01\x08\x13\x0b\x03\x03\x03\x07\x08\x04\x07\n\x08\x04\x07\x08\n\x07\x08\x0c\x01\x03\x01\x03\x03\x04\x04\x04\x1b\x03\n\x03\x03\n\x02\n\x02\x03\x03\x03\x03\x03\x03\x02\x02\x07\x08\x08\x07\x08\x08\x03\x03\x03\x03\x07\x08\t\x01\x03\x01\x01\x01\x01\x03\x01\x02\x07\n\x02\x08\x01\x07\x08\x02\x08\r\x03\x03\n\x02\x01\x08\r\x0b\x03\x03\x03\x03\x07\x08\x04\x07\n\x08\x04\x03\x07\x08\x0c\x03\x03\x04\n\x03\x03\x03\x03\x07\x08\x04\x07\n\x08\x04\x07\x08\x06\x07\x08\x0c\x05\x07\x08\x10\x01\x06\x08\x11\x08\x03\x03\x07\x08\x0f\x05\x01\x03\x07\x08\x0e\x07\n\x08\x0e\x08Exchange\x03BCS\x04Diem\x0bDiemAccount\rDiemTimestamp\x05Event\x06Signer\x03VLS\x06Vector\tBurnEvent\tEventInfo\tMintEvent\x08PoolInfo\x0cPoolUserInfo\rPoolUserInfos\x14RegisteredCurrencies\x07Reserve\x08Reserves\x0bRewardAdmin\x0bRewardEvent\x0bRewardPools\tSwapEvent\x05Token\x06Tokens\x08UserInfo\x12WithdrawCapability\rcurrency_code\x10accepts_currency\x0cadd_currency\x07balance\x1bextract_withdraw_capability\x08pay_from\x1brestore_withdraw_capability\x06borrow\nborrow_mut\x08contains\x05empty\x08index_of\x06length\tpush_back\naddress_of\x0bEventHandle\nemit_event\x10new_event_handle\x0bnow_seconds\x08to_bytes\radd_liquidity\x0fadd_reward_pool\nadmin_addr\nburn_event\x0fchange_rewarder\x07deposit\x0eget_amount_out\x0bget_coin_id\rget_currencys\x15get_liquidity_balance\x12get_mint_liquidity\x19get_or_add_pool_user_info\x0fget_pair_indexs\x12get_pool_user_info\x0bget_reserve\x14get_reserve_internal\tget_token\ninitialize\x03min\x04mint\nmint_event\x0epending_reward\x05quote\x10remove_liquidity\x0creward_event\x0eset_fee_factor\x10set_next_rewards\x14set_pool_alloc_point\x04sqrt\x04swap\nswap_event\x0bupdate_pool\x17update_user_reward_info\x08withdraw\x14withdraw_mine_reward\x05coina\x10withdraw_amounta\x05coinb\x10withdraw_amountb\x0bburn_amount\x05etype\x04data\ttimestamp\x06events\x07factor1\x07factor2\x0fdeposit_amounta\x0fdeposit_amountb\x0bmint_amount\x02id\tlp_supply\x0balloc_point\x11acc_vls_per_share\x07pool_id\tuser_info\x0fpool_user_infos\x0ecurrency_codes\x16liquidity_total_supply\x08reserves\x04addr\rreward_amount\nstart_time\x08end_time\x10last_reward_time\x14total_reward_balance\x11reward_per_second\x11total_alloc_point\npool_infos\ninput_name\x0cinput_amount\x0boutput_name\routput_amount\x05index\x05value\x06tokens\x06amount\x0breward_debt\x03cap\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x10\x00\xca\x9a;\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x10rW\xc2A~M\x108\xe1\x81|\x8f(:\xce.\n\x02\x01\x00\x00\x02\x05Q\n\x02R\x03S\n\x02T\x03U\x03\x01\x02\x03V\x03W\n\x02X\x03\x02\x02\x03Y\x0b\x14\x01\x08\x01Z\x04[\x04\x03\x02\x05Q\n\x02\\\x03S\n\x02]\x03^\x03\x04\x02\x04_\x03`\x03a\x03b\x04\x05\x02\x02c\x03d\x08\x10\x06\x02\x01e\n\x08\x05\x07\x02\x01f\n\n\x02\x08\x02\x03g\x03Q\x08\x0eS\x08\x0e\t\x02\x01h\n\x08\x08\n\x02\x01i\x05\x0b\x02\x02c\x03j\x03\x0c\x02\x07k\x03l\x03m\x03n\x03o\x03p\x03q\n\x08\x04\r\x02\x05r\n\x02s\x03t\n\x02u\x03W\n\x02\x0e\x02\x02v\x03w\x03\x0f\x02\x01x\n\x08\x0e\x10\x02\x02y\x03z\x03\x11\x02\x01{\x08\x12\x13\x00\x01\x07\x00\x058\x00\x01\x11\x178\x01\x02\x14\x01\x01\x07,*\n\x00\x11\x0e\x11\x17!\x0c\x03\x0b\x03\x03\x0b\x0b\x00\x01\x06\x89\x13\x00\x00\x00\x00\x00\x00\'8\x02\x0c\x01\x11\x17*\x07\x0c\x02\n\x02\x10\x00\x0e\x018\x03\x03\x16\x05\x1b\x0b\x02\x01\x0b\x00\x01\x02\x0b\x02\x0f\x00\x0b\x018\x04\x11\x178\x01 \x03$\x05\'\x0b\x008\x05\x05)\x0b\x00\x01\x02\x15\x01\x07\x02\x06\x07\t\x0c\x0f\x11-J8\x06\x03\x03\x05\x068\x07\x0c\x0f\x05\x08\t\x0c\x0f\x0b\x0f\x0c\r\x0b\r\x03\x10\x0b\x00\x01\x06\xc4\x13\x00\x00\x00\x00\x00\x00\'\x11\x17*\t\x0c\x0c8\x08\x0c\x08\x0c\x07\n\x07\n\x08\x0b\x0c\x11$\x0c\t\n\t\x10\x01\x14\n\t\x10\x02\x10\x03\x14\n\t\x10\x04\x10\x03\x14\x0c\x0b\x0c\n\x0c\x10\x0b\x00\n\x07\n\x08\n\x01\n\x02\n\x03\n\x04\n\n\n\x0b\n\x108\t\x0c\x06\x0c\x05\x0c\x11\n\x11\n\t\x0f\x01\x15\n\n\n\x05\x16\n\t\x0f\x02\x0f\x03\x15\n\x0b\n\x06\x16\x0b\t\x0f\x04\x0f\x03\x15\x02\x16\x00\x01\x0c0%\x11\x17)\x0c\x0c\x07\x0b\x07\x03\x07\x06\xa1\x0f\x00\x00\x00\x00\x00\x00\'\x11\x17*\x0c\x0c\x06\n\x06\x0f\x05\x0c\x05\n\x001 /\n\x01\x16\x0c\x04\x06\xe8\x03\x00\x00\x00\x00\x00\x00\x0c\x03\x0b\x05\n\x04\n\x02\n\x032\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x048\n\n\x06\x10\x06\x14\n\x03\x16\x0b\x06\x0f\x06\x15\x02\x17\x00\x00\x00\x02\x07\x01\x02\x18\x00\x01\x022\x1b\x0b\x00\n\x01\x0b\x02\n\x03\n\x04\x12\x00\x0c\x05\x0e\x058\x0b\x0c\x06\x11\x11\x0c\n\x0b\x06\x0c\x0b\x06\x02\x00\x00\x00\x00\x00\x00\x00\x0b\x0b\x0b\n\x12\x01\x0c\x07\x11\x17*\x02\x0c\x08\x0b\x08\x0f\x07\x0b\x078\x0c\x02\x19\x01\x01\n5\x11\x0b\x00\x11\x0e\x11\x17!\x0c\x03\x0b\x03\x03\t\x06\x88\x13\x00\x00\x00\x00\x00\x00\'\x11\x17*\n\x0c\x02\n\x01\x0b\x02\x0f\x08\x15\x02\x1a\x00\x00\x06\x0c\x0b\x00\x11\x04\x0c\x02\x0e\x02\x11\x17\n\x01\x07\x02\x07\x028\r\x0b\x02\x11\x06\x02\x1b\x01\x01\x0269\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03\x05\x05\n\n\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\t\x05\x0c\t\x0c\t\x0b\t\x03\x0f\x05\x14\n\x02\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\n\x05\x16\t\x0c\n\x0b\n\x0c\x07\x0b\x07\x03\x1c\x06\xd2\x0f\x00\x00\x00\x00\x00\x00\'\x11\x17*\x02\x0c\x05\n\x005\n\x05\x10\t\x14\x18\x0c\x03\n\x03\n\x025\x18\x0c\x06\n\x015\x0b\x05\x10\n\x14\x18\n\x03\x16\x0c\x04\n\x06\n\x04\x1a4\x02\x1c\x01\x01\x077\x118\x02\x0c\x00\x11\x1d\x0c\x01\x0e\x01\x0e\x008\x0e\x0c\x03\x0c\x02\n\x02\x0c\x04\x0b\x04\x03\x0f\x06\x92\x13\x00\x00\x00\x00\x00\x00\'\n\x03\x02\x1d\x01\x01\x078\x07\x11\x17*\x07\x0c\x00\x0b\x00\x10\x00\x14\x02\x1e\x01\x02\x07\x0f9 8\x08\x0c\x03\x0c\x02\n\x021 /\n\x03\x16\x0c\x01\n\x00*\x0f\x0c\x07\n\x01\x0b\x07\x11%\x0c\x06\n\x06\x10\x03\x14\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x04\x0b\x04\x03\x1c\x0b\x06\x01\x06\x9c\x13\x00\x00\x00\x00\x00\x00\'\x0b\x06\x10\x03\x14\x02\x1f\x01\x00:\x81\x01\n\x04\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x03\x05\x05\n\n\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x0c\x11\x05\x0c\t\x0c\x11\x0b\x11\x03\x0f\x05\x14\n\x00\n\x01\x0c\x1a\x0c\x19\x05J\n\x00\n\x04\n\x05\x11+\x0c\n\n\n\n\x01%\x03\x1e\x05+\n\n\n\x03&\x0c\x12\x0b\x12\x03&\x06\xbe\x0f\x00\x00\x00\x00\x00\x00\'\n\x00\n\n\x0c\x18\x0c\x17\x05F\n\x01\n\x05\n\x04\x11+\x0c\x08\n\x08\n\x00%\x035\x05:\n\x08\n\x02&\x0c\x16\x05<\t\x0c\x16\x0b\x16\x0c\x14\x0b\x14\x03B\x06\xbf\x0f\x00\x00\x00\x00\x00\x00\'\n\x08\n\x01\x0c\x18\x0c\x17\x0b\x17\x0b\x18\x0c\x1a\x0c\x19\x0b\x19\x0b\x1a\x0c\t\x0c\x07\n\x075\x0c\x0b\n\t5\x0c\x0c\n\x065\x0c\x0f\n\x045\x0c\r\n\x055\x0c\x0e\n\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x03b\x05g\n\x07\n\t\x111\x0c\x1b\x05s\n\x0b\n\x0f\x18\n\r\x1a\n\x0c\n\x0f\x18\n\x0e\x1a\x11\'\x0c\x1b\x0b\x1b\x0c\x10\n\x10\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x1c\x0b\x1c\x03}\x06\xc0\x0f\x00\x00\x00\x00\x00\x00\'\n\x10\n\x07\n\t\x02 \x00\x00;3\x0b\x01\x0f\x0b\x0c\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x02\n\x06.8\x0f\x0c\x03\n\x02\n\x03#\x03\x0e\x05%\n\x06\n\x028\x10\x0c\x04\n\x04\x10\x0c\x14\n\x00!\x03\x19\x05\x1e\x0b\x06\x01\x0b\x04\x0f\r\x02\x0b\x04\x01\n\x02\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x02\x05\t\n\x06\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x10\x12\x058\x11\x0b\x06\n\x028\x10\x0c\x05\x0b\x05\x0f\r\x02!\x01\x01\x07=\x0f8\x008\x12\x0c\x01\x0c\x00\n\x00\n\x01#\x0c\x02\x0b\x02\x03\x0c\x06\xa6\x13\x00\x00\x00\x00\x00\x00\'\n\x00\n\x01\x02"\x00\x01\x06>0\n\x01+\x06\x0c\x06\x0b\x06\x10\x0b\x0c\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x02\n\x058\x0f\x0c\x03\n\x02\n\x03#\x03\x10\x05)\n\x05\n\x028\x13\x0c\x04\n\x04\x10\x0c\x14\n\x00!\x03\x1b\x05"\x0b\x05\x01\x08\x0b\x04\x10\r\x14\x02\x0b\x04\x01\n\x02\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x02\x05\x0b\x0b\x05\x01\t\x06\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x10\x02#\x01\x03\x07\t\x0c?18\x08\x0c\x01\x0c\x00\x11\x17*\t\x0c\x03\n\x00\n\x01\x0b\x03\x11$\x0c\x02\x11\x178\x14\x0c\x07\x11\x178\x15\x0c\x08\n\x07\n\x02\x10\x02\x10\x03\x14!\x03\x19\x05!\n\x08\n\x02\x10\x04\x10\x03\x14!\x0c\x06\x05#\t\x0c\x06\x0b\x06\x0c\x04\x0b\x04\x03+\x0b\x02\x01\x06\xb0\x13\x00\x00\x00\x00\x00\x00\'\x0b\x02\x10\x01\x14\n\x07\n\x08\x02$\x00\x01\x0c@P\n\x00\n\x01#\x0c\x08\x0b\x08\x03\n\x0b\x02\x01\x06\xba\x13\x00\x00\x00\x00\x00\x00\'\x0b\x02\x0f\x0e\x0c\x07\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x03\n\x07.8\x16\x0c\x04\n\x03\n\x04#\x03\x18\x05<\n\x07\n\x038\x17\x0c\x05\n\x05\x10\x02\x10\x0f\x14\n\x00!\x03$\x05,\n\x05\x10\x04\x10\x0f\x14\n\x01!\x0c\n\x05.\t\x0c\n\x0b\n\x031\x055\x0b\x07\x01\x0b\x05\x02\x0b\x05\x01\n\x03\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x03\x05\x13\n\x00\n\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00\x11\x16\n\x07\x06\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x0e\n\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x0e\x12\x088\x18\x0b\x07\n\x038\x17\x0c\x06\x0b\x06\x02%\x00\x00B/\x0b\x01\x0f\x10\x0c\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x02\n\x06.8\x19\x0c\x03\n\x02\n\x03#\x03\x0e\x05$\n\x06\n\x028\x1a\x0c\x04\n\x04\x10\x0f\x14\n\x00!\x03\x19\x05\x1d\x0b\x06\x01\x0b\x04\x02\x0b\x04\x01\n\x02\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x02\x05\t\n\x06\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x12\x0e8\x1b\x0b\x06\n\x028\x1a\x0c\x05\x0b\x05\x02&\x01\x00\x0e.\n\x00\x11\x0e\x11\x17!\x0c\x02\x0b\x02\x03\x0b\x0b\x00\x01\x06\x88\x13\x00\x00\x00\x00\x00\x00\'\n\x00\x11\x11\x11\x11\x11\x11\x06\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\x008\x1c\x12\x0c-\x0c\n\x008\x1d\x12\t-\t\n\x008\x1e\x12\x07-\x07\n\x00\n\x00\x11\x04\x12\x11-\x11\n\x00\n\x008\x1f2\r\'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x002\x10\'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x02-\x02\x0b\x00\n\x01\x12\n-\n\x02\'\x00\x00\x05\x0e\n\x00\n\x01#\x03\x05\x05\t\n\x004\x0c\x02\x05\x0c\n\x014\x0c\x02\x0b\x02\x02(\x00\x05\x02\x06\x0c\x0f\x11DI\n\x00\x11\x0e\x0c\x10\n\x10)\x0f \x03\x08\x05\x0c\n\x008 \x12\x0f-\x0f\n\x011 /\n\x02\x16\x0c\x0e\n\x10*\x0f\x0c\x12\n\x0e\x0b\x12\x11%\x0c\x11\n\x03\n\x04\n\x05\n\x06\n\x07\n\x08\n\t\x11\x1f\x0c\x0b\x0c\n\x0c\x0f\n\x11\x10\x03\x14\n\x0f\x16\n\x11\x0f\x03\x158\x02\x0c\x0c8!\x0c\r\x0b\x0c\n\n\x0b\r\n\x0b\n\x0f\x11)\n\x00\n\n8"\n\x00\n\x0b8#\x114\x0b\x00\n\x0e\x0b\x11\x10\x03\x14\x115\n\t\n\x0f\x16\n\n\n\x0b\x02)\x00\x01\x02E\x1b\x0b\x00\n\x01\x0b\x02\n\x03\n\x04\x12\x03\x0c\x08\x0e\x088$\x0c\x05\x11\x11\x0c\n\x0b\x05\x0c\x0b\x06\x01\x00\x00\x00\x00\x00\x00\x00\x0b\x0b\x0b\n\x12\x01\x0c\x06\x11\x17*\x02\x0c\x07\x0b\x07\x0f\x07\x0b\x068\x0c\x02*\x01\x02\x06\x0cG\x92\x01\x11\x17+\x0c\x0c\x0b\n\x0b\x10\x05\x0c\t\n\t8%\x0c\x04\x11\x11\x0c\x06\n\x06\n\x0b\x10\x11\x14$\x03\x12\x05\x16\n\x0b\x10\x11\x14\x0c\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x07\n\x06\n\x0b\x10\x12\x14$\x03\x1f\x05\x8c\x01\n\x0b\x10\x06\x14\x0c\r\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x03\n\x03\n\x04#\x03*\x05\x87\x012\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x01\n\t\n\x038&\x0c\x08\n\x03\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x03\n\x08\x10\x13\x14\x0c\x05\n\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03=\x05`\n\x0b\x10\x14\x14\x0c\n\n\x06\n\x0b\x10\x12\x14\x17\x0c\x0c\n\x0c5\n\n5\x18\n\x08\x10\x15\x145\x18\n\r5\x1a\x0c\x0f\n\x08\x10\x16\x14\n\x0f\x07\x00\x18\n\x055\x1a\x16\x0c\x01\x0b\x08\x10\x17\x14\n\x00\x11"\x0c\x0e\x0c\x02\n\x02 \x03k\x05l\x05%\n\x0b\x10\x18\x14\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x03s\x05u2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x01\n\x07\x0e\x0e\x10\x19\x145\n\x01\x18\x07\x00\x1a\x0e\x0e\x10\x1a\x145\x174\x16\x0c\x07\x05%\x0b\x0b\x01\x0b\t\x01\x05\x90\x01\x0b\x0b\x01\x0b\t\x01\n\x07\x02+\x00\x00H(\n\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03\x05\x05\n\n\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x06\x05\x0c\t\x0c\x06\x0b\x06\x03\x0f\x05\x14\n\x02\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x0c\x07\x05\x16\t\x0c\x07\x0b\x07\x0c\x04\x0b\x04\x03\x1c\x06\xc8\x0f\x00\x00\x00\x00\x00\x00\'\n\x005\n\x025\x18\n\x015\x1a4\x0c\x03\n\x03\x02,\x01\x07\x02\x06\x07\t\x0c\x0f\x11I\x97\x01\x11\x17*\t\x0c\x0e8\x08\x0c\n\x0c\t\n\t\n\n\x0b\x0e\x11$\x0c\x0b\n\x0b\x10\x01\x14\n\x0b\x10\x02\x10\x03\x14\n\x0b\x10\x04\x10\x03\x14\x0c\r\x0c\x0c\x0c\x16\n\x00\x11\x0e*\x0f\x0c\x15\n\t1 /\n\n\x16\x0c\x08\n\x08\x0b\x15\x11%\x0c\x14\n\x015\n\x0c5\x18\n\x165\x1a4\x0c\x04\n\x015\n\r5\x18\n\x165\x1a4\x0c\x05\n\x04\n\x02&\x03@\x05E\n\x05\n\x03&\x0c\x11\x05G\t\x0c\x11\x0b\x11\x0c\x0f\x0b\x0f\x03S\x0b\x14\x01\x0b\x0b\x01\x0b\x00\x01\x06\xce\x13\x00\x00\x00\x00\x00\x00\'\n\x16\n\x01\x17\n\x0b\x0f\x01\x15\n\x0c\n\x04\x17\n\x0b\x0f\x02\x0f\x03\x15\n\r\n\x05\x17\x0b\x0b\x0f\x04\x0f\x03\x15\n\x14\x10\x03\x14\n\x01&\x0c\x12\x0b\x12\x03u\x0b\x14\x01\x0b\x00\x01\x06\xcf\x13\x00\x00\x00\x00\x00\x00\'\n\x14\x10\x03\x14\n\x01\x17\n\x14\x0f\x03\x15\x114\n\x00\n\x08\x0b\x14\x10\x03\x14\x1158\x02\x0c\x068!\x0c\x07\x0b\x06\n\x04\x0b\x07\n\x05\n\x01\x11\x18\n\x00\x11\x0e\n\x048\'\x0b\x00\x11\x0e\n\x058(\x02-\x00\x01\x02J\x18\n\x00\n\x01\x12\x0b\x0c\x05\x0e\x058)\x0c\x02\x11\x11\x0c\x07\x0b\x02\x0c\x08\x06\x04\x00\x00\x00\x00\x00\x00\x00\x0b\x08\x0b\x07\x12\x01\x0c\x03\x11\x17*\x02\x0c\x04\x0b\x04\x0f\x07\x0b\x038\x0c\x02.\x01\x01\x02L\x15\x0b\x00\x11\x0e\x11\x17!\x0c\x04\x0b\x04\x03\t\x06\xaa\x0f\x00\x00\x00\x00\x00\x00\'\x11\x17*\x02\x0c\x03\n\x01\n\x03\x0f\t\x15\n\x02\x0b\x03\x0f\n\x15\x02/\x01\x02\n\x0cM;\x11\x17)\x0c\x0c\x06\x0b\x06\x03\t\x0b\x00\x01\x06\xa1\x0f\x00\x00\x00\x00\x00\x00\'\x11\x17*\n\x0c\x05\n\x00\x11\x0e\x0b\x05\x10\x08\x14!\x0c\x08\x0b\x08\x03\x19\x0b\x00\x01\x06\xa2\x0f\x00\x00\x00\x00\x00\x00\'\x114\x11\x17*\x0c\x0c\x04\n\x02\n\x04\x0f\x1b\x15\n\x03\n\x04\x0f\x11\x15\n\x02\n\x04\x0f\x12\x15\n\x01\n\x03\n\x02\x17\x1a\x06\x01\x00\x00\x00\x00\x00\x00\x00\x17\n\x04\x0f\x14\x15\n\x01\x0b\x04\x0f\x18\x15\x0b\x00\n\x018*\x020\x01\x02\n\x0cOT\x11\x17)\x0c\x0c\n\x0b\n\x03\t\x0b\x00\x01\x06\xa1\x0f\x00\x00\x00\x00\x00\x00\'\x11\x17*\n\x0c\x08\x0b\x00\x11\x0e\x0b\x08\x10\x08\x14!\x0c\x0c\x0b\x0c\x03\x17\x06\xa2\x0f\x00\x00\x00\x00\x00\x00\'\x11\x17*\x0c\x0c\t\n\t\x0f\x05\x0c\x07\n\x07.8%\x0c\x04\n\x07\x06\x00\x00\x00\x00\x00\x00\x00\x008+\x0c\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x03\n\x03\n\x04#\x03,\x05A\x0b\x06\x01\n\x07\n\x038+\x0c\x06\n\x06\x10\x17\x14\n\x01!\x039\x05<\x0b\x07\x01\x05A\n\x03\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x03\x05\'\n\x06\x10\x15\x14\x0c\x05\n\x02\x0b\x06\x0f\x15\x15\n\t\x10\x06\x14\n\x05\x17\n\x02\x16\x0b\t\x0f\x06\x15\x021\x00\x00P0\n\x005\n\x015\x18\x0c\x032\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x04\n\x032\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x03\r\x05&\n\x03\x0c\x04\n\x032\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a2\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x02\n\x02\n\x04#\x03\x1a\x05%\n\x02\x0c\x04\n\x03\n\x02\x1a\n\x02\x162\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a\x0c\x02\x05\x15\x05-\n\x032\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"\x03+\x05-2\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x04\n\x044\x022\x01\x05\x02\x07\t\x0c\x11Q\xf9\x018\x08\x0c\x0f\x0c\x0e8\x02\x0c\t8!\x0c\n\x0e\x048,\x0c\x10\x0e\x04\x06\x00\x00\x00\x00\x00\x00\x00\x008-\x14\x0e\x04\n\x10\x06\x01\x00\x00\x00\x00\x00\x00\x00\x178-\x14\x0c\x12\x0c\x11\n\x11\n\x12$\x03\x1b\x05#\n\x0f\n\x0e\x0c\x0f\x0c\x0e\x0b\n\x0b\t\x0c\n\x0c\t\n\x10\x06\x01\x00\x00\x00\x00\x00\x00\x00$\x03(\x05-\n\x0e\n\x0f"\x0c\x1c\x05/\t\x0c\x1c\x0b\x1c\x032\x058\n\x0e\n\x114!\x0c\x1d\x05:\t\x0c\x1d\x0b\x1d\x03=\x05C\n\x0f\n\x124!\x0c\x1e\x05E\t\x0c\x1e\x0b\x1e\x0c\x1a\x0b\x1a\x03M\x0b\x00\x01\x06\xd8\x13\x00\x00\x00\x00\x00\x00\'8.\x0c\x07\r\x07\n\x028/\x11\x17*\t\x0c\x19\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x0b\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x06\n\x0b\n\x10\x06\x01\x00\x00\x00\x00\x00\x00\x00\x17#\x03`\x05\xd4\x01\x0e\x07\n\x0b80\x14\x0c\x08\x0e\x04\n\x0b8-\x144\x0c\x0c\x0e\x04\n\x0b\x06\x01\x00\x00\x00\x00\x00\x00\x00\x168-\x144\x0c\r\n\x0c\n\r#\x03x\x05\xa4\x01\n\x0c\n\r\n\x19\x11$\x0c\x13\n\x13\x10\x02\x10\x03\x14\n\x13\x10\x04\x10\x03\x14\x0c\x17\x0c\x15\n\x08\n\x15\n\x17\x11\x1b\x0c\x06\r\x07\n\x068/\n\x13\x10\x02\x10\x03\x14\n\x08\x16\n\x13\x0f\x02\x0f\x03\x15\n\x13\x10\x04\x10\x03\x14\n\x06\x17\x0b\x13\x0f\x04\x0f\x03\x15\x05\xcf\x01\n\r\n\x0c\n\x19\x11$\x0c\x14\n\x14\x10\x04\x10\x03\x14\n\x14\x10\x02\x10\x03\x14\x0c\x18\x0c\x16\n\x08\n\x16\n\x18\x11\x1b\x0c\x06\r\x07\n\x068/\n\x14\x10\x02\x10\x03\x14\n\x06\x17\n\x14\x0f\x02\x0f\x03\x15\n\x14\x10\x04\x10\x03\x14\n\x08\x16\x0b\x14\x0f\x04\x0f\x03\x15\n\x0b\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x0b\x05Y\x0b\x19\x01\n\x06\n\x03&\x0c\x1f\x0b\x1f\x03\xe0\x01\x0b\x00\x01\x06\xd9\x13\x00\x00\x00\x00\x00\x00\'\x0b\t\n\x02\x0b\n\n\x06\x0b\x05\x113\n\x11\n\x12#\x03\xeb\x01\x05\xf2\x01\x0b\x00\n\x028"\n\x01\n\x068(\x05\xf8\x01\x0b\x00\n\x028#\n\x01\n\x068\'\x023\x00\x01\x02S\x1b\x0b\x00\n\x01\x0b\x02\n\x03\x0b\x04\x12\r\x0c\x08\x0e\x0881\x0c\x05\x11\x11\x0c\n\x0b\x05\x0c\x0b\x06\x03\x00\x00\x00\x00\x00\x00\x00\x0b\x0b\x0b\n\x12\x01\x0c\x06\x11\x17*\x02\x0c\x07\x0b\x07\x0f\x07\x0b\x068\x0c\x024\x00\x01\x0cUz\x11\x17*\x0c\x0c\x07\n\x07\x0f\x05\x0c\x05\n\x05.8%\x0c\x01\x11\x11\x0c\x03\n\x03\n\x07\x10\x11\x14$\x03\x13\x05\x17\n\x07\x10\x11\x14\x0c\x03\n\x03\n\x07\x10\x12\x14$\x03\x1e\x05u\n\x07\x10\x06\x14\x0c\t\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\n\x01#\x03)\x05n\n\x05\n\x008+\x0c\x04\n\x00\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x00\n\x04\x10\x13\x14\x0c\x02\n\x02\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03:\x05_\n\x07\x10\x14\x14\x0c\x06\n\x03\n\x07\x10\x12\x14\x17\x0c\x08\n\x085\n\x065\x18\n\x04\x10\x15\x145\x18\n\t5\x1a\x0c\n\n\x04\x10\x16\x14\n\n\x07\x00\x18\n\x025\x1a\x16\n\x04\x0f\x16\x15\n\x07\x10\x18\x14\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x03f\x05k2\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\x04\x0f\x16\x15\x05m\x0b\x04\x01\x05$\x0b\x05\x01\n\x03\x0b\x07\x0f\x12\x15\x05y\x0b\x07\x01\x0b\x05\x01\x025\x00\x04\x02\x06\x0c\x11V\x9e\x01\n\x00\x11\x0e\x0c\x0b\n\x0b)\x06 \x03\x08\x05\r\x0b\x0082\x12\x06-\x06\x05\x0f\x0b\x00\x01\n\x0b*\x06\x0c\t\x11\x17*\x0c\x0c\n\n\n\x0f\x05\x0c\x08\n\x08.8%\x0c\x04\n\x08\x06\x00\x00\x00\x00\x00\x00\x00\x008+\x0c\x07\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x03\n\x03\n\x04#\x03\'\x05<\x0b\x07\x01\n\x08\n\x038+\x0c\x07\n\x07\x10\x17\x14\n\x01!\x034\x057\x0b\x08\x01\x05<\n\x03\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x03\x05"\n\x01\x0b\t\x11 \x0c\x0c\n\x0c\x10\x19\x14\x0c\x05\n\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03I\x05\x7f\n\x055\n\x07\x10\x16\x14\x18\x07\x00\x1a\n\x0c\x10\x1a\x145\x174\x0c\x06\n\x06\x06\x00\x00\x00\x00\x00\x00\x00\x00$\x03]\x05|\n\x01\n\x06\x11-\n\n\x10\x18\x14\n\x06#\x03g\x05p\x0b\x0c\x01\x0b\x07\x01\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0b\n\x0f\x18\x15\x02\n\n\x10\x18\x14\n\x06\x17\x0b\n\x0f\x18\x15\n\x0b\n\x0683\x05~\x0b\n\x01\x05\x81\x01\x0b\n\x01\n\x02\n\x0c\x0f\x19\x15\n\x07\x10\x13\x14\n\x02\x16\n\x05\x17\n\x07\x0f\x13\x15\n\x0c\x10\x19\x145\x0b\x07\x10\x16\x14\x18\x07\x00\x1a4\x0b\x0c\x0f\x1a\x15\x026\x00\x01\x11W\x0b\x11\x17+\x11\x0c\x02\x0b\x02\x10\x1c\n\x00\n\x01\x07\x02\x07\x028\r\x027\x01\x05\x02\x06\x0c\x0f\x11X>\n\x00\x11\x0e\x0c\x04\n\x04)\x06\x0c\x05\x0b\x05\x03\x0c\x0b\x00\x01\x06\x0f\x10\x00\x00\x00\x00\x00\x00\'\n\x04*\x0f\x0c\x03\x0b\x03\x0f\x10\x0c\x08\x114\x06\x00\x00\x00\x00\x00\x00\x00\x00\x0c\x01\n\x08.8\x19\x0c\x02\n\x01\n\x02#\x03\x1e\x059\n\x08\n\x018\x1a\x0c\x07\n\x07\x10\x03\x14\x06\x00\x00\x00\x00\x00\x00\x00\x00!\x03)\x05,\x0b\x07\x01\x05\x19\n\x00\n\x07\x10\x0f\x14\x0b\x07\x10\x03\x14\x115\n\x01\x06\x01\x00\x00\x00\x00\x00\x00\x00\x16\x0c\x01\x05\x19\x0b\x08\x01\x0b\x00\x01\x02\x07\x00\x08\x00\x08\x01\x0e\x01\x08\x02\x0c\x06\x0c\x05\x02\x00\n\x00\x02\x01\x02\x02\x06\x00\x05\x00\x05\x01\t\x00\x0e\x00\x0f\x00\x0c\x01\x0c\x02\x04\x01\x0c\x04\x04\x02\x04\x03\x04\x00\x0c\x03\x10\x00\x10\x01\x0c\x00\x11\x00\x00',
    "add_currency": b"\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x06\x01\x00\x02\x03\x02\x06\x04\x08\x02\x05\n\x07\x07\x11\x16\x08'\x10\x00\x00\x00\x01\x00\x01\x01\x01\x00\x02\x01\x06\x0c\x00\x01\t\x00\x08Exchange\x0cadd_currency\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x00\x01\x03\x0b\x008\x00\x02",
    "add_liquidity": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x06\x01\x00\x02\x03\x02\x07\x04\t\x02\x05\x0b\r\x07\x18\x17\x08/\x10\x00\x00\x00\x01\x00\x01\x02\x01\x01\x00\x02\x05\x06\x0c\x03\x03\x03\x03\x00\x02\t\x00\t\x01\x08Exchange\radd_liquidity\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x01\x01\x00\x01\x07\x0b\x00\n\x01\n\x02\n\x03\n\x048\x00\x02',
    "change_rewarder": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x05\x01\x00\x02\x03\x02\x05\x05\x07\x05\x07\x0c\x19\x08%\x10\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\x05\x00\x08Exchange\x0fchange_rewarder\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x04\x0b\x00\n\x01\x11\x00\x02',
    "initialize": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x05\x01\x00\x02\x03\x02\x05\x05\x07\x05\x07\x0c\x14\x08 \x10\x00\x00\x00\x01\x00\x01\x00\x02\x06\x0c\x05\x00\x08Exchange\ninitialize\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x04\x0b\x00\n\x01\x11\x00\x02',
    "remove_liquidity": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x06\x01\x00\x02\x03\x02\x07\x04\t\x02\x05\x0b\x0c\x07\x17\x1a\x081\x10\x00\x00\x00\x01\x00\x01\x02\x01\x01\x00\x02\x04\x06\x0c\x03\x03\x03\x00\x02\t\x00\t\x01\x08Exchange\x10remove_liquidity\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x01\x01\x00\x01\x06\x0b\x00\n\x01\n\x02\n\x038\x00\x02',
    "set_next_rewardpool": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x05\x01\x00\x04\x03\x04\n\x05\x0e\x10\x07\x1e4\x08R\x10\x00\x00\x00\x01\x00\x02\x00\x01\x00\x01\x03\x02\x00\x00\x00\x01\x03\x04\x06\x0c\x03\x03\x03\x02\x06\x0c\x03\x02\x03\x03\rDiemTimestamp\x08Exchange\x0bnow_seconds\x10set_next_rewards\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x03\x04\x0c\x11\x00\x0c\x03\n\x03\x06\x80Q\x01\x00\x00\x00\x00\x00\x16\x0c\x02\x0b\x00\n\x01\n\x03\n\x02\x11\x01\x02',
    "set_pool_alloc_point": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x05\x01\x00\x02\x03\x02\x05\x05\x07\x06\x07\r\x1e\x08+\x10\x00\x00\x00\x01\x00\x01\x00\x03\x06\x0c\x03\x03\x00\x08Exchange\x14set_pool_alloc_point\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x05\x0b\x00\n\x01\n\x02\x11\x00\x02',
    "swap": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x06\x01\x00\x02\x03\x02\x07\x04\t\x02\x05\x0b\x10\x07\x1b\x0e\x08)\x10\x00\x00\x00\x01\x00\x01\x02\x01\x01\x00\x02\x06\x06\x0c\x05\x03\x03\n\x02\n\x02\x00\x02\t\x00\t\x01\x08Exchange\x04swap\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x01\x01\x00\x01\x08\x0b\x00\n\x01\n\x02\n\x03\x0b\x04\x0b\x058\x00\x02',
    "withdraw_mine_reward": b'\xa1\x1c\xeb\x0b\x01\x00\x00\x00\x05\x01\x00\x02\x03\x02\x05\x05\x07\x04\x07\x0b\x1e\x08)\x10\x00\x00\x00\x01\x00\x01\x00\x01\x06\x0c\x00\x08Exchange\x14withdraw_mine_reward\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x03\x0b\x00\x11\x00\x02',
}

type_to_code_map = {

    CodeType.EXCHANGE: bytecodes["exchange"],
    CodeType.ADD_CURRENCY: bytecodes["add_currency"],
    CodeType.ADD_LIQUIDITY: bytecodes["add_liquidity"],
    CodeType.CHANGE_REWARDER: bytecodes["change_rewarder"],
    CodeType.INITIALIZE: bytecodes["initialize"],
    CodeType.REMOVE_LIQUIDITY: bytecodes["remove_liquidity"],
    CodeType.SET_NEXT_REWARDPOOL: bytecodes["set_next_rewardpool"],
    CodeType.SET_POOL_ALLOC_POINT: bytecodes["set_pool_alloc_point"],
    CodeType.SWAP: bytecodes["swap"],
    CodeType.WITHDRAW_MINE_REWARD: bytecodes["withdraw_mine_reward"],
}

hash_to_type_map = { gen_hex_hash(v): k for k, v in type_to_code_map.items()}

default_module_address = bytes.fromhex("7257c2417e4d1038e1817c8f283ace2e")
current_module_address = default_module_address


def update_hash_to_type_map(module_address):
    global hash_to_type_map
    global current_module_address
    module_address = AccountAddress.normalize_to_bytes(module_address)
    hash_to_type_map = { gen_hex_hash(v.replace(default_module_address, module_address)): k for k, v in type_to_code_map.items()}
    current_module_address = module_address

def get_code_type(code_hash: bytes, module_address=None):
    if isinstance(code_hash, bytes):
        code_hash = code_hash.hex()
    m = hash_to_type_map
    if module_address:
        module_address = AccountAddress.normalize_to_bytes(module_address)
        m = {gen_hex_hash(v.replace(default_module_address, module_address)): k for k, v in
                            type_to_code_map.items()}
    type = m.get(code_hash)
    if type is not None:
        return type
    return LibraCodeType.UNKNOWN


def get_code(type, module_address=None):
    code = type_to_code_map.get(type)
    if code is not None:
        if module_address:
            module_address = AccountAddress.normalize_to_bytes(module_address)
            code = code.replace(default_module_address, module_address)
        return code

def gen_code_type():
    for index, key in enumerate(bytecodes.keys()):
        print(f"{key.upper()} = {index+1000}")

def gen_type_to_code_map():
    for key in bytecodes.keys():
        print(f'CodeType.{key.upper()}: bytecodes["{key}"],')


if __name__ == "__main__":
    gen_code_type()
    gen_type_to_code_map()