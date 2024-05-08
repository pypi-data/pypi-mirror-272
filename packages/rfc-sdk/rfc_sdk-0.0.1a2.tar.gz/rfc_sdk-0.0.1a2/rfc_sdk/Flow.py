from __future__ import annotations
from rfc_sdk.utils.createApiCaller import TIMEOUT, createApiCaller
import logging
import time
from threading import Timer


class Flow:
    def __init__(self, flowId: str, flowKey: str | None = None, userKey: str | None = None, baseUrl: str | None = None):
        """
        Start using your flow in the SDK by passing your RFCloud flow key/ user key

        Parameters
        ----------
        flowId : string
            Flow ID
        flowKey : string
            Flow key obtained from RFCloud Dashboard
        userKey : string
            User key obtained from RFCloud Dashboard
        """
        if (flowKey and not flowKey.startswith("FLOW-")):
            raise ValueError("Invalid flow key")
        if (userKey and not userKey.startswith("USER-")):
            raise ValueError("Invalid user key")
        apiKey = flowKey if flowKey else userKey
        if (not apiKey):
            raise ValueError("Either flowKey or userKey must be provided")

        self._apiCaller = createApiCaller(apiKey, baseUrl)

        self.flowId = flowId

        self._streamUrls = None

        self._isSubscribed = False
        self._lastGetOutputAt = 0
        self._listenerTimer = None

    def getStreamUrls(self):
        """
        Get the stream URLs
        If this is a push flow, check the containing pushUrls
        e.g. [
            "rtmp://stream.randomforest.cloud/FLOW-...",
            "rtsp://stream.randomforest.cloud/FLOW-...",
        ]
        If this is a pull flow, check the containing pullUrl
        e.g. "rtmp://camera.example.com/live1"
        """
        if (self._streamUrls):
            return self._streamUrls
        resp = self._apiCaller.get(
            f"flow/{self.flowId}/secrets", timeout=TIMEOUT)
        resp.raise_for_status()

        json = resp.json()
        print(json)
        self._streamUrls = {
            'pushUrls': json.get('pushUrls'),
            'pullUrl': json.get('pullUrl')
        }
        return self._streamUrls

    def getOutput(self, engine: str = 'object_detection', classes: list[str] | None = None, withFrames: bool = False):
        """
        One-shot call to get the output
        Note: Your flow should be inferencing

        Parameters
        ----------
        engine : string
            Engine to use. Only accepted value: "object_detection"
        classes : string[]
            Classes to filter. See the complete list at [src/CocoClasses.ts](js/src/CocoClasses.ts) or [dist/CocoClasses.d.ts](js/dist/CocoClasses.d.ts). Code completion should be available in your IDE.
        withFrames : boolean
            Whether you want to get the latest video frame if available. Video frame is not guaranteed even if you pass `true`
        """
        resp = self._apiCaller.get(f"flow/{self.flowId}/output", params={
            'engine': engine,
            'classes[]': classes,
            'withFrames': 'true' if withFrames else None
        }, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()

    def subscribe(self, minimumInterval: int = 1000, requestOptions={}, callbackBatchResult: callable | None = None, callbackSingleResult: callable | None = None):
        """
        Subscribe to the flow inference output
        Provide at least one of callbackBatchResult or callbackSingleResult
        Note: You should always unsubscribe when you're done in order to avoid unintentional costs

        Parameters
        ----------
        minimumInterval : number
            Minimum interval in milliseconds, minimum 1000ms. Calculated with (time taken to get output + time taken for all callbacks to finish)
        callbackBatchResult : callable
            Callback function with batch result (empty array if no result). See the output array of flow.getOutput
        callbackSingleResult : callable
            Callback function with single result (null if no result). See the output array element of flow.getOutput
        requestOptions : dict
            Options to pass to getOutput. See the parameters of flow.getOutput

        Returns
        -------
        unsubscribe : callable
            Function to unsubscribe from the flow inference output
        """
        interval = minimumInterval or 1000
        if (interval < 1000):
            raise ValueError("Minimum interval is 1000ms")

        if (not callable(callbackBatchResult) and not callable(callbackSingleResult)):
            raise ValueError(
                "At least one of callbackBatchResult or callbackSingleResult must be provided")

        if (self._isSubscribed):
            raise ValueError("Already subscribed")

        self._isSubscribed = True
        self._lastGetOutputAt = 0

        try:
            self.setStreamInferencing(True)
        except:
            self._isSubscribed = False
            raise ValueError("Error starting stream inferencing")

        def getOutputNow():
            if (not self._isSubscribed):
                self._lastGetOutputAt = 0
                return

            if (self._listenerTimer):
                self._listenerTimer.cancel()
                self._listenerTimer = None
            self._lastGetOutputAt = time.time() * 1000

            try:
                output = self.getOutput(**requestOptions)
                if (callbackBatchResult):
                    callbackBatchResult(output)
                if (callbackSingleResult):
                    if (len(output) == 0):
                        callbackSingleResult(None)
                    else:
                        for singleResult in output:
                            try:
                                callbackSingleResult(singleResult)
                            except:
                                logging.exception(
                                    "Error handling single result")

            except:
                logging.exception("Error getting output")
            finally:
                if (not self._isSubscribed):
                    return

                if (time.time()*1000 - self._lastGetOutputAt < interval):
                    self._listenerTimer = Timer(
                        (interval - (time.time()*1000 - self._lastGetOutputAt))/1000, getOutputNow)
                    self._listenerTimer.start()
                else:
                    getOutputNow()

        getOutputNow()

        return self.unsubscribe

    def unsubscribe(self):
        """
        Unsubscribe from the flow inference output
        """
        if (not self._isSubscribed):
            raise ValueError("Already unsubscribed")

        self._lastGetOutputAt = 0
        if (self._listenerTimer):
            self._listenerTimer.cancel()
            self._listenerTimer = None
        try:
            self.setStreamInferencing(False)
        except:
            raise ValueError("Error stopping stream inferencing")
        finally:
            self._isSubscribed = False

    def setStreamInferencing(self, status: bool):
        """
        Set stream inferencing
        Starting a started flow throws error
        Stopping a stopped flow throws error
        """
        fn = self._apiCaller.post if status else self._apiCaller.delete
        resp = fn(f"flow/{self.flowId}/infer", timeout=TIMEOUT)
        resp.raise_for_status()

    def __str__(self):
        return f"Flow {self.flowId}, streamUrl: {self._streamUrls}, isListening: {self._isSubscribed}"
