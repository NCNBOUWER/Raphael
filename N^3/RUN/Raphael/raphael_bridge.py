#!/usr/bin/env python3
"""Controlled placeholder bridge for future private Raphael integration.

This module intentionally contains no private Raphael equations. It supplies stable
interfaces for later mapping/crosswalk work without affecting the standalone TPW
proof package.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Literal

ProofRelation = Literal[
    "identity",
    "direct_proof",
    "derived_support",
    "computational_check",
    "structural_correspondence",
    "analogy",
    "hypothesis",
    "blocked",
]

@dataclass(frozen=True)
class RaphaelLink:
    private_id: str
    public_label: str
    relation: ProofRelation
    status: str
    notes: str = ""


def classify_link(link: RaphaelLink) -> str:
    if link.relation in {"identity", "direct_proof", "derived_support", "computational_check"}:
        return "mathematical_support"
    if link.relation in {"structural_correspondence", "analogy"}:
        return "correspondence_only"
    if link.relation == "hypothesis":
        return "audit_pending"
    return "blocked"
