import json
import logging
from unittest import mock

import numpy as np
from google.protobuf import any_pb2

from kozmo_core.proto import prediction_pb2
from kozmo_core.kozmo_client import (
    KozmoClient,
    KozmoClientCombine,
    KozmoClientPrediction,
)
from kozmo_core.utils import (
    array_to_grpc_datadef,
    json_to_kozmo_message,
    kozmo_message_to_json,
)

JSON_TEST_DATA = {"test": [0.0, 1.0]}
RAW_DATA_TEST = {"data": {"ndarray": [[0.0, 1.0, 2.0]]}}
CUSTOM_TEST_DATA = any_pb2.Any(value=b"test")


class MockResponse:
    def __init__(self, json_data, status_code, reason="", text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.reason = reason
        self.text = text

    def json(self):
        return self.json_data


def mocked_requests_post_404(url, *args, **kwargs):
    return MockResponse(None, 404, "Not Found")


def mocked_requests_post_success(url, *args, **kwargs):
    data = np.random.rand(1, 1)
    datadef = array_to_grpc_datadef("tensor", data)
    request = prediction_pb2.KozmoMessage(data=datadef)
    json = kozmo_message_to_json(request)
    return MockResponse(json, 200, text="{}")


def mocked_requests_post_success_json_data(url, *args, **kwargs):
    request = json_to_kozmo_message({"jsonData": JSON_TEST_DATA})
    json = kozmo_message_to_json(request)
    return MockResponse(json, 200, text="{}")


@mock.patch("requests.post", side_effect=mocked_requests_post_404)
def test_predict_rest_404(mock_post):
    sc = KozmoClient(deployment_name="404")
    response = sc.predict()
    assert response.success == False
    assert response.msg == "404:Not Found"


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_rest(mock_post):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.predict(client_return_type="proto")
    logging.info(mock_post.call_args)
    assert response.success == True
    assert response.response.data.tensor.shape == [1, 1]
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_rest_with_names(mock_post):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.predict(names=["a", "b"], client_return_type="proto")
    assert mock_post.call_args[1]["json"]["data"]["names"] == ["a", "b"]
    assert response.success == True
    assert response.response.data.tensor.shape == [1, 1]
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success_json_data)
def test_predict_rest_json_data_ambassador(mock_post):
    sc = KozmoClient(deployment_name="mymodel", gateway="ambassador")
    response = sc.predict(json_data=JSON_TEST_DATA, client_return_type="proto")
    json_response = kozmo_message_to_json(response.response)
    assert "jsonData" in mock_post.call_args[1]["json"]
    assert mock_post.call_args[1]["json"]["jsonData"] == JSON_TEST_DATA
    assert response.success is True
    assert json_response["jsonData"] == JSON_TEST_DATA
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success_json_data)
def test_predict_rest_json_data_ambassador_dict_response(mock_post):
    sc = KozmoClient(
        deployment_name="mymodel", gateway="ambassador", client_return_type="dict"
    )
    response = sc.predict(json_data=JSON_TEST_DATA)
    json_response = response.response
    assert "jsonData" in mock_post.call_args[1]["json"]
    assert mock_post.call_args[1]["json"]["jsonData"] == JSON_TEST_DATA
    assert response.success is True
    assert json_response["jsonData"] == JSON_TEST_DATA
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success_json_data)
def test_predict_rest_json_data_kozmo(mock_post):
    sc = KozmoClient(
        deployment_name="mymodel", gateway="kozmo", client_return_type="proto"
    )
    response = sc.predict(json_data=JSON_TEST_DATA)
    json_response = kozmo_message_to_json(response.response)
    assert "jsonData" in mock_post.call_args[1]["json"]
    assert mock_post.call_args[1]["json"]["jsonData"] == JSON_TEST_DATA
    assert response.success is True
    assert json_response["jsonData"] == JSON_TEST_DATA
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_rest_raw_data_kozmo_proto(mock_post):
    sc = KozmoClient(
        deployment_name="mymodel", gateway="kozmo", client_return_type="proto"
    )
    response = sc.predict(raw_data=RAW_DATA_TEST)
    json_response = kozmo_message_to_json(response.response)
    assert mock_post.call_args[1]["json"] == RAW_DATA_TEST
    assert response.success is True
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_rest_raw_data_gateway_dict(mock_post):
    sc = KozmoClient(
        deployment_name="mymodel", gateway="istio", client_return_type="dict"
    )
    response = sc.predict(raw_data=RAW_DATA_TEST)
    json_response = response.response
    assert mock_post.call_args[1]["json"] == RAW_DATA_TEST
    assert response.success is True
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success_json_data)
def test_predict_rest_json_data_kozmo_return_type(mock_post):
    sc = KozmoClient(
        deployment_name="mymodel", gateway="kozmo", client_return_type="dict"
    )
    response = sc.predict(json_data=JSON_TEST_DATA)
    json_response = response.response
    assert "jsonData" in mock_post.call_args[1]["json"]
    assert mock_post.call_args[1]["json"]["jsonData"] == JSON_TEST_DATA
    assert response.success is True
    assert json_response["jsonData"] == JSON_TEST_DATA
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success_json_data)
def test_explain_rest_json_data_ambassador(mock_post):
    sc = KozmoClient(
        deployment_name="mymodel", gateway="ambassador", client_return_type="dict"
    )
    response = sc.explain(json_data=JSON_TEST_DATA, predictor="default")
    json_response = response.response
    # Currently this doesn't need to convert to JSON due to #1083
    # i.e. json_response = kozmo_message_to_json(response.response)
    assert "jsonData" in mock_post.call_args[1]["json"]
    assert mock_post.call_args[1]["json"]["jsonData"] == JSON_TEST_DATA
    assert json_response["jsonData"] == JSON_TEST_DATA
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success_json_data)
def test_explain_rest_json_data_ambassador_dict_response(mock_post):
    sc = KozmoClient(
        deployment_name="mymodel", gateway="ambassador", client_return_type="dict"
    )
    response = sc.explain(json_data=JSON_TEST_DATA, predictor="default")
    json_response = response.response
    # Currently this doesn't need to convert to JSON due to #1083
    # i.e. json_response = kozmo_message_to_json(response.response)
    assert "jsonData" in mock_post.call_args[1]["json"]
    assert mock_post.call_args[1]["json"]["jsonData"] == JSON_TEST_DATA
    assert json_response["jsonData"] == JSON_TEST_DATA
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_rest_with_meta(mock_post):
    sc = KozmoClient(deployment_name="mymodel")
    meta = {"key": "value"}
    response = sc.predict(names=["a", "b"], meta=meta, client_return_type="proto")
    assert mock_post.call_args[1]["json"]["data"]["names"] == ["a", "b"]
    assert mock_post.call_args[1]["json"]["meta"]["tags"] == meta
    assert response.success == True
    assert response.response.data.tensor.shape == [1, 1]
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_rest_with_ambassador_prefix(mock_post):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.predict(
        gateway="ambassador",
        transport="rest",
        gateway_prefix="/mycompany/ml",
        client_return_type="proto",
    )
    assert mock_post.call_args[0][0].index("/mycompany/ml") > 0
    assert response.success == True
    assert response.response.data.tensor.shape == [1, 1]
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_rest_with_ambassador_prefix_dict_response(mock_post):
    sc = KozmoClient(deployment_name="mymodel", client_return_type="dict")
    response = sc.predict(
        gateway="ambassador", transport="rest", gateway_prefix="/mycompany/ml"
    )
    assert mock_post.call_args[0][0].index("/mycompany/ml") > 0
    assert response.success == True
    assert response.response["data"]["tensor"]["shape"] == [1, 1]
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_predict_microservice_rest(mock_post):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.microservice(method="predict")
    logging.info(response)
    assert response.success == True
    assert response.response.data.tensor.shape == [1, 1]
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success_json_data)
def test_predict_microservice_rest_json_data(mock_post):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.microservice(method="predict", json_data=JSON_TEST_DATA)
    json_response = kozmo_message_to_json(response.response)
    assert "jsonData" in mock_post.call_args[1]["data"]["json"]
    assert response.success is True
    assert mock_post.call_args[1]["data"]["json"] == json.dumps(
        {"jsonData": JSON_TEST_DATA}
    )
    assert json_response["jsonData"] == JSON_TEST_DATA
    assert mock_post.call_count == 1


