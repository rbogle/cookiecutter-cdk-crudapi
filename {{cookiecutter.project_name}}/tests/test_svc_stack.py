
import json
import pytest
import sys
from aws_cdk import core
from fnds_aws_acct_svc.fnds_aws_acct_svc_stack import FndsAwsAcctSvcStack

def get_template():
    app = core.App()
    FndsAwsAcctSvcStack(app, "fnds-aws-acct-svc")
    rval = True
    try:
        app.synth()
    except BaseException as e:
        rval = False
    return rval

def test_svc_stack_synth():
    # test if synth runs correctly on local host only
    if not sys.platform.startswith('darwin'):
        pytest.skip("skipping if not on workstation")
    assert( get_template() is True)