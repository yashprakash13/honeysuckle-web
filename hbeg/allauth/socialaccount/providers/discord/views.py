import requests

from allauth.socialaccount.providers.discord.provider import DiscordProvider
from allauth.socialaccount.providers.oauth2.views import (
    OAuth2Adapter,
    OAuth2CallbackView,
    OAuth2LoginView,
)


class DiscordOAuth2Adapter(OAuth2Adapter):
    provider_id = DiscordProvider.id
    access_token_url = "https://discord.com/api/oauth2/token"
    authorize_url = "https://discord.com/api/oauth2/authorize"
    profile_url = "https://discord.com/api/users/@me"
    all_guilds_url = "https://discord.com/api/users/@me/guilds"

    def complete_login(self, request, app, token, **kwargs):
        headers = {
            "Authorization": "Bearer {0}".format(token.token),
            "Content-Type": "application/json",
        }
        extra_data = requests.get(self.profile_url, headers=headers).json()
        all_guilds = requests.get(self.all_guilds_url, headers=headers)
        all_guilds = all_guilds.json()

        try:
            if_3h_member = next(guild for guild in all_guilds if guild["id"] == '685366333319151636')
            if len(if_3h_member) > 0:
                extra_data['if_3h_member'] = 'True'
        except StopIteration:
            extra_data['if_3h_member'] = 'False'

        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth2_login = OAuth2LoginView.adapter_view(DiscordOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(DiscordOAuth2Adapter)

