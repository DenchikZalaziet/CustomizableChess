from menu import Menu


def main() -> None:
    app = Menu()
    while True:
        app.check_mode()


if __name__ == "__main__":
    main()
