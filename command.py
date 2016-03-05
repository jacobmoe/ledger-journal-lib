import argparse, datetime

class Command():
    DEFAULT_OPTIONS = [
        {'name': '--write', 'help': 'write file', 'action': 'store_true'}
    ]

    OPTIONS = []

    def __init__(self, name):
        self.args, self.file_names = self.__parse_arguments()
        self.name = name

    def run(self):
        raise NotImplementedError

    def output(self, result):
        if (self.args.write):
            with open(self._file_name(), "w") as f:
                f.write('; -*- ledger -*-\n\n')

                for item in result:
                    f.write(item)
        else:
            print('; -*- ledger -*-\n')
            for item in result:
                print(item)

    def __parse_arguments(self):
        arg_parser = argparse.ArgumentParser()

        for arg_info in (self.DEFAULT_OPTIONS + self.OPTIONS):
            arg_parser.add_argument(
                arg_info['name'],
                help=arg_info.get('help'),
                action=arg_info.get('action')
            )

        args, file_names = arg_parser.parse_known_args()
        return (args, file_names)

    # overridables:

    def _file_name(self):
        return "%s_%s.dat" % (self.name, str(datetime.date.today()))
