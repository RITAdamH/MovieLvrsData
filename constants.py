from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple

Tool = Tuple[str, str, Optional[str], Optional[date],
             Optional[Decimal], bool, Optional[str]]
Tool_Request = Tuple[str, str, date, date, timedelta, str,
                     Optional[datetime], Optional[date], Optional[date]]
