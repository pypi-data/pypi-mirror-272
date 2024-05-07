# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['SecurityNotificationEmailsArgs', 'SecurityNotificationEmails']

@pulumi.input_type
class SecurityNotificationEmailsArgs:
    def __init__(__self__, *,
                 report_suspicious_activity_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_enrollment_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_reset_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_new_device_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_password_changed_enabled: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a SecurityNotificationEmails resource.
        :param pulumi.Input[bool] report_suspicious_activity_enabled: Notifies end users about suspicious or unrecognized activity from their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_enrollment_enabled: Notifies end users of any activity on their account related to MFA factor enrollment. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_reset_enabled: Notifies end users that one or more factors have been reset for their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_new_device_enabled: Notifies end users about new sign-on activity. Default is `true`.
        :param pulumi.Input[bool] send_email_for_password_changed_enabled: Notifies end users that the password for their account has changed. Default is `true`.
        """
        if report_suspicious_activity_enabled is not None:
            pulumi.set(__self__, "report_suspicious_activity_enabled", report_suspicious_activity_enabled)
        if send_email_for_factor_enrollment_enabled is not None:
            pulumi.set(__self__, "send_email_for_factor_enrollment_enabled", send_email_for_factor_enrollment_enabled)
        if send_email_for_factor_reset_enabled is not None:
            pulumi.set(__self__, "send_email_for_factor_reset_enabled", send_email_for_factor_reset_enabled)
        if send_email_for_new_device_enabled is not None:
            pulumi.set(__self__, "send_email_for_new_device_enabled", send_email_for_new_device_enabled)
        if send_email_for_password_changed_enabled is not None:
            pulumi.set(__self__, "send_email_for_password_changed_enabled", send_email_for_password_changed_enabled)

    @property
    @pulumi.getter(name="reportSuspiciousActivityEnabled")
    def report_suspicious_activity_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users about suspicious or unrecognized activity from their account. Default is `true`.
        """
        return pulumi.get(self, "report_suspicious_activity_enabled")

    @report_suspicious_activity_enabled.setter
    def report_suspicious_activity_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "report_suspicious_activity_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForFactorEnrollmentEnabled")
    def send_email_for_factor_enrollment_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users of any activity on their account related to MFA factor enrollment. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_factor_enrollment_enabled")

    @send_email_for_factor_enrollment_enabled.setter
    def send_email_for_factor_enrollment_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_factor_enrollment_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForFactorResetEnabled")
    def send_email_for_factor_reset_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users that one or more factors have been reset for their account. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_factor_reset_enabled")

    @send_email_for_factor_reset_enabled.setter
    def send_email_for_factor_reset_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_factor_reset_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForNewDeviceEnabled")
    def send_email_for_new_device_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users about new sign-on activity. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_new_device_enabled")

    @send_email_for_new_device_enabled.setter
    def send_email_for_new_device_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_new_device_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForPasswordChangedEnabled")
    def send_email_for_password_changed_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users that the password for their account has changed. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_password_changed_enabled")

    @send_email_for_password_changed_enabled.setter
    def send_email_for_password_changed_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_password_changed_enabled", value)


