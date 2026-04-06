from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired

USERNAME = "hn_1234321"   # 👈 yahan apna username
PASSWORD = "thesuitstory159753"   # 👈 yahan apna password

cl = Client()

# Mobile jaisi setting lagao — suspicious nahi lagega
cl.set_settings({
    "uuids": {
        "phone_id": "57d64c41-a916-3fa5-bd7a-3796c1dab122",
        "uuid": "8aa373c6-f316-44d7-b7ec-1b7d9a2edcb7",
        "client_session_id": "6c296d0a-efeb-4a72-9f5d-dc9b0bfe4f95",
        "advertising_id": "8dc88b76-dfbc-44dc-abbc-31a6f1d54b04",
        "device_id": "android-e021b636b7941859"
    },
    "device_settings": {
        "app_version": "269.0.0.18.75",
        "android_version": 26,
        "android_release": "8.0.0",
        "dpi": "480dpi",
        "resolution": "1080x1920",
        "manufacturer": "OnePlus",
        "device": "ONEPLUS A3010",
        "model": "OnePlus3T",
        "cpu": "qcom",
        "version_code": "314665256"
    },
    "user_agent": "Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; OnePlus; ONEPLUS A3010; OnePlus3T; qcom; en_US; 314665256)"
})

try:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")
    print("✅ Login ho gaya! session.json save ho gaya.")

except ChallengeRequired:
    print("⚠️  Instagram ne challenge maanga...")
    cl.challenge_resolve(cl.last_json)

    method = input("Email ya Phone? (email/phone): ").strip()
    if method == "email":
        cl.challenge_send_email(cl.last_json)
    else:
        cl.challenge_send_phone(cl.last_json)

    code = input("Instagram ka OTP code daalo: ").strip()
    cl.challenge_resolve_enter_code(cl.last_json, code)

    cl.dump_settings("session.json")
    print("✅ Challenge solve ho gaya! session.json save ho gaya.")

except Exception as e:
    print(f"❌ Error: {e}")