from rfc_sdk.Flow import Flow
from rfc_sdk.utils.createApiCaller import TIMEOUT, createApiCaller
from datetime import datetime



class Account:
    def __init__(self, userKey: str, baseUrl: str = ""):
        """
        Start using your account in the SDK by passing your RFCloud user key

        Parameters
        ----------
        userKey : string
            Your user key obtained from the RFCloud Dashboard https://portal.randomforest.cloud/account
        """
        if (not userKey.startswith("USER-")):
            raise ValueError("Invalid user key")

        self._apiCaller = createApiCaller(userKey, baseUrl)

        self._userKey = userKey

    def getFlows(self):
        """
        Get all flows in the account
        """
        resp = self._apiCaller.get("flow", timeout=TIMEOUT)
        resp.raise_for_status()
        x = resp.json()

        print(x)

        return map(lambda flow: Flow(flow['id'], userKey=self._userKey, baseUrl=self._apiCaller.base_url), x)

    def getFlow(self, id: str):
        """
        Get a flow in the account
        This is a syntactic sugar for `new Flow({ flowId, userKey })`
        Note: This does not verify your access to the Flow

        Parameters
        ----------
        id : string
            Flow ID 
        """
        return Flow(id, userKey=self._userKey, baseUrl=self._apiCaller.base_url)

    def createFlow(self, name: str = "", mode: str = "PUSH", pullUrl: str = "", plan: str = "PAY_AS_YOU_GO"):
        """
        Create a new flow in the account

        Parameters
        ----------
        name : string
            Flow name
        mode : string
            "PUSH" | "PULL"
        pullUrl : string
            URL to pull data from (only applicable in PULL mode)
        plan : string
            Flow plan
            "PAY_AS_YOU_GO" | "RESERVED"
        """
        if (mode != "PULL" and pullUrl):
            raise ValueError("pullUrl is only applicable in PULL mode")
        if (mode == "PULL" and not pullUrl):
            raise ValueError("pullUrl is required for PULL mode")

        resp = self._apiCaller.post("flow", json={
            'name': name or f"New Stream At {datetime.now().isoformat()} (SDK)",
            'plan': plan or "PAY_AS_YOU_GO",
            'mode': mode,
            **({'pullUrl': pullUrl} if mode == "PULL" else {})
        }, timeout=TIMEOUT)
        resp.raise_for_status()
        x = resp.json()

        return Flow(x['id'], flowKey=x['secrets']['apiKey'], baseUrl=self._apiCaller.base_url)
