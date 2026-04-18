"""Pydantic models for meeting data structures."""

from pydantic import BaseModel


class MeetingSummary(BaseModel):
    """Main meeting summary model."""
    
    title: str
    date: str
    summary: str
