from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    """Test the Django admin functionality."""

    def setUp(self):
        """Set up the test case."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password',
            name='Admin User'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='password',
            name='Test User'
        )

    def test_users_list(self):
        """Test that the users list is on page."""
        response = self.client.get(reverse('admin:core_user_changelist'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser@example.com')
        self.assertContains(response, 'Test User')  # Ensure the test user is listed

    def test_admin_login(self):
        """Test that the admin user can log in."""
        self.client.logout()
        response = self.client.login(username='admin@example.com', password='password')
        self.assertTrue(response)

    def test_admin_site_access(self):
        """Test that the admin site is accessible."""
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Django administration')

    def test_user_list(self):
        """Test that the user list is accessible in the admin."""
        response = self.client.get(reverse('admin:core_user_changelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Users')

    def test_create_user(self):
        """Test creating a new user through the admin."""
        response = self.client.post(
            reverse('admin:core_user_add'),
            {
                'email': 'newuser@example.com',
                'password1': 'StrongPass123!',  # Use a stronger password
                'password2': 'StrongPass123!',
                'name': 'New User',
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        new_user = get_user_model().objects.get(email='newuser@example.com')
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.name, 'New User')

    def test_user_change(self):
        """Test changing a user's details through the admin."""
        response = self.client.post(
            reverse('admin:core_user_change', args=[self.user.id]),
            {
                'email': 'newupdateduser@example.com',
                'name': 'New User updated',
                'is_active': 'on',
                'is_staff': 'on',
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        # Refresh the user from the database
        self.user.refresh_from_db()
        # Now check the updated values
        self.assertEqual(self.user.email, 'newupdateduser@example.com')
        self.assertEqual(self.user.name, 'New User updated')