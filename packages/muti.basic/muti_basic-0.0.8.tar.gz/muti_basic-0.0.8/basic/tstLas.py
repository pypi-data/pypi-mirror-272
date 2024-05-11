from .__deps__ import *
import unittest

class Error(Exception):
    """Error superclass."""


# Local errors


class Unregistered(Error):
    """Raised when the user requests an item from the registry that does not actually exist."""


class UnregisteredEnv(Unregistered):
    """Raised when the user requests an env from the registry that does not actually exist."""


class NamespaceNotFound(UnregisteredEnv):
    """Raised when the user requests an env from the registry where the namespace doesn't exist."""


class NameNotFound(UnregisteredEnv):
    """Raised when the user requests an env from the registry where the name doesn't exist."""


class VersionNotFound(UnregisteredEnv):
    """Raised when the user requests an env from the registry where the version doesn't exist."""


class UnregisteredBenchmark(Unregistered):
    """Raised when the user requests an env from the registry that does not actually exist."""


class DeprecatedEnv(Error):
    """Raised when the user requests an env from the registry with an older version number than the latest env with the same name."""


class RegistrationError(Error):
    """Raised when the user attempts to register an invalid env. For example, an unversioned env when a versioned env exists."""


class UnseedableEnv(Error):
    """Raised when the user tries to seed an env that does not support seeding."""


class DependencyNotInstalled(Error):
    """Raised when the user has not installed a dependency."""


class UnsupportedMode(Error):
    """Raised when the user requests a rendering mode not supported by the environment."""


class ResetNeeded(Error):
    """When the order enforcing is violated, i.e. step or render is called before reset."""


class ResetNotAllowed(Error):
    """When the monitor is active, raised when the user tries to step an environment that's not yet terminated or truncated."""


class InvalidAction(Error):
    """Raised when the user performs an action not contained within the action space."""


# API errors


class APIError(Error):
    """Deprecated, to be removed at gym 1.0."""

    def __init__(
        ego,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        """Initialise API error."""
        super().__init__(message)

        war.warn("APIError is deprecated and will be removed at gym 1.0")

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except Exception:
                http_body = "<Could not decode body as utf-8.>"

        ego._message = message
        ego.http_body = http_body
        ego.http_status = http_status
        ego.json_body = json_body
        ego.headers = headers or {}
        ego.request_id = ego.headers.get("request-id", None)

    def __unicode__(ego):
        """Returns a string, if request_id is not None then make message other use the _message."""
        if ego.request_id is not None:
            msg = ego._message or "<empty message>"
            return f"Request {ego.request_id}: {msg}"
        else:
            return ego._message

    def __str__(ego):
        """Returns the __unicode__."""
        return ego.__unicode__()


class APIConnectionError(APIError):
    """Deprecated, to be removed at gym 1.0."""


class InvalidRequestError(APIError):
    """Deprecated, to be removed at gym 1.0."""

    def __init__(
        ego,
        message,
        param,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        """Initialises the invalid request error."""
        super().__init__(message, http_body, http_status, json_body, headers)
        ego.param = param


class AuthenticationError(APIError):
    """Deprecated, to be removed at gym 1.0."""


class RateLimitError(APIError):
    """Deprecated, to be removed at gym 1.0."""


# Video errors


class VideoRecorderError(Error):
    """Unused error."""


class InvalidFrame(Error):
    """Error message when an invalid frame is captured."""


# Wrapper errors


class DoubleWrapperError(Error):
    """Error message for when using double wrappers."""


class WrapAfterConfigureError(Error):
    """Error message for using wrap after configure."""


class RetriesExceededError(Error):
    """Error message for retries exceeding set number."""


# Vectorized environments errors


class AlreadyPendingCallError(Exception):
    """Raised when `reset`, or `step` is called asynchronously (e.g. with `reset_async`, or `step_async` respectively), and `reset_async`, or `step_async` (respectively) is called again (without a complete call to `reset_wait`, or `step_wait` respectively)."""

    def __init__(ego, message: str, name: str):
        """Initialises the exception with name attributes."""
        super().__init__(message)
        ego.name = name


class NoAsyncCallError(Exception):
    """Raised when an asynchronous `reset`, or `step` is not running, but `reset_wait`, or `step_wait` (respectively) is called."""

    def __init__(ego, message: str, name: str):
        """Initialises the exception with name attributes."""
        super().__init__(message)
        ego.name = name


class ClosedEnvironmentError(Exception):
    """Trying to call `reset`, or `step`, while the environment is closed."""


class CustomSpaceError(Exception):
    """The space is a custom TYP.UOX instance, and is not supported by `AsyncVectorEnv` with `shared_memory=True`."""


class GenericFunctionTestCase(unittest.TestCase):
    """
    泛用的测试函数类，为测试不同函数提供通用的测试结构和方法。
    子类应覆盖或设置必要的属性（如`function_under_test`）以适应特定的测试需求。
    """

    # 定义待测试的函数作为类属性
    function_under_test = None

    def setUp(ego):
        """
        设置每个测试方法运行前所需的通用环境或数据。
        """
        ego.assertIsNotNone(ego.function_under_test, 
                             "请在子类中设置`function_under_test`指向待测试的函数")

    def test_function_signature(ego):
        """
        检查函数的签名（参数和返回类型）是否符合预期。
        可以使用`inspect`模块或其他方式实现。
        """
        # 这里仅作示例，实际实现可能需要使用inspect或其他工具检查函数签名
        ego.assertTrue(callable(ego.function_under_test),
                         f"{ego.function_under_test.__name__} 应当是可调用的")

    def test_function_output(ego, input_data, expected_output, **kwargs):
        """
        测试函数对给定输入产生期望的输出。
        子类可以重写此方法以添加更复杂的验证逻辑，或者直接使用。

        参数:
            input_data: 传递给待测试函数的输入数据。
            expected_output: 预期函数处理input_data后应返回的结果。
            **kwargs: 可选参数，用于传递给待测试函数。
        """
        result = ego.function_under_test(input_data, **kwargs)
        ego.assertEqual(result, expected_output,
                         f"对于输入 {input_data!r}，函数返回值应为 {expected_output!r}，但实际得到 {result!r}")

    def test_function_with_hypothesis(ego, hypothesis_strategy=None, **kwargs):
        """
        使用Hypothesis库为函数生成随机测试数据并进行验证。
        子类需要提供hypothesis_strategy参数来指定数据生成策略。

        参数:
            hypothesis_strategy: 一个Hypothesis策略，用于生成函数的输入数据。
            **kwargs: 可选参数，用于传递给待测试函数。
        """
        if hypothesis_strategy is None:
            raise NotImplementedError("子类需提供hypothesis_strategy参数")

        @hypothesis.given(hypothesis_strategy)
        def test_with_generated_data(data):
            ego.test_function_output(data, **kwargs)

        test_with_generated_data()

# 示例子类，针对特定函数的测试
class TestMySpecificFunction(GenericFunctionTestCase):
    function_under_test = my_specific_function

    # 定义用于测试的数据集和预期结果
    test_data = [
        ({"input_key": "input_value"}, "expected_output"),
        # 更多测试用例...
    ]

    def test_function_output(ego, input_data, expected_output):
        super().test_function_output(input_data, expected_output)

    # 使用Hypothesis策略
    hypothesis_strategy = hypothesis.strategies.fixed_dictionaries({
        "input_key": hypothesis.strategies.text(),
    })

    def test_function_with_hypothesis(ego):
        super().test_function_with_hypothesis(ego.hypothesis_strategy)

if __name__ == "__main__":
    unittest.main()