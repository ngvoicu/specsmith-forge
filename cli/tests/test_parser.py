"""Tests for core/parser.py."""

from specsmith.core.parser import (
    get_resume_context,
    parse_frontmatter,
    parse_progress,
    update_frontmatter,
)

SAMPLE_SPEC = """\
---
id: test-spec
title: Test Spec
status: active
created: 2026-01-01
updated: 2026-01-01
priority: high
tags: []
---

# Test Spec

## Overview

A test spec.

## Phase 1: Setup [completed]

- [x] Task A
- [x] Task B

## Phase 2: Implementation [in-progress]

- [x] Task C
- [ ] Task D \u2190 current
- [ ] Task E

## Phase 3: Polish [pending]

- [ ] Task F
- [ ] Task G

---

## Resume Context

> Working on Task D. File is src/foo.ts.

## Decision Log

| Date | Decision | Rationale |
|------|----------|-----------|
"""


def test_parse_frontmatter():
    meta, body = parse_frontmatter(SAMPLE_SPEC)
    assert meta["id"] == "test-spec"
    assert meta["title"] == "Test Spec"
    assert meta["status"] == "active"
    assert "# Test Spec" in body


def test_parse_frontmatter_no_frontmatter():
    meta, body = parse_frontmatter("# Just markdown")
    assert meta == {}
    assert body == "# Just markdown"


def test_parse_progress():
    _, body = parse_frontmatter(SAMPLE_SPEC)
    progress = parse_progress(body)
    assert progress["total_done"] == 3
    assert progress["total_all"] == 7
    assert len(progress["phases"]) == 3

    p1 = progress["phases"][0]
    assert p1["name"] == "Setup"
    assert p1["status"] == "completed"
    assert p1["tasks_done"] == 2
    assert p1["tasks_total"] == 2

    p2 = progress["phases"][1]
    assert p2["name"] == "Implementation"
    assert p2["status"] == "in-progress"
    assert p2["current_task"] == "Task D"


def test_get_resume_context():
    _, body = parse_frontmatter(SAMPLE_SPEC)
    ctx = get_resume_context(body)
    assert "Working on Task D" in ctx
    assert "src/foo.ts" in ctx


def test_update_frontmatter():
    updated = update_frontmatter(SAMPLE_SPEC, {"status": "paused", "updated": "2026-02-01"})
    meta, body = parse_frontmatter(updated)
    assert meta["status"] == "paused"
    assert meta["updated"] == "2026-02-01"
    # Original fields preserved
    assert meta["id"] == "test-spec"
    assert meta["title"] == "Test Spec"
    # Body preserved
    assert "# Test Spec" in body
    assert "Task D" in body
