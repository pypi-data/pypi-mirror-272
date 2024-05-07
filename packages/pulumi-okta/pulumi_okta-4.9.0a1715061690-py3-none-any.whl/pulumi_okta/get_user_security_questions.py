# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'GetUserSecurityQuestionsResult',
    'AwaitableGetUserSecurityQuestionsResult',
    'get_user_security_questions',
    'get_user_security_questions_output',
]

@pulumi.output_type
class GetUserSecurityQuestionsResult:
    """
    A collection of values returned by getUserSecurityQuestions.
    """
    def __init__(__self__, id=None, questions=None, user_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if questions and not isinstance(questions, list):
            raise TypeError("Expected argument 'questions' to be a list")
        pulumi.set(__self__, "questions", questions)
        if user_id and not isinstance(user_id, str):
            raise TypeError("Expected argument 'user_id' to be a str")
        pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def questions(self) -> Sequence['outputs.GetUserSecurityQuestionsQuestionResult']:
        """
        collection of user's security question retrieved from Okta with the following properties:
        """
        return pulumi.get(self, "questions")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> str:
        return pulumi.get(self, "user_id")


class AwaitableGetUserSecurityQuestionsResult(GetUserSecurityQuestionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserSecurityQuestionsResult(
            id=self.id,
            questions=self.questions,
            user_id=self.user_id)


def get_user_security_questions(user_id: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserSecurityQuestionsResult:
    """
    Use this data source to retrieve a list of user's security questions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_okta as okta

    example_user = okta.user.User("example",
        first_name="John",
        last_name="Smith",
        login="john.smith@example.com",
        email="john.smith@example.com")
    example = okta.get_user_security_questions_output(user_id=example_user.id)
    ```


    :param str user_id: User ID.
    """
    __args__ = dict()
    __args__['userId'] = user_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('okta:index/getUserSecurityQuestions:getUserSecurityQuestions', __args__, opts=opts, typ=GetUserSecurityQuestionsResult).value

    return AwaitableGetUserSecurityQuestionsResult(
        id=pulumi.get(__ret__, 'id'),
        questions=pulumi.get(__ret__, 'questions'),
        user_id=pulumi.get(__ret__, 'user_id'))


@_utilities.lift_output_func(get_user_security_questions)
def get_user_security_questions_output(user_id: Optional[pulumi.Input[str]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserSecurityQuestionsResult]:
    """
    Use this data source to retrieve a list of user's security questions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_okta as okta

    example_user = okta.user.User("example",
        first_name="John",
        last_name="Smith",
        login="john.smith@example.com",
        email="john.smith@example.com")
    example = okta.get_user_security_questions_output(user_id=example_user.id)
    ```


    :param str user_id: User ID.
    """
    ...