@pulumi.input_type
class _SecurityNotificationEmailsState:
    def __init__(__self__, *,
                 report_suspicious_activity_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_enrollment_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_reset_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_new_device_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_password_changed_enabled: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering SecurityNotificationEmails resources.
        :param pulumi.Input[bool] report_suspicious_activity_enabled: Notifies end users about suspicious or unrecognized activity from their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_enrollment_enabled: Notifies end users of any activity on their account related to MFA factor enrollment. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_reset_enabled: Notifies end users that one or more factors have been reset for their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_new_device_enabled: Notifies end users about new sign-on activity. Default is `true`.
        :param pulumi.Input[bool] send_email_for_password_changed_enabled: Notifies end users that the password for their account has changed. Default is `true`.
        """
        if report_suspicious_activity_enabled is not None:
            pulumi.set(__self__, "report_suspicious_activity_enabled", report_suspicious_activity_enabled)
        if send_email_for_factor_enrollment_enabled is not None:
            pulumi.set(__self__, "send_email_for_factor_enrollment_enabled", send_email_for_factor_enrollment_enabled)
        if send_email_for_factor_reset_enabled is not None:
            pulumi.set(__self__, "send_email_for_factor_reset_enabled", send_email_for_factor_reset_enabled)
        if send_email_for_new_device_enabled is not None:
            pulumi.set(__self__, "send_email_for_new_device_enabled", send_email_for_new_device_enabled)
        if send_email_for_password_changed_enabled is not None:
            pulumi.set(__self__, "send_email_for_password_changed_enabled", send_email_for_password_changed_enabled)

    @property
    @pulumi.getter(name="reportSuspiciousActivityEnabled")
    def report_suspicious_activity_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users about suspicious or unrecognized activity from their account. Default is `true`.
        """
        return pulumi.get(self, "report_suspicious_activity_enabled")

    @report_suspicious_activity_enabled.setter
    def report_suspicious_activity_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "report_suspicious_activity_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForFactorEnrollmentEnabled")
    def send_email_for_factor_enrollment_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users of any activity on their account related to MFA factor enrollment. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_factor_enrollment_enabled")

    @send_email_for_factor_enrollment_enabled.setter
    def send_email_for_factor_enrollment_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_factor_enrollment_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForFactorResetEnabled")
    def send_email_for_factor_reset_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users that one or more factors have been reset for their account. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_factor_reset_enabled")

    @send_email_for_factor_reset_enabled.setter
    def send_email_for_factor_reset_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_factor_reset_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForNewDeviceEnabled")
    def send_email_for_new_device_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users about new sign-on activity. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_new_device_enabled")

    @send_email_for_new_device_enabled.setter
    def send_email_for_new_device_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_new_device_enabled", value)

    @property
    @pulumi.getter(name="sendEmailForPasswordChangedEnabled")
    def send_email_for_password_changed_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Notifies end users that the password for their account has changed. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_password_changed_enabled")

    @send_email_for_password_changed_enabled.setter
    def send_email_for_password_changed_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "send_email_for_password_changed_enabled", value)


