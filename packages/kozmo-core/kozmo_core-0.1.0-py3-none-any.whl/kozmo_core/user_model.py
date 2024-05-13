import inspect
import json
import logging
import os
from typing import Dict, Iterable, List, Tuple, Union

import numpy as np

from kozmo_core.flask_utils import KozmoMicroserviceException
from kozmo_core.metrics import KozmoMetrics, validate_metrics
from kozmo_core.proto import prediction_pb2

logger = logging.getLogger(__name__)


INCLUDE_METRICS_IN_CLIENT_RESPONSE = (
    os.environ.get("INCLUDE_METRICS_IN_CLIENT_RESPONSE", "true").lower() == "true"
)


class KozmoNotImplementedError(KozmoMicroserviceException):
    status_code = 400

    def __init__(self, message):
        KozmoMicroserviceException.__init__(self, message)


class KozmoResponse:
    """KozmoResponse

    Simple class to store data returned by KozmoComponent methods together
    with relevant runtime metrics and runtime request tags.
    """

    def __init__(
        self,
        data: Union[np.ndarray, List, str, bytes],
        tags: Dict = None,
        metrics: List[Dict] = None,
    ):
        self.data = data
        self.tags = tags if tags is not None else {}
        self.metrics = metrics if metrics is not None else []

    @classmethod
    def create(
        cls, data: Union[np.ndarray, List, Dict, str, bytes, "KozmoResponse"]
    ) -> "KozmoResponse":
        if isinstance(data, cls):
            return data
        else:
            return cls(data=data)


class KozmoComponent:
    def __init__(self, **kwargs):
        pass

    def tags(self) -> Dict:
        raise KozmoNotImplementedError("tags is not implemented")

    def class_names(self) -> Iterable[str]:
        raise KozmoNotImplementedError("class_names is not implemented")

    def load(self):
        pass

    def predict(
        self, X: np.ndarray, names: Iterable[str], meta: Dict = None
    ) -> Union[np.ndarray, List, Dict, str, bytes, KozmoResponse]:
        raise KozmoNotImplementedError("predict is not implemented")

    def predict_raw(
        self, msg: prediction_pb2.KozmoMessage
    ) -> Union[prediction_pb2.KozmoMessage, Dict]:
        raise KozmoNotImplementedError("predict_raw is not implemented")

    def send_feedback_raw(
        self, feedback: prediction_pb2.Feedback
    ) -> Union[prediction_pb2.KozmoMessage, Dict]:
        raise KozmoNotImplementedError("send_feedback_raw is not implemented")

    def transform_input(
        self, X: np.ndarray, names: Iterable[str], meta: Dict = None
    ) -> Union[np.ndarray, List, Dict, str, bytes, KozmoResponse]:
        raise KozmoNotImplementedError("transform_input is not implemented")

    def transform_input_raw(
        self, msg: prediction_pb2.KozmoMessage
    ) -> Union[prediction_pb2.KozmoMessage, Dict]:
        raise KozmoNotImplementedError("transform_input_raw is not implemented")

    def transform_output(
        self, X: np.ndarray, names: Iterable[str], meta: Dict = None
    ) -> Union[np.ndarray, List, Dict, str, bytes, KozmoResponse]:
        raise KozmoNotImplementedError("transform_output is not implemented")

    def transform_output_raw(
        self, msg: prediction_pb2.KozmoMessage
    ) -> Union[prediction_pb2.KozmoMessage, Dict]:
        raise KozmoNotImplementedError("transform_output_raw is not implemented")

    def metrics(self) -> List[Dict]:
        raise KozmoNotImplementedError("metrics is not implemented")

    def feature_names(self) -> Iterable[str]:
        raise KozmoNotImplementedError("feature_names is not implemented")

    def send_feedback(
        self,
        features: Union[np.ndarray, str, bytes],
        feature_names: Iterable[str],
        reward: float,
        truth: Union[np.ndarray, str, bytes],
        routing: Union[int, None],
    ) -> Union[np.ndarray, List, Dict, str, bytes, None, KozmoResponse]:
        raise KozmoNotImplementedError("send_feedback is not implemented")

    def route(
        self, features: Union[np.ndarray, str, bytes], feature_names: Iterable[str]
    ) -> Union[int, KozmoResponse]:
        raise KozmoNotImplementedError("route is not implemented")

    def route_raw(
        self, msg: prediction_pb2.KozmoMessage
    ) -> Union[prediction_pb2.KozmoMessage, Dict]:
        raise KozmoNotImplementedError("route_raw is not implemented")

    def aggregate(
        self,
        features_list: List[Union[np.ndarray, str, bytes]],
        feature_names_list: List,
    ) -> Union[np.ndarray, List, Dict, str, bytes, KozmoResponse]:
        raise KozmoNotImplementedError("aggregate is not implemented")

    def aggregate_raw(
        self, msgs: prediction_pb2.KozmoMessageList
    ) -> Union[prediction_pb2.KozmoMessage, Dict]:
        raise KozmoNotImplementedError("aggregate_raw is not implemented")

    def health_status(self) -> Union[np.ndarray, List, str, bytes]:
        raise KozmoNotImplementedError("health is not implemented")

    def health_status_raw(self) -> prediction_pb2.KozmoMessage:
        raise KozmoNotImplementedError("health_raw is not implemented")

    def metadata(self) -> Dict:
        raise KozmoNotImplementedError("metadata is not implemented")

    def init_metadata(self) -> Dict:
        raise KozmoNotImplementedError("init_metadata is not implemented")


