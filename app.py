from flask import Flask, render_template, jsonify
from instagrapi import Client
import os

from flask import Flask, send_file

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))


# ============================================================
MY_USERNAME = "hn_1234321"        # tumhara login username
MY_PASSWORD = "yoyohoney123"        # tumhara password
TARGET_ACCOUNT = "thee.suit.story"  # jis account ki posts chahiye
PORT           = 1200
# ============================================================

cl = Client()
_logged_in = False
SESSION_FILE = "session.json"

def get_client():
    global _logged_in
    if not _logged_in:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(MY_USERNAME, MY_PASSWORD)
        else:
            cl.login(MY_USERNAME, MY_PASSWORD)
            cl.dump_settings(SESSION_FILE)
        _logged_in = True
    return cl

@app.route("/")
def index():
    # return render_template("index.html", target=TARGET_ACCOUNT)
    return send_file("index.html", target=TARGET_ACCOUNT)

@app.route("/api/profile")
def get_profile():
    """Profile pic (logo) fetch karne ke liye"""
    try:
        client = get_client()
        info = client.user_info_by_username_v1(TARGET_ACCOUNT)
        logo = str(info.profile_pic_url) if info.profile_pic_url else ""
        return jsonify({"success": True, "logo": logo})
    except Exception as e:
        return jsonify({"success": False, "logo": "", "error": str(e)})

@app.route("/api/posts")
def get_posts():
    try:
        client = get_client()
        info   = client.user_info_by_username_v1(TARGET_ACCOUNT)
        medias = client.user_medias(info.pk, amount=108)

        posts = []
        for m in medias:
            post = {
                "id":         str(m.pk),
                "type":       m.media_type,
                "caption":    m.caption_text or "",
                "like_count": m.like_count,
                "timestamp":  m.taken_at.strftime("%d %b %Y"),
            }
            if m.media_type == 1:                        # Photo
                post["image"] = str(m.thumbnail_url)
            elif m.media_type == 2:                      # Reel/Video
                post["image"]   = str(m.thumbnail_url)
                post["is_reel"] = True
            elif m.media_type == 8 and m.resources:     # Album
                post["image"]    = str(m.resources[0].thumbnail_url)
                post["is_album"] = True
            else:
                continue

            posts.append(post)

        return jsonify({"success": True, "posts": posts})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

#
#  if __name__ == "__main__":
#     # app.run(debug=True, host="0.0.0.0", port=1200)
#     app.run(debug=True, port=1200)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)