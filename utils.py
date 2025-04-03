# CLI stuff
def ask(prompt: str, predicate: callable) -> str:
    while True:
        try:
            value = input(prompt)
            if predicate(value):
                return value

        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            exit()

        except ValueError:
            pass

ask_range = lambda prompt, start, end: int(ask(prompt, lambda x: start <= int(x) <= end))
ask_in = lambda prompt, values: ask(prompt, lambda x: x in map(str, values))