def client_custom_tags(user_model: KozmoComponent) -> Dict:
    """
    Get tags from user model

    Parameters
    ----------
    user_model

    Returns
    -------
       Dictionary of key value pairs

    """
    if hasattr(user_model, "tags"):
        try:
            return user_model.tags()
        except KozmoNotImplementedError:
            pass
    logger.debug("custom_tags is not implemented")
    return {}


def client_class_names(
    user_model: KozmoComponent, predictions: np.ndarray
) -> Iterable[str]:
    """
    Get class names from user model

    Parameters
    ----------
    user_model
       User defined class instance
    predictions
       Prediction results
    Returns
    -------
       Class names
    """
    if len(predictions.shape) > 1:
        if hasattr(user_model, "class_names"):
            if inspect.ismethod(getattr(user_model, "class_names")):
                try:
                    return user_model.class_names()
                except KozmoNotImplementedError:
                    pass
            else:
                logger.warning(
                    "class_names attribute is deprecated. Please define a class_names method"
                )
                return user_model.class_names
        logger.debug("class_names is not implemented")
        n_targets = predictions.shape[1]
        return ["t:{}".format(i) for i in range(n_targets)]
    else:
        return []


def client_predict(
    user_model: KozmoComponent,
    features: Union[np.ndarray, str, bytes],
    feature_names: Iterable[str],
    **kwargs: Dict,
) -> KozmoResponse:
    """
    Get prediction from user model

    Parameters
    ----------
    user_model
       A kozmo user model
    features
       The data payload
    feature_names
       The feature names in the payload
    kwargs
       Optional keyword arguments
    Returns
    -------
       A prediction from the user model
    """
    if hasattr(user_model, "predict"):
        try:
            try:
                client_response = user_model.predict(features, feature_names, **kwargs)
            except TypeError:
                client_response = user_model.predict(features, feature_names)
            return KozmoResponse.create(client_response)
        except KozmoNotImplementedError:
            pass
    logger.debug("predict is not implemented")
    return KozmoResponse.create([])


def client_transform_input(
    user_model: KozmoComponent,
    features: Union[np.ndarray, str, bytes],
    feature_names: Iterable[str],
    **kwargs: Dict,
) -> KozmoResponse:
    """
    Transform data with user model

    Parameters
    ----------
    user_model
       A Kozmo user model
    features
       Data payload
    feature_names
       Data payload column names
    kwargs
       Optional keyword args

    Returns
    -------
       Transformed data

    """
    if hasattr(user_model, "transform_input"):
        try:
            try:
                client_response = user_model.transform_input(
                    features, feature_names, **kwargs
                )
            except TypeError:
                client_response = user_model.transform_input(features, feature_names)
            return KozmoResponse.create(client_response)
        except KozmoNotImplementedError:
            pass
    logger.debug("transform_input is not implemented")
    return KozmoResponse.create(features)


def client_transform_output(
    user_model: KozmoComponent,
    features: Union[np.ndarray, str, bytes],
    feature_names: Iterable[str],
    **kwargs: Dict,
) -> KozmoResponse:
    """
    Transform output

    Parameters
    ----------
    user_model
       A Kozmo user model
    features
       Data payload
    feature_names
       Data payload column names
    kwargs
       Optional keyword args
    Returns
    -------
       Transformed data

    """
    if hasattr(user_model, "transform_output"):
        try:
            try:
                client_response = user_model.transform_output(
                    features, feature_names, **kwargs
                )
            except TypeError:
                client_response = user_model.transform_output(features, feature_names)
            return KozmoResponse.create(client_response)
        except KozmoNotImplementedError:
            pass
    logger.debug("transform_output is not implemented")
    return KozmoResponse.create(features)


