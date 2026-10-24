from typing import Optional

from pydantic import BaseModel, Field

class ProcessRequest(BaseModel):
    file_id: Optional[str] = Field(default=None)
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0
