"""
test_users.py
Seed test accounts for GridCare-Lite
"""

from login import add_user


def seed_test_users():
    print("Creating test users...")
    add_user('admin1', 'password321', 'admin')
    add_user('eng1', 'password246', 'engineer')
    add_user('tech1', 'password642', 'technician')
    print("Test users created successfully!")


if __name__ == '__main__':
    seed_test_users()
