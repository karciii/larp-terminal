import json
import time
from colorama import Fore
import tabulate
from animations import slow_print

class UserManager:
    def __init__(self):
        self.users = self.load_users()
        self.failed_attempts = {}
        self.locked_users = {}

    def load_users(self):
        try:
            with open('data/users.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            slow_print(Fore.RED + "ERROR: users.json not found!")
            return {}
        except json.JSONDecodeError:
            slow_print(Fore.RED + "ERROR: Error parsing users.json!")
            return {}
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: {str(e)}")
            return {}

    def save_users(self):
        try:
            with open('data/users.json', 'w') as f:
                json.dump(self.users, f)
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Failed to save users data - {str(e)}")

    def log_operation(self, username, operation_type, message_length):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "username": username,
            "operation": operation_type,
            "length": message_length
        }
        try:
            with open('data/crypto_logs.json', 'a') as log_file:
                log_file.write(json.dumps(log_entry) + "\n")
        except Exception as e:
            slow_print(Fore.RED + f"ERROR: Failed to write log - {str(e)}")

    def view_crypto_logs(self):
        try:
            with open('data/crypto_logs.json', 'r') as log_file:
                logs = [json.loads(log) for log in log_file.readlines()]
                if logs:
                    table = [
                        [log["timestamp"], log["username"], log["operation"], log["length"]]
                        for log in logs
                    ]
                    slow_print(Fore.GREEN + tabulate(
                        table, headers=["Timestamp", "Username", "Operation", "Message Length"], tablefmt="grid"
                    ))
                else:
                    slow_print(Fore.YELLOW + "No logs available.")
        except FileNotFoundError:
            slow_print(Fore.RED + "No logs file found.")
        except json.JSONDecodeError:
            slow_print(Fore.RED + "Error reading logs file.")

    def check_credentials(self, username, password):
        return username in self.users and self.users[username]['password'] == password

    def lock_user(self, username):
        self.locked_users[username] = time.time() + 60

    def is_user_locked(self, username):
        if username in self.locked_users:
            if time.time() < self.locked_users[username]:
                return True
            else:
                del self.locked_users[username]
        return False