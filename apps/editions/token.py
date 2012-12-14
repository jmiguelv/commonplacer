import datetime
import jwt

# Replace these with your details
CONSUMER_KEY = '610c1aecc1f14f0b8e0bd6d7867c2512'
CONSUMER_SECRET = 'd5c6ef78-090c-40cf-a412-d63dee0f0f6d'

# Only change this if you're sure you know what you're doing
CONSUMER_TTL = 86400

ZERO = datetime.timedelta(0)
class Utc(datetime.tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
UTC = Utc()

def generate_token(user_id):
    payload = {
        'consumerKey': CONSUMER_KEY,
        'userId': user_id,
        'issuedAt': _now().isoformat(),
        'ttl': CONSUMER_TTL
    }

    return jwt.encode(payload, CONSUMER_SECRET)

def _now():
    return datetime.datetime.now(UTC).replace(microsecond=0)
