from flask import Flask, render_template, jsonify
from instagrapi import Client
import os

app = Flask(__name__)

# ============================================================
# APNA CREDENTIALS YAHAN DALO
# ============================================================
MY_USERNAME = "hn_1234321"        # tumhara login username
MY_PASSWORD = "yoyohoney123"        # tumhara password
TARGET_ACCOUNT = "thee.suit.story"  # jis account ki posts chahiye
# ============================================================

cl = Client()
_logged_in = False

def get_client():
    global _logged_in
    if not _logged_in:
        cl.login(MY_USERNAME, MY_PASSWORD)
        _logged_in = True
    return cl

@app.route("/")
def index():
    return render_template("index.html", target=TARGET_ACCOUNT)

@app.route("/api/posts")
def get_posts():
    try:
        client = get_client()
        # user_id = client.user_id_from_username(TARGET_ACCOUNT)
        # medias = client.user_medias(user_id, amount=2400000000)

        user_info = client.user_info_by_username_v1(TARGET_ACCOUNT)
        medias = client.user_medias(user_info.pk, amount=10800000000000)

        posts = []
        for m in medias:
            post = {
                "id": str(m.pk),
                "type": m.media_type,   # 1=Photo, 2=Video/Reel, 8=Album
                "caption": m.caption_text or "",
                "like_count": m.like_count,
                "timestamp": m.taken_at.strftime("%d %b %Y"),
                "url": m.thumbnail_url.path if m.thumbnail_url else None,
            }

            # Photo
            if m.media_type == 1:
                post["image"] = str(m.thumbnail_url)

            # Video / Reel
            elif m.media_type == 2:
                post["image"] = str(m.thumbnail_url)
                post["is_reel"] = True

            # Album / Carousel
            elif m.media_type == 8 and m.resources:
                post["image"] = str(m.resources[0].thumbnail_url)
                post["is_album"] = True

            posts.append(post)

        return jsonify({"success": True, "posts": posts, "target": TARGET_ACCOUNT})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, port=1200)




















# from flask import Flask, render_template, jsonify
# from instagrapi import Client
# import os

# app = Flask(__name__)

# # ============================================================
# # APNA CREDENTIALS YAHAN DALO
# # ============================================================
# MY_USERNAME = "hn_1234321"        # tumhara login username
# MY_PASSWORD = "thesuitstory159753"        # tumhara password
# TARGET_ACCOUNT = "thee.suit.story"  # jis account ki posts chahiye
# # ============================================================

# cl = Client()
# _logged_in = False
# SESSION_FILE = "session.json"

# def get_client():
#     global _logged_in
#     if not _logged_in:
#         if os.path.exists(SESSION_FILE):
#             # Pehle session load karo — login mat karo baar baar
#             cl.load_settings(SESSION_FILE)
#             cl.login(MY_USERNAME, MY_PASSWORD)
#         else:
#             # Pehli baar login + session save karo
#             cl.login(MY_USERNAME, MY_PASSWORD)
#             cl.dump_settings(SESSION_FILE)
#         _logged_in = True
#     return cl

# @app.route("/")
# def index():
#     return render_template("index.html", target=TARGET_ACCOUNT)

# @app.route("/api/posts")
# def get_posts():
#     try:
#         client = get_client()
#         user_id = client.user_id_from_username(TARGET_ACCOUNT)
#         medias = client.user_medias(user_id, amount=24)

#         posts = []
#         for m in medias:
#             post = {
#                 "id": str(m.pk),
#                 "type": m.media_type,   # 1=Photo, 2=Video/Reel, 8=Album
#                 "caption": m.caption_text or "",
#                 "like_count": m.like_count,
#                 "timestamp": m.taken_at.strftime("%d %b %Y"),
#                 "url": m.thumbnail_url.path if m.thumbnail_url else None,
#             }

#             # Photo
#             if m.media_type == 1:
#                 post["image"] = str(m.thumbnail_url)

#             # Video / Reel
#             elif m.media_type == 2:
#                 post["image"] = str(m.thumbnail_url)
#                 post["is_reel"] = True

#             # Album / Carousel
#             elif m.media_type == 8 and m.resources:
#                 post["image"] = str(m.resources[0].thumbnail_url)
#                 post["is_album"] = True

#             posts.append(post)

#         return jsonify({"success": True, "posts": posts, "target": TARGET_ACCOUNT})

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)}), 500

# if __name__ == "__main__":
#     app.run(debug=True)