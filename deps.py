from cookie import suno_auth, keep_alive


def get_token():
    keep_alive(suno_auth)
    token = suno_auth.get_token()
    return token
