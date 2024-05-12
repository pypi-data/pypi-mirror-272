# moschitta_auth/basic_authenticator.py

import sqlite3
from typing import Optional

import bcrypt


class BasicAuthenticator:
    """Concrete authentication class implementing basic authentication."""

    def __init__(self, db_path: str = "../auth.db"):
        self.db_path = db_path
        # Create necessary tables if they do not exist
        self._create_user_table()
        self._create_session_table()

    def _create_user_table(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, hashed_password TEXT)"""
        )
        conn.commit()
        conn.close()

    def _create_session_table(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            """CREATE TABLE IF NOT EXISTS sessions
                     (session_id TEXT PRIMARY KEY, username TEXT)"""
        )
        conn.commit()
        conn.close()

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def register_user(self, username: str, password: str) -> None:
        hashed_password = self._hash_password(password)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, hashed_password) VALUES (?, ?)",
            (username, hashed_password),
        )
        conn.commit()
        conn.close()

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT hashed_password FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        if result:
            hashed_password = result[0]
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                return {"username": username}
        return None

    def authorize(self, user: dict, permissions: list) -> bool:
        # Placeholder implementation for authorization logic
        # Check if the user has the required permissions
        # For example, if the user has the 'admin' permission
        if "admin" in permissions:
            return True
        else:
            return False

    def logout(self, session_id: str) -> None:
        """Logout the user."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM sessions WHERE session_id = ?", (session_id,))
        conn.commit()
        conn.close()
