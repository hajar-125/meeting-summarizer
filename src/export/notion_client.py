"""Notion API client for exporting meeting data."""
import os
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv
from extraction.schemas import MeetingSummary

load_dotenv()

def export_to_notion(meeting: MeetingSummary) -> str:
    """
    Crée une page Notion structurée avec le compte-rendu de réunion.
    Retourne l'URL de la page créée.
    """
    token   = os.getenv("NOTION_TOKEN")
    page_id = os.getenv("NOTION_PAGE_ID")

    if not all([token, page_id]):
        raise ValueError("NOTION_TOKEN ou NOTION_PAGE_ID manquant dans .env")

    notion = Client(auth=token)
    date   = datetime.now().strftime("%d/%m/%Y à %H:%M")

    # ── Résumé propre sans markdown ──
    clean_summary = meeting.summary.replace("**", "").replace("*", "").replace("#", "").strip()

    # ── Blocs de la page ──
    children = [

        # Résumé exécutif
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📝 Résumé exécutif"}}]
            }
        },
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": clean_summary[:2000]}}]
            }
        },

        # Décisions
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "✅ Décisions prises"}}]
            }
        },
        *[
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": d}}]
                }
            }
            for d in meeting.decisions
        ],

        # Plan d'action
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🎯 Plan d'action"}}]
            }
        },
        {
            "object": "block",
            "type": "table",
            "table": {
                "table_width": 3,
                "has_column_header": True,
                "has_row_header": False,
                "children": [
                    # En-tête
                    {
                        "object": "block",
                        "type": "table_row",
                        "table_row": {
                            "cells": [
                                [{"type": "text", "text": {"content": "Tâche"}}],
                                [{"type": "text", "text": {"content": "Responsable"}}],
                                [{"type": "text", "text": {"content": "Deadline"}}],
                            ]
                        }
                    },
                    # Lignes tâches
                    *[
                        {
                            "object": "block",
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": t.title}}],
                                    [{"type": "text", "text": {"content": t.owner or "—"}}],
                                    [{"type": "text", "text": {"content": t.deadline or "—"}}],
                                ]
                            }
                        }
                        for t in meeting.tasks
                    ]
                ]
            }
        },

        # Prochain meeting
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "📅 Prochain meeting"}}]
            }
        },
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": meeting.next_meeting or "Non défini"}}],
                "icon": {"type": "emoji", "emoji": "📅"},
                "color": "green_background"
            }
        },
    ]

    # ── Créer la page ──
    print("[Notion] Création de la page...")
    response = notion.pages.create(
        parent={"page_id": page_id},
        properties={
            "title": {
                "title": [
                    {"type": "text", "text": {"content": f"Réunion du {date}"}}
                ]
            }
        },
        children=children
    )

    page_url = response.get("url", "")
    print(f"[Notion] Page créée : {page_url} ✓")
    return page_url