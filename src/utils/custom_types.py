from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Annotated, Any
from uuid import uuid4

from sqlalchemy import UUID, DateTime, Integer, text, Sequence
from sqlalchemy.orm import mapped_column

async_func = Callable[..., Awaitable[Any]]

id_seq = Sequence('struct_adm_id_seq')

integer_pk = Annotated[int, mapped_column(Integer, primary_key=True, server_default=id_seq.next_value())]
uuid_pk = Annotated[uuid4, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)]

dt_now_utc_sql = text("TIMEZONE('utc', now())")
created_at = Annotated[datetime, mapped_column(DateTime, server_default=dt_now_utc_sql)]
updated_at = Annotated[datetime, mapped_column(
    DateTime,
    server_default=dt_now_utc_sql,
    onupdate=dt_now_utc_sql,
)]
