from typing import Any, cast

from django.http import HttpRequest
from django.views.generic import RedirectView

NAVER_CALLBACK_URL = "/auth/naver/callback/"
NAVER_STATE = "naver_login"
NAVER_LOGIN_URL = "https://nid.naver.com/oauth2.0/authorize"


class NaverLoginRedirectView(RedirectView):
    def get_redirect_url(self, request: HttpRequest, *args: tuple[Any, ...], **kwargs: dict[str, Any]) -> str:
        scheme = request.scheme or "http"
        host = request.META.get("HTTP_HOST", "")
        domain = scheme + "://" + host
        callback_url = cast(str, domain + NAVER_CALLBACK_URL)
        return callback_url
