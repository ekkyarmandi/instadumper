from instaloader import Instaloader, Profile
from credentials import USERNAME, PASSWORD
from pprint import pprint
from pandas import DataFrame
import json

# login into Instagram
L = Instaloader()
L.login(USERNAME,PASSWORD)

# load target handle
target_handle = "worldofnolabel"
profile = Profile.from_username(L.context,target_handle)

# iterate account followers
try:
    entries = []
    for user in profile.get_followers():

        # find latest post
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
            last_post_url=post_url if post.mediacount != 0 else None,
            last_post_date=post_date if post.mediacount != 0 else None,
            biography=user.biography,
            is_bussiness=user.is_business_account,
            business_category=user.business_category_name,
            links=user.external_url
        )
        entries.append(entry)
        pprint(entry, sort_dicts=False)

except Exception:
    print(Exception)

# dump the collected data
json.dump(
    entries,
    open(target_handle+".json","w",encoding="utf-8"),
    indent=4
)

# write it out into a csv
data = DataFrame(entries)
data.to_csv(target_handle+".csv",index=False)