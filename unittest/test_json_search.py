import unittest
import display_color
import copy
from recursive_json_search import *
from test_data import *
from policy import *

def_usr = "viewer"
sen_f_field = "connectedDevice"
sen_fields = ["apiKey", "managementIpAddress"]
avl_roles = ["admin", "operator", "viewer"]
secret = "SNMP-COMMUNITY-STRING-7f3a9c"

class json_search_test(unittest.TestCase):
    '''test module to test search function in `recursive_json_search.py`'''
    def test_search_found(self):
        '''--> key should be found, return list should not be empty'''
        self.assertTrue([] != json_search(key1, data, def_usr))

    def test_search_not_found(self):
        '''--> key should not be found, should return an empty list'''
        self.assertTrue([] == json_search(key2, data, def_usr))

    def test_is_a_list(self):
        '''--> should return a list'''
        self.assertIsInstance(json_search(key1, data, def_usr), list)

    def test_wrong_role_cannot_read_secret(self):
        '''*** Testcase 1: viewer can not read `apiKey` !!!'''
        result = json_search("apiKey", data, role="viewer")
        self.assertEqual([], result)

    def test_unavailable_roles_deny_by_default(self):
        '''*** Testcase 2: invalid role !!!'''
        result = json_search("managementIpAddress", data, role="hacker")
        self.assertTrue([] == result)

    def test_admin_is_ALL_MIGHTY(self):
        '''*** Testcase 3: admin knows everything !!!'''
        all_mighty = True
        for field in POLICY:
            if not json_search(field, data, role="admin"):
                all_mighty = False
                break
        self.assertTrue(all_mighty)

    def test_never_show_sensitive_unallowed_fields(self):
        '''*** Testcase 4: sensitive things never leak if not allowed !!!'''
        res = True
        for r in avl_roles:
            ans = json_search(sen_f_field, data, r) 
            if ans in sen_fields or not ans:
                res = False
                break
        self.assertTrue(res)

    def test_unrevealed_key(self):
        '''*** Testcase 5: something even admin does not know !!!'''
        self.assertEqual([], json_search("k13t_search_history", data, "admin"))

    def test_input_data_not_modified(self):
        '''*** Testcase 6: you can only CRY (write) !!!'''
        p0 = copy.deepcopy(data)
        for role in avl_roles + ["hacker", None]:
            json_search("connectedDevice", data, role)
            json_search("apiKey", data, role)
        self.assertTrue(p0 == data)

    def test_isolated_querries(self):
        '''*** Testcase 7: focus on your own tasks'''
        p0 = json_search("apiKey", data, "admin")
        self.assertEqual([], json_search("apiKey", data, "viewer"))
        self.assertNotIn(secret, str(json_search("connectedDevice", data, "viewer")))
        p1 = json_search("issueSummary", data, "viewer")
        p2 = json_search("issueSummary", data, "viewer")
        self.assertEqual(p1, p2)

if __name__ == '__main__':
    unittest.main()
