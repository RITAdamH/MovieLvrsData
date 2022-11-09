from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple

HELP_STR = """Commands:
help                -  displays this menu
quit                -  exits the program
tool [v a e d r s]  -  manage your tools [view add edit delete return search]
categ [v c e d]     -  manage your categories [view create edit delete]
req [g r]           -  manage your borrow requests [given received]
stat [d l b]        -  show statistics [dashboard lent borrowed]"""

Tool = Tuple[str, str, Optional[str], Optional[date],
             Optional[Decimal], bool, Optional[str]]
Tool_Request = Tuple[str, str, date, date, timedelta, str,
                     Optional[datetime], Optional[date], Optional[date]]
