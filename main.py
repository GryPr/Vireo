from utilities import startup


def main() -> None:
    startup.run_sanity_checks()
    bot = startup.create_bot()
    startup.load_extensions(bot, 'cogs')
    startup.run_bot(bot)


if __name__ == "__main__":
    main()