@mock.patch("requests.post", side_effect=mocked_requests_post_success)
def test_feedback_microservice_rest(mock_post):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.microservice_feedback(
        prediction_request=prediction_pb2.KozmoMessage(),
        prediction_response=prediction_pb2.KozmoMessage(),
        reward=1.0,
    )
    assert response.success == True
    assert response.response.data.tensor.shape == [1, 1]
    assert mock_post.call_count == 1


class MyStub:
    def __init__(self, channel):
        self.channel = channel

    def Predict(self, **kwargs):
        return prediction_pb2.KozmoMessage(strData="predict")

    def TransformInput(selfself, **kwargs):
        return prediction_pb2.KozmoMessage(strData="transform-input")

    def TransformOutput(selfself, **kwargs):
        return prediction_pb2.KozmoMessage(strData="transform-output")

    def Route(selfself, **kwargs):
        return prediction_pb2.KozmoMessage(strData="route")


def mock_grpc_stub_predict(channel):
    return MyStub()


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_predict_grpc_ambassador():
    sc = KozmoClient(deployment_name="mymodel", transport="grpc", gateway="ambassador")
    response = sc.predict(client_return_type="proto")
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_predict_grpc_ambassador_with_meta():
    sc = KozmoClient(deployment_name="mymodel", transport="grpc", gateway="ambassador")
    response = sc.predict(meta={"key": "value"}, client_return_type="proto")
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_grpc_predict_json_data_ambassador():
    sc = KozmoClient(deployment_name="mymodel", transport="grpc", gateway="ambassador")
    response = sc.predict(json_data=JSON_TEST_DATA, client_return_type="proto")
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_grpc_predict_custom_data_ambassador():
    sc = KozmoClient(deployment_name="mymodel", transport="grpc", gateway="ambassador")
    response = sc.predict(custom_data=CUSTOM_TEST_DATA, client_return_type="proto")
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_predict_grpc_kozmo():
    sc = KozmoClient(deployment_name="mymodel", transport="grpc", gateway="kozmo")
    response = sc.predict(client_return_type="proto")
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_predict_grpc_proto_raw_data_kozmo():
    sc = KozmoClient(deployment_name="mymodel", transport="grpc", gateway="kozmo")
    proto_raw_data = json_to_kozmo_message(RAW_DATA_TEST)
    response = sc.predict(raw_data=proto_raw_data, client_return_type="proto")
    request = kozmo_message_to_json(response.request)
    assert request == RAW_DATA_TEST


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_predict_grpc_raw_data_gateway():
    sc = KozmoClient(deployment_name="mymodel", transport="grpc", gateway="istio")
    response = sc.predict(raw_data=RAW_DATA_TEST, client_return_type="proto")
    request = kozmo_message_to_json(response.request)
    assert request == RAW_DATA_TEST


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_grpc_predict_json_data_kozmo():
    sc = KozmoClient(
        deployment_name="mymodel",
        transport="grpc",
        gateway="kozmo",
        client_return_type="proto",
    )
    response = sc.predict(json_data=JSON_TEST_DATA)
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.KozmoStub", new=MyStub)
def test_grpc_predict_custom_data_kozmo():
    sc = KozmoClient(
        deployment_name="mymodel",
        transport="grpc",
        gateway="kozmo",
        client_return_type="proto",
    )
    response = sc.predict(custom_data=CUSTOM_TEST_DATA)
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.ModelStub", new=MyStub)
def test_predict_grpc_microservice_predict():
    sc = KozmoClient(transport="grpc")
    response = sc.microservice(method="predict")
    assert response.response.strData == "predict"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.GenericStub", new=MyStub)
