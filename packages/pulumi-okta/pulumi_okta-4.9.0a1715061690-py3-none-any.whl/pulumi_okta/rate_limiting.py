# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['RateLimitingArgs', 'RateLimiting']

@pulumi.input_type
class RateLimitingArgs:
    def __init__(__self__, *,
                 authorize: pulumi.Input[str],
                 login: pulumi.Input[str],
                 communications_enabled: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a RateLimiting resource.
        :param pulumi.Input[str] authorize: Called during authentication. Valid values: `"ENFORCE"` _(Enforce limit and
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        :param pulumi.Input[str] login: Called when accessing the Okta hosted login page. Valid values: `"ENFORCE"` _(Enforce limit and 
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        :param pulumi.Input[bool] communications_enabled: Enable or disable rate limiting communications. By default, it is `true`.
        """
        pulumi.set(__self__, "authorize", authorize)
        pulumi.set(__self__, "login", login)
        if communications_enabled is not None:
            pulumi.set(__self__, "communications_enabled", communications_enabled)

    @property
    @pulumi.getter
    def authorize(self) -> pulumi.Input[str]:
        """
        Called during authentication. Valid values: `"ENFORCE"` _(Enforce limit and
        log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        return pulumi.get(self, "authorize")

    @authorize.setter
    def authorize(self, value: pulumi.Input[str]):
        pulumi.set(self, "authorize", value)

    @property
    @pulumi.getter
    def login(self) -> pulumi.Input[str]:
        """
        Called when accessing the Okta hosted login page. Valid values: `"ENFORCE"` _(Enforce limit and 
        log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        return pulumi.get(self, "login")

    @login.setter
    def login(self, value: pulumi.Input[str]):
        pulumi.set(self, "login", value)

    @property
    @pulumi.getter(name="communicationsEnabled")
    def communications_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable rate limiting communications. By default, it is `true`.
        """
        return pulumi.get(self, "communications_enabled")

    @communications_enabled.setter
    def communications_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "communications_enabled", value)


@pulumi.input_type
class _RateLimitingState:
    def __init__(__self__, *,
                 authorize: Optional[pulumi.Input[str]] = None,
                 communications_enabled: Optional[pulumi.Input[bool]] = None,
                 login: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering RateLimiting resources.
        :param pulumi.Input[str] authorize: Called during authentication. Valid values: `"ENFORCE"` _(Enforce limit and
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        :param pulumi.Input[bool] communications_enabled: Enable or disable rate limiting communications. By default, it is `true`.
        :param pulumi.Input[str] login: Called when accessing the Okta hosted login page. Valid values: `"ENFORCE"` _(Enforce limit and 
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        if authorize is not None:
            pulumi.set(__self__, "authorize", authorize)
        if communications_enabled is not None:
            pulumi.set(__self__, "communications_enabled", communications_enabled)
        if login is not None:
            pulumi.set(__self__, "login", login)

    @property
    @pulumi.getter
    def authorize(self) -> Optional[pulumi.Input[str]]:
        """
        Called during authentication. Valid values: `"ENFORCE"` _(Enforce limit and
        log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        return pulumi.get(self, "authorize")

    @authorize.setter
    def authorize(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authorize", value)

    @property
    @pulumi.getter(name="communicationsEnabled")
    def communications_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable rate limiting communications. By default, it is `true`.
        """
        return pulumi.get(self, "communications_enabled")

    @communications_enabled.setter
    def communications_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "communications_enabled", value)

    @property
    @pulumi.getter
    def login(self) -> Optional[pulumi.Input[str]]:
        """
        Called when accessing the Okta hosted login page. Valid values: `"ENFORCE"` _(Enforce limit and 
        log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        return pulumi.get(self, "login")

    @login.setter
    def login(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "login", value)


class RateLimiting(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorize: Optional[pulumi.Input[str]] = None,
                 communications_enabled: Optional[pulumi.Input[bool]] = None,
                 login: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource allows you to configure the client-based rate limit and rate limiting communications settings.

        > **WARNING:** This resource is available only when using a SSWS API token in the provider config, it is incompatible with OAuth 2.0 authentication.

        > **WARNING:** This resource makes use of an internal/private Okta API endpoint that could change without notice rendering this resource inoperable.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.RateLimiting("example",
            login="ENFORCE",
            authorize="ENFORCE",
            communications_enabled=True)
        ```

        ## Import

        Rate limit settings can be imported without any parameters.

        ```sh
        $ pulumi import okta:index/rateLimiting:RateLimiting example .
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorize: Called during authentication. Valid values: `"ENFORCE"` _(Enforce limit and
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        :param pulumi.Input[bool] communications_enabled: Enable or disable rate limiting communications. By default, it is `true`.
        :param pulumi.Input[str] login: Called when accessing the Okta hosted login page. Valid values: `"ENFORCE"` _(Enforce limit and 
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RateLimitingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows you to configure the client-based rate limit and rate limiting communications settings.

        > **WARNING:** This resource is available only when using a SSWS API token in the provider config, it is incompatible with OAuth 2.0 authentication.

        > **WARNING:** This resource makes use of an internal/private Okta API endpoint that could change without notice rendering this resource inoperable.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.RateLimiting("example",
            login="ENFORCE",
            authorize="ENFORCE",
            communications_enabled=True)
        ```

        ## Import

        Rate limit settings can be imported without any parameters.

        ```sh
        $ pulumi import okta:index/rateLimiting:RateLimiting example .
        ```

        :param str resource_name: The name of the resource.
        :param RateLimitingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RateLimitingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorize: Optional[pulumi.Input[str]] = None,
                 communications_enabled: Optional[pulumi.Input[bool]] = None,
                 login: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = RateLimitingArgs.__new__(RateLimitingArgs)

            if authorize is None and not opts.urn:
                raise TypeError("Missing required property 'authorize'")
            __props__.__dict__["authorize"] = authorize
            __props__.__dict__["communications_enabled"] = communications_enabled
            if login is None and not opts.urn:
                raise TypeError("Missing required property 'login'")
            __props__.__dict__["login"] = login
        super(RateLimiting, __self__).__init__(
            'okta:index/rateLimiting:RateLimiting',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            authorize: Optional[pulumi.Input[str]] = None,
            communications_enabled: Optional[pulumi.Input[bool]] = None,
            login: Optional[pulumi.Input[str]] = None) -> 'RateLimiting':
        """
        Get an existing RateLimiting resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorize: Called during authentication. Valid values: `"ENFORCE"` _(Enforce limit and
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        :param pulumi.Input[bool] communications_enabled: Enable or disable rate limiting communications. By default, it is `true`.
        :param pulumi.Input[str] login: Called when accessing the Okta hosted login page. Valid values: `"ENFORCE"` _(Enforce limit and 
               log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _RateLimitingState.__new__(_RateLimitingState)

        __props__.__dict__["authorize"] = authorize
        __props__.__dict__["communications_enabled"] = communications_enabled
        __props__.__dict__["login"] = login
        return RateLimiting(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def authorize(self) -> pulumi.Output[str]:
        """
        Called during authentication. Valid values: `"ENFORCE"` _(Enforce limit and
        log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        return pulumi.get(self, "authorize")

    @property
    @pulumi.getter(name="communicationsEnabled")
    def communications_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable or disable rate limiting communications. By default, it is `true`.
        """
        return pulumi.get(self, "communications_enabled")

    @property
    @pulumi.getter
    def login(self) -> pulumi.Output[str]:
        """
        Called when accessing the Okta hosted login page. Valid values: `"ENFORCE"` _(Enforce limit and 
        log per client (recommended))_, `"DISABLE"` _(Do nothing (not recommended))_, `"PREVIEW"` _(Log per client)_.
        """
        return pulumi.get(self, "login")

