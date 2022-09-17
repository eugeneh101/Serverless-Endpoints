from aws_cdk import (
    Duration,
    Stack,
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
)
from constructs import Construct


class ServerlessEndpointsStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, environment: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.endpoints_lambda = _lambda.Function(
            self,
            "EndpointsLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset(
                "source/endpoints", exclude=[".venv/*", "tests/*"]
            ),
            handler="handler.lambda_handler",
            timeout=Duration.seconds(1),  # should be effectively instantaneous
            memory_size=128,  # in MB
        )

        # dependency: API Gateway, lambda layer
        apigateway.LambdaRestApi(self, "ApiGateway", handler=self.endpoints_lambda)
        powertools_layer = _lambda.LayerVersion.from_layer_version_arn(
            self,
            "aws_lambda_powertools",
            layer_version_arn=(
                f"arn:aws:lambda:{environment['AWS_REGION']}:"
                "017000801446:layer:AWSLambdaPowertoolsPython:29"  # might consider getting latest layer
            ),
        )
        self.endpoints_lambda.add_layers(powertools_layer)