def test_predict_grpc_microservice_transform_input():
    sc = KozmoClient(transport="grpc")
    response = sc.microservice(method="transform-input")
    assert response.response.strData == "transform-input"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.GenericStub", new=MyStub)
def test_predict_grpc_microservice_transform_output():
    sc = KozmoClient(transport="grpc")
    response = sc.microservice(method="transform-output")
    assert response.response.strData == "transform-output"


@mock.patch("kozmo_core.kozmo_client.prediction_pb2_grpc.GenericStub", new=MyStub)
def test_predict_grpc_microservice_transform_route():
    sc = KozmoClient(transport="grpc")
    response = sc.microservice(method="route")
    assert response.response.strData == "route"


#
# Wiring Tests
#


@mock.patch(
    "kozmo_core.kozmo_client.microservice_api_rest_kozmo_message",
    return_value=KozmoClientPrediction(None, None),
)
def test_wiring_microservice_api_rest_kozmo_message(mock_handler):
    sc = KozmoClient()
    response = sc.microservice(transport="rest", method="predict")
    assert mock_handler.call_count == 1


@mock.patch(
    "kozmo_core.kozmo_client.microservice_api_rest_aggregate",
    return_value=KozmoClientCombine(None, None),
)
def test_wiring_microservice_api_rest_aggregate(mock_handler):
    sc = KozmoClient()
    response = sc.microservice(transport="rest", method="aggregate")
    assert mock_handler.call_count == 1


