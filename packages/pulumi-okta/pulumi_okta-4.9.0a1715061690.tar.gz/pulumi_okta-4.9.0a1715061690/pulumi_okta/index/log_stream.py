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

__all__ = ['LogStreamArgs', 'LogStream']

@pulumi.input_type
class LogStreamArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input['LogStreamSettingsArgs']] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a LogStream resource.
        :param pulumi.Input[str] type: Type of the Log Stream - can either be `"aws_eventbridge"` or `"splunk_cloud_logstreaming"` only.
        :param pulumi.Input[str] name: Name of the Log Stream Resource.
        :param pulumi.Input['LogStreamSettingsArgs'] settings: Stream provider specific configuration.
        :param pulumi.Input[str] status: Log Stream Status - can either be ACTIVE or INACTIVE only. Default is ACTIVE.
        """
        pulumi.set(__self__, "type", type)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if settings is not None:
            pulumi.set(__self__, "settings", settings)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Type of the Log Stream - can either be `"aws_eventbridge"` or `"splunk_cloud_logstreaming"` only.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Log Stream Resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def settings(self) -> Optional[pulumi.Input['LogStreamSettingsArgs']]:
        """
        Stream provider specific configuration.
        """
        return pulumi.get(self, "settings")

    @settings.setter
    def settings(self, value: Optional[pulumi.Input['LogStreamSettingsArgs']]):
        pulumi.set(self, "settings", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Log Stream Status - can either be ACTIVE or INACTIVE only. Default is ACTIVE.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _LogStreamState:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input['LogStreamSettingsArgs']] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LogStream resources.
        :param pulumi.Input[str] name: Name of the Log Stream Resource.
        :param pulumi.Input['LogStreamSettingsArgs'] settings: Stream provider specific configuration.
        :param pulumi.Input[str] status: Log Stream Status - can either be ACTIVE or INACTIVE only. Default is ACTIVE.
        :param pulumi.Input[str] type: Type of the Log Stream - can either be `"aws_eventbridge"` or `"splunk_cloud_logstreaming"` only.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if settings is not None:
            pulumi.set(__self__, "settings", settings)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Log Stream Resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def settings(self) -> Optional[pulumi.Input['LogStreamSettingsArgs']]:
        """
        Stream provider specific configuration.
        """
        return pulumi.get(self, "settings")

    @settings.setter
    def settings(self, value: Optional[pulumi.Input['LogStreamSettingsArgs']]):
        pulumi.set(self, "settings", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Log Stream Status - can either be ACTIVE or INACTIVE only. Default is ACTIVE.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of the Log Stream - can either be `"aws_eventbridge"` or `"splunk_cloud_logstreaming"` only.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class LogStream(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[pulumi.InputType['LogStreamSettingsArgs']]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates an Okta Log Stream.

        This resource allows you to create and configure an Okta Log Stream.

        ## Example Usage

        ## Import

        Okta Log Stream can be imported via the Okta ID.

        ```sh
        $ pulumi import okta:Index/logStream:LogStream example &#60;strema id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the Log Stream Resource.
        :param pulumi.Input[pulumi.InputType['LogStreamSettingsArgs']] settings: Stream provider specific configuration.
        :param pulumi.Input[str] status: Log Stream Status - can either be ACTIVE or INACTIVE only. Default is ACTIVE.
        :param pulumi.Input[str] type: Type of the Log Stream - can either be `"aws_eventbridge"` or `"splunk_cloud_logstreaming"` only.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LogStreamArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates an Okta Log Stream.

        This resource allows you to create and configure an Okta Log Stream.

        ## Example Usage

        ## Import

        Okta Log Stream can be imported via the Okta ID.

        ```sh
        $ pulumi import okta:Index/logStream:LogStream example &#60;strema id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param LogStreamArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogStreamArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[pulumi.InputType['LogStreamSettingsArgs']]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LogStreamArgs.__new__(LogStreamArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["settings"] = settings
            __props__.__dict__["status"] = status
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        super(LogStream, __self__).__init__(
            'okta:Index/logStream:LogStream',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            settings: Optional[pulumi.Input[pulumi.InputType['LogStreamSettingsArgs']]] = None,
            status: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'LogStream':
        """
        Get an existing LogStream resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: Name of the Log Stream Resource.
        :param pulumi.Input[pulumi.InputType['LogStreamSettingsArgs']] settings: Stream provider specific configuration.
        :param pulumi.Input[str] status: Log Stream Status - can either be ACTIVE or INACTIVE only. Default is ACTIVE.
        :param pulumi.Input[str] type: Type of the Log Stream - can either be `"aws_eventbridge"` or `"splunk_cloud_logstreaming"` only.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LogStreamState.__new__(_LogStreamState)

        __props__.__dict__["name"] = name
        __props__.__dict__["settings"] = settings
        __props__.__dict__["status"] = status
        __props__.__dict__["type"] = type
        return LogStream(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the Log Stream Resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def settings(self) -> pulumi.Output[Optional['outputs.LogStreamSettings']]:
        """
        Stream provider specific configuration.
        """
        return pulumi.get(self, "settings")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[str]]:
        """
        Log Stream Status - can either be ACTIVE or INACTIVE only. Default is ACTIVE.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the Log Stream - can either be `"aws_eventbridge"` or `"splunk_cloud_logstreaming"` only.
        """
        return pulumi.get(self, "type")

