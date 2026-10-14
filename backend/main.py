import os
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

load_dotenv(Path(__file__).with_name(".env"))

app = FastAPI(title="BrandShield AI Backend")

# Local development only. Restrict allowed origins before public deployment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

PLATFORMS = [
    "Instagram", "Facebook", "YouTube", "Telegram",
    "Bluesky", "Threads", "LinkedIn", "X (Twitter)",
    "TikTok", "Reddit", "Pinterest", "Snapchat",
    "Google Play", "Apple App Store",
]

connections = {
    name: {
        "connected": False,
        "status": "not_configured",
        "message": "Connector has not been tested yet.",
    }
    for name in PLATFORMS
}


class BrandProfile(BaseModel):
    name: str
    website: Optional[HttpUrl] = None


def fetch_json(url: str):
    request = Request(
        url,
        headers={"User-Agent": "BrandShieldAI/0.1"},
    )
    with urlopen(request, timeout=12) as response:
        return response.status, json.loads(response.read().decode("utf-8"))


def set_status(platform: str, connected: bool, status: str, message: str):
    connections[platform] = {
        "connected": connected,
        "status": status,
        "message": message,
    }


def check_youtube_connection():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        set_status("YouTube", False, "not_configured",
                   "Add YOUTUBE_API_KEY to backend/.env.")
        return

    query = urlencode({
        "part": "snippet", "type": "channel", "q": "YouTube",
        "maxResults": 1, "key": api_key,
    })
    try:
        fetch_json("https://www.googleapis.com/youtube/v3/search?" + query)
        set_status("YouTube", True, "connected",
                   "YouTube Data API key verified by a successful API request.")
    except HTTPError as exc:
        message = f"YouTube API returned HTTP {exc.code}."
        if exc.code in (401, 403):
            message += " Check API key, API enablement, quota, and restrictions."
        set_status("YouTube", False, "error", message)
    except (URLError, TimeoutError, ValueError, OSError):
        set_status("YouTube", False, "error",
                   "YouTube connection test failed. Check network and API setup.")


def check_apple_connection():
    query = urlencode({"term": "Apple", "entity": "software", "limit": 1})
    try:
        fetch_json("https://itunes.apple.com/search?" + query)
        set_status("Apple App Store", True, "connected",
                   "Apple public app lookup responded successfully; no API key required.")
    except HTTPError as exc:
        set_status("Apple App Store", False, "error",
                   f"Apple public lookup returned HTTP {exc.code}.")
    except (URLError, TimeoutError, ValueError, OSError):
        set_status("Apple App Store", False, "error",
                   "Apple public lookup failed. Check network and try again.")



def refresh_configured_connections():
    check_youtube_connection()
    check_apple_connection()
    check_bluesky_connection()
    check_telegram_connection()

    for platform in PLATFORMS:
        if platform not in (
    "YouTube",
    "Apple App Store",
    "Bluesky",
    "Telegram"
):
            set_status(
                platform,
                False,
                "not_configured",
                "Connector and required platform authorization are not configured."
            )



def search_youtube(brand_name: str):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        set_status("YouTube", False, "not_configured",
                   "Add YOUTUBE_API_KEY to backend/.env.")
        return []

    query = urlencode({
        "part": "snippet", "type": "channel", "q": brand_name,
        "maxResults": 10, "key": api_key,
    })
    try:
        _, data = fetch_json("https://www.googleapis.com/youtube/v3/search?" + query)
        set_status("YouTube", True, "connected", "YouTube Data API brand search succeeded.")
        results = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            channel_id = item.get("id", {}).get("channelId")
            if not channel_id:
                continue
            results.append({
                "name": snippet.get("title", "Unknown channel"),
                "type": "Social",
                "identity": "https://www.youtube.com/channel/" + channel_id,
                "publisher": "",
                "source": "YouTube Data API",
                "evidence": [
                    "Public channel search result",
                    "Channel title returned by YouTube Data API",
                ],
            })
        return results
    except HTTPError as exc:
        message = f"YouTube API returned HTTP {exc.code}."
        if exc.code in (401, 403):
            message += " Check API key, API enablement, quota, and restrictions."
        set_status("YouTube", False, "error", message)
    except (URLError, TimeoutError, ValueError, OSError):
        set_status("YouTube", False, "error",
                   "YouTube request failed. Check network and API setup.")
    return []

