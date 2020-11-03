"""
Everything required for adding this project to the Pipeline Forge

While there are a lot of methods in this module, there are a few
main ones of concern:

1. stack_configs - loop over the results of this and create a stack for each iteration
2. stack_id - helper function for creating your stack ID/name
3. stack_configure - helper function to configure your stack properly

You should not need to call any of the other methods unless you
have an odd use case.
"""

import os
from typing import List
from typing import Optional
from typing import Tuple

import jsii
from aws_cdk import aws_iam
from aws_cdk import core


def stack_configs() -> Tuple[str, List[core.Environment], Optional[str]]:
    """
    Reads environment variables to produce a list of stack configurations
    Each returned set of values should be used to create a new stack.
    :return: The stage name, stack environment and (optionally) a deployment name
    """
    for stage in __stages():
        for account in __accounts(stage):
            for region, deployment in __regions(stage, account):
                env = core.Environment(account=account, region=region)
                yield stage, env, deployment


def stack_id(
    name: str, stage: str, env: core.Environment, deployment: Optional[str]
) -> str:
    """
    Create a stack CloudFormation ID
    :param name: The project name
    :param stage: The stage
    :param env: The stack environment
    :param deployment: The deployment name (optional)
    :return: The stack CloudFormation ID
    """
    dep = "" if deployment is None else f"-{deployment}"
    return f"{name}-{stage}-{env.account}-{env.region}{dep}"


def stack_configure(
    stack: core.Stack, stage: str, *, department: str, product: str, product_detail: str
) -> None:
    """
    Everything required by the Pipeline Forge

    1. Add tags to the stack
    2. Add permission boundary

    :param stack: The stack configure
    :param stage: The stage
    :param department: The department code
    :param product: Product
    :param product_detail: Product detail
    """
    stack_boundary(stack)
    stack_tags(
        stack,
        stage,
        department=department,
        product=product,
        product_detail=product_detail,
    )


def stack_boundary(stack: core.Stack) -> None:
    """
    Given a stack, add a CloudFormation parameter for permission boundary
    and then apply that boundary to every AIM role in the stack.
    :param stack:
    :return:
    """
    param = cfn_boundary_parameter(stack)
    aspect = PermissionBoundaryAspect(param.value_as_string)
    # noinspection PyTypeChecker
    core.Aspects.of(stack).add(aspect)


def cfn_boundary_parameter(stack: core.Stack) -> core.CfnParameter:
    """
    Create a CloudFormation parameter for the permission boundary ARN
    :param stack: Add the parameter to this stack
    :return: The created parameter
    """
    return core.CfnParameter(
        stack,
        "BoundaryPolicyArn",
        description="Permission boundary for all roles",
        type="String",
    )


@jsii.implements(core.IAspect)
class PermissionBoundaryAspect:
    """
    This aspect finds all aws_iam.Role objects in a node (ie. CDK stack)
    and sets permission boundary to the given ARN.
    """

    def __init__(self, policy_arn: str) -> None:
        """
        :param policy_arn: Permissions boundary managed policy's ARN
        """
        self.policy_arn = policy_arn

    def visit(self, node: "core.IConstruct") -> None:
        """
        :param node: The node that we are visiting
        :return: None
        """
        if isinstance(node, aws_iam.CfnRole):
            node.permissions_boundary = self.policy_arn


# noinspection PyTypeChecker
def stack_tags(
    stack: core.Stack, stage: str, *, department: str, product: str, product_detail: str
) -> None:
    """
    Tag the stack
    :param stack: The stack to tag
    :param stage: The stage
    :param department: The department code
    :param product: Product
    :param product_detail: Product detail
    """
    env_tag = "Production" if stage in ["prod", "tp"] else "Development"
    core.Tags.of(stack).add("Department", department)
    core.Tags.of(stack).add("Environment", env_tag)
    core.Tags.of(stack).add("Product", product)
    core.Tags.of(stack).add("ProductDetail", product_detail)


def __stages() -> List[str]:
    """
    :return: List of stages from env variable
    """
    stages = os.environ.get("CDK_DEPLOY_STAGES", "dev")
    return stages.split(" ")


def __accounts(stage: str) -> List[str]:
    """
    :return: List of accounts for a stage from env variable
    """
    accounts = os.environ.get(
        f"CDK_DEPLOY_{stage}_ACCOUNTS", os.environ["CDK_DEFAULT_ACCOUNT"]
    )
    return accounts.split(" ")


def __regions(stage: str, account: str) -> Tuple[str, Optional[str]]:
    """
    :return: Yields region and optional deployment name for a stage and account from env variable
    """
    regions = os.environ.get(
        f"CDK_DEPLOY_{stage}_{account}_REGIONS", os.environ["CDK_DEFAULT_REGION"],
    )
    for region in regions.split(" "):
        parts = region.split(":")
        if len(parts) > 2:
            raise Exception(f"Invalid region format on '{region}'")

        yield parts[0], parts[1] if len(parts) == 2 else None
