import re
from datetime import datetime
from io import open
from os import walk
from os.path import isdir, isfile, join

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from cyb_oko.settings import TIME_ZONE
from z.models import Kassetransaksjon, Kvittering, Salgsvare, Zrapport


class Command(BaseCommand):
    args = "<file or directories ...>"
    help = "Load the given z-report files into the database"

    #
    # Compiled regexes used to parse the input file
    #

    # Match all lines that we skip
    skip_lines = re.compile(
        r"^(\s$|\d[A-Z\/]|JOURNAL DES VENTES|FIN DE LECTURE|-D|B\s+\d+\s(TIROIR|TA|AT))"
    )

    # Match the start date lines
    start_date = re.compile(r"^\/(\d{2}-\d{2}-\d{4} \d{2}:\d{2})")

    # Match the receipt transaction lines
    receipt_transaction = re.compile(
        r"^([a-zA-Z])\s+(\d+)\s(.{15})\s+(-?\d+)\s+(-?\d+\.\d{2})"
    )

    # Match the receipt date line
    receipt_date = re.compile(r"^ <(\d{2}-\d{2}-\d{2} \d{2}:\d{2})(\d{6})")

    # Match the z-report date line
    z_number = re.compile(r"^\s+Z READING NR (\d+)")

    #
    # Timezone stuff
    #

    # Store the pytz timezone object for out current timezone
    tz = pytz.timezone(TIME_ZONE)

    def handle(self, *args, **options):
        print("Parsing in timezone: %s" % TIME_ZONE)

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
        with open(file, "rt", encoding="iso8859-1") as f:
            # Skip the first line
            f.readline()

            # Create models
            self.z = Zrapport()
            self.kvitteringer = []

            self.new_receipt()

            # Parse each line
            for line in f:
                self.parse_line(line)

            # self.save_z()

    def new_receipt(self):
        # Store the previous receipt, if needed
        if hasattr(self, "kvittering"):
            self.kvitteringer.append(self.kvittering)

        # Create a new one
        self.kvittering = Kvittering()
        self.kvittering.linjer = []

    def save_z(self):
        self.z.save()
        self.z.kvitteringer = self.kvitteringer

        for k in self.kvitteringer:
            if len(k.linjer) > 0:
                for linje in k.linjer:
                    linje.tidspunkt = k.tidspunkt
                    k.transaksjoner.add(linje)

    def parse_line(self, line):
        if self.skip_lines.search(line):
            return
        elif self.receipt_date_line(line):
            self.new_receipt()
            return
        elif self.receipt_transaction_line(line):
            return
        elif self.z_number_line(line):
            return
        elif self.start_date_line(line):
            return
        else:
            raise Exception("Unknown line: %s" % line)

    def receipt_date_line(self, line):
        m = self.receipt_date.search(line)
        if m:
            self.kvittering.tidspunkt = self.tz.localize(
                datetime.strptime(m.group(1), "%d-%m-%y %H:%M")
            )
            self.kvittering.nummer = int(m.group(2), base=10)
            return True
        else:
            return False

    def receipt_transaction_line(self, line):
        m = self.receipt_transaction.search(line)
        if m:
            try:
                self.kvittering.linjer.append(
                    self.to_line(
                        m.group(1),
                        m.group(2),
                        m.group(3).strip(),
                        m.group(4),
                        m.group(5),
                    )
                )
            except IgnoredLineException:
                pass
            return True
        else:
            return False

    def z_number_line(self, line):
        m = self.z_number.search(line)
        if m:
            self.z.nummer = int(m.group(1), base=10)
            return True
        else:
            return False

    def start_date_line(self, line):
        m = self.start_date.search(line)
        if m:
            if not self.z.tidspunkt:
                self.z.tidspunkt = self.tz.localize(
                    datetime.strptime(m.group(1), "%d-%m-%Y %H:%M")
                )
            return True
        else:
            return False

    def to_line(self, code, number, name, count, sum):
        t = self.type(code)
        nummer = int(number, base=10)

        if t == "sale" or t == "refund":
            try:
                vare = Salgsvare.objects.get(kassenr=nummer)
                if vare.kassenavn == name:
                    return Kassetransaksjon(
                        kvittering=self.kvittering,
                        salgsvare=vare,
                        antall=int(count, base=10),
                    )
                else:
                    self.name_mismatch(vare, name)
            except ObjectDoesNotExist:
                print("Fant ingen match for: %s %d %s" % (t, nummer, name))
                print("Hva vil du gjøre?")
                print("Lag ny salgsvare [1]")
                print("Lag ny mapping til eksisterende salgsvare [2]")
                action = int(input("Velg kommando: "))
                if action == 1:
                    self.create_salgsvare(number)
                elif action == 2:
                    self.create_mapping(number, name)
        raise IgnoredLineException()

    def type(self, code):
        if code == "A":
            return "sale"
        elif code == "R":
            return "payment"
        elif code == "x":
            return "tax"
        elif code == "K":
            return "refund"
        elif code == "L":
            # return 'cancelled_sale'
            # Ignore canelled sales
            raise IgnoredLineException()
        elif code == "c" or code == "h":
            raise IgnoredLineException()
        else:
            raise UnknownLineException("Unknown line code: %s" % code)

    def name_mismatch(self, vare, name):
        """
        Handler for mismatch between the name stored in the database and the
        name stored in the pos system.
        """
        print(
            'Kassenavn for vare #%d ("%s") matcher ikke ("%s" != "%s")'
            % (vare.kassenr, vare.navn, vare.kassenavn, name)
        )
        print("Oppdater navn på salgsvare [1]")
        print("Map til annen vare [2]")
        action = int(input("Velg kommando: "))
        if action == 1:
            vare.kassenavn = name
            vare.save()
        elif action == 2:
            self.find_salgsvare()
            # self.create_mapping(vare.kassenr, name)

    def create_salgsvare(self, number):
        category = input("Kategori: ")
        name = input("Navn: ")
        account = input("Salgskonto: ")
        status = input("Status: ")
        print("%s %s %s %s %s" % (category, name, account, status, number))

    def create_mapping(self, num, name):
        target = int(input("Kassenummer: "))
        vare = Salgsvare.objects.get(kassenr=target)
        print("Ny map fra %d:%s til %d:%s" % (num, name, vare.kassenr, vare.navn))

    def find_salgsvare(self):
        while True:
            name = input("Søk etter vare: ")
            varer = Salgsvare.objects.filter(navn__icontains=name)[:10]
            if len(varer) == 0:
                print("Fant ingen varer som matcher")
            else:
                for vare in varer:
                    print("#%d %s" % (vare.pk, vare.navn))
                try:
                    int(input("Velg en vare (ctrl-c for å søke på nytt): "))
                    return True
                except KeyboardInterrupt:
                    print("")


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
