# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetUsersResult',
    'AwaitableGetUsersResult',
    'get_users',
    'get_users_output',
]

@pulumi.output_type
class GetUsersResult:
    """
    A collection of values returned by getUsers.
    """
    def __init__(__self__, compound_search_operator=None, delay_read_seconds=None, group_id=None, id=None, include_groups=None, include_roles=None, searches=None, users=None):
        if compound_search_operator and not isinstance(compound_search_operator, str):
            raise TypeError("Expected argument 'compound_search_operator' to be a str")
        pulumi.set(__self__, "compound_search_operator", compound_search_operator)
        if delay_read_seconds and not isinstance(delay_read_seconds, str):
            raise TypeError("Expected argument 'delay_read_seconds' to be a str")
        pulumi.set(__self__, "delay_read_seconds", delay_read_seconds)
        if group_id and not isinstance(group_id, str):
            raise TypeError("Expected argument 'group_id' to be a str")
        pulumi.set(__self__, "group_id", group_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if include_groups and not isinstance(include_groups, bool):
            raise TypeError("Expected argument 'include_groups' to be a bool")
        pulumi.set(__self__, "include_groups", include_groups)
        if include_roles and not isinstance(include_roles, bool):
            raise TypeError("Expected argument 'include_roles' to be a bool")
        pulumi.set(__self__, "include_roles", include_roles)
        if searches and not isinstance(searches, list):
            raise TypeError("Expected argument 'searches' to be a list")
        pulumi.set(__self__, "searches", searches)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="compoundSearchOperator")
    def compound_search_operator(self) -> Optional[str]:
        return pulumi.get(self, "compound_search_operator")

    @property
    @pulumi.getter(name="delayReadSeconds")
    def delay_read_seconds(self) -> Optional[str]:
        return pulumi.get(self, "delay_read_seconds")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[str]:
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="includeGroups")
    def include_groups(self) -> Optional[bool]:
        return pulumi.get(self, "include_groups")

    @property
    @pulumi.getter(name="includeRoles")
    def include_roles(self) -> Optional[bool]:
        return pulumi.get(self, "include_roles")

    @property
    @pulumi.getter
    def searches(self) -> Optional[Sequence['outputs.GetUsersSearchResult']]:
        return pulumi.get(self, "searches")

    @property
    @pulumi.getter
    def users(self) -> Sequence['outputs.GetUsersUserResult']:
        """
        collection of users retrieved from Okta with the following properties.
        """
        return pulumi.get(self, "users")


class AwaitableGetUsersResult(GetUsersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUsersResult(
            compound_search_operator=self.compound_search_operator,
            delay_read_seconds=self.delay_read_seconds,
            group_id=self.group_id,
            id=self.id,
            include_groups=self.include_groups,
            include_roles=self.include_roles,
            searches=self.searches,
            users=self.users)


def get_users(compound_search_operator: Optional[str] = None,
              delay_read_seconds: Optional[str] = None,
              group_id: Optional[str] = None,
              include_groups: Optional[bool] = None,
              include_roles: Optional[bool] = None,
              searches: Optional[Sequence[pulumi.InputType['GetUsersSearchArgs']]] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUsersResult:
    """
    Use this data source to retrieve a list of users from Okta.

    ## Example Usage

    ### Lookup Users by Group Membership
    ```python
    import pulumi
    import pulumi_okta as okta

    example_group = okta.group.Group("example", name="example-group")
    example = okta.user.get_users_output(group_id=example_group.id,
        include_groups=True,
        include_roles=True)
    ```


    :param str compound_search_operator: Given multiple search elements they will be compounded together with the op. Default is `and`, `or` is also valid.
    :param str delay_read_seconds: Force delay of the users read by N seconds. Useful when eventual consistency of users information needs to be allowed for; for instance, when administrator roles are known to have been applied.
    :param str group_id: Id of group used to find users based on membership.
    :param bool include_groups: Fetch each user's group memberships. Defaults to `false`, in which case the `group_memberships` user attribute will be empty.
    :param bool include_roles: Fetch each user's administrator roles. Defaults to `false`, in which case the `admin_roles` user attribute will be empty.
    :param Sequence[pulumi.InputType['GetUsersSearchArgs']] searches: Map of search criteria. It supports the following properties.
    """
    __args__ = dict()
    __args__['compoundSearchOperator'] = compound_search_operator
    __args__['delayReadSeconds'] = delay_read_seconds
    __args__['groupId'] = group_id
    __args__['includeGroups'] = include_groups
    __args__['includeRoles'] = include_roles
    __args__['searches'] = searches
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('okta:user/getUsers:getUsers', __args__, opts=opts, typ=GetUsersResult).value

    return AwaitableGetUsersResult(
        compound_search_operator=pulumi.get(__ret__, 'compound_search_operator'),
        delay_read_seconds=pulumi.get(__ret__, 'delay_read_seconds'),
        group_id=pulumi.get(__ret__, 'group_id'),
        id=pulumi.get(__ret__, 'id'),
        include_groups=pulumi.get(__ret__, 'include_groups'),
        include_roles=pulumi.get(__ret__, 'include_roles'),
        searches=pulumi.get(__ret__, 'searches'),
        users=pulumi.get(__ret__, 'users'))


@_utilities.lift_output_func(get_users)
def get_users_output(compound_search_operator: Optional[pulumi.Input[Optional[str]]] = None,
                     delay_read_seconds: Optional[pulumi.Input[Optional[str]]] = None,
                     group_id: Optional[pulumi.Input[Optional[str]]] = None,
                     include_groups: Optional[pulumi.Input[Optional[bool]]] = None,
                     include_roles: Optional[pulumi.Input[Optional[bool]]] = None,
                     searches: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetUsersSearchArgs']]]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUsersResult]:
    """
    Use this data source to retrieve a list of users from Okta.

    ## Example Usage

    ### Lookup Users by Group Membership
    ```python
    import pulumi
    import pulumi_okta as okta

    example_group = okta.group.Group("example", name="example-group")
    example = okta.user.get_users_output(group_id=example_group.id,
        include_groups=True,
        include_roles=True)
    ```


    :param str compound_search_operator: Given multiple search elements they will be compounded together with the op. Default is `and`, `or` is also valid.
    :param str delay_read_seconds: Force delay of the users read by N seconds. Useful when eventual consistency of users information needs to be allowed for; for instance, when administrator roles are known to have been applied.
    :param str group_id: Id of group used to find users based on membership.
    :param bool include_groups: Fetch each user's group memberships. Defaults to `false`, in which case the `group_memberships` user attribute will be empty.
    :param bool include_roles: Fetch each user's administrator roles. Defaults to `false`, in which case the `admin_roles` user attribute will be empty.
    :param Sequence[pulumi.InputType['GetUsersSearchArgs']] searches: Map of search criteria. It supports the following properties.
    """
    ...
