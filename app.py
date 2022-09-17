#!/usr/bin/env python3
import aws_cdk as cdk

from cdk_infrastructure import ServerlessEndpointsStack


app = cdk.App()
environment: dict = app.node.try_get_context("environment")
env = cdk.Environment(region=environment["AWS_REGION"])
ServerlessEndpointsStack(
    app, "ServerlessEndpointsStack", environment=environment, env=env
)
app.synth()
