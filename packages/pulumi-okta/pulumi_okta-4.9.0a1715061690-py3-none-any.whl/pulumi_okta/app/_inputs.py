# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'OAuthGroupsClaimArgs',
    'OAuthJwkArgs',
    'SamlAttributeStatementArgs',
    'SamlKeyArgs',
]

@pulumi.input_type
class OAuthGroupsClaimArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 type: pulumi.Input[str],
                 value: pulumi.Input[str],
                 filter_type: Optional[pulumi.Input[str]] = None,
                 issuer_mode: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Name of the claim that will be used in the token.
        :param pulumi.Input[str] type: Groups claim type. Valid values: `"FILTER"`, `"EXPRESSION"`.
        :param pulumi.Input[str] value: Value of the claim. Can be an Okta Expression Language statement that evaluates at the time the token is minted.
        :param pulumi.Input[str] filter_type: Groups claim filter. Can only be set if type is `"FILTER"`. Valid values: `"EQUALS"`, `"STARTS_WITH"`, `"CONTAINS"`, `"REGEX"`.
        :param pulumi.Input[str] issuer_mode: Issuer Mode is inherited from the Issuer Mode on the OAuth app itself.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)
        if filter_type is not None:
            pulumi.set(__self__, "filter_type", filter_type)
        if issuer_mode is not None:
            pulumi.set(__self__, "issuer_mode", issuer_mode)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the claim that will be used in the token.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Groups claim type. Valid values: `"FILTER"`, `"EXPRESSION"`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Value of the claim. Can be an Okta Expression Language statement that evaluates at the time the token is minted.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)

    @property
    @pulumi.getter(name="filterType")
    def filter_type(self) -> Optional[pulumi.Input[str]]:
        """
        Groups claim filter. Can only be set if type is `"FILTER"`. Valid values: `"EQUALS"`, `"STARTS_WITH"`, `"CONTAINS"`, `"REGEX"`.
        """
        return pulumi.get(self, "filter_type")

    @filter_type.setter
    def filter_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_type", value)

    @property
    @pulumi.getter(name="issuerMode")
    def issuer_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Issuer Mode is inherited from the Issuer Mode on the OAuth app itself.
        """
        return pulumi.get(self, "issuer_mode")

    @issuer_mode.setter
    def issuer_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer_mode", value)


@pulumi.input_type
class OAuthJwkArgs:
    def __init__(__self__, *,
                 kid: pulumi.Input[str],
                 kty: pulumi.Input[str],
                 e: Optional[pulumi.Input[str]] = None,
                 n: Optional[pulumi.Input[str]] = None,
                 x: Optional[pulumi.Input[str]] = None,
                 y: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] kid: Key ID
        :param pulumi.Input[str] kty: Key type
        :param pulumi.Input[str] e: RSA Exponent
        :param pulumi.Input[str] n: RSA Modulus
        :param pulumi.Input[str] x: X coordinate of the elliptic curve point
        :param pulumi.Input[str] y: Y coordinate of the elliptic curve point
        """
        pulumi.set(__self__, "kid", kid)
        pulumi.set(__self__, "kty", kty)
        if e is not None:
            pulumi.set(__self__, "e", e)
        if n is not None:
            pulumi.set(__self__, "n", n)
        if x is not None:
            pulumi.set(__self__, "x", x)
        if y is not None:
            pulumi.set(__self__, "y", y)

    @property
    @pulumi.getter
    def kid(self) -> pulumi.Input[str]:
        """
        Key ID
        """
        return pulumi.get(self, "kid")

    @kid.setter
    def kid(self, value: pulumi.Input[str]):
        pulumi.set(self, "kid", value)

    @property
    @pulumi.getter
    def kty(self) -> pulumi.Input[str]:
        """
        Key type
        """
        return pulumi.get(self, "kty")

    @kty.setter
    def kty(self, value: pulumi.Input[str]):
        pulumi.set(self, "kty", value)

    @property
    @pulumi.getter
    def e(self) -> Optional[pulumi.Input[str]]:
        """
        RSA Exponent
        """
        return pulumi.get(self, "e")

    @e.setter
    def e(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "e", value)

    @property
    @pulumi.getter
    def n(self) -> Optional[pulumi.Input[str]]:
        """
        RSA Modulus
        """
        return pulumi.get(self, "n")

    @n.setter
    def n(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "n", value)

    @property
    @pulumi.getter
    def x(self) -> Optional[pulumi.Input[str]]:
        """
        X coordinate of the elliptic curve point
        """
        return pulumi.get(self, "x")

    @x.setter
    def x(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "x", value)

    @property
    @pulumi.getter
    def y(self) -> Optional[pulumi.Input[str]]:
        """
        Y coordinate of the elliptic curve point
        """
        return pulumi.get(self, "y")

    @y.setter
    def y(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "y", value)


