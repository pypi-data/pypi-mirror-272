import typer

app = typer.Typer()

existing_usernames = ["rick", "morty"]


def create_user(username: str):
    if username in existing_usernames:
        print("The user already exists")
    else:
        existing_usernames.append(username)
        print(f"User created: {username}")


def send_notification(username: str):
    if username not in existing_usernames:
        print("User not found")
    else:
        print(f"Notification sent for user: {username}")


def main():
    while True:
        command = input("Enter command (create, notify, exit): ").strip()
        if command == "exit":
            print("Exiting...")
            break
        elif command == "create":  # noqa: RET508
            username = input("Enter username to create: ").strip()
            create_user(username)
        elif command == "notify":
            username = input("Enter username to notify: ").strip()
            send_notification(username)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
