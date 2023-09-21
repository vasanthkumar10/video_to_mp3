import pika, json


def upload(f, fs, channel, access_token):
    try:
        fid = fs.put(f)
    except Exception as err:
        return f"Internal server error - {err}", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access_token["username"]
    }

    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception as err:
        fs.delete(fid)
        return f"Internal server error - {err}", 500
