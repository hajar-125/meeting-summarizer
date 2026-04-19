"""Pydantic models for meeting data structures."""

from pydantic import BaseModel
from typing import List, Optional

class Task(BaseModel):
    title: str
    owner: Optional[str] = None
    deadline: Optional[str] = None

class MeetingSummary(BaseModel):
    summary: str
    decisions: List[str]
    tasks: List[Task]
    next_meeting: Optional[str] = None