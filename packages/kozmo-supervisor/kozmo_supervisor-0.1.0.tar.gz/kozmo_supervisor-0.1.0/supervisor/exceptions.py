"""
This module defines the Supervisor exception hierarchy and common exceptions
used across the library.
"""
from abc import ABC


class SupervisorException(Exception, ABC):
    """
    Abstract base class of all supervisor exceptions.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


# Legacy exception classes starting with the prefix `Supervisor`.
# These have been kept around for backwards compatibility.
# Any new exception classes should not start with the `Supervisor` prefix.
class SupervisorPredictorCallException:
    pass


class SupervisorPredictorReturnTypeError:
    pass


# Exception classes. These should only inherit from `SupervisorException`. Ones inheriting from
# other classes beginning with the prefix `Supervisor` are to do with backwards compatibility as
# exception classes used to all start with the prefix `Supervisor`.`
class PredictorCallError(SupervisorException, SupervisorPredictorCallException):
    """
    This exception is raised whenever a call to a user supplied predictor fails at runtime.
    """
    pass


class PredictorReturnTypeError(SupervisorException, SupervisorPredictorReturnTypeError):
    """
    This exception is raised whenever the return type of a user supplied predictor is of
    an unexpected or unsupported type.
    """
    pass


class NotFittedError(SupervisorException):
    """
    This exception is raised whenever a compulsory call to a `fit` method has not been carried out.
    """

    def __init__(self, object_name: str):
        super().__init__(
            f"This {object_name} instance is not fitted yet. Call 'fit' with appropriate arguments first."
        )


class SerializationError(SupervisorException):
    """
    This exception is raised whenever an explainer cannot be serialized.
    """
    def __init__(self, message: str):
        super().__init__(message)
