from enum import Enum

class BikerStatus(Enum):
    IDLE = 0
    GOING_TO_RESTAURANT = 1
    GOING_TO_CLIENT = 2


class BikerInteraction:
    bikers = None

    def __init__(self):
        self.bikers = {}
        for i in [0, 1]:
            self.bikers[i] = {'deliveries': [], 'status': BikerStatus.IDLE, 'path': []}

    def parse_bikers_pos(self, args):
        for biker in [0, 1]:
            self.bikers[biker]['pos'] = [int(e) for e in args[biker].split(';')[1:]]

    def get_pos(self, biker):
        return self.bikers[biker]['pos']

    def get_status(self, biker):
        return self.bikers[biker]['status']

    def set_status(self, biker, status):
        self.bikers[biker]['status'] = status

    def __getattr__(self, biker):
        return self.bikers[biker]

    def set_path(self, biker, path):
        self.bikers[biker]['path'] = path

    def move_biker(self, biker, pos):
        self.bikers[biker]['pos'] = pos

    def get_next_move(self, biker):
        return self.bikers[biker]['path'].pop(0) if self.bikers[biker]['path'] else None

    def is_arrived(self, biker):
        b = self.bikers[biker]
        if b['status'] == BikerStatus.GOING_TO_RESTAURANT:
            return self.is_at_restaurant(biker)
        elif b['status'] == BikerStatus.GOING_TO_CLIENT:
            return self.is_at_client(biker)
        return False

    def is_at_restaurant(self, biker):
        for d in self.bikers[biker]['deliveries']:
            if self.bikers[biker]['pos'] == d.resto_loc:
                return d.order_id
        return False

    def is_at_client(self, biker):
        for d in self.bikers[biker]['deliveries']:
            if self.bikers[biker]['pos'] == d.maison_loc:
                return d.order_id
        return False

    def take_delivery(self, biker, delivery):
        self.bikers[biker]['deliveries'].append(delivery)

    def deliver(self, biker, delivery):
        self.bikers[biker]['deliveries'].remove(delivery)

    def get_deliveries(self, biker):
        return self.bikers[biker]['deliveries']

    @staticmethod
    def __around(dest, pos):
        dest = tuple(dest)
        return dest == (pos[0] - 1, pos[1]) or dest == (pos[0] + 1, pos[1]) \
            or dest == (pos[0], pos[1] - 1) or dest == (pos[0], pos[1] + 1)
#Petit easteregg pour les coquins ;)
#                               _.._
#                             .'    '.
#                            (____/`\ \
#                           (  |' ' )  )
#                           )  _\= _/  (
#                 __..---.(`_.'  ` \    )
#                `;-""-._(_( .      `; (
#                /       `-`'--'     ; )
#               /    /  .    ( .  ,| |(
#_.-`'---...__,'    /-,..___.-'--'_| |_)
#'-'``'-.._       ,'  |   / .........'
#          ``;--"`;   |   `-`
#             `'..__.'
#