import unittest
from HydrangeaApp.Models import Auth


class AuthTest(unittest.TestCase):

    def test_create_session(self):
        user = 'lucas'
        role = 'admin'
        auth = Auth.Auth()
        auth.create_session(user, role)
        data = auth.see_session()
        self.assertEqual(data['user'], user)
        self.assertEqual(data['role'], role)
        self.assertTrue(data['is_logged'])

    def test_logout(self):
        auth = Auth.Auth()
        auth.logout()
        data = auth.see_session()
        self.assertEqual(data['user'], '')
        self.assertEqual(data['role'], '')
        self.assertFalse(data['is_logged'])


if __name__ == '__main__':
    unittest.main()
