from instabot import Bot
import instaloader


media_id=['p/C-aBwshyIhD','p/C9beh9GyqyO','p/C-XtnGFSTFh','p/DAikbHUy-j3','p/DAdeXExS7sv','p/DAXJN3vyK7p','p/DATiOXZSMWo','p/DAR-PjxyMaT','p/DAM1FbMSXL8','p/C__-l6MSwxE','p/C__6Uh3yvrc','p/C_oy7rWS4xw','p/C_I1CpvS3te','p/C_HPOAyyZPY','p/C--JzneyEiL','p/C-2ej3lyjML','p/C-zxML4yGvq','p/C-rOO6YyQtH','p/C-hzjnKy44l','p/C-aTuovyGz7','p/C-T-Cg7SVRk','p/C99uVEYS7bX','p/C97TC3JSLGT','p/C9zd_GgSltj','p/C9v6Yp7yor5','p/C9e6DNFSXk8','p/C9d4KTNSEGy','p/C9Z8V3eSpw2','p/C8yTdWAyDju','p/C8pFfLsymEw','p/C8j76gKyBnt','p/C8VzofDS243','p/C8UKWNRSVLW','p/C8PJ77tSvhz','p/C8DvVunSPab','p/C7_WJKGyEqg','p/C7MKoxyScTz','p/C7G88GBy5Oc','p/C6zeYfUya-S','p/C6OhZT6S7py','p/C6DLRcwStJc','p/C5m09SkSxGj','p/C5Z1MA2y8yN','p/C4nhq0AyW07','p/C3WYb3UyEw8','p/C2068pSy8CO','p/C2jApx7xAQS','p/C14PWhHJJGn','p/C1lf5zVLe2t','p/C1S7e1VSA8k','p/C0y3kTupPd7','p/C0rrF3dSHWO','p/C0iQiqtpSGG','p/C0eT_DHpmMj','p/C0dQ8d5LafJ','p/C0EdK6BLL2B','p/Cz_PHlILhdX','p/Cz7hrfySGrn','p/Cz6bp8QxB61','p/Cz6VJNuxYl2','p/Cz2TVLFyzJ_','p/CzkZZ3nJWx0','p/CxUTt3ISrRE','p/Cw6fMbop2M4','p/Cu41YMRrySA','p/CuHTawvpYCY','p/Ct16c54szKH','p/Ct13I_SMmV0','p/CtapuHwp8sc','p/CtXx4L7M7RQ','p/CtLRKpkqCBG','p/CtGT6R4M-3W','p/Cs-pp_ZtrW3','p/CsJdKP_stAY','p/Cr3b467P6Yq','p/Cr2gSmDJevc','p/CreuFFhuO9i','p/CraHJ1vuYL4','p/CrXJgvBpZpi','p/CrPqNfkt5vR','p/Cq722opJQ6E','p/Cq23kq8J5-q','p/CquMpgvLVS9','p/CqrnckiuD7D','p/Cqk6vN_JRfo','p/CqUKttQJKwf','p/CqPyOEJPGYs','p/Cp7S44sLxPR','p/Cpr-g4YpPHK','p/Cpk3j4eNmvV','p/CpjE6XPKSTe','p/CpexKCBjd5B','p/CpXAU_7DFcY','p/CpNGJN9JAXv','p/CpC1wlNpGla','p/Co36ou-s3Jn','p/CozEz-Wpev1','p/CoufaVsPyLv','p/Coh3obZMak5','p/CobPIWippQL','p/CoUyspLJmxN','p/CoUwgWCppKC','p/Cm5lptlK3Y_','p/Cmp6WEVKNQN','p/Chw5FIdJlKp','p/CgynBFip31Z','p/Cgb8_T4paIS','p/CgMgF4BpiVX','p/Cf_exYAhCpz','p/CepnRKiJQ1W','p/CenNxz8p7rU','p/Cei5IgQJVi0','p/CegxVoipX9u','p/CecWLUWhZWr','p/CeY5Bj9hWYo','p/Cd3aE5ZpOH-','p/Cdu2agQFep7','p/Ccg-2Typ5UQ','p/CcKamK1gAvb','p/CawBoffha9o','p/CX8uKOdqwff','p/CLRZ6QpHZ-L','p/CKyDqGOn_QQ','p/CKAhm9pHIBN','p/B7ymBbHlSDW']
media_link=['https://www.instagram.com/p/C-aBwshyIhD/','https://www.instagram.com/p/C9beh9GyqyO/','https://www.instagram.com/p/C-XtnGFSTFh/','https://www.instagram.com/p/DAikbHUy-j3/','https://www.instagram.com/p/DAdeXExS7sv/','https://www.instagram.com/p/DAXJN3vyK7p/','https://www.instagram.com/p/DATiOXZSMWo/','https://www.instagram.com/p/DAR-PjxyMaT/','https://www.instagram.com/p/DAM1FbMSXL8/','https://www.instagram.com/p/C__-l6MSwxE/','https://www.instagram.com/p/C__6Uh3yvrc/','https://www.instagram.com/p/C_oy7rWS4xw/','https://www.instagram.com/p/C_I1CpvS3te/','https://www.instagram.com/p/C_HPOAyyZPY/','https://www.instagram.com/p/C--JzneyEiL/','https://www.instagram.com/p/C-2ej3lyjML/','https://www.instagram.com/p/C-zxML4yGvq/','https://www.instagram.com/p/C-rOO6YyQtH/','https://www.instagram.com/p/C-hzjnKy44l/','https://www.instagram.com/p/C-aTuovyGz7/','https://www.instagram.com/p/C-T-Cg7SVRk/','https://www.instagram.com/p/C99uVEYS7bX/','https://www.instagram.com/p/C97TC3JSLGT/','https://www.instagram.com/p/C9zd_GgSltj/','https://www.instagram.com/p/C9v6Yp7yor5/','https://www.instagram.com/p/C9e6DNFSXk8/','https://www.instagram.com/p/C9d4KTNSEGy/','https://www.instagram.com/p/C9Z8V3eSpw2/','https://www.instagram.com/p/C8yTdWAyDju/','https://www.instagram.com/p/C8pFfLsymEw/','https://www.instagram.com/p/C8j76gKyBnt/','https://www.instagram.com/p/C8VzofDS243/','https://www.instagram.com/p/C8UKWNRSVLW/','https://www.instagram.com/p/C8PJ77tSvhz/','https://www.instagram.com/p/C8DvVunSPab/','https://www.instagram.com/p/C7_WJKGyEqg/','https://www.instagram.com/p/C7MKoxyScTz/','https://www.instagram.com/p/C7G88GBy5Oc/','https://www.instagram.com/p/C6zeYfUya-S/','https://www.instagram.com/p/C6OhZT6S7py/','https://www.instagram.com/p/C6DLRcwStJc/','https://www.instagram.com/p/C5m09SkSxGj/','https://www.instagram.com/p/C5Z1MA2y8yN/','https://www.instagram.com/p/C4nhq0AyW07/','https://www.instagram.com/p/C3WYb3UyEw8/','https://www.instagram.com/p/C2068pSy8CO/','https://www.instagram.com/p/C2jApx7xAQS/','https://www.instagram.com/p/C14PWhHJJGn/','https://www.instagram.com/p/C1lf5zVLe2t/','https://www.instagram.com/p/C1S7e1VSA8k/','https://www.instagram.com/p/C0y3kTupPd7/','https://www.instagram.com/p/C0rrF3dSHWO/','https://www.instagram.com/p/C0iQiqtpSGG/','https://www.instagram.com/p/C0eT_DHpmMj/','https://www.instagram.com/p/C0dQ8d5LafJ/','https://www.instagram.com/p/C0EdK6BLL2B/','https://www.instagram.com/p/Cz_PHlILhdX/','https://www.instagram.com/p/Cz7hrfySGrn/','https://www.instagram.com/p/Cz6bp8QxB61/','https://www.instagram.com/p/Cz6VJNuxYl2/','https://www.instagram.com/p/Cz2TVLFyzJ_/','https://www.instagram.com/p/CzkZZ3nJWx0/','https://www.instagram.com/p/CxUTt3ISrRE/','https://www.instagram.com/p/Cw6fMbop2M4/','https://www.instagram.com/p/Cu41YMRrySA/','https://www.instagram.com/p/CuHTawvpYCY/','https://www.instagram.com/p/Ct16c54szKH/','https://www.instagram.com/p/Ct13I_SMmV0/','https://www.instagram.com/p/CtapuHwp8sc/','https://www.instagram.com/p/CtXx4L7M7RQ/','https://www.instagram.com/p/CtLRKpkqCBG/','https://www.instagram.com/p/CtGT6R4M-3W/','https://www.instagram.com/p/Cs-pp_ZtrW3/','https://www.instagram.com/p/CsJdKP_stAY/','https://www.instagram.com/p/Cr3b467P6Yq/','https://www.instagram.com/p/Cr2gSmDJevc/','https://www.instagram.com/p/CreuFFhuO9i/','https://www.instagram.com/p/CraHJ1vuYL4/','https://www.instagram.com/p/CrXJgvBpZpi/','https://www.instagram.com/p/CrPqNfkt5vR/','https://www.instagram.com/p/Cq722opJQ6E/','https://www.instagram.com/p/Cq23kq8J5-q/','https://www.instagram.com/p/CquMpgvLVS9/','https://www.instagram.com/p/CqrnckiuD7D/','https://www.instagram.com/p/Cqk6vN_JRfo/','https://www.instagram.com/p/CqUKttQJKwf/','https://www.instagram.com/p/CqPyOEJPGYs/','https://www.instagram.com/p/Cp7S44sLxPR/','https://www.instagram.com/p/Cpr-g4YpPHK/','https://www.instagram.com/p/Cpk3j4eNmvV/','https://www.instagram.com/p/CpjE6XPKSTe/','https://www.instagram.com/p/CpexKCBjd5B/','https://www.instagram.com/p/CpXAU_7DFcY/','https://www.instagram.com/p/CpNGJN9JAXv/','https://www.instagram.com/p/CpC1wlNpGla/','https://www.instagram.com/p/Co36ou-s3Jn/','https://www.instagram.com/p/CozEz-Wpev1/','https://www.instagram.com/p/CoufaVsPyLv/','https://www.instagram.com/p/Coh3obZMak5/','https://www.instagram.com/p/CobPIWippQL/','https://www.instagram.com/p/CoUyspLJmxN/','https://www.instagram.com/p/CoUwgWCppKC/','https://www.instagram.com/p/Cm5lptlK3Y_/','https://www.instagram.com/p/Cmp6WEVKNQN/','https://www.instagram.com/p/Chw5FIdJlKp/','https://www.instagram.com/p/CgynBFip31Z/','https://www.instagram.com/p/Cgb8_T4paIS/','https://www.instagram.com/p/CgMgF4BpiVX/','https://www.instagram.com/p/Cf_exYAhCpz/','https://www.instagram.com/p/CepnRKiJQ1W/','https://www.instagram.com/p/CenNxz8p7rU/','https://www.instagram.com/p/Cei5IgQJVi0/','https://www.instagram.com/p/CegxVoipX9u/','https://www.instagram.com/p/CecWLUWhZWr/','https://www.instagram.com/p/CeY5Bj9hWYo/','https://www.instagram.com/p/Cd3aE5ZpOH-/','https://www.instagram.com/p/Cdu2agQFep7/','https://www.instagram.com/p/Ccg-2Typ5UQ/','https://www.instagram.com/p/CcKamK1gAvb/','https://www.instagram.com/p/CawBoffha9o/','https://www.instagram.com/p/CX8uKOdqwff/','https://www.instagram.com/p/CLRZ6QpHZ-L/','https://www.instagram.com/p/CKyDqGOn_QQ/','https://www.instagram.com/p/CKAhm9pHIBN/','https://www.instagram.com/p/B7ymBbHlSDW/']

def reel_liker():
    # Create an instance of the Bot
    bot = Bot()

    # Login to your Instagram account
    username = 'softskilliq@gmail.com'
    password = 'HK1998@k'
    hhk=bot.login(username=username, password=password)
    print(hhk)

    # The media ID of the Reel you want to like
    reel_media_id = 'DAiX-vToYcS'  # Replace with the actual media ID

    # Like the Reel
    bot.like(reel_media_id)

    print("Liked the Reel successfully!")





def get_reel_id():
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    # Replace with the target username
    username = 'iamharsh_kumar'  # The username of the account you want to scrape

    # Load the profile
    profile = instaloader.Profile.from_username(loader.context, username)

    # Iterate through the posts and collect Reels links
    reels_links = []
    for post in profile.get_posts():
        if post.typename == 'GraphVideo' and post.is_video:
            reels_links.append(f"https://www.instagram.com/p/{post.shortcode}/")

    # Print the collected Reels links
    for link in reels_links:
        print(link)

reel_liker()