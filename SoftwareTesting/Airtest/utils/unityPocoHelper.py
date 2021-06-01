from poco.drivers.unity3d.unity3d_poco import UnityPoco


class unityError(UnityPoco):
    def __init__(self):
        super(unityError, self).__init__()

    def GetErrorMsg(self):
        client = self.agent.rpc
        if client is None:
            return
        msg = client.call("GetLogMessage").wait()
        return msg[0]
