from app.models.database import initialize_database
from app.views.login import show_login

if __name__ == "__main__":
    initialize_database()
    show_login()
