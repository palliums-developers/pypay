from libra_client.canoser import RustEnum, Uint64
from libra_client.lbrtypes.account_config.resources import ParentVASP, ChildVASP

class AccountRole(RustEnum):
    _enums = [
        ("ParentVASP", ParentVASP),
        ("ChildVASP", ChildVASP),
        ("Unhosted", None),
        ("Unknown", None),
    ]
