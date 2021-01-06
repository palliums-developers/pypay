from libra_client.canoser import RustEnum, Uint64, Struct

from libra_client.lbrtypes.account_config.resources import ParentVASP, ChildVASP
from .dual_attestation import CredentialResource
from .designated_dealer import DesignatedDealer
from .preburn_balance import PreburnResource

class ParentVASPRole(Struct):
    _fields = [
        ("vasp", ParentVASP),
        ("credential", CredentialResource)
    ]

class DesignatedDealerRole(Struct):
    _fields = [
        ("dd_credential", CredentialResource),
        ("preburn_balances", {str, PreburnResource}),
        ("designated_dealer", DesignatedDealer),
    ]

class AccountRole(RustEnum):
    _enums = [
        ("ParentVASP", ParentVASPRole),
        ("ChildVASP", ChildVASP),
        ("DesignatedDealer", DesignatedDealerRole),
        ("Unknown", None),
    ]