def client_custom_metrics(
    user_model: KozmoComponent,
    kozmo_metrics: KozmoMetrics,
    method: str,
    runtime_metrics: List[Dict] = [],
) -> List[Dict]:
    """
    Get custom metrics for client and update KozmoMetrics.

    This function will return empty list if INCLUDE_METRICS_IN_CLIENT_RESPONSE environmental
    variable is NOT set to "true" or "True".

    Parameters
    ----------
    user_model
       A Kozmo user model
    kozmo_metrics
        A KozmoMetrics instance
    method:
        tag of a method that collected the metrics
    runtime_metrics:
        metrics that were defined on runtime
    Returns
    -------
       A list of custom metrics

    """
    if not validate_metrics(runtime_metrics):
        raise KozmoMicroserviceException(
            f"Bad metric created during request: {json.dumps(runtime_metrics)}",
            status_code=500,
            reason="MICROSERVICE_BAD_METRIC",
        )
    kozmo_metrics.update(runtime_metrics, method)

    if hasattr(user_model, "metrics"):
        try:
            metrics = user_model.metrics()
            if not validate_metrics(metrics):
                raise KozmoMicroserviceException(
                    f"Bad metric created during request: {json.dumps(metrics)}",
                    status_code=500,
                    reason="MICROSERVICE_BAD_METRIC",
                )

            kozmo_metrics.update(metrics, method)
            if INCLUDE_METRICS_IN_CLIENT_RESPONSE:
                return metrics + runtime_metrics
            else:
                return []
        except KozmoNotImplementedError:
            pass
    logger.debug("custom_metrics is not implemented")
    if INCLUDE_METRICS_IN_CLIENT_RESPONSE:
        return runtime_metrics
    else:
        return []


def client_feature_names(
    user_model: KozmoComponent, original: Iterable[str]
) -> Iterable[str]:
    """
    Get feature names for user model

    Parameters
    ----------
    user_model
       A Kozmo user model
    original
       Original feature names
    Returns
    -------
       A list if feature names
    """
    if hasattr(user_model, "feature_names"):
        try:
            return user_model.feature_names()
        except KozmoNotImplementedError:
            pass
    logger.debug("feature_names is not implemented")
    return original


def client_send_feedback(
    user_model: KozmoComponent,
    features: Union[np.ndarray, str, bytes],
    feature_names: Iterable[str],
    reward: float,
    truth: Union[np.ndarray, str, bytes],
    routing: Union[int, None],
) -> KozmoResponse:
    """
    Feedback to user model

    Parameters
    ----------
    user_model
       A Kozmo user model
    features
       A payload
    feature_names
       Payload column names
    reward
       Reward
    truth
       True outcome
    routing
       Optional routing

    Returns
    -------
       Optional payload

    """
    if hasattr(user_model, "send_feedback"):
        try:
            client_response = user_model.send_feedback(
                features, feature_names, reward, truth, routing=routing
            )
            return KozmoResponse.create(client_response)
        except KozmoNotImplementedError:
            pass
    logger.debug("send_feedback is not implemented")
    return KozmoResponse.create(None)


def client_route(
    user_model: KozmoComponent,
    features: Union[np.ndarray, str, bytes],
    feature_names: Iterable[str],
    **kwargs: Dict,
) -> KozmoResponse:
    """
    Get routing from user model

    Parameters
    ----------
    user_model
       A Kozmo user model
    features
       Payload
    feature_names
       Columns for payload

    Returns
    -------
       Routing index for one of children
    """
    if hasattr(user_model, "route"):
        try:
            client_response = user_model.route(features, feature_names, **kwargs)
        except TypeError:
            client_response = user_model.route(features, feature_names)
        return KozmoResponse.create(client_response)
    else:
        raise KozmoNotImplementedError("Route not defined")


def client_aggregate(
    user_model: KozmoComponent,
    features_list: List[Union[np.ndarray, str, bytes]],
    feature_names_list: List,
) -> KozmoResponse:
    """
    Aggregate payloads

    Parameters
    ----------
    user_model
       A Kozmo user model
    features_list
       A list of payloads
    feature_names_list
       Column names for payloads
    Returns
    -------
       An aggregated payload
    """
    if hasattr(user_model, "aggregate"):
        client_response = user_model.aggregate(features_list, feature_names_list)
        return KozmoResponse.create(client_response)
    else:
        raise KozmoNotImplementedError("Aggregate not defined")


def client_health_status(
    user_model: KozmoComponent,
) -> Union[np.ndarray, List, str, bytes]:
    """
    Perform a health check

    Parameters
    ----------
    user_model
       A Kozmo user model
    Returns
    -------
       Health check results
    """
    if hasattr(user_model, "health_status"):
        try:
            return user_model.health_status()
        except KozmoNotImplementedError:
            return "not implemented - assuming healthy"
    else:
        return "healthy"