@pulumi.input_type
class SamlAttributeStatementArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 filter_type: Optional[pulumi.Input[str]] = None,
                 filter_value: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] name: The name of the attribute statement.
        :param pulumi.Input[str] filter_type: Type of group attribute filter. Valid values are: `"STARTS_WITH"`, `"EQUALS"`, `"CONTAINS"`, or `"REGEX"`
        :param pulumi.Input[str] filter_value: Filter value to use.
        :param pulumi.Input[str] namespace: The attribute namespace. It can be set to `"urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified"`, `"urn:oasis:names:tc:SAML:2.0:attrname-format:uri"`, or `"urn:oasis:names:tc:SAML:2.0:attrname-format:basic"`.
        :param pulumi.Input[str] type: The type of attribute statement value. Valid values are: `"EXPRESSION"` or `"GROUP"`. Default is `"EXPRESSION"`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: Array of values to use.
        """
        pulumi.set(__self__, "name", name)
        if filter_type is not None:
            pulumi.set(__self__, "filter_type", filter_type)
        if filter_value is not None:
            pulumi.set(__self__, "filter_value", filter_value)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the attribute statement.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="filterType")
    def filter_type(self) -> Optional[pulumi.Input[str]]:
        """
        Type of group attribute filter. Valid values are: `"STARTS_WITH"`, `"EQUALS"`, `"CONTAINS"`, or `"REGEX"`
        """
        return pulumi.get(self, "filter_type")

    @filter_type.setter
    def filter_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_type", value)

    @property
    @pulumi.getter(name="filterValue")
    def filter_value(self) -> Optional[pulumi.Input[str]]:
        """
        Filter value to use.
        """
        return pulumi.get(self, "filter_value")

    @filter_value.setter
    def filter_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_value", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The attribute namespace. It can be set to `"urn:oasis:names:tc:SAML:2.0:attrname-format:unspecified"`, `"urn:oasis:names:tc:SAML:2.0:attrname-format:uri"`, or `"urn:oasis:names:tc:SAML:2.0:attrname-format:basic"`.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of attribute statement value. Valid values are: `"EXPRESSION"` or `"GROUP"`. Default is `"EXPRESSION"`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Array of values to use.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class SamlKeyArgs:
    def __init__(__self__, *,
                 created: Optional[pulumi.Input[str]] = None,
                 e: Optional[pulumi.Input[str]] = None,
                 expires_at: Optional[pulumi.Input[str]] = None,
                 kid: Optional[pulumi.Input[str]] = None,
                 kty: Optional[pulumi.Input[str]] = None,
                 last_updated: Optional[pulumi.Input[str]] = None,
                 n: Optional[pulumi.Input[str]] = None,
                 use: Optional[pulumi.Input[str]] = None,
                 x5cs: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 x5t_s256: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] created: Date created.
        :param pulumi.Input[str] e: RSA exponent.
        :param pulumi.Input[str] expires_at: Date the key expires.
        :param pulumi.Input[str] kid: Key ID.
        :param pulumi.Input[str] kty: Identifies the cryptographic algorithm family used with the key.
        :param pulumi.Input[str] last_updated: Date the key was last updated.
        :param pulumi.Input[str] n: RSA modulus.
        :param pulumi.Input[str] use: Intended use of the public key.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] x5cs: X.509 certificate chain.
        :param pulumi.Input[str] x5t_s256: X.509 certificate SHA-256 thumbprint.
        """
        if created is not None:
            pulumi.set(__self__, "created", created)
        if e is not None:
            pulumi.set(__self__, "e", e)
        if expires_at is not None:
            pulumi.set(__self__, "expires_at", expires_at)
        if kid is not None:
            pulumi.set(__self__, "kid", kid)
        if kty is not None:
            pulumi.set(__self__, "kty", kty)
        if last_updated is not None:
            pulumi.set(__self__, "last_updated", last_updated)
        if n is not None:
            pulumi.set(__self__, "n", n)
        if use is not None:
            pulumi.set(__self__, "use", use)
        if x5cs is not None:
            pulumi.set(__self__, "x5cs", x5cs)
        if x5t_s256 is not None:
            pulumi.set(__self__, "x5t_s256", x5t_s256)

    @property
    @pulumi.getter
    def created(self) -> Optional[pulumi.Input[str]]:
        """
        Date created.
        """
        return pulumi.get(self, "created")

    @created.setter
    def created(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created", value)

    @property
    @pulumi.getter
    def e(self) -> Optional[pulumi.Input[str]]:
        """
        RSA exponent.
        """
        return pulumi.get(self, "e")

    @e.setter
    def e(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "e", value)

    @property
    @pulumi.getter(name="expiresAt")
    def expires_at(self) -> Optional[pulumi.Input[str]]:
        """
        Date the key expires.
        """
        return pulumi.get(self, "expires_at")

    @expires_at.setter
    def expires_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expires_at", value)

    @property
    @pulumi.getter
    def kid(self) -> Optional[pulumi.Input[str]]:
        """
        Key ID.
        """
        return pulumi.get(self, "kid")

    @kid.setter
    def kid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kid", value)

    @property
    @pulumi.getter
    def kty(self) -> Optional[pulumi.Input[str]]:
        """
        Identifies the cryptographic algorithm family used with the key.
        """
        return pulumi.get(self, "kty")

    @kty.setter
    def kty(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kty", value)

    @property
    @pulumi.getter(name="lastUpdated")
    def last_updated(self) -> Optional[pulumi.Input[str]]:
        """
        Date the key was last updated.
        """
        return pulumi.get(self, "last_updated")

    @last_updated.setter
    def last_updated(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_updated", value)

    @property
    @pulumi.getter
    def n(self) -> Optional[pulumi.Input[str]]:
        """
        RSA modulus.
        """
        return pulumi.get(self, "n")

    @n.setter
    def n(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "n", value)

    @property
    @pulumi.getter
    def use(self) -> Optional[pulumi.Input[str]]:
        """
        Intended use of the public key.
        """
        return pulumi.get(self, "use")

    @use.setter
    def use(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "use", value)

    @property
    @pulumi.getter
    def x5cs(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        X.509 certificate chain.
        """
        return pulumi.get(self, "x5cs")

    @x5cs.setter
    def x5cs(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "x5cs", value)

    @property
    @pulumi.getter(name="x5tS256")
    def x5t_s256(self) -> Optional[pulumi.Input[str]]:
        """
        X.509 certificate SHA-256 thumbprint.
        """
        return pulumi.get(self, "x5t_s256")

    @x5t_s256.setter
    def x5t_s256(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "x5t_s256", value)


