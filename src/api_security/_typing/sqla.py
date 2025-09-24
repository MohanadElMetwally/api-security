from typing import Annotated

from sqlalchemy import VARCHAR
from sqlalchemy.orm import mapped_column

bit0 = Annotated[bool, mapped_column(server_default="0")]
bit1 = Annotated[bool, mapped_column(server_default="1")]
vstr = Annotated[str, mapped_column(VARCHAR)]
vstr255  = Annotated[str, mapped_column(VARCHAR(255))]
