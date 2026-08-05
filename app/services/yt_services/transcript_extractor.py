import os
import re
import requests
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

# All recognized YouTube hostnames
_YT_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtube-nocookie.com",
    "www.youtube-nocookie.com",
    "youtu.be",
}

# Path prefixes that carry the video ID as the next path segment
_PATH_ID_PREFIXES = ("/shorts/", "/live/", "/embed/", "/e/", "/v/")


def _is_youtube_url(token: str) -> bool:
    """Return True if the token looks like a YouTube URL we can handle."""
    try:
        parsed = urlparse(token)
        return parsed.scheme in ("http", "https") and parsed.netloc in _YT_HOSTS
    except Exception:
        return False


def extract_video_id(url: str) -> str | None:
    """
    Extract the YouTube video ID from any supported URL format.

    Supported:
        https://youtu.be/<id>
        https://www.youtube.com/watch?v=<id>
        https://m.youtube.com/watch?v=<id>
        https://music.youtube.com/watch?v=<id>
        https://youtube.com/shorts/<id>
        https://youtube.com/live/<id>
        https://youtube.com/embed/<id>
        https://youtube.com/e/<id>
        https://youtube.com/v/<id>
        https://youtube-nocookie.com/embed/<id>

    Returns None if no valid ID can be extracted.
    """
    try:
        parsed = urlparse(url)
    except Exception:
        return None

    if parsed.netloc not in _YT_HOSTS:
        return None

    path = parsed.path  # e.g. "/watch", "/shorts/abc123"

    # youtu.be/<id>
    if parsed.netloc == "youtu.be":
        video_id = path.lstrip("/").split("/")[0]
        return video_id or None

    # Path-based formats: /shorts/<id>, /live/<id>, /embed/<id>, /e/<id>, /v/<id>
    for prefix in _PATH_ID_PREFIXES:
        if path.startswith(prefix):
            video_id = path[len(prefix):].split("/")[0]
            return video_id or None

    # Standard watch URL: ?v=<id>
    qs = parse_qs(parsed.query)
    if "v" in qs:
        return qs["v"][0]  # parse_qs already handles multiple values

    return None


def is_youtube_prompt(prompt: str) -> bool:
    """
    Return True if any token in the prompt is a recognizable YouTube URL.
    Replaces the fragile `"youtube.com/watch" in prompt or "youtu.be/" in prompt` check.
    """
    for token in prompt.split():
        if _is_youtube_url(token) and extract_video_id(token) is not None:
            return True
    return False


def _extract_url_from_prompt(prompt: str) -> str | None:
    """Pull the first valid YouTube URL out of a mixed prompt string."""
    for token in prompt.split():
        if _is_youtube_url(token) and extract_video_id(token) is not None:
            return token
    return None


def extract_rest_prompt(prompt: str) -> str:
    """
    Return the non-URL portion of the prompt (the user's actual question).
    Works regardless of whether the URL appears at the start, middle, or end.
    """
    url = _extract_url_from_prompt(prompt)
    if url is None:
        return prompt
    # Remove the URL token and collapse extra whitespace
    return re.sub(r"\s+", " ", prompt.replace(url, "")).strip()


def get_transcript(prompt_or_url: str) -> str:
    """
    Fetch the transcript for the YouTube video found in `prompt_or_url`.

    Raises:
        ValueError: if no valid YouTube video ID can be found.
        requests.HTTPError: on non-2xx API responses.
    """
    url = _extract_url_from_prompt(prompt_or_url) or prompt_or_url
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError(
            f"Could not extract a YouTube video ID from: {prompt_or_url!r}\n"
            f"Supported formats: youtu.be/<id>, youtube.com/watch?v=<id>, "
            f"youtube.com/shorts/<id>, youtube.com/live/<id>, youtube.com/embed/<id>"
        )

    api_key = os.getenv("SUPADATA_API_KEY")
    if not api_key:
        raise EnvironmentError("SUPADATA_API_KEY is not set in environment / .env file")

    response = requests.get(
        "https://api.supadata.ai/v1/youtube/transcript",
        params={"videoId": video_id, "text": True},
        headers={"x-api-key": api_key},
        timeout=15,
    )
    response.raise_for_status()

    data = response.json()
    content = data.get("content")
    if not content:
        raise ValueError(f"No transcript content returned for video ID: {video_id}")

    return " ".join(str(chunk["text"]) for chunk in content)