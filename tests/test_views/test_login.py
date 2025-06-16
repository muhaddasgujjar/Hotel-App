import unittest
from unittest.mock import patch, MagicMock
from app.views import login

class TestLogin(unittest.TestCase):

    @patch("app.views.login.check_credentials")
    @patch("app.views.login.open_dashboard")
    def test_login_success(self, mock_open_dashboard, mock_check_credentials):
        mock_check_credentials.return_value = True
        login.username_entry = MagicMock()
        login.password_entry = MagicMock()
        login.username_entry.get.return_value = "muhaddas"
        login.password_entry.get.return_value = "1234"

        login_window = MagicMock()
        login.attempt_login(login_window)

        mock_open_dashboard.assert_called_once()

    @patch("app.views.login.check_credentials")
    def test_login_failure(self, mock_check_credentials):
        mock_check_credentials.return_value = False
        login.username_entry = MagicMock()
        login.password_entry = MagicMock()
        login.username_entry.get.return_value = "wrong"
        login.password_entry.get.return_value = "user"

        login_window = MagicMock()
        with patch("tkinter.messagebox.showerror") as mock_msg:
            login.attempt_login(login_window)
            mock_msg.assert_called_once_with("Login Failed", "Invalid credentials.")

if __name__ == "__main__":
    unittest.main()