@mock.patch(
    "kozmo_core.kozmo_client.microservice_api_rest_feedback",
    return_value=KozmoClientCombine(None, None),
)
def test_wiring_microservice_api_rest_feedback(mock_handler):
    sc = KozmoClient()
    response = sc.microservice_feedback(
        prediction_pb2.KozmoMessage(),
        prediction_pb2.KozmoMessage(),
        1.0,
        transport="rest",
    )
    assert mock_handler.call_count == 1


@mock.patch(
    "kozmo_core.kozmo_client.microservice_api_grpc_kozmo_message",
    return_value=KozmoClientPrediction(None, None),
)
def test_wiring_microservice_api_grpc_kozmo_message(mock_handler):
    sc = KozmoClient()
    response = sc.microservice(transport="grpc", method="predict")
    assert mock_handler.call_count == 1


@mock.patch(
    "kozmo_core.kozmo_client.microservice_api_grpc_aggregate",
    return_value=KozmoClientCombine(None, None),
)
def test_wiring_microservice_api_grpc_aggregate(mock_handler):
    sc = KozmoClient()
    response = sc.microservice(transport="grpc", method="aggregate")
    assert mock_handler.call_count == 1


@mock.patch(
    "kozmo_core.kozmo_client.microservice_api_grpc_feedback",
    return_value=KozmoClientCombine(None, None),
)
def test_wiring_microservice_api_grpc_feedback(mock_handler):
    sc = KozmoClient()
    response = sc.microservice_feedback(
        prediction_pb2.KozmoMessage(),
        prediction_pb2.KozmoMessage(),
        1.0,
        transport="grpc",
    )
    assert mock_handler.call_count == 1


@mock.patch(
    "kozmo_core.kozmo_client.rest_predict_gateway",
    return_value=KozmoClientPrediction(None, None),
)
def test_wiring_rest_predict_ambassador(mock_rest_predict_ambassador):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.predict(gateway="ambassador", transport="rest")
    assert mock_rest_predict_ambassador.call_count == 1


@mock.patch(
    "kozmo_core.kozmo_client.grpc_predict_gateway",
    return_value=KozmoClientPrediction(None, None),
)
def test_wiring_grpc_predict_ambassador(mock_grpc_predict_ambassador):
    sc = KozmoClient(deployment_name="mymodel")
    response = sc.predict(gateway="ambassador", transport="grpc")
    assert mock_grpc_predict_ambassador.call_count == 1
