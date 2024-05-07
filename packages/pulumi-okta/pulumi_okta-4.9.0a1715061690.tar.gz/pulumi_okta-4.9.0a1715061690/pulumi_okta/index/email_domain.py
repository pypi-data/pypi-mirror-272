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

__all__ = ['EmailDomainArgs', 'EmailDomain']

@pulumi.input_type
class EmailDomainArgs:
    def __init__(__self__, *,
                 brand_id: pulumi.Input[str],
                 display_name: pulumi.Input[str],
                 domain: pulumi.Input[str],
                 user_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a EmailDomain resource.
        :param pulumi.Input[str] brand_id: Brand id of the email domain.
        :param pulumi.Input[str] display_name: Display name of the email domain.
        :param pulumi.Input[str] domain: Mail domain to send from.
        :param pulumi.Input[str] user_name: User name of the email domain.
        """
        pulumi.set(__self__, "brand_id", brand_id)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "domain", domain)
        pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="brandId")
    def brand_id(self) -> pulumi.Input[str]:
        """
        Brand id of the email domain.
        """
        return pulumi.get(self, "brand_id")

    @brand_id.setter
    def brand_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "brand_id", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        Display name of the email domain.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Input[str]:
        """
        Mail domain to send from.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Input[str]:
        """
        User name of the email domain.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_name", value)


@pulumi.input_type
class _EmailDomainState:
    def __init__(__self__, *,
                 brand_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 dns_validation_records: Optional[pulumi.Input[Sequence[pulumi.Input['EmailDomainDnsValidationRecordArgs']]]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 validation_status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EmailDomain resources.
        :param pulumi.Input[str] brand_id: Brand id of the email domain.
        :param pulumi.Input[str] display_name: Display name of the email domain.
        :param pulumi.Input[Sequence[pulumi.Input['EmailDomainDnsValidationRecordArgs']]] dns_validation_records: TXT and CNAME records to be registered for the domain.
        :param pulumi.Input[str] domain: Mail domain to send from.
        :param pulumi.Input[str] user_name: User name of the email domain.
        :param pulumi.Input[str] validation_status: Status of the email domain (shows whether the domain is verified).
        """
        if brand_id is not None:
            pulumi.set(__self__, "brand_id", brand_id)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if dns_validation_records is not None:
            pulumi.set(__self__, "dns_validation_records", dns_validation_records)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)
        if validation_status is not None:
            pulumi.set(__self__, "validation_status", validation_status)

    @property
    @pulumi.getter(name="brandId")
    def brand_id(self) -> Optional[pulumi.Input[str]]:
        """
        Brand id of the email domain.
        """
        return pulumi.get(self, "brand_id")

    @brand_id.setter
    def brand_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "brand_id", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Display name of the email domain.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="dnsValidationRecords")
    def dns_validation_records(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EmailDomainDnsValidationRecordArgs']]]]:
        """
        TXT and CNAME records to be registered for the domain.
        """
        return pulumi.get(self, "dns_validation_records")

    @dns_validation_records.setter
    def dns_validation_records(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EmailDomainDnsValidationRecordArgs']]]]):
        pulumi.set(self, "dns_validation_records", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        Mail domain to send from.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        User name of the email domain.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)

    @property
    @pulumi.getter(name="validationStatus")
    def validation_status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of the email domain (shows whether the domain is verified).
        """
        return pulumi.get(self, "validation_status")

    @validation_status.setter
    def validation_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "validation_status", value)


class EmailDomain(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 brand_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This resource allows you to create and configure an email domain.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.index.EmailDomain("example",
            brand_id="abc123",
            domain="example.com",
            display_name="test",
            user_name="paul_atreides")
        ```

        ## Import

        Custom email domain can be imported via the Okta ID.

        ```sh
        $ pulumi import okta:Index/emailDomain:EmailDomain example &#60;domain id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] brand_id: Brand id of the email domain.
        :param pulumi.Input[str] display_name: Display name of the email domain.
        :param pulumi.Input[str] domain: Mail domain to send from.
        :param pulumi.Input[str] user_name: User name of the email domain.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EmailDomainArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows you to create and configure an email domain.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.index.EmailDomain("example",
            brand_id="abc123",
            domain="example.com",
            display_name="test",
            user_name="paul_atreides")
        ```

        ## Import

        Custom email domain can be imported via the Okta ID.

        ```sh
        $ pulumi import okta:Index/emailDomain:EmailDomain example &#60;domain id&#62;
        ```

        :param str resource_name: The name of the resource.
        :param EmailDomainArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EmailDomainArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 brand_id: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EmailDomainArgs.__new__(EmailDomainArgs)

            if brand_id is None and not opts.urn:
                raise TypeError("Missing required property 'brand_id'")
            __props__.__dict__["brand_id"] = brand_id
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            if domain is None and not opts.urn:
                raise TypeError("Missing required property 'domain'")
            __props__.__dict__["domain"] = domain
            if user_name is None and not opts.urn:
                raise TypeError("Missing required property 'user_name'")
            __props__.__dict__["user_name"] = user_name
            __props__.__dict__["dns_validation_records"] = None
            __props__.__dict__["validation_status"] = None
        super(EmailDomain, __self__).__init__(
            'okta:Index/emailDomain:EmailDomain',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            brand_id: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            dns_validation_records: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EmailDomainDnsValidationRecordArgs']]]]] = None,
            domain: Optional[pulumi.Input[str]] = None,
            user_name: Optional[pulumi.Input[str]] = None,
            validation_status: Optional[pulumi.Input[str]] = None) -> 'EmailDomain':
        """
        Get an existing EmailDomain resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] brand_id: Brand id of the email domain.
        :param pulumi.Input[str] display_name: Display name of the email domain.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EmailDomainDnsValidationRecordArgs']]]] dns_validation_records: TXT and CNAME records to be registered for the domain.
        :param pulumi.Input[str] domain: Mail domain to send from.
        :param pulumi.Input[str] user_name: User name of the email domain.
        :param pulumi.Input[str] validation_status: Status of the email domain (shows whether the domain is verified).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EmailDomainState.__new__(_EmailDomainState)

        __props__.__dict__["brand_id"] = brand_id
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["dns_validation_records"] = dns_validation_records
        __props__.__dict__["domain"] = domain
        __props__.__dict__["user_name"] = user_name
        __props__.__dict__["validation_status"] = validation_status
        return EmailDomain(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="brandId")
    def brand_id(self) -> pulumi.Output[str]:
        """
        Brand id of the email domain.
        """
        return pulumi.get(self, "brand_id")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Display name of the email domain.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="dnsValidationRecords")
    def dns_validation_records(self) -> pulumi.Output[Sequence['outputs.EmailDomainDnsValidationRecord']]:
        """
        TXT and CNAME records to be registered for the domain.
        """
        return pulumi.get(self, "dns_validation_records")

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[str]:
        """
        Mail domain to send from.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[str]:
        """
        User name of the email domain.
        """
        return pulumi.get(self, "user_name")

    @property
    @pulumi.getter(name="validationStatus")
    def validation_status(self) -> pulumi.Output[str]:
        """
        Status of the email domain (shows whether the domain is verified).
        """
        return pulumi.get(self, "validation_status")

