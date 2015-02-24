from os import open, walk
from os.path import isdir, isfile, join

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    args = '<file or directories ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for arg in args:
            self.parse_files(arg)

    def parse_files(self, path):
        if isdir(path):
            for root, dirs, files in walk(path):
                for file in files:
                    self.parse_file(join(root, file))
        elif isfile(path):
            self.parse_file(path)

    def parse_file(self, file):
        print('Parse file: "%s"' % file)
        pass

    def to_line(code, number, name, count, sum):
        return {
                'type': self.type(type),
                'number': int(number),
                'name': name.strip(),
                'count': int(count),
                'sum': float(sum)
                }

    def type(code):
        if code == 'A':
            return 'sale'
        elif code == 'R':
            return 'payment'
        elif code == 'x':
            return 'tax'
        elif code == 'K':
            return 'refund'
        elif code == 'L':
            return 'cancelled_sale'
        elif code == 'c' or code == 'h':
            raise IgnoredLineException()
        else:
            raise UnknownLineException('Unknown line code: %s' % code)

class UnknownLineException(Exception):
    """
    Thrown when we find a linetype we do not support
    """
    pass

class IgnoredLineException(Exception):
    """
    An exception to throw when a line should be ignored
    """
    pass
