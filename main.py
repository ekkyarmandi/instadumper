from instaloader import Instaloader, Profile, load_structure_from_file, save_structure_to_file
from credentials import USERNAME, PASSWORD
from pandas import DataFrame
import json
import time
import os

# login into Instagram
L = Instaloader()
L.login(USERNAME,PASSWORD)

# load target handle
max_counter = 50
target_handle = "jakesthekidds"
profile = Profile.from_username(L.context,target_handle)

# iterate account followers
followers_iterator = profile.get_followers()
if os.path.exists("previous_iteration.json"):
    prev = load_structure_from_file(
        L.context,
        "previous_iteration.json"
    )
    followers_iterator.thaw(prev)
    entries = json.load(open("entries.json",encoding="utf-8"))
else:
    entries = []

try:
    counter = 0
    for user in followers_iterator:

        # find latest post
        post_url = None
        post_date = None
        for post in user.get_posts():
            post_url = "https://www.instagram.com/p/" + str(post.shortcode)
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
            last_post_url=post_url if user.mediacount != 0 else None,
            last_post_date=post_date if user.mediacount != 0 else None,
            biography=user.biography,
            is_private=user.is_private,
            is_bussiness=user.is_business_account,
            business_category=user.business_category_name,
            links=user.external_url
        )
        entries.append(entry)
        print(entry)
        print("Total data:",len(entries),"\n")
        counter += 1
        if counter >= max_counter:
            raise Exception("Program stoped by counter")

except:
    json.dump(
        entries,
        open("entries.json","w",encoding="utf-8"),
        indent=4
    )
    save_structure_to_file(
        followers_iterator.freeze(),
        "previous_iteration.json"
    )

# write it out into a csv
data = DataFrame(entries)
data.to_csv(target_handle+".csv",index=False)