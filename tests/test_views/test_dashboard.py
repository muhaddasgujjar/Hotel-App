import unittest
from unittest.mock import patch, MagicMock
from app.views import dashboard

class TestDashboard(unittest.TestCase):

    @patch("app.views.dashboard.get_connection")
    def test_save_room_inserts_room(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        dashboard.room_num_entry = MagicMock()
        dashboard.room_type_entry = MagicMock()
        dashboard.room_num_entry.get.return_value = "101"
        dashboard.room_type_entry.get.return_value = "Single"

        dashboard.load_rooms = MagicMock()
        dashboard.load_available_rooms = MagicMock()

        dashboard.save_room()

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

    @patch("app.views.dashboard.get_connection")
    def test_save_employee_inserts_employee(self, mock_get_connection):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        dashboard.emp_name = MagicMock()
        dashboard.emp_role = MagicMock()
        dashboard.emp_name.get.return_value = "Ali"
        dashboard.emp_role.get.return_value = "Manager"

        dashboard.load_employees = MagicMock()

        dashboard.save_employee()

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
