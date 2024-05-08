"""Entity definitions"""
import enum


class Entity(enum.StrEnum):
    """MSD Entities."""

    INCIDENT = 'incident'
    EMAIL = 'email'
