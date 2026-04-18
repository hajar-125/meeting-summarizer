"""Tests for transcriber module."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from audio.transcriber import transcribe

result = transcribe("tests/sample_meetings/test_meeting.mp3")
print("\n=== TRANSCRIPTION ===")
print(result)