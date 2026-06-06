import os
from flask import Flask
from redis import Redis

app = Flask(__name__)

# 1. Dynamically read the Redis host from environment variables.
# If 'REDIS_HOST' is not set, it defaults to 'localhost' (perfect for sidecars)
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

redis = Redis(host=redis_host, port=redis_port)

@app.route('/')
def hello():
    redis.incr('hits')
    # Note the .decode('utf-8') -> Python 3 compatibility safeguard
    return 'Hello World! I have been seen %s times.' % redis.get('hits').decode('utf-8')

if __name__ == "__main__":
    # 2. Let Cloud Run dictate the port via the PORT environment variable.
    # It defaults to 5000 if running locally or if not specified.
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
