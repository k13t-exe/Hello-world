"""Functional and access-control tests for recursive JSON search."""

import unittest

try:  # Support invocation both from this directory and from the repository root.
    from .recursive_json_search import json_search
    from .test_data import data, key1
except ImportError:  # pragma: no cover - used by ``python -m unittest`` in unittest/
    from recursive_json_search import json_search
    from test_data import data, key1


class json_search_test(unittest.TestCase):
    """Check recursive search results and policy enforcement."""

    def test_search_found(self):
        """Find a requested key nested inside dictionaries and lists."""
        self.assertEqual(
            json_search(key1, data, role="viewer"),
            ["Network Device 10.10.20.82 Is Unreachable From Controller"],
        )

    def test_search_not_found(self):
        """Return an empty list when the requested key does not exist."""
        self.assertEqual(json_search("missing", data, role="viewer"), [])

    def test_is_a_list(self):
        """Return results as a list and retain every matching nested value."""
        sample = {"item": [
            {"target": 1},
            [{"target": 2}, {"other": {"target": 3}}],
        ]}
        result = json_search("target", sample, role="admin")
        self.assertIsInstance(result, list)
        self.assertEqual(result, [1, 2, 3])

    def test_api_key_admin_allowed(self):
        """Allow administrators to retrieve the protected API key."""
        self.assertEqual(
            json_search("apiKey", data, role="admin"), ["SNMP-COMMUNITY-STRING-7f3a9c"]
        )

    def test_api_key_operator_denied(self):
        """Deny operators access to the administrator-only API key."""
        self.assertEqual(json_search("apiKey", data, role="operator"), [])

    def test_management_ip_operator_allowed(self):
        """Allow operators to read management IP addresses."""
        self.assertEqual(json_search("managementIpAddress", data, role="operator"), ["10.10.20.21"])

    def test_management_ip_viewer_denied(self):
        """Deny viewers access to management IP addresses."""
        self.assertEqual(json_search("managementIpAddress", data, role="viewer"), [])

    def test_missing_or_unknown_role_denied(self):
        """Fail closed when the caller supplies no recognized role."""
        self.assertEqual(json_search(key1, data), [])
        self.assertEqual(json_search(key1, data, role="guest"), [])


if __name__ == "__main__":
    unittest.main()
