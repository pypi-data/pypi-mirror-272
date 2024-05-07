# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['DomainCertificateArgs', 'DomainCertificate']

@pulumi.input_type
class DomainCertificateArgs:
    def __init__(__self__, *,
                 certificate: pulumi.Input[str],
                 certificate_chain: pulumi.Input[str],
                 domain_id: pulumi.Input[str],
                 private_key: pulumi.Input[str],
                 type: pulumi.Input[str]):
        """
        The set of arguments for constructing a DomainCertificate resource.
        :param pulumi.Input[str] certificate: Certificate content.
        :param pulumi.Input[str] certificate_chain: Certificate certificate chain.
        :param pulumi.Input[str] domain_id: Domain ID.
        :param pulumi.Input[str] private_key: Certificate private key.
        :param pulumi.Input[str] type: Certificate type. Valid value is `"PEM"`.
        """
        pulumi.set(__self__, "certificate", certificate)
        pulumi.set(__self__, "certificate_chain", certificate_chain)
        pulumi.set(__self__, "domain_id", domain_id)
        pulumi.set(__self__, "private_key", private_key)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Input[str]:
        """
        Certificate content.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter(name="certificateChain")
    def certificate_chain(self) -> pulumi.Input[str]:
        """
        Certificate certificate chain.
        """
        return pulumi.get(self, "certificate_chain")

    @certificate_chain.setter
    def certificate_chain(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_chain", value)

    @property
    @pulumi.getter(name="domainId")
    def domain_id(self) -> pulumi.Input[str]:
        """
        Domain ID.
        """
        return pulumi.get(self, "domain_id")

    @domain_id.setter
    def domain_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_id", value)

    @property
    @pulumi.getter(name="privateKey")
    def private_key(self) -> pulumi.Input[str]:
        """
        Certificate private key.
        """
        return pulumi.get(self, "private_key")

    @private_key.setter
    def private_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "private_key", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Certificate type. Valid value is `"PEM"`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class _DomainCertificateState:
    def __init__(__self__, *,
                 certificate: Optional[pulumi.Input[str]] = None,
                 certificate_chain: Optional[pulumi.Input[str]] = None,
                 domain_id: Optional[pulumi.Input[str]] = None,
                 private_key: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DomainCertificate resources.
        :param pulumi.Input[str] certificate: Certificate content.
        :param pulumi.Input[str] certificate_chain: Certificate certificate chain.
        :param pulumi.Input[str] domain_id: Domain ID.
        :param pulumi.Input[str] private_key: Certificate private key.
        :param pulumi.Input[str] type: Certificate type. Valid value is `"PEM"`.
        """
        if certificate is not None:
            pulumi.set(__self__, "certificate", certificate)
        if certificate_chain is not None:
            pulumi.set(__self__, "certificate_chain", certificate_chain)
        if domain_id is not None:
            pulumi.set(__self__, "domain_id", domain_id)
        if private_key is not None:
            pulumi.set(__self__, "private_key", private_key)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def certificate(self) -> Optional[pulumi.Input[str]]:
        """
        Certificate content.
        """
        return pulumi.get(self, "certificate")

    @certificate.setter
    def certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate", value)

    @property
    @pulumi.getter(name="certificateChain")
    def certificate_chain(self) -> Optional[pulumi.Input[str]]:
        """
        Certificate certificate chain.
        """
        return pulumi.get(self, "certificate_chain")

    @certificate_chain.setter
    def certificate_chain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_chain", value)

    @property
    @pulumi.getter(name="domainId")
    def domain_id(self) -> Optional[pulumi.Input[str]]:
        """
        Domain ID.
        """
        return pulumi.get(self, "domain_id")

    @domain_id.setter
    def domain_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_id", value)

    @property
    @pulumi.getter(name="privateKey")
    def private_key(self) -> Optional[pulumi.Input[str]]:
        """
        Certificate private key.
        """
        return pulumi.get(self, "private_key")

    @private_key.setter
    def private_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_key", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Certificate type. Valid value is `"PEM"`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


class DomainCertificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 certificate_chain: Optional[pulumi.Input[str]] = None,
                 domain_id: Optional[pulumi.Input[str]] = None,
                 private_key: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages certificate for the domain.

        This resource's `certificate`, `private_key`, and `certificate_chain` attributes
        hold actual PEM values and can be referred to by other configs requiring
        certificate and private key inputs. This is inline with TF's best
        practices
        of not encrypting state.

        See Let's Encrypt Certbot notes at the end of this
        documentation for notes on how to generate a domain certificate with Let's
        Encrypt Certbot

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.Domain("example", name="www.example.com")
        test = okta.DomainCertificate("test",
            domain_id=test_okta_domain["id"],
            type="PEM",
            certificate=\"\"\"-----BEGIN CERTIFICATE-----
        MIIFNzCCBB+gAwIBAgISBAXomJWRama3ypu8TIxdA9wzMA0GCSqGSIb3DQEBCwUA
        ...
        NSgRtSXq11j8O4JONi8EXe7cEtvzUiLR5PL3itsK2svtrZ9jIwQ95wOPaA==
        -----END CERTIFICATE-----
        \"\"\",
            certificate_chain=\"\"\"-----BEGIN CERTIFICATE-----
        MIIFFjCCAv6gAwIBAgIRAJErCErPDBinU/bWLiWnX1owDQYJKoZIhvcNAQELBQAw
        ...
        Dfvp7OOGAN6dEOM4+qR9sdjoSYKEBpsr6GtPAQw4dy753ec5
        -----END CERTIFICATE-----
        \"\"\",
            private_key=\"\"\"-----BEGIN PRIVATE KEY-----
        MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC5cyk6x63iBJSW
        ...
        nUFLNE8pXSnsqb0eOL74f3uQ
        -----END PRIVATE KEY-----
        \"\"\")
        ```

        ## Let's Encrypt Certbot

        This example demonstrates generatoring a domain certificate with letsencrypt
        certbot https://letsencrypt.org/getting-started/

        Use letsencrypt's certbot to generate domain certificates in RSA output mode.
        The generator's output corresponds to `DomainCertificate` fields in the
        following manner.

        Okta Field          | Certbot file
        --------------------|--------------
        `certificate`       | `cert.pem`
        `certificate_chain` | `chain.pem`
        `private_key`       | `privkey.pem`

        ## Import

        This resource does not support importing.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate: Certificate content.
        :param pulumi.Input[str] certificate_chain: Certificate certificate chain.
        :param pulumi.Input[str] domain_id: Domain ID.
        :param pulumi.Input[str] private_key: Certificate private key.
        :param pulumi.Input[str] type: Certificate type. Valid value is `"PEM"`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DomainCertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages certificate for the domain.

        This resource's `certificate`, `private_key`, and `certificate_chain` attributes
        hold actual PEM values and can be referred to by other configs requiring
        certificate and private key inputs. This is inline with TF's best
        practices
        of not encrypting state.

        See Let's Encrypt Certbot notes at the end of this
        documentation for notes on how to generate a domain certificate with Let's
        Encrypt Certbot

        ## Example Usage

        ```python
        import pulumi
        import pulumi_okta as okta

        example = okta.Domain("example", name="www.example.com")
        test = okta.DomainCertificate("test",
            domain_id=test_okta_domain["id"],
            type="PEM",
            certificate=\"\"\"-----BEGIN CERTIFICATE-----
        MIIFNzCCBB+gAwIBAgISBAXomJWRama3ypu8TIxdA9wzMA0GCSqGSIb3DQEBCwUA
        ...
        NSgRtSXq11j8O4JONi8EXe7cEtvzUiLR5PL3itsK2svtrZ9jIwQ95wOPaA==
        -----END CERTIFICATE-----
        \"\"\",
            certificate_chain=\"\"\"-----BEGIN CERTIFICATE-----
        MIIFFjCCAv6gAwIBAgIRAJErCErPDBinU/bWLiWnX1owDQYJKoZIhvcNAQELBQAw
        ...
        Dfvp7OOGAN6dEOM4+qR9sdjoSYKEBpsr6GtPAQw4dy753ec5
        -----END CERTIFICATE-----
        \"\"\",
            private_key=\"\"\"-----BEGIN PRIVATE KEY-----
        MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC5cyk6x63iBJSW
        ...
        nUFLNE8pXSnsqb0eOL74f3uQ
        -----END PRIVATE KEY-----
        \"\"\")
        ```

        ## Let's Encrypt Certbot

        This example demonstrates generatoring a domain certificate with letsencrypt
        certbot https://letsencrypt.org/getting-started/

        Use letsencrypt's certbot to generate domain certificates in RSA output mode.
        The generator's output corresponds to `DomainCertificate` fields in the
        following manner.

        Okta Field          | Certbot file
        --------------------|--------------
        `certificate`       | `cert.pem`
        `certificate_chain` | `chain.pem`
        `private_key`       | `privkey.pem`

        ## Import

        This resource does not support importing.

        :param str resource_name: The name of the resource.
        :param DomainCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DomainCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 certificate: Optional[pulumi.Input[str]] = None,
                 certificate_chain: Optional[pulumi.Input[str]] = None,
                 domain_id: Optional[pulumi.Input[str]] = None,
                 private_key: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DomainCertificateArgs.__new__(DomainCertificateArgs)

            if certificate is None and not opts.urn:
                raise TypeError("Missing required property 'certificate'")
            __props__.__dict__["certificate"] = certificate
            if certificate_chain is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_chain'")
            __props__.__dict__["certificate_chain"] = certificate_chain
            if domain_id is None and not opts.urn:
                raise TypeError("Missing required property 'domain_id'")
            __props__.__dict__["domain_id"] = domain_id
            if private_key is None and not opts.urn:
                raise TypeError("Missing required property 'private_key'")
            __props__.__dict__["private_key"] = private_key
            if type is None and not opts.urn:
                raise TypeError("Missing required property 'type'")
            __props__.__dict__["type"] = type
        super(DomainCertificate, __self__).__init__(
            'okta:index/domainCertificate:DomainCertificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            certificate: Optional[pulumi.Input[str]] = None,
            certificate_chain: Optional[pulumi.Input[str]] = None,
            domain_id: Optional[pulumi.Input[str]] = None,
            private_key: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None) -> 'DomainCertificate':
        """
        Get an existing DomainCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] certificate: Certificate content.
        :param pulumi.Input[str] certificate_chain: Certificate certificate chain.
        :param pulumi.Input[str] domain_id: Domain ID.
        :param pulumi.Input[str] private_key: Certificate private key.
        :param pulumi.Input[str] type: Certificate type. Valid value is `"PEM"`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DomainCertificateState.__new__(_DomainCertificateState)

        __props__.__dict__["certificate"] = certificate
        __props__.__dict__["certificate_chain"] = certificate_chain
        __props__.__dict__["domain_id"] = domain_id
        __props__.__dict__["private_key"] = private_key
        __props__.__dict__["type"] = type
        return DomainCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def certificate(self) -> pulumi.Output[str]:
        """
        Certificate content.
        """
        return pulumi.get(self, "certificate")

    @property
    @pulumi.getter(name="certificateChain")
    def certificate_chain(self) -> pulumi.Output[str]:
        """
        Certificate certificate chain.
        """
        return pulumi.get(self, "certificate_chain")

    @property
    @pulumi.getter(name="domainId")
    def domain_id(self) -> pulumi.Output[str]:
        """
        Domain ID.
        """
        return pulumi.get(self, "domain_id")

    @property
    @pulumi.getter(name="privateKey")
    def private_key(self) -> pulumi.Output[str]:
        """
        Certificate private key.
        """
        return pulumi.get(self, "private_key")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Certificate type. Valid value is `"PEM"`.
        """
        return pulumi.get(self, "type")

