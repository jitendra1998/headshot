import redis
import json
from datetime import datetime, timedelta

# set redis_database in r
r = redis.StrictRedis(host='localhost', db=4)


# banner_id = {'link': 'add_link_to_banner', 'eyeballs': [], 'clicks': [], 'shares': []}
class BannerStats:
    def __init__(self, banner_id):
        self.banner_id = banner_id
        redis_banner = r.get(self.banner_id)
        if not redis_banner:
            self.create_banner()

    def get_banner_stats(self):
        return json.loads(r.get(self.banner_id))

    def save_banner_stats(self, banner):
        r.set(self.banner_id, json.dumps(banner))

    def create_banner(self, banner_link=None):
        self.save_banner_stats({'link': banner_link, 'eyeballs': [], 'clicks': [], 'shares': []})

    def update_banner(self, viewed_by=None, clicked_by=None, shared_by=None):
        banner = self.get_banner_stats()
        if viewed_by is not None and viewed_by not in banner['eyeballs']:
            banner['eyeballs'].append(viewed_by)
        if clicked_by is not None and clicked_by not in banner['clicks']:
            banner['clicks'].append(clicked_by)
        if shared_by is not None and shared_by not in banner['shares']:
            banner['shares'].append(shared_by)
        self.save_banner_stats(banner)

    def edit_link(self, link):
        banner = self.get_banner_stats()
        banner['link'] = link
        self.save_banner_stats(banner)


# banner_dict = {'banner_id': {'timeslot': {'gameroom_id': ['positions']}}}
class BannerDict:
    def __init__(self):
        redis_banner_dict = r.get('banner_dict')
        if not redis_banner_dict:
            self.create_banner_dict()

    def get_banner_dict(self):
        return json.loads(r.get('banner_dict'))

    def save_banner_dict(self, banner_dict):
        r.set('banner_dict', json.dumps(banner_dict))

    def create_banner_dict(self):
        self.save_banner_dict({})

    def add_banner_dict_entry(self, banner_id, timeslot, gameroom_id, positions):
        banner_dict = self.get_banner_dict()
        banner_dict[banner_id] = {}
        banner_dict[banner_id]['timeslot'] = timeslot
        banner_dict[banner_id]['gamerooms'] = { gameroom_id : positions }
        self.save_banner_dict(banner_dict)


def view_dictionary():
    banner_dict = BannerDict()
    print "banner_dict -", banner_dict.get_banner_dict()


def view_banner_list():
    banner_dict = BannerDict()
    print "banners -", banner_dict.get_banner_dict().keys()


def view_all_banners():
    banner_dict = BannerDict()
    for banner_id in banner_dict.get_banner_dict().keys():
        view_banner(banner_id)


def view_banner(banner_id):
    banner = BannerStats(banner_id)
    print banner_id, banner.get_banner_stats()


def upload_banner(banner_id, link=None, duration=None, timeslot=None, gameroom=None, positions=None):
    # sample banner
    # banner_id = 'test1'
    # link = 'default'
    # duration = 8
    # timeslot = str(datetime.now()) + " to " + str(datetime.now() + timedelta(hours=duration))
    # gameroom = '1'
    # positions = ['1', '2', '3']

    # create a banner
    banner_obj = BannerStats(banner_id)
    # banner_obj.create_banner()
    banner_obj.edit_link(link)

    # update in banner dictionary
    dictionary_obj = BannerDict()
    dictionary_obj.add_banner_dict_entry(banner_id, timeslot, gameroom, positions)

# upload_banner()
# view_banner_list()
# view_all_banners()
# view_dictionary()
