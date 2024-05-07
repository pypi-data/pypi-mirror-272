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
    'GetEncryptResult',
    'AwaitableGetEncryptResult',
    'get_encrypt',
    'get_encrypt_output',
]

@pulumi.output_type
class GetEncryptResult:
    """
    A collection of values returned by getEncrypt.
    """
    def __init__(__self__, backend=None, ciphertext=None, context=None, id=None, key=None, key_version=None, namespace=None, plaintext=None):
        if backend and not isinstance(backend, str):
            raise TypeError("Expected argument 'backend' to be a str")
        pulumi.set(__self__, "backend", backend)
        if ciphertext and not isinstance(ciphertext, str):
            raise TypeError("Expected argument 'ciphertext' to be a str")
        pulumi.set(__self__, "ciphertext", ciphertext)
        if context and not isinstance(context, str):
            raise TypeError("Expected argument 'context' to be a str")
        pulumi.set(__self__, "context", context)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if key and not isinstance(key, str):
            raise TypeError("Expected argument 'key' to be a str")
        pulumi.set(__self__, "key", key)
        if key_version and not isinstance(key_version, int):
            raise TypeError("Expected argument 'key_version' to be a int")
        pulumi.set(__self__, "key_version", key_version)
        if namespace and not isinstance(namespace, str):
            raise TypeError("Expected argument 'namespace' to be a str")
        pulumi.set(__self__, "namespace", namespace)
        if plaintext and not isinstance(plaintext, str):
            raise TypeError("Expected argument 'plaintext' to be a str")
        pulumi.set(__self__, "plaintext", plaintext)

    @property
    @pulumi.getter
    def backend(self) -> str:
        return pulumi.get(self, "backend")

    @property
    @pulumi.getter
    def ciphertext(self) -> str:
        """
        Encrypted ciphertext returned from Vault
        """
        return pulumi.get(self, "ciphertext")

    @property
    @pulumi.getter
    def context(self) -> Optional[str]:
        return pulumi.get(self, "context")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter(name="keyVersion")
    def key_version(self) -> Optional[int]:
        return pulumi.get(self, "key_version")

    @property
    @pulumi.getter
    def namespace(self) -> Optional[str]:
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter
    def plaintext(self) -> str:
        return pulumi.get(self, "plaintext")


class AwaitableGetEncryptResult(GetEncryptResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEncryptResult(
            backend=self.backend,
            ciphertext=self.ciphertext,
            context=self.context,
            id=self.id,
            key=self.key,
            key_version=self.key_version,
            namespace=self.namespace,
            plaintext=self.plaintext)


def get_encrypt(backend: Optional[str] = None,
                context: Optional[str] = None,
                key: Optional[str] = None,
                key_version: Optional[int] = None,
                namespace: Optional[str] = None,
                plaintext: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEncryptResult:
    """
    This is a data source which can be used to encrypt plaintext using a Vault Transit key.
    """
    __args__ = dict()
    __args__['backend'] = backend
    __args__['context'] = context
    __args__['key'] = key
    __args__['keyVersion'] = key_version
    __args__['namespace'] = namespace
    __args__['plaintext'] = plaintext
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('vault:transit/getEncrypt:getEncrypt', __args__, opts=opts, typ=GetEncryptResult).value

    return AwaitableGetEncryptResult(
        backend=pulumi.get(__ret__, 'backend'),
        ciphertext=pulumi.get(__ret__, 'ciphertext'),
        context=pulumi.get(__ret__, 'context'),
        id=pulumi.get(__ret__, 'id'),
        key=pulumi.get(__ret__, 'key'),
        key_version=pulumi.get(__ret__, 'key_version'),
        namespace=pulumi.get(__ret__, 'namespace'),
        plaintext=pulumi.get(__ret__, 'plaintext'))


@_utilities.lift_output_func(get_encrypt)
def get_encrypt_output(backend: Optional[pulumi.Input[str]] = None,
                       context: Optional[pulumi.Input[Optional[str]]] = None,
                       key: Optional[pulumi.Input[str]] = None,
                       key_version: Optional[pulumi.Input[Optional[int]]] = None,
                       namespace: Optional[pulumi.Input[Optional[str]]] = None,
                       plaintext: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEncryptResult]:
    """
    This is a data source which can be used to encrypt plaintext using a Vault Transit key.
    """
    ...
