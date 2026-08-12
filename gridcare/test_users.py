"""
test_users.py
Seed and verify test accounts for GridCare-Lite
"""

from login import add_user


def seed_test_users():
    print("Checking test users in database...")
    accounts = [
        ('admin1', 'password321', 'admin'),
        ('eng1', 'password246', 'engineer'),
        ('tech1', 'password642', 'technician'),
    ]

    new_count = 0   
    for username, password, role in accounts:
        if add_user(username, password, role):
            new_count += 1

    if new_count > 0:
        print(f"\nSuccessfully created {new_count} new test user(s)!")
    else:
        print("\nAll test users are already present in the database. You're ready to log in!")


if __name__ == '__main__':
    seed_test_users()