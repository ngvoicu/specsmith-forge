"""Title to spec-id conversion."""

import re


def slugify(title: str) -> str:
    """Convert a title to a URL-safe spec ID.

    >>> slugify("User Auth System")
    'user-auth-system'
    >>> slugify("  Fix Upload Bug!  ")
    'fix-upload-bug'
    """
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")
