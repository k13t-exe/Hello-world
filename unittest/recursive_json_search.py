"""Read-only recursive search for values in JSON-like Python objects."""

try:  # Support both ``python -m unittest`` from unittest/ and package imports.
    from .policy import POLICY
except ImportError:  # pragma: no cover - exercised by direct module invocation
    from policy import POLICY


_KNOWN_ROLES = {allowed_role for roles in POLICY.values() for allowed_role in roles}


def json_search(key, input_object, role=None):
    """Return all values under *key* that *role* is allowed to read.

    Dicts and lists are traversed recursively, preserving their natural order.
    Missing, empty, and unknown roles fail closed. Keys without an explicit
    policy are readable by any role named in the policy.
    """
    if not isinstance(role, str) or role not in _KNOWN_ROLES:
        return []

    allowed_roles = POLICY.get(key)
    if allowed_roles is not None and role not in allowed_roles:
        return []

    matches = []

    def visit(value):
        if isinstance(value, dict):
            for current_key, current_value in value.items():
                if current_key == key:
                    matches.append(current_value)
                visit(current_value)
        elif isinstance(value, list):
            for item in value:
                visit(item)

    visit(input_object)
    return matches
