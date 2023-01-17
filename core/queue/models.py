from pydantic import BaseModel


class Event(BaseModel):
    batch_id: int
    push_id: int
