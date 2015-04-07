from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from skitur.models import Trip, Cabin, Participant, Wish

class Command(BaseCommand):
    args = '<Trip name>'

    def handle(self, *args, **options):
        for name in args:
            self.calculate(name)

    def calculate(self, trip):
        trip = Trip.objects.get(name=trip)

        nodes = {}

        for participant in trip.participants.all():
            nodes[participant] = Node(participant)

        for participant in trip.participants.all():
            for wish in participant.wishes.all():
                p = nodes[participant]
                n = nodes[wish.wish]
                p.wish(n)
                #n.wished_by(p)

        cost = 0
        for key in nodes:
            cost += nodes[key].cost()

        print('Total cost: %d' % cost)

class Node:

    def __init__(self, p):
        self.participant = p;
        self._wishes = []
        self._wished_by = []

        if p.cabin:
            self.cabin = p.cabin
            self.pinned = True
        else:
            self.cabin = None
            self.pinned = False

    def wish(self, node):
        self._wishes.append(node)
        node.wished_by(self)

    def wished_by(self, node):
        self._wished_by.append(node)

    def pinned(self):
        return self.pinned

    def cost(self, cabin=None):
        if not cabin:
            cabin = self.cabin

        if not cabin or len(self._wishes) == 0:
            return 0

        cost = 0
        per_wish = 12 / len(self._wishes)
        for wish in self._wishes:
            if wish.cabin != cabin:
                cost += per_wish

        return cost

    def choices(self):
        if len(self._wishes) == 0:
            return 12

        choices = 12
        for wish in self._wishes:
            if wish.cabin:
                choices -= 12 / len(self._wishes)

        return choices


