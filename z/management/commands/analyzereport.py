from datetime import datetime
from io import open
from os import walk
from os.path import isdir, isfile, join

import re
import pytz

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from cyb_oko.settings import TIME_ZONE

from varer.models import Salgsvare, Konto


class Command(BaseCommand):
    args = '<file or directories ...>'
    help = 'Load the given z-report files into the database'

    #
    # Timezone stuff
    #

    # Store the pytz timezone object for out current timezone
    tz = pytz.timezone(TIME_ZONE)

    parser = None

    def handle(self, *args, **options):
        self.parser = ZSimpleParser()

        print('Parsing in timezone: %s' % TIME_ZONE)

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
        z = self.parser.parse(file)

        self.find_products(z)

        self.generate_report(z)

    def find_products(self, z):
        for product in z.product_totals:
            try:
                obj = Salgsvare.objects.select_related('salgskonto').get(kassenr=product.id)
                product.reference_product = obj
                product.account = obj.salgskonto
            except ObjectDoesNotExist:
                accounts = Konto.objects.all()

                print()
                print('Unknown product: %s (number %d)' % (product.title, product.id))
                print('Account list:')

                for idx, account in enumerate(accounts):
                    print(' [%d] %s' % (idx, account))

                while True:
                    try:
                        action = int(input('Select the account this product belongs: '))
                        product.account = accounts[action]
                        break
                    except Exception:
                        print('Unknown account')

    def generate_report(self, z):
        class Group(object):
            def __init__(self, title):
                self.products = []
                self.title = title

            def add(self, product):
                self.products.append(product)

            def sum_amount(self):
                s = 0
                for product in self.products:
                    s += product.amount
                return s

        groups = {}
        for product in z.product_totals:
            group = groups.get(product.account.gruppe)
            if not group:
                group = Group(product.account.gruppe)
                groups[product.account.gruppe] = group

            group.products.append(product)

        groups = sorted(groups.values(), key=lambda x: x.title)

        print('Z %d' % z.number)
        print()
        print('First transaction: %s' % z.time_first)
        print('Last transaction: %s' % z.time_last)
        print()

        print('Sales:')

        for group in groups:
            print()
            print('  %-25s %10.2f' % (group.title, group.sum_amount()))
            for product in sorted(group.products, key=lambda x: x.title):
                print('    %-18s %4d %10.2f' % (product.title, product.count, product.amount))

        print()
        print('  %-25s %10.2f' % ('TOTAL SALES: ', z.total_amount()))

        print()
        print('Payment methods:')

        for payment in z.payment_totals:
            print('  %-25s %10.2f' % (payment.title, payment.amount))

        print()
        print('Report generated from DTT file')


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


class ZSimpleParser(object):
    # Match the receipt date line
    receipt_date = re.compile('^ <(\d{2}-\d{2}-\d{2} \d{2}:\d{2})(\d{6})')

    # Match the z-report date line
    z_number = re.compile('^\s+(Z READING NR |RAZ EFFECTUEE No )(\d+)')

    # Match the various "totals" lines
    # 1T 534 Mohawk Snowmelt        10     625.003520P
    total_line = re.compile('^(1.) \s?\s?(\d+) (.{18}) (.{6}) (.{10})')

    """
    :type Z
    """
    z = None

    def parse(self, file):
        # Create models
        self.z = Z()

        with open(file, 'rt', encoding='iso8859-1') as f:
            # Skip the first line
            f.readline()

            # Parse each line
            for line in f:
                self.parse_line(line)

        return self.z

    def parse_line(self, line):
        if line[0:2] == '1T':
            self.parse_product_total(line)
        elif line[0:2] == '1R':
            self.parse_payment_total(line)
        elif self.receipt_date_line(line):
            return
        elif self.z_number_line(line):
            return

    def parse_product_total(self, line):
        m = self.total_line.search(line)
        if not m:
            raise UnknownLineException()

        # skip sum row
        if m.group(2) == '0':
            return

        elm = ProductTotal()
        elm.id = m.group(2)
        elm.title = m.group(3).strip()
        elm.count = int(m.group(4))
        elm.amount = float(m.group(5))

        self.z.product_totals.append(elm)

    def parse_payment_total(self, line):
        m = self.total_line.search(line)
        if not m:
            raise UnknownLineException()

        # skip sum row
        if m.group(2) == '0':
            return

        elm = PaymentTotal()
        elm.id = m.group(2)
        elm.title = m.group(3).strip()
        elm.count = int(m.group(4))
        elm.amount = float(m.group(5))

        self.z.payment_totals.append(elm)

    def receipt_date_line(self, line):
        m = self.receipt_date.search(line)
        if m:
            time = Command.tz.localize(datetime.strptime(m.group(1), '%d-%m-%y %H:%M'))
            if not self.z.time_first:
                self.z.time_first = time
            else:
                self.z.time_last = time
            return True
        else:
            return False

    def z_number_line(self, line):
        m = self.z_number.search(line)
        if m:
            self.z.number = int(m.group(2), base=10)
            return True
        else:
            return False


class Z(object):
    """
    :type [ProductTotal]
    """
    product_totals = []

    """
    :type [PaymentTotal]
    """
    payment_totals = []

    number = None
    time_first = None
    time_last = None

    def __repr__(self):
        return 'Z nr %d with %d products and %d payment types' % (
            self.number or -1, len(self.product_totals), len(self.payment_totals))

    def total_amount(self):
        amount = 0
        for product in self.product_totals:
            amount += product.amount
        return amount


class ProductTotal(object):
    id = None
    title = None
    count = 0
    amount = 0
    reference_product = None
    account = None


class PaymentTotal(object):
    id = None
    title = None
    count = 0
    amount = 0
