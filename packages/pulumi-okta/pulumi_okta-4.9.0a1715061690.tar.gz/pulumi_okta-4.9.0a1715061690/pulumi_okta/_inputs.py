# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'AppGroupAssignmentsGroupArgs',
    'AppSignonPolicyRulePlatformIncludeArgs',
    'AppUserSchemaPropertyArrayOneOfArgs',
    'AppUserSchemaPropertyOneOfArgs',
    'DomainDnsRecordArgs',
    'EmailSenderDnsRecordArgs',
    'EventHookHeaderArgs',
    'GroupSchemaPropertyArrayOneOfArgs',
    'GroupSchemaPropertyMasterOverridePriorityArgs',
    'GroupSchemaPropertyOneOfArgs',
    'PolicyRuleProfileEnrollmentProfileAttributeArgs',
    'TemplateSmsTranslationArgs',
    'UserSchemaPropertyArrayOneOfArgs',
    'UserSchemaPropertyMasterOverridePriorityArgs',
    'UserSchemaPropertyOneOfArgs',
]

@pulumi.input_type
class AppGroupAssignmentsGroupArgs:
    def __init__(__self__, *,
                 id: pulumi.Input[str],
                 profile: pulumi.Input[str],
                 priority: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] id: ID of the group to assign.
        :param pulumi.Input[str] profile: JSON document containing [application profile](https://developer.okta.com/docs/reference/api/apps/#profile-object)
        :param pulumi.Input[int] priority: Priority of group assignment
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "profile", profile)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)

    @property
    @pulumi.getter
    def id(self) -> pulumi.Input[str]:
        """
        ID of the group to assign.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: pulumi.Input[str]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def profile(self) -> pulumi.Input[str]:
        """
        JSON document containing [application profile](https://developer.okta.com/docs/reference/api/apps/#profile-object)
        """
        return pulumi.get(self, "profile")

    @profile.setter
    def profile(self, value: pulumi.Input[str]):
        pulumi.set(self, "profile", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        Priority of group assignment
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)


@pulumi.input_type
class AppSignonPolicyRulePlatformIncludeArgs:
    def __init__(__self__, *,
                 os_expression: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] os_expression: Only available and required when using `os_type = "OTHER"`
        :param pulumi.Input[str] os_type: One of: `"ANY"`, `"IOS"`, `"WINDOWS"`, `"ANDROID"`, `"OTHER"`, `"OSX"`, `"MACOS"`, `"CHROMEOS"`
        :param pulumi.Input[str] type: One of: `"ANY"`, `"MOBILE"`, `"DESKTOP"`
        """
        if os_expression is not None:
            pulumi.set(__self__, "os_expression", os_expression)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="osExpression")
    def os_expression(self) -> Optional[pulumi.Input[str]]:
        """
        Only available and required when using `os_type = "OTHER"`
        """
        return pulumi.get(self, "os_expression")

    @os_expression.setter
    def os_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "os_expression", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[str]]:
        """
        One of: `"ANY"`, `"IOS"`, `"WINDOWS"`, `"ANDROID"`, `"OTHER"`, `"OSX"`, `"MACOS"`, `"CHROMEOS"`
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        One of: `"ANY"`, `"MOBILE"`, `"DESKTOP"`
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class AppUserSchemaPropertyArrayOneOfArgs:
    def __init__(__self__, *,
                 const: pulumi.Input[str],
                 title: pulumi.Input[str]):
        """
        :param pulumi.Input[str] const: value mapping to member of `array_enum`.
        :param pulumi.Input[str] title: display name for the enum value.
        """
        pulumi.set(__self__, "const", const)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def const(self) -> pulumi.Input[str]:
        """
        value mapping to member of `array_enum`.
        """
        return pulumi.get(self, "const")

    @const.setter
    def const(self, value: pulumi.Input[str]):
        pulumi.set(self, "const", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        display name for the enum value.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class AppUserSchemaPropertyOneOfArgs:
    def __init__(__self__, *,
                 const: pulumi.Input[str],
                 title: pulumi.Input[str]):
        """
        :param pulumi.Input[str] const: value mapping to member of `enum`.
        :param pulumi.Input[str] title: display name for the enum value.
        """
        pulumi.set(__self__, "const", const)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def const(self) -> pulumi.Input[str]:
        """
        value mapping to member of `enum`.
        """
        return pulumi.get(self, "const")

    @const.setter
    def const(self, value: pulumi.Input[str]):
        pulumi.set(self, "const", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        display name for the enum value.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class DomainDnsRecordArgs:
    def __init__(__self__, *,
                 expiration: Optional[pulumi.Input[str]] = None,
                 fqdn: Optional[pulumi.Input[str]] = None,
                 record_type: Optional[pulumi.Input[str]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] expiration: TXT record expiration.
        :param pulumi.Input[str] fqdn: DNS record name.
        :param pulumi.Input[str] record_type: Record type can be TXT or CNAME.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: DNS verification value
        """
        if expiration is not None:
            pulumi.set(__self__, "expiration", expiration)
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if record_type is not None:
            pulumi.set(__self__, "record_type", record_type)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def expiration(self) -> Optional[pulumi.Input[str]]:
        """
        TXT record expiration.
        """
        return pulumi.get(self, "expiration")

    @expiration.setter
    def expiration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration", value)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        DNS record name.
        """
        return pulumi.get(self, "fqdn")

    @fqdn.setter
    def fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fqdn", value)

    @property
    @pulumi.getter(name="recordType")
    def record_type(self) -> Optional[pulumi.Input[str]]:
        """
        Record type can be TXT or CNAME.
        """
        return pulumi.get(self, "record_type")

    @record_type.setter
    def record_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "record_type", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        DNS verification value
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class EmailSenderDnsRecordArgs:
    def __init__(__self__, *,
                 fqdn: Optional[pulumi.Input[str]] = None,
                 record_type: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] fqdn: DNS record name.
        :param pulumi.Input[str] record_type: Record type can be TXT or CNAME.
        :param pulumi.Input[str] value: DNS verification value
        """
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if record_type is not None:
            pulumi.set(__self__, "record_type", record_type)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        DNS record name.
        """
        return pulumi.get(self, "fqdn")

    @fqdn.setter
    def fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fqdn", value)

    @property
    @pulumi.getter(name="recordType")
    def record_type(self) -> Optional[pulumi.Input[str]]:
        """
        Record type can be TXT or CNAME.
        """
        return pulumi.get(self, "record_type")

    @record_type.setter
    def record_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "record_type", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        DNS verification value
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class EventHookHeaderArgs:
    def __init__(__self__, *,
                 key: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        if key is not None:
            pulumi.set(__self__, "key", key)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class GroupSchemaPropertyArrayOneOfArgs:
    def __init__(__self__, *,
                 const: pulumi.Input[str],
                 title: pulumi.Input[str]):
        """
        :param pulumi.Input[str] const: value mapping to member of `enum`.
        :param pulumi.Input[str] title: display name for the enum value.
        """
        pulumi.set(__self__, "const", const)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def const(self) -> pulumi.Input[str]:
        """
        value mapping to member of `enum`.
        """
        return pulumi.get(self, "const")

    @const.setter
    def const(self, value: pulumi.Input[str]):
        pulumi.set(self, "const", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        display name for the enum value.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class GroupSchemaPropertyMasterOverridePriorityArgs:
    def __init__(__self__, *,
                 value: pulumi.Input[str],
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] value: ID of profile source.
        :param pulumi.Input[str] type: Type of profile source.
        """
        pulumi.set(__self__, "value", value)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        ID of profile source.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of profile source.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class GroupSchemaPropertyOneOfArgs:
    def __init__(__self__, *,
                 const: pulumi.Input[str],
                 title: pulumi.Input[str]):
        """
        :param pulumi.Input[str] const: value mapping to member of `enum`.
        :param pulumi.Input[str] title: display name for the enum value.
        """
        pulumi.set(__self__, "const", const)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def const(self) -> pulumi.Input[str]:
        """
        value mapping to member of `enum`.
        """
        return pulumi.get(self, "const")

    @const.setter
    def const(self, value: pulumi.Input[str]):
        pulumi.set(self, "const", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        display name for the enum value.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class PolicyRuleProfileEnrollmentProfileAttributeArgs:
    def __init__(__self__, *,
                 label: pulumi.Input[str],
                 name: pulumi.Input[str],
                 required: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] label: A display-friendly label for this property
        :param pulumi.Input[str] name: The name of a User Profile property
        :param pulumi.Input[bool] required: Indicates if this property is required for enrollment. Default is `false`.
        """
        pulumi.set(__self__, "label", label)
        pulumi.set(__self__, "name", name)
        if required is not None:
            pulumi.set(__self__, "required", required)

    @property
    @pulumi.getter
    def label(self) -> pulumi.Input[str]:
        """
        A display-friendly label for this property
        """
        return pulumi.get(self, "label")

    @label.setter
    def label(self, value: pulumi.Input[str]):
        pulumi.set(self, "label", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of a User Profile property
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def required(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates if this property is required for enrollment. Default is `false`.
        """
        return pulumi.get(self, "required")

    @required.setter
    def required(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "required", value)


@pulumi.input_type
class TemplateSmsTranslationArgs:
    def __init__(__self__, *,
                 language: pulumi.Input[str],
                 template: pulumi.Input[str]):
        """
        :param pulumi.Input[str] language: The language to map the template to.
        :param pulumi.Input[str] template: The SMS message.
        """
        pulumi.set(__self__, "language", language)
        pulumi.set(__self__, "template", template)

    @property
    @pulumi.getter
    def language(self) -> pulumi.Input[str]:
        """
        The language to map the template to.
        """
        return pulumi.get(self, "language")

    @language.setter
    def language(self, value: pulumi.Input[str]):
        pulumi.set(self, "language", value)

    @property
    @pulumi.getter
    def template(self) -> pulumi.Input[str]:
        """
        The SMS message.
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: pulumi.Input[str]):
        pulumi.set(self, "template", value)


@pulumi.input_type
class UserSchemaPropertyArrayOneOfArgs:
    def __init__(__self__, *,
                 const: pulumi.Input[str],
                 title: pulumi.Input[str]):
        """
        :param pulumi.Input[str] const: value mapping to member of `enum`.
        :param pulumi.Input[str] title: display name for the enum value.
        """
        pulumi.set(__self__, "const", const)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def const(self) -> pulumi.Input[str]:
        """
        value mapping to member of `enum`.
        """
        return pulumi.get(self, "const")

    @const.setter
    def const(self, value: pulumi.Input[str]):
        pulumi.set(self, "const", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        display name for the enum value.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)


@pulumi.input_type
class UserSchemaPropertyMasterOverridePriorityArgs:
    def __init__(__self__, *,
                 value: pulumi.Input[str],
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] value: ID of profile source.
        :param pulumi.Input[str] type: Type of profile source.
        """
        pulumi.set(__self__, "value", value)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        ID of profile source.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of profile source.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class UserSchemaPropertyOneOfArgs:
    def __init__(__self__, *,
                 const: pulumi.Input[str],
                 title: pulumi.Input[str]):
        """
        :param pulumi.Input[str] const: value mapping to member of `enum`.
        :param pulumi.Input[str] title: display name for the enum value.
        """
        pulumi.set(__self__, "const", const)
        pulumi.set(__self__, "title", title)

    @property
    @pulumi.getter
    def const(self) -> pulumi.Input[str]:
        """
        value mapping to member of `enum`.
        """
        return pulumi.get(self, "const")

    @const.setter
    def const(self, value: pulumi.Input[str]):
        pulumi.set(self, "const", value)

    @property
    @pulumi.getter
    def title(self) -> pulumi.Input[str]:
        """
        display name for the enum value.
        """
        return pulumi.get(self, "title")

    @title.setter
    def title(self, value: pulumi.Input[str]):
        pulumi.set(self, "title", value)


