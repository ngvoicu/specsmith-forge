"""Anthropic SDK wrapper."""

from anthropic import Anthropic


def create_client(api_key: str) -> Anthropic:
    """Create an Anthropic client."""
    return Anthropic(api_key=api_key)
