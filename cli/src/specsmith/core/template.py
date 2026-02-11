"""SPEC.md template rendering."""

SPEC_TEMPLATE = """\
---
id: {id}
title: {title}
status: active
created: {date}
updated: {date}
priority: {priority}
tags: []
---

# {title}

## Overview

<!-- Describe what this spec accomplishes and why. -->

## Requirements

- <!-- When X happens, the system shall Y -->

## Phase 1: Setup [in-progress]

- [ ] Task 1 \u2190 current
- [ ] Task 2
- [ ] Task 3

## Phase 2: Implementation [pending]

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Phase 3: Testing & Polish [pending]

- [ ] Task 1
- [ ] Task 2

---

## Resume Context

> Spec just created. No work started yet.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
"""


def render_template(spec_id: str, title: str, date: str, priority: str = "medium") -> str:
    """Render a new SPEC.md from the template."""
    return SPEC_TEMPLATE.format(id=spec_id, title=title, date=date, priority=priority)
