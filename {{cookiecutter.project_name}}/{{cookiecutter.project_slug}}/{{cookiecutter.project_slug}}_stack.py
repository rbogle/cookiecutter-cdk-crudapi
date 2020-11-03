from aws_cdk import core
from aws_cdk import aws_lambda
from aws_cdk import aws_apigatewayv2 as apigw2
from aws_cdk import aws_dynamodb as ddb
from aws_cdk import aws_iam as iam
from aws_cdk import aws_events

class {{ cookiecutter.project_class }}Stack(core.Stack):
    def __init__(self, scope: core.Construct, id_: str, **kwargs) -> None:
        super().__init__(scope, id_, **kwargs)

        # create account database 
        ddb_table  = ddb.Table(
            self, 
            "{{cookiecutter.api_domain}}-api-ddb-table",
            partition_key=ddb.Attribute(
                name='id', 
                type=ddb.AttributeType.NUMBER
            )
        )

        # create http api-gw
        http_api = apigw2.HttpApi(
            self,
            "{{cookiecutter.api_domain}}-http-api-gw"
        )

        # iam policy for making custom events by Create, Update, and Delete
        event_policy = iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=['*'], actions=['events:PutEvents'])

        # create account lambda
        api_create = aws_lambda.Function(
            self, 
            "{{cookiecutter.api_domain}}-api-create",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="create.handler",
            code=aws_lambda.Code.from_asset("lambdas/api"),
            timeout=core.Duration.seconds(30),
            environment = dict(DDB_TABLE_NAME=ddb_table.table_name),
        )
        # allow lambda to publish custom events
        api_create.add_to_role_policy(event_policy)
        # allow lambda to write to ddb        
        ddb_table.grant_read_write_data(api_create)
        # create lambda integration and configure route
        api_create_int = apigw2.LambdaProxyIntegration(handler=api_create)
        http_api.add_routes(
            path="/{{cookiecutter.api_domain}}",
            methods=[apigw2.HttpMethod.POST],
            integration=api_create_int
        )

        # read one/all lambda
        api_read = aws_lambda.Function(
            self, 
            "{{cookiecutter.api_domain}}-api-read",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="read.handler",
            code=aws_lambda.Code.from_asset("lambdas/api"),
            timeout=core.Duration.seconds(30),
            environment = dict(DDB_TABLE_NAME=ddb_table.table_name),
        )
        # allow lambda to write to ddb
        ddb_table.grant_read_data(api_read)
        # create lambda integration and configure route
        api_read_int = apigw2.LambdaProxyIntegration(handler=api_read)
        http_api.add_routes(
            path="/{{cookiecutter.api_domain}}",
            methods=[apigw2.HttpMethod.GET],
            integration=api_read_int
        )
        http_api.add_routes(
            path="/{{cookiecutter.api_domain}}/{id}",
            methods=[apigw2.HttpMethod.GET],
            integration=api_read_int
        )

        # update account lambda
        api_update = aws_lambda.Function(
            self, 
            "{{cookiecutter.api_domain}}-api-update",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="update.handler",
            code=aws_lambda.Code.from_asset("lambdas/api"),
            timeout=core.Duration.seconds(30),
            environment = dict(DDB_TABLE_NAME=ddb_table.table_name),
        )
        # allow lambda to publish custom events
        api_update.add_to_role_policy(event_policy)
        # allow lambda to write to ddb
        ddb_table.grant_read_write_data(api_update)
        # create lambda integration and configure route
        api_update_int = apigw2.LambdaProxyIntegration(handler=api_update)
        http_api.add_routes(
            path="/{{cookiecutter.api_domain}}/{id}",
            methods=[apigw2.HttpMethod.PUT,apigw2.HttpMethod.PATCH],
            integration=api_update_int
        )

        # delete account lambda
        api_delete = aws_lambda.Function(
            self, 
            "{{cookiecutter.api_domain}}-api-delete",
            runtime=aws_lambda.Runtime.PYTHON_3_7,
            handler="delete.handler",
            code=aws_lambda.Code.from_asset("lambdas/api"),
            timeout=core.Duration.seconds(30),
            environment = dict(DDB_TABLE_NAME=ddb_table.table_name),
        )
        # allow lambda to publish custom events
        api_delete.add_to_role_policy(event_policy)
        # allow lambda to write to ddb
        ddb_table.grant_read_write_data(api_delete)
        # create lambda integration and configure route
        api_delete_int = apigw2.LambdaProxyIntegration(handler=api_delete)
        http_api.add_routes(
            path="/{{cookiecutter.api_domain}}/{id}",
            methods=[apigw2.HttpMethod.DELETE],
            integration=api_delete_int
        )

        core.CfnOutput(self, "Api", value=http_api.url, description="URL of the API Gateway")
        core.CfnOutput(self, "DynamoDB_Name", value=ddb_table.table_name, description="DynamoDB Table Name")
        core.CfnOutput(self, "DynamoDB_ARN", value=ddb_table.table_arn, description="DynamoDB Table ARN")