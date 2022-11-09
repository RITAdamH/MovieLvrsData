from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple

COMMAND_FLAGS = {
    'help': (),
    'quit': (),
    'tool': ('v', 'a', 'e', 'd', 'r', 's'),
    'categ': ('v', 'c', 'e', 'd'),
    'req': ('g', 'r'),
    'stat': ('d', 'l', 'b')
}

DB_NAME = 'p32001_17'

HELP_STR = """Commands:
help                -  displays this menu
quit                -  exits the program
tool [v a e d r s]  -  manage your tools [view add edit delete return search]
categ [v c e d]     -  manage your categories [view create edit delete]
req [g r]           -  manage your borrow requests [given received]
stat [d l b]        -  show statistics [dashboard lent borrowed]"""

TOOL = Tuple[str, str, Optional[str], Optional[date],
             Optional[Decimal], bool, Optional[str]]
TOOL_REQUEST = Tuple[str, str, date, date, timedelta, str,
                     Optional[datetime], Optional[date], Optional[date]]
