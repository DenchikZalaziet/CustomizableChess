from menu import Menu


def main() -> None:
    app = Menu()
    while True:
        try:
            app.check_mode()
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
