from streamflow.ext.plugin import StreamFlowPlugin

from streamflow_lsf.connector import LSFConnector


class LSFStreamFlowPlugin(StreamFlowPlugin):
    def register(self) -> None:
        self.register_connector("unito.lsf", LSFConnector)
