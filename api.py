import requests
import time


class ListenBrainz:
    def __init__(self, token=""):
        self.ROOT = "https://api.listenbrainz.org"
        self.token = token
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Token {token}"
        try:
            self.token_valid, self.token_username = self._validate_token()
            print(f"Successfully validated ListenBrainz token as {self.token_valid} as user {self.token_username} with token {self.token[0:5]}...{self.token[-5:]}")
        except Exception as e:
            raise ValueError("Invalid ListenBrainz token") from e

    def _validate_token(self) -> tuple[bool, str]:
        response = self.session.get(f"{self.ROOT}/1/validate-token")
        response.raise_for_status()
        return response.json()["valid"], response.json()["user_name"]

    """
        POST METHODS
    """

    def submit_listen(self, listen_type, payload) -> dict:
        # listen_type: either of 'single', 'import' or 'playing_now'
        # single: a single listen submission
        # import: a batch submission of listens
        # playing_now: a listen submission for a track that is currently being played

        response = requests.post(
            url="{0}/1/submit-listens".format(self.ROOT),
            json={
                "listen_type": listen_type,
                "payload": payload,
            },
            headers={
                "Authorization": "Token {0}".format(self.token)
            }
        )
        response.raise_for_status()
        return response.json()

    def payload_creator(self, artist, track, release, listenTime=time.time()) -> list:
        payload = [
        {
            "listened_at": int(listenTime),
            "track_metadata": {
                "artist_name": artist,
                "track_name": track,
                "release_name": release,
            }
        }
        ]
        return payload

    def submit_feedback(self, recording_mbid: str, score: int) -> dict:
        response = self.session.post(
            f"{self.ROOT}/1/feedback/recording-feedback",
            json={
                "recording_mbid": recording_mbid,
                "score": score,
            },
        )

        response.raise_for_status()
        return response.json()

    def clear_tokens_playing_now(self) -> dict:
        response = self.session.post(
            f"{self.ROOT}/1/playing-now/delete",
        )

        response.raise_for_status()
        return response.json()

    def delete_listen(self, listened_at: int, recording_mbid: str) -> dict:
        response = self.session.delete(
            f"{self.ROOT}/1/delete-listen",
            json={
                "listened_at": listened_at,
                "recording_mbid": recording_mbid
            }
        )

        response.raise_for_status()
        return response.json()
    
    """
        GET METHODS
    """

    def get_listens(self, username, min_ts=None, max_ts=None, count=None):
        if min_ts is not None and max_ts is not None:
            raise ValueError("Only one of min_ts or max_ts may be specified. ListenBrainz API limitation.")

        response = self.session.get(
            f"{self.ROOT}/1/user/{username}/listens",
            params={
                "min_ts": min_ts,
                "max_ts": max_ts,
                "count": count,
            },
        )

        response.raise_for_status()
        return response.json()["payload"]["listens"]

    def lookup_metadata(self, track_name: str, artist_name: str, incs: str | None = None) -> dict:
        params: dict[str, str | bool] = {
            "recording_name": track_name,
            "artist_name": artist_name,
        }

        if incs:
            params["metadata"] = True
            params["incs"] = incs

        response = self.session.get(
            f"{self.ROOT}/1/metadata/lookup/",
            params=params,
        )

        response.raise_for_status()
        return response.json()

    def search_users(self, user_search):
        response = self.session.get(
            f"{self.ROOT}/1/search/users",
            params={
                "search_term": user_search,
            },
        )

        response.raise_for_status()
        return response.json()

    def get_user_listen_count(self, username) -> int:
        response = self.session.get(
            f"{self.ROOT}/1/user/{username}/listen-count",
        )

        response.raise_for_status()
        return response.json()["payload"]["count"]

    def get_users_current_listen(self, username) -> dict:
        response = self.session.get(
            f"{self.ROOT}/1/user/{username}/playing-now",
        )

        response.raise_for_status()
        return response.json()["payload"]

    def get_similar_users(self, username) -> dict:
        response = self.session.get(
            f"{self.ROOT}/1/user/{username}/similar-users",
            params={
                "user_name": username,
            }
        )

        response.raise_for_status()
        return response.json()["payload"]

    def compare_user_similarities(self, user1, user2) -> dict:
        response = self.session.get(
            f"{self.ROOT}/1/user/{user1}/similar-to/{user2}",
            params={
                "user_name": user1,
                "other_user_name": user2,
            }
        )

        response.raise_for_status()
        return response.json()["payload"]