import ipih

from pih import A
from pih.tools import nn, ne

from MobileHelperService.service_api import MobileHelperService


def checker(telephone_number: str) -> bool:
    if ne(A.SRV.get_support_host_list(A.CT_SR.MOBILE_HELPER)):
        pih_cli_group_name: str = A.D.get(A.CT_ME_WH.GROUP.PIH_CLI) 
        pih_cli_administator_login: str | None = A.S.get(A.CT_S.PIH_CLI_ADMINISTRATOR_LOGIN)
        is_alisa: bool = telephone_number.endswith(A.CT_ME_WH.ALISA_SUFFIX)
        as_administrator: bool = telephone_number == pih_cli_group_name or (
            nn(pih_cli_administator_login) and telephone_number == A.D_TN.by_login(pih_cli_administator_login)
        )
        if MobileHelperService.as_administator():
            return as_administrator
        return not as_administrator
    return True


if __name__ == "__main__":
    MobileHelperService(checker=checker).start()
