from django.views.generic import RedirectView

NAVER_CALLBACK_URL = "/naver/callback/"
NAVER_STATE = "naver_login"
NAVER_LOGIN_URL = "https://nid.naver.com/oauth2.0/authorize"


class NaverLoginRedirectView(RedirectView):
    def get_redirect_url(self, args, **kwargs):
        domain = self.request.scheme + "://" + self.request.META.get("HTTP_HOST", "")
        callback_url = domain + NAVER_CALLBACK_URL
