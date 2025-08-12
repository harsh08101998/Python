import instaloader

# Create an instance of Instaloader
loader = instaloader.Instaloader()

# Replace with the target username
username = 'iamharsh_kumar'  # The username of the account you want to scrape

# Load the profile
profile = instaloader.Profile.from_username(loader.context, username)

# Iterate through the posts and collect Reels media IDs
reels_media_ids = []
for post in profile.get_posts():
    print(post)
    if post.typename == 'DAiX-vToYcS' and post.is_video:
        reels_media_ids.append(post.media_id)

# Print the collected media IDs
for media_id in reels_media_ids:
    print(media_id)