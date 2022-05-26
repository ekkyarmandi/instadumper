from instaloader import Instaloader, Profile
from credentials import USERNAME, PASSWORD
from pandas import DataFrame
import time

# login into Instagram
L = Instaloader()
L.login(USERNAME,PASSWORD)

# load target handle
target_handle = "jakesthekidd"
profile = Profile.from_username(L.context,target_handle)

# iterate account followers
try:
    entries = []
    for user in profile.get_followers():

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
        print("Total followers being scraped:",len(entries))
        print(entry)
        time.sleep(1)

except Exception as E:
    print(E)

# write it out into a csv
data = DataFrame(entries)
data.to_csv(target_handle+".csv",index=False)