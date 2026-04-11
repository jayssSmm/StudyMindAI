from app.extensions import redis_client

def guest_limit_reached(guest_id, limit=5):
    key = f"guest_limit:{guest_id}"

    current = redis_client.get(key)

    if current is None:
        redis_client.set(key, 1)
        return False

    if int(current) >= limit:
        return True

    redis_client.incr(key)
    return False