def check_bluesky_connection():
    params = urlencode({"q": "BrandShieldAI", "limit": 1})
    url = "https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors?" + params

    try:
        fetch_json(url)
        set_status(
            "Bluesky",
            True,
            "connected",
            "Bluesky public actor search responded successfully."
        )
    except HTTPError as exc:
        set_status(
            "Bluesky", False, "error",
            f"Bluesky API returned HTTP {exc.code}."
        )
    except (URLError, TimeoutError, ValueError, OSError):
        set_status(
            "Bluesky", False, "error",
            "Bluesky connection failed. Check network and try again."
        )
  

def check_telegram_connection():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        set_status(
            "Telegram", False, "not_configured",
            "Add TELEGRAM_BOT_TOKEN to backend/.env."
        )
        return

    url = f"https://api.telegram.org/bot{token}/getMe"

    try:
        _, data = fetch_json(url)

        if data.get("ok") is True:
            bot_name = data.get("result", {}).get("username", "your bot")
            set_status(
                "Telegram", True, "connected",
                f"Telegram bot token verified: @{bot_name}. "
                "This verifies the bot only, not channel monitoring."
            )
        else:
            set_status(
                "Telegram", False, "error",
                "Telegram did not validate the bot token."
            )

    except HTTPError as exc:
        set_status(
            "Telegram", False, "error",
            f"Telegram API returned HTTP {exc.code}. Check the bot token."
        )
    except (URLError, TimeoutError, ValueError, OSError):
        set_status(
            "Telegram", False, "error",
            "Telegram connection failed. Check network and token setup."
        )



def search_bluesky(brand_name: str):
    params = urlencode({"q": brand_name, "limit": 10})
    url = "https://public.api.bsky.app/xrpc/app.bsky.actor.searchActors?" + params

    try:
        _, data = fetch_json(url)
        set_status(
            "Bluesky", True, "connected",
            "Bluesky public actor search succeeded."
        )

        results = []
        for actor in data.get("actors", []):
            handle = actor.get("handle")
            if not handle:
                continue

            results.append({
                "name": actor.get("displayName") or handle,
                "type": "Social",
                "identity": "https://bsky.app/profile/" + handle,
                "publisher": handle,
                "source": "Bluesky public API",
                "evidence": [
                    "Public actor search result",
                    "Profile handle returned by Bluesky API"
                ],
            })

        return results

    except HTTPError as exc:
        set_status(
            "Bluesky", False, "error",
            f"Bluesky API returned HTTP {exc.code}."
        )
    except (URLError, TimeoutError, ValueError, OSError):
        set_status(
            "Bluesky", False, "error",
            "Bluesky search failed. Check network and try again."
        )

    return []



def search_apple_apps(brand_name: str):
    params = urlencode({"term": brand_name, "entity": "software", "limit": 10})
    try:
        _, data = fetch_json("https://itunes.apple.com/search?" + params)
        set_status("Apple App Store", True, "connected",
                   "Apple public app lookup search succeeded.")
        results = []
        for item in data.get("results", []):
            results.append({
                "name": item.get("trackName", "Unknown app"),
                "type": "App",
                "identity": item.get("trackViewUrl", ""),
                "publisher": item.get("sellerName", ""),
                "source": "Apple public lookup",
                "evidence": [
                    "Public app listing search result",
                    "App name and seller returned by Apple lookup",
                ],
            })
        return results
    except HTTPError as exc:
        set_status("Apple App Store", False, "error",
                   f"Apple public lookup returned HTTP {exc.code}.")
    except (URLError, TimeoutError, ValueError, OSError):
        set_status("Apple App Store", False, "error",
                   "Apple lookup failed. Check network and try again.")
    return []


@app.get("/")
def home():
    return {"service": "BrandShield AI Backend", "running": True}


@app.get("/api/integrations/status")
def integration_status():
    refresh_configured_connections()
    connected_count = sum(1 for item in connections.values() if item["connected"])
    return {
        "integrations": connections,
        "connected_count": connected_count,
        "platform_count": len(PLATFORMS),
        "live_monitoring_enabled": connected_count > 0,
        "note": (
            "Connected means a source request succeeded. It does not mean "
            "full platform coverage or continuous monitoring. Only YouTube "
            "Data API and Apple's public app lookup are implemented here; "
            "other platforms need their own authorized connectors."
        ),
    }



@app.post("/api/scan")
def scan_brand(brand: BrandProfile):
    candidates = []
    candidates.extend(search_youtube(brand.name))
    candidates.extend(search_apple_apps(brand.name))
    candidates.extend(search_bluesky(brand.name))

    return {
        "brand": brand.name,
        "candidates": candidates,
        "sources_checked": [
            "YouTube Data API",
            "Apple public app lookup",
            "Bluesky public API"
        ],
        "message": (
            "Results are potential matches requiring human review. "
            "Only the listed sources were scanned."
        ),
    }
