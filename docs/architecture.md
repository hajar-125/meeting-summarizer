# Meeting Summarizer Architecture

## Overview

This document describes the architecture of the meeting summarizer application.

## Components

- **Audio Processing**: Extract audio from video and transcribe using Whisper
- **Processing**: Segment and summarize meeting content
- **Extraction**: Extract key information (decisions, tasks, owners)
- **Export**: Generate PDFs, send to Notion, or email summaries
