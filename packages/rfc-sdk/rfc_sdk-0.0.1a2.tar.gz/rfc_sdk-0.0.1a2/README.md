# RFCloud Python SDK

## Also See [RFCloud Website](https://randomforest.cloud)

## Also See [Documentation for RFCloud](https://docs.randomforest.cloud)

## Prerequisite

- An account of RFCloud. You may create one for free at https://portal.randomforest.cloud

## Installing

Using pip:

```console
$ pip install rfc-sdk
```

Using poetry:

```console
$ poetry add rfc-sdk
```

To use:

```py
from rfc_sdk import Account
from rfc_sdk import Flow
```

## Account-Level Operations

### Start Using Your Account in the SDK

Pass your RFCloud user key

Obtain your user key from the RFCloud Dashboard https://portal.randomforest.cloud/account

```py
account = Account(userKey)
```

### Get All Flows in the Account

```py
for flow in account.getFlows():
    print(flow)
    pass
```

### Get A Flow in the Account

This is a syntactic sugar for `Flow(flowId, userKey=userKey)`

Note: This does not verify your access to the Flow

```py
flow2 = account.getFlow("00000000-0000-0000-0000-000000000000")
```

### Create a Flow in the Account

```py
flow3 = account.createFlow(
    f"New Stream At {datetime.now().isoformat()} (SDK)",
    "PUSH",
    # pullUrl is not applicable for PUSH mode
)
```

```py
flow4 = account.createFlow(
    f"New Stream At {datetime.now().isoformat()} (SDK)",
    "PULL",
    "rtmp://example.com/live1")
```

## Flow-Level Operations

### Start Using Your Account in the SDK

Pass your RFCloud flow key

Obtain your flow key from the RFCloud Dashboard https://portal.randomforest.cloud/ > Select a flow

```py
flow1 = Flow(flowId, flowKey=flowKey)
```

```py
flow2 = Flow(flowId, userKey=userKey)
```

Also see [Get A Flow in the Account](#get-a-flow-in-the-account)

### Get the Stream URLs

If this is a push flow, check the containing `pushUrls`
e.g.

```py
[
  "rtmp://stream.randomforest.cloud/FLOW-...",
  "rtsp://stream.randomforest.cloud/FLOW-...",
]
```

If this is a pull flow, check the containing `pullUrl`
e.g.

```py
"rtmp://camera.example.com/live1"
```

```py
streamUrls = flow1.getStreamUrls()
streamUrls['pushUrls']
streamUrls['pullUrl']
```

### One-Shot Call to Get the Output

Note: Your flow should be inferencing

```py
batchResult = flow1.getOutput(engine='object_detection',
                              classes=['person'],
                              withFrames=True)

for singleResult in batchResult:
    print(singleResult)

    # base64-encoded JPEG, e.g. /9j/4AAQSkZJRgABAQAAA... | None
    singleResult.get("frame")
    if (singleResult.get("frame") is not None):
        decodedFrame = base64.b64decode(singleResult['frame'])
        # image_2024-01-23T080123.456000Z.jpg
        with open(f"image_{datetime.fromtimestamp(singleResult['inferenceTimestamp']/1000).strftime('%Y-%m-%dT%H:%M:%S.%fZ').replace(":", "")}.jpg", "wb") as f:
            f.write(decodedFrame)
    singleResult.inferenceTimestamp  # string
    for p in singleResult.payload:
        p.trackingId  # number
        p.get("class")  # string
        p.bounds[0]  # x, number
        p.bounds[1]  # y, number
        p.bounds[2]  # w, number
        p.bounds[3]  # h, number
        p.centroid[0]  # x, number
        p.centroid[1]  # y, number
```

Accepted parameters:

- `engine`
  - Engine to use. Only accepted value: "object_detection"
- `classes`
  - Classes to filter. See the complete list at [src/CocoClasses.ts](js/src/CocoClasses.ts) or [dist/CocoClasses.d.ts](js/dist/CocoClasses.d.ts).
- `withFrames`
  - Whether you want to get the latest video frame if available. Video frame is not guaranteed even if you pass `true`

Returns:
See above code block

### Subscribe to the Flow Inference Output

Note: You should always unsubscribe when you're done in order to avoid unintentional costs

```py
def callbackBatchResult(batchResult):
    # This callback would repeatedly be called until flowUnsubscribe(), or flow.stop() is called
    if (len(batchResult) == 0):
        # No result
        return
    for singleResult in batchResult:
        print(singleResult)


def callbackSingleResult(singleResult):
    # This callback would repeatedly be called until flowUnsubscribe(), or flow.stop() is called
    if (singleResult is None):
        # No result
        return
    print(singleResult)


# Subscribe to the flow inference output
flowUnsubscribe = flow1.subscribe(
    minimumInterval=1000,
    requestOptions={"engine": "object_detection",
                    "classes": ["person"],
                    "withFrames": True
                    },
    # Provide at least one of callbackBatchResult or callbackSingleResult
    callbackBatchResult=callbackBatchResult,
    callbackSingleResult=callbackSingleResult
)
```

Accepted parameters:

- `minimumInterval`
  - Minimum interval in milliseconds, minimum 1000ms. Calculated with (time taken to get output + time taken for all callbacks to finish)
- `callbackBatchResult`
  - Callback function with batch result (empty array if no result). See the output array of [flow.getOutput](#one-shot-call-to-get-the-output)
- `callbackSingleResult`
  - Callback function with single result (null if no result). See the output array element of [flow.getOutput](#one-shot-call-to-get-the-output)
- `requestOptions`
  - Options to pass to getOutput. See the parameters of [flow.getOutput](#one-shot-call-to-get-the-output)

Sample of single result:

```json
{
  "payload": [
    {
      "trackingId": 11,
      "class": "truck",
      "bounds": [909, 340, 935, 364],
      "centroid": [1376, 522]
    }
  ],
  "inferenceTimestamp": 1714449453312
}
```

```json
{
  "payload": [
    {
      "trackingId": 11,
      "class": "car",
      "bounds": [372, 392, 409, 421],
      "centroid": [576, 602]
    },
    {
      "trackingId": 22,
      "class": "truck",
      "bounds": [910, 339, 936, 363],
      "centroid": [1378, 520]
    }
  ],
  "inferenceTimestamp": 1714449452614
}
```

```json
{
    "payload": [
        {
            "trackingId": 11,
            "class": "truck",
            "bounds": [
                912,
                339,
                937,
                363
            ],
            "centroid": [
                1380,
                520
            ]
        }
    ],
    "frame": "/9j/4AAQSkZJRgABAQAAA...",
    "inferenceTimestamp": 1714449452614
}
```

Provide at least one of `callbackBatchResult` or `callbackSingleResult`

Returns:
Function to unsubscribe from the flow inference output

### Unsubscribe From the Flow Inference Output

```py
flow1.unsubscribe()
```

Or call the return function of [flow.subscribe](#subscribe-to-the-flow-inference-output)

```py
flowUnsubscribe()
```
