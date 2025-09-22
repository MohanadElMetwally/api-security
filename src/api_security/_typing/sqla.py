from typing import Annotated

from sqlalchemy.orm import mapped_column

bit0 = Annotated[bool, mapped_column(server_default="0")]
bit1 = Annotated[bool, mapped_column(server_default="1")]
