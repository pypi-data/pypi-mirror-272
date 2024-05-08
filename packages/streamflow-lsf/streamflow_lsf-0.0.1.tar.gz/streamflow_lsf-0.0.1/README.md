# LSF Plugin for StreamFlow

## Installation
Simply install the package directory from [PyPI]() using [pip](https://pip.pypa.io/en/stable/). StreamFlow will automatically recognise it as a plugin and load it at each workflow execution.
```bash
pip install streamflow-lsf
```

If everything worked correctly, whenever a workflow execution start the following message should be printed in the log:
```bash
Successfully registered plugin streamflow_lsf.plugin.LSFStreamFlowPlugin
```

## Usage
This plugin registers a new `Connector` component, called `LSFConnector`, which extends the StreamFlow `ConnectorWrapper` class. This implies that the `LSFConnector` can wrap an underlying `Connector` object through the `wraps` directive. The example below shows a possible `streamflow.yml` configuration file, where the `LSFConnector` wraps an `SSHConnector` for remote execution offloading.
```bash
deployments:
  ssh-deplyoment:
    type: ssh
    config:
      nodes:
        - 10.0.0.1
        - 10.0.0.2
      sshKey: /path/to/ssh/key
      username: <username>
  lsf-deployment:
    type: unito.lsf
    config: {}
    wraps: ssh-deplyoment
```