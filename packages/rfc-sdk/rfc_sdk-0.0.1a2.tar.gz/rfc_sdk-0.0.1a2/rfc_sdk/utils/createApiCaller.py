from requests_toolbelt.utils import user_agent as ua
from requests_toolbelt import sessions
import logging

logging.basicConfig(level=logging.DEBUG)

TIMEOUT = 10_000


def createApiCaller(apiKey: str, baseUrl: str = ""):
    apiCaller = sessions.BaseUrlSession(
        base_url=baseUrl or "https://api.randomforest.cloud/")
    apiCaller.headers.update(
        {"X-Api-Key": apiKey, "User-Agent": ua.user_agent('rfc_sdk_py', '0.1.0')})
    # apiCaller.proxies = {
    #     "http": "http://localhost:8080",
    #     "https": "http://localhost:8080"
    # }

    return apiCaller
