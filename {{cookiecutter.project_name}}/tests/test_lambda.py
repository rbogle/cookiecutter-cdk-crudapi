from lambdas.api.api_handler import *
from tests import *
import pytest
import sys

def test_api_handler():
    # test if synth runs correctly on local host only
    if not sys.platform.startswith('darwin'):
        pytest.skip("skipping if not on workstation")

    body ={
        "message": "Hello World"
    }

    resp = handler(api_gateway_event(body), None)
 
    resp_body = resp.get('body')
    assert  resp_body == json.dumps(body)
