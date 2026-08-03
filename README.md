# listenbrainzhook

A lightweight Python wrapper for the ListenBrainz API.

`listenbrainzhook` provides a simple interface for interacting with the ListenBrainz API without having to manually construct HTTP requests. It handles authentication, session management, request formatting, and response parsing while exposing a clean, Pythonic API.

## Features

* Automatic token validation during client initialisation
* Persistent authenticated session
* Submit listens and "playing now" updates
* Create correctly formatted listen payloads
* Retrieve a user's listening history
* Search for ListenBrainz users
* Retrieve currently playing tracks
* Look up recording metadata
* Find similar users and compare user similarity
* Submit recording feedback
* Delete listens and clear playing status

## Installation

```bash
pip install listenbrainzhook
```

## Quick Start

```python
from listenbrainzhook import ListenBrainz

lb = ListenBrainz("YOUR_TOKEN")
```

## Authentication

Authentication is performed when the client is created. If the supplied token is invalid, a `ValueError` is raised.

```python
lb = ListenBrainz("YOUR_TOKEN")
```

Once authenticated, the following attributes are available:

* `token_valid`
* `token_username`

## API Reference

### Authentication

| Method              | Description                       |
| ------------------- | --------------------------------- |
| `_validate_token()` | Validate an authentication token. |

### Listen Submission

| Method              | Description                                  |
| ------------------- | -------------------------------------------- |
| `submit_listen()`   | Submit one or more listens to ListenBrainz.  |
| `payload_creator()` | Create a correctly formatted listen payload. |

Example:

```python
from listenbrainzhook import ListenBrainz

lb = ListenBrainz("YOUR_TOKEN")

payload = lb.payload_creator("Jamiroquai", "Virtual Insanity", "Travelling Without Moving") # Artist, Title, Release
response = lb.submit_listen("single", payload)
```

### Listen Management

| Method                       | Description                                    |
| ---------------------------- | ---------------------------------------------- |
| `get_listens()`              | Retrieve a user's listening history.           |
| `delete_listen()`            | Delete a previously submitted listen.          |
| `clear_tokens_playing_now()` | Clear the authenticated user's playing status. |

Example:

```python
from listenbrainzhook import ListenBrainz
import json

lb = ListenBrainz("YOUR_TOKEN")

listenHistory = lb.get_listens("benjjvi", min_ts=1785542400, count=10) #use min_ts for the minimum submitted time, or max for opposite
print(json.dumps(listenHistory))

lb.delete_listen(1785542400, "recording-mbid") #deletes listen for the user whos token was used

lb.clear_tokens_playing_now()
```

### Users

| Method                       | Description                              |
| ---------------------------- | ---------------------------------------- |
| `search_users()`             | Search for ListenBrainz users.           |
| `get_user_listen_count()`    | Retrieve a user's total listen count.    |
| `get_users_current_listen()` | Retrieve a user's current playing track. |

Example:

```python
from listenbrainzhook import ListenBrainz

lb = ListenBrainz("YOUR_TOKEN")

print(lb.search_users("benjjvi"))
print(lb.get_user_listen_count("benjjvi"))
print(lb.get_users_current_listen("benjjvi"))
```

### Metadata

| Method              | Description                       |
| ------------------- | --------------------------------- |
| `lookup_metadata()` | Look up metadata for a recording. |

Example:

```python
from listenbrainzhook import ListenBrainz
import json

lb = ListenBrainz("YOUR_TOKEN")

meta = lb.lookup_metadata("Virtual Insanity", "Jamiroquai")
print(json.dumps(meta))
```

### Social

| Method                        | Description                                   |
| ----------------------------- | --------------------------------------------- |
| `get_similar_users()`         | Retrieve users with similar listening habits. |
| `compare_user_similarities()` | Compare two users' listening similarity.      |

Example:

```python
from listenbrainzhook import ListenBrainz
import json

lb = ListenBrainz("YOUR_TOKEN")

similars = lb.get_similar_users("benjjvi")
print(json.dumps(similars))

comparison = lb.compare_user_similarities("benjjvi", "cuylerotsuka")
print(json.dumps(comparison))
```

### Feedback

| Method              | Description                      |
| ------------------- | -------------------------------- |
| `submit_feedback()` | Submit feedback for a recording. |

Example:

```python
from listenbrainzhook import ListenBrainz

lb = ListenBrainz("YOUR_TOKEN")

response = lb.submit_feedback("recording-mbid", 1) #1 like, 0 neutral, -1 dislike
```

## Error Handling

All requests call `raise_for_status()`, allowing HTTP errors returned by the ListenBrainz API to propagate as standard `requests` exceptions.

Client initialisation raises a `ValueError` if the supplied authentication token is invalid.

## Requirements

* Python 3.10 or later
* requests

## Contributing

Contributions are welcome. If you encounter a bug or would like to request an additional API endpoint, please open an issue or submit a pull request.

## AI Usage

AI has been a topic of consideration when building this project. AI tools used include VSC IntelliSense/IntelliCode, GitHub Copilot, and ChatGPT (to generate parts of this README document.)

When AI has been utilised, thought was put in to consider the ethical usage of such products, and the environmental impact.

In projects where this API is used, it would be appreciated that you put in similar considerations.

This project was NOT built by AI. AI was used to help assist with questions, explain code, demonstrate fixes, and automate repetitive tasks.

## License

This project is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE v3.

ListenBrainz is developed by the MetaBrainz Foundation. This project is an independent Python wrapper and is not affiliated with or endorsed by the ListenBrainz project.