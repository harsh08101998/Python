from instagrapi import Client
import random

# Define your username and password
instagram_username = "saini_boy_1276"
instagram_password = "HK1998@k"

# Initialize the client and load session
ig_client = Client()
instagram_session = "instagram_session"
instagram_session_path = f"./{instagram_session}.json"
print(instagram_session_path)

# Try loading an existing session, otherwise log in
try:
    ig_client.load_settings(instagram_session_path)
except FileNotFoundError:
    ig_client.login(instagram_username, instagram_password)
    ig_client.dump_settings(instagram_session_path)


my_pk = ig_client.account_info().dict()["pk"]
following_dict = ig_client.user_followers(my_pk)
# print(following_dict)


# Get the ID of a random user you are following
ids2 = [key for key, user in following_dict.items() if not user.is_private]
print(ids2)
for ids in ids2:
    random_user = random.choice(ids)
    # print(random)

    # Retrieve their media (posts)
    media_list = ig_client.user_medias(random_user)

    # Like their latest post
    if len(media_list) > 0:
        last_post_id = media_list[0].dict()["id"]
        ig_client.media_like(last_post_id)
    else:
        print(f"No media for user with id {random_user}")