import sys


def usage():
    print("Usage: string_art [options] <input file>")
    print("Options:")
    print("  --help           prints this help message.")
    print("  --full-thread    gives a result that can require multiple threads but is more accurate.")


class Config:
    def __init__(self, input_file, full_thread):
        self.input_file = input_file
        self.full_thread = full_thread

    @classmethod
    def create(cls, args):
        if len(args) < 2:
            raise ValueError("Not enough arguments")

        input_file = None
        full_thread = False

        for i, arg in enumerate(args):
            if arg == "--help":
                usage()
                sys.exit(0)
            elif arg == "--full-thread":
                full_thread = True
            elif input_file is None:
                input_file = arg
            else:
                raise ValueError("Too many arguments")

        if input_file is None:
            raise ValueError("No input file")

        return cls(input_file, full_thread)


if __name__ == "__main__":
    args = sys.argv
    try:
        config = Config.create(args)
        print(config.__dict__)  # DEBUG
    except ValueError as err:
        print(f"string_art: {err}")
        usage()
        sys.exit(1)
