from instaloader import Instaloader, Profile
from credentials import USERNAME, PASSWORD
from pprint import pprint
import json

# login into Instagram
L = Instaloader()
L.login(USERNAME,PASSWORD)

# load target handle
target_handle = "ekkyarmandi"
profile = Profile.from_username(L.context,target_handle)

# iterate account followers
entries = []
for user in profile.get_followees():

    # find latest post
    for post in user.get_post():
        post_url = post.url
        post_date = post.date_local.strftime("%H:%M:%S %d/%m/%Y")
        break

    # define entry data
    entry = dict( 
        id=user.userid,
        username=user.username,
        fullname=user.full_name,
        followers=user.followers,
        followings=user.followees,
        posts=user.mediacount,
        last_post_url=post_url,
        last_post_date=post_date,
        biography=user.biography,
        is_bussiness=user.is_business_account,
        business_category=user.bisness_category_name,
        links=user.external_url
    )
    entries.append(entry)
    pprint(entry, sort_dicts=False)

# dump the collected data
json.dump(
    entries,
    open("entries.json","w"),
    indent=4
)