class SecurityNotificationEmails(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 report_suspicious_activity_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_enrollment_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_reset_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_new_device_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_password_changed_enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        This resource allows you to configure Security Notification Emails.

        > **WARNING:** This resource is available only when using a SSWS API token in the provider config, it is incompatible with OAuth 2.0 authentication.

        > **WARNING:** This resource makes use of an internal/private Okta API endpoint that could change without notice rendering this resource inoperable.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.SecurityNotificationEmails("example",
            report_suspicious_activity_enabled=True,
            send_email_for_factor_enrollment_enabled=True,
            send_email_for_factor_reset_enabled=True,
            send_email_for_new_device_enabled=True,
            send_email_for_password_changed_enabled=True)
        ```

        ## Import

        Security Notification Emails can be imported without any parameters.

        ```sh
        $ pulumi import okta:index/securityNotificationEmails:SecurityNotificationEmails example _
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] report_suspicious_activity_enabled: Notifies end users about suspicious or unrecognized activity from their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_enrollment_enabled: Notifies end users of any activity on their account related to MFA factor enrollment. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_reset_enabled: Notifies end users that one or more factors have been reset for their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_new_device_enabled: Notifies end users about new sign-on activity. Default is `true`.
        :param pulumi.Input[bool] send_email_for_password_changed_enabled: Notifies end users that the password for their account has changed. Default is `true`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[SecurityNotificationEmailsArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This resource allows you to configure Security Notification Emails.

        > **WARNING:** This resource is available only when using a SSWS API token in the provider config, it is incompatible with OAuth 2.0 authentication.

        > **WARNING:** This resource makes use of an internal/private Okta API endpoint that could change without notice rendering this resource inoperable.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.SecurityNotificationEmails("example",
            report_suspicious_activity_enabled=True,
            send_email_for_factor_enrollment_enabled=True,
            send_email_for_factor_reset_enabled=True,
            send_email_for_new_device_enabled=True,
            send_email_for_password_changed_enabled=True)
        ```

        ## Import

        Security Notification Emails can be imported without any parameters.

        ```sh
        $ pulumi import okta:index/securityNotificationEmails:SecurityNotificationEmails example _
        ```

        :param str resource_name: The name of the resource.
        :param SecurityNotificationEmailsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecurityNotificationEmailsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 report_suspicious_activity_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_enrollment_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_factor_reset_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_new_device_enabled: Optional[pulumi.Input[bool]] = None,
                 send_email_for_password_changed_enabled: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SecurityNotificationEmailsArgs.__new__(SecurityNotificationEmailsArgs)

            __props__.__dict__["report_suspicious_activity_enabled"] = report_suspicious_activity_enabled
            __props__.__dict__["send_email_for_factor_enrollment_enabled"] = send_email_for_factor_enrollment_enabled
            __props__.__dict__["send_email_for_factor_reset_enabled"] = send_email_for_factor_reset_enabled
            __props__.__dict__["send_email_for_new_device_enabled"] = send_email_for_new_device_enabled
            __props__.__dict__["send_email_for_password_changed_enabled"] = send_email_for_password_changed_enabled
        super(SecurityNotificationEmails, __self__).__init__(
            'okta:index/securityNotificationEmails:SecurityNotificationEmails',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            report_suspicious_activity_enabled: Optional[pulumi.Input[bool]] = None,
            send_email_for_factor_enrollment_enabled: Optional[pulumi.Input[bool]] = None,
            send_email_for_factor_reset_enabled: Optional[pulumi.Input[bool]] = None,
            send_email_for_new_device_enabled: Optional[pulumi.Input[bool]] = None,
            send_email_for_password_changed_enabled: Optional[pulumi.Input[bool]] = None) -> 'SecurityNotificationEmails':
        """
        Get an existing SecurityNotificationEmails resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] report_suspicious_activity_enabled: Notifies end users about suspicious or unrecognized activity from their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_enrollment_enabled: Notifies end users of any activity on their account related to MFA factor enrollment. Default is `true`.
        :param pulumi.Input[bool] send_email_for_factor_reset_enabled: Notifies end users that one or more factors have been reset for their account. Default is `true`.
        :param pulumi.Input[bool] send_email_for_new_device_enabled: Notifies end users about new sign-on activity. Default is `true`.
        :param pulumi.Input[bool] send_email_for_password_changed_enabled: Notifies end users that the password for their account has changed. Default is `true`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SecurityNotificationEmailsState.__new__(_SecurityNotificationEmailsState)

        __props__.__dict__["report_suspicious_activity_enabled"] = report_suspicious_activity_enabled
        __props__.__dict__["send_email_for_factor_enrollment_enabled"] = send_email_for_factor_enrollment_enabled
        __props__.__dict__["send_email_for_factor_reset_enabled"] = send_email_for_factor_reset_enabled
        __props__.__dict__["send_email_for_new_device_enabled"] = send_email_for_new_device_enabled
        __props__.__dict__["send_email_for_password_changed_enabled"] = send_email_for_password_changed_enabled
        return SecurityNotificationEmails(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="reportSuspiciousActivityEnabled")
    def report_suspicious_activity_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Notifies end users about suspicious or unrecognized activity from their account. Default is `true`.
        """
        return pulumi.get(self, "report_suspicious_activity_enabled")

    @property
    @pulumi.getter(name="sendEmailForFactorEnrollmentEnabled")
    def send_email_for_factor_enrollment_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Notifies end users of any activity on their account related to MFA factor enrollment. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_factor_enrollment_enabled")

    @property
    @pulumi.getter(name="sendEmailForFactorResetEnabled")
    def send_email_for_factor_reset_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Notifies end users that one or more factors have been reset for their account. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_factor_reset_enabled")

    @property
    @pulumi.getter(name="sendEmailForNewDeviceEnabled")
    def send_email_for_new_device_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Notifies end users about new sign-on activity. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_new_device_enabled")

    @property
    @pulumi.getter(name="sendEmailForPasswordChangedEnabled")
    def send_email_for_password_changed_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Notifies end users that the password for their account has changed. Default is `true`.
        """
        return pulumi.get(self, "send_email_for_password_changed_enabled")

