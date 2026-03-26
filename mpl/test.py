import os
from pathlib import Path
from typing import Dict, Optional, Tuple

import requests
import tweepy
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi

from utils.security import redact_sensitive


class APIHandler:
    """Centralized posting logic for X, Instagram and Facebook."""

    def __init__(self) -> None:
        load_dotenv()
        self.twitter_api_key = os.getenv("X_API_KEY", "").strip()
        self.twitter_api_secret = os.getenv("X_API_SECRET", "").strip()
        self.twitter_access_token = os.getenv("X_ACCESS_TOKEN", "").strip()
        self.twitter_access_secret = os.getenv("X_ACCESS_SECRET", "").strip()
        self.twitter_bearer = os.getenv("X_BEARER_TOKEN", "").strip()

        self.meta_access_token = os.getenv("META_ACCESS_TOKEN", "").strip()
        self.facebook_page_id = os.getenv("FB_PAGE_ID", "").strip()
        self.instagram_user_id = os.getenv("IG_USER_ID", "").strip()
        self.instagram_public_media_base_url = os.getenv("INSTAGRAM_MEDIA_PUBLIC_BASE_URL", "").strip()

        if self.meta_access_token:
            FacebookAdsApi.init(access_token=self.meta_access_token)

    def post_to_platform(self, platform: str, text: str, media_path: Optional[str] = None) -> Tuple[bool, str]:
        try:
            if platform == "x":
                return self._post_to_x(text, media_path)
            if platform == "instagram":
                return self._post_to_instagram(text, media_path)
            if platform == "facebook":
                return self._post_to_facebook(text, media_path)
            return False, f"Desteklenmeyen platform: {platform}"
        except Exception as exc:  # noqa: BLE001
            return False, f"Platform istegi basarisiz: {redact_sensitive(str(exc))}"

    def _post_to_x(self, text: str, media_path: Optional[str]) -> Tuple[bool, str]:
        required = [
            self.twitter_api_key,
            self.twitter_api_secret,
            self.twitter_access_token,
            self.twitter_access_secret,
        ]
        if not all(required):
            return False, "X kimlik bilgileri eksik. .env dosyasini kontrol edin."

        auth = tweepy.OAuth1UserHandler(
            self.twitter_api_key,
            self.twitter_api_secret,
            self.twitter_access_token,
            self.twitter_access_secret,
        )
        v1_api = tweepy.API(auth)
        client = tweepy.Client(
            consumer_key=self.twitter_api_key,
            consumer_secret=self.twitter_api_secret,
            access_token=self.twitter_access_token,
            access_token_secret=self.twitter_access_secret,
        )
        try:
            v1_api.verify_credentials()
        except Exception as exc:  # noqa: BLE001
            return False, f"X kimlik dogrulama basarisiz: {redact_sensitive(str(exc))}"

        media_ids = None
        if media_path:
            upload_result = v1_api.media_upload(filename=media_path)
            media_ids = [upload_result.media_id]

        response = client.create_tweet(text=text, media_ids=media_ids, user_auth=True)
        tweet_id = response.data.get("id") if response and response.data else "unknown"
        return True, f"X paylasimi basarili. tweet_id={tweet_id}"

    def _post_to_facebook(self, text: str, media_path: Optional[str]) -> Tuple[bool, str]:
        if not self.meta_access_token or not self.facebook_page_id:
            return False, "Facebook kimlik bilgileri eksik. .env dosyasini kontrol edin."

        if media_path:
            endpoint = f"https://graph.facebook.com/v20.0/{self.facebook_page_id}/photos"
            with open(media_path, "rb") as image_file:
                files = {"source": image_file}
                data = {"caption": text, "access_token": self.meta_access_token}
                response = requests.post(endpoint, files=files, data=data, timeout=25)
        else:
            endpoint = f"https://graph.facebook.com/v20.0/{self.facebook_page_id}/feed"
            data = {"message": text, "access_token": self.meta_access_token}
            response = requests.post(endpoint, data=data, timeout=25)

        payload = response.json()
        if response.ok and payload.get("id"):
            return True, f"Facebook paylasimi basarili. id={payload['id']}"

        return False, f"Facebook hatasi: {redact_sensitive(str(payload))}"

    def _post_to_instagram(self, text: str, media_path: Optional[str]) -> Tuple[bool, str]:
        if not self.meta_access_token or not self.instagram_user_id:
            return False, "Instagram kimlik bilgileri eksik. .env dosyasini kontrol edin."
        if not media_path:
            return False, "Instagram gorsel gerektirir."

        image_url = self._build_public_media_url(media_path)
        if not image_url:
            return (
                False,
                "Instagram icin kamuya acik medya URL gerekli. INSTAGRAM_MEDIA_PUBLIC_BASE_URL ayarlanmali.",
            )

        create_container_endpoint = f"https://graph.facebook.com/v20.0/{self.instagram_user_id}/media"
        create_payload = {
            "image_url": image_url,
            "caption": text,
            "access_token": self.meta_access_token,
        }
        container_response = requests.post(create_container_endpoint, data=create_payload, timeout=25)
        container_data = container_response.json()
        creation_id = container_data.get("id")

        if not container_response.ok or not creation_id:
            return False, f"Instagram container hatasi: {redact_sensitive(str(container_data))}"

        publish_endpoint = f"https://graph.facebook.com/v20.0/{self.instagram_user_id}/media_publish"
        publish_payload = {"creation_id": creation_id, "access_token": self.meta_access_token}
        publish_response = requests.post(publish_endpoint, data=publish_payload, timeout=25)
        publish_data = publish_response.json()

        if publish_response.ok and publish_data.get("id"):
            return True, f"Instagram paylasimi basarili. id={publish_data['id']}"
        return False, f"Instagram publish hatasi: {redact_sensitive(str(publish_data))}"

    def _build_public_media_url(self, media_path: str) -> Optional[str]:
        if not self.instagram_public_media_base_url:
            return None
        base_url = self.instagram_public_media_base_url.rstrip("/")
        filename = Path(media_path).name
        return f"{base_url}/{filename}"

    def get_scope_guidance(self) -> Dict[str, str]:
        """Returns minimal permission guidance for least privilege setup."""
        return {
            "x": "tweet.read tweet.write users.read",
            "facebook": "pages_manage_posts pages_read_engagement",
            "instagram": "instagram_basic instagram_content_publish pages_read_engagement",
        }
