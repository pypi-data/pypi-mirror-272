# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['OidcClientArgs', 'OidcClient']

@pulumi.input_type
class OidcClientArgs:
    def __init__(__self__, *,
                 access_token_ttl: Optional[pulumi.Input[int]] = None,
                 assignments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_type: Optional[pulumi.Input[str]] = None,
                 id_token_ttl: Optional[pulumi.Input[int]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a OidcClient resource.
        :param pulumi.Input[int] access_token_ttl: The time-to-live for access tokens obtained by the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignments: A list of assignment resources associated with the client.
        :param pulumi.Input[str] client_type: The client type based on its ability to maintain confidentiality of credentials.
               The following client types are supported: `confidential`, `public`. Defaults to `confidential`.
        :param pulumi.Input[int] id_token_ttl: The time-to-live for ID tokens obtained by the client. 
               The value should be less than the `verification_ttl` on the key.
        :param pulumi.Input[str] key: A reference to a named key resource in Vault.
               This cannot be modified after creation. If not provided, the `default`
               key is used.
        :param pulumi.Input[str] name: The name of the client.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] redirect_uris: Redirection URI values used by the client. 
               One of these values must exactly match the `redirect_uri` parameter value
               used in each authentication request.
        """
        if access_token_ttl is not None:
            pulumi.set(__self__, "access_token_ttl", access_token_ttl)
        if assignments is not None:
            pulumi.set(__self__, "assignments", assignments)
        if client_type is not None:
            pulumi.set(__self__, "client_type", client_type)
        if id_token_ttl is not None:
            pulumi.set(__self__, "id_token_ttl", id_token_ttl)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if redirect_uris is not None:
            pulumi.set(__self__, "redirect_uris", redirect_uris)

    @property
    @pulumi.getter(name="accessTokenTtl")
    def access_token_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The time-to-live for access tokens obtained by the client.
        """
        return pulumi.get(self, "access_token_ttl")

    @access_token_ttl.setter
    def access_token_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "access_token_ttl", value)

    @property
    @pulumi.getter
    def assignments(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of assignment resources associated with the client.
        """
        return pulumi.get(self, "assignments")

    @assignments.setter
    def assignments(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "assignments", value)

    @property
    @pulumi.getter(name="clientType")
    def client_type(self) -> Optional[pulumi.Input[str]]:
        """
        The client type based on its ability to maintain confidentiality of credentials.
        The following client types are supported: `confidential`, `public`. Defaults to `confidential`.
        """
        return pulumi.get(self, "client_type")

    @client_type.setter
    def client_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_type", value)

    @property
    @pulumi.getter(name="idTokenTtl")
    def id_token_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The time-to-live for ID tokens obtained by the client. 
        The value should be less than the `verification_ttl` on the key.
        """
        return pulumi.get(self, "id_token_ttl")

    @id_token_ttl.setter
    def id_token_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "id_token_ttl", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to a named key resource in Vault.
        This cannot be modified after creation. If not provided, the `default`
        key is used.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the client.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="redirectUris")
    def redirect_uris(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Redirection URI values used by the client. 
        One of these values must exactly match the `redirect_uri` parameter value
        used in each authentication request.
        """
        return pulumi.get(self, "redirect_uris")

    @redirect_uris.setter
    def redirect_uris(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "redirect_uris", value)


@pulumi.input_type
class _OidcClientState:
    def __init__(__self__, *,
                 access_token_ttl: Optional[pulumi.Input[int]] = None,
                 assignments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_id: Optional[pulumi.Input[str]] = None,
                 client_secret: Optional[pulumi.Input[str]] = None,
                 client_type: Optional[pulumi.Input[str]] = None,
                 id_token_ttl: Optional[pulumi.Input[int]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering OidcClient resources.
        :param pulumi.Input[int] access_token_ttl: The time-to-live for access tokens obtained by the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignments: A list of assignment resources associated with the client.
        :param pulumi.Input[str] client_id: The Client ID returned by Vault.
        :param pulumi.Input[str] client_secret: The Client Secret Key returned by Vault.
               For public OpenID Clients `client_secret` is set to an empty string `""`
        :param pulumi.Input[str] client_type: The client type based on its ability to maintain confidentiality of credentials.
               The following client types are supported: `confidential`, `public`. Defaults to `confidential`.
        :param pulumi.Input[int] id_token_ttl: The time-to-live for ID tokens obtained by the client. 
               The value should be less than the `verification_ttl` on the key.
        :param pulumi.Input[str] key: A reference to a named key resource in Vault.
               This cannot be modified after creation. If not provided, the `default`
               key is used.
        :param pulumi.Input[str] name: The name of the client.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] redirect_uris: Redirection URI values used by the client. 
               One of these values must exactly match the `redirect_uri` parameter value
               used in each authentication request.
        """
        if access_token_ttl is not None:
            pulumi.set(__self__, "access_token_ttl", access_token_ttl)
        if assignments is not None:
            pulumi.set(__self__, "assignments", assignments)
        if client_id is not None:
            pulumi.set(__self__, "client_id", client_id)
        if client_secret is not None:
            pulumi.set(__self__, "client_secret", client_secret)
        if client_type is not None:
            pulumi.set(__self__, "client_type", client_type)
        if id_token_ttl is not None:
            pulumi.set(__self__, "id_token_ttl", id_token_ttl)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)
        if redirect_uris is not None:
            pulumi.set(__self__, "redirect_uris", redirect_uris)

    @property
    @pulumi.getter(name="accessTokenTtl")
    def access_token_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The time-to-live for access tokens obtained by the client.
        """
        return pulumi.get(self, "access_token_ttl")

    @access_token_ttl.setter
    def access_token_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "access_token_ttl", value)

    @property
    @pulumi.getter
    def assignments(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of assignment resources associated with the client.
        """
        return pulumi.get(self, "assignments")

    @assignments.setter
    def assignments(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "assignments", value)

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Client ID returned by Vault.
        """
        return pulumi.get(self, "client_id")

    @client_id.setter
    def client_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_id", value)

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> Optional[pulumi.Input[str]]:
        """
        The Client Secret Key returned by Vault.
        For public OpenID Clients `client_secret` is set to an empty string `""`
        """
        return pulumi.get(self, "client_secret")

    @client_secret.setter
    def client_secret(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_secret", value)

    @property
    @pulumi.getter(name="clientType")
    def client_type(self) -> Optional[pulumi.Input[str]]:
        """
        The client type based on its ability to maintain confidentiality of credentials.
        The following client types are supported: `confidential`, `public`. Defaults to `confidential`.
        """
        return pulumi.get(self, "client_type")

    @client_type.setter
    def client_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "client_type", value)

    @property
    @pulumi.getter(name="idTokenTtl")
    def id_token_ttl(self) -> Optional[pulumi.Input[int]]:
        """
        The time-to-live for ID tokens obtained by the client. 
        The value should be less than the `verification_ttl` on the key.
        """
        return pulumi.get(self, "id_token_ttl")

    @id_token_ttl.setter
    def id_token_ttl(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "id_token_ttl", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        A reference to a named key resource in Vault.
        This cannot be modified after creation. If not provided, the `default`
        key is used.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the client.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "namespace", value)

    @property
    @pulumi.getter(name="redirectUris")
    def redirect_uris(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Redirection URI values used by the client. 
        One of these values must exactly match the `redirect_uri` parameter value
        used in each authentication request.
        """
        return pulumi.get(self, "redirect_uris")

    @redirect_uris.setter
    def redirect_uris(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "redirect_uris", value)


class OidcClient(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_token_ttl: Optional[pulumi.Input[int]] = None,
                 assignments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_type: Optional[pulumi.Input[str]] = None,
                 id_token_ttl: Optional[pulumi.Input[int]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages OIDC Clients in a Vault server. See the [Vault documentation](https://www.vaultproject.io/api-docs/secret/identity/oidc-provider#create-or-update-an-assignment)
        for more information.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_vault as vault

        test = vault.identity.OidcAssignment("test",
            name="my-assignment",
            entity_ids=["ascbascas-2231a-sdfaa"],
            group_ids=["sajkdsad-32414-sfsada"])
        test_oidc_client = vault.identity.OidcClient("test",
            name="my-app",
            redirect_uris=[
                "http://127.0.0.1:9200/v1/auth-methods/oidc:authenticate:callback",
                "http://127.0.0.1:8251/callback",
                "http://127.0.0.1:8080/callback",
            ],
            assignments=[test.name],
            id_token_ttl=2400,
            access_token_ttl=7200)
        ```

        ## Import

        OIDC Clients can be imported using the `name`, e.g.

        ```sh
        $ pulumi import vault:identity/oidcClient:OidcClient test my-app
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] access_token_ttl: The time-to-live for access tokens obtained by the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignments: A list of assignment resources associated with the client.
        :param pulumi.Input[str] client_type: The client type based on its ability to maintain confidentiality of credentials.
               The following client types are supported: `confidential`, `public`. Defaults to `confidential`.
        :param pulumi.Input[int] id_token_ttl: The time-to-live for ID tokens obtained by the client. 
               The value should be less than the `verification_ttl` on the key.
        :param pulumi.Input[str] key: A reference to a named key resource in Vault.
               This cannot be modified after creation. If not provided, the `default`
               key is used.
        :param pulumi.Input[str] name: The name of the client.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] redirect_uris: Redirection URI values used by the client. 
               One of these values must exactly match the `redirect_uri` parameter value
               used in each authentication request.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[OidcClientArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages OIDC Clients in a Vault server. See the [Vault documentation](https://www.vaultproject.io/api-docs/secret/identity/oidc-provider#create-or-update-an-assignment)
        for more information.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_vault as vault

        test = vault.identity.OidcAssignment("test",
            name="my-assignment",
            entity_ids=["ascbascas-2231a-sdfaa"],
            group_ids=["sajkdsad-32414-sfsada"])
        test_oidc_client = vault.identity.OidcClient("test",
            name="my-app",
            redirect_uris=[
                "http://127.0.0.1:9200/v1/auth-methods/oidc:authenticate:callback",
                "http://127.0.0.1:8251/callback",
                "http://127.0.0.1:8080/callback",
            ],
            assignments=[test.name],
            id_token_ttl=2400,
            access_token_ttl=7200)
        ```

        ## Import

        OIDC Clients can be imported using the `name`, e.g.

        ```sh
        $ pulumi import vault:identity/oidcClient:OidcClient test my-app
        ```

        :param str resource_name: The name of the resource.
        :param OidcClientArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OidcClientArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_token_ttl: Optional[pulumi.Input[int]] = None,
                 assignments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 client_type: Optional[pulumi.Input[str]] = None,
                 id_token_ttl: Optional[pulumi.Input[int]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 namespace: Optional[pulumi.Input[str]] = None,
                 redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OidcClientArgs.__new__(OidcClientArgs)

            __props__.__dict__["access_token_ttl"] = access_token_ttl
            __props__.__dict__["assignments"] = assignments
            __props__.__dict__["client_type"] = client_type
            __props__.__dict__["id_token_ttl"] = id_token_ttl
            __props__.__dict__["key"] = key
            __props__.__dict__["name"] = name
            __props__.__dict__["namespace"] = namespace
            __props__.__dict__["redirect_uris"] = redirect_uris
            __props__.__dict__["client_id"] = None
            __props__.__dict__["client_secret"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["clientSecret"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(OidcClient, __self__).__init__(
            'vault:identity/oidcClient:OidcClient',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            access_token_ttl: Optional[pulumi.Input[int]] = None,
            assignments: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            client_id: Optional[pulumi.Input[str]] = None,
            client_secret: Optional[pulumi.Input[str]] = None,
            client_type: Optional[pulumi.Input[str]] = None,
            id_token_ttl: Optional[pulumi.Input[int]] = None,
            key: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            namespace: Optional[pulumi.Input[str]] = None,
            redirect_uris: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'OidcClient':
        """
        Get an existing OidcClient resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] access_token_ttl: The time-to-live for access tokens obtained by the client.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] assignments: A list of assignment resources associated with the client.
        :param pulumi.Input[str] client_id: The Client ID returned by Vault.
        :param pulumi.Input[str] client_secret: The Client Secret Key returned by Vault.
               For public OpenID Clients `client_secret` is set to an empty string `""`
        :param pulumi.Input[str] client_type: The client type based on its ability to maintain confidentiality of credentials.
               The following client types are supported: `confidential`, `public`. Defaults to `confidential`.
        :param pulumi.Input[int] id_token_ttl: The time-to-live for ID tokens obtained by the client. 
               The value should be less than the `verification_ttl` on the key.
        :param pulumi.Input[str] key: A reference to a named key resource in Vault.
               This cannot be modified after creation. If not provided, the `default`
               key is used.
        :param pulumi.Input[str] name: The name of the client.
        :param pulumi.Input[str] namespace: The namespace to provision the resource in.
               The value should not contain leading or trailing forward slashes.
               The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
               *Available only for Vault Enterprise*.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] redirect_uris: Redirection URI values used by the client. 
               One of these values must exactly match the `redirect_uri` parameter value
               used in each authentication request.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OidcClientState.__new__(_OidcClientState)

        __props__.__dict__["access_token_ttl"] = access_token_ttl
        __props__.__dict__["assignments"] = assignments
        __props__.__dict__["client_id"] = client_id
        __props__.__dict__["client_secret"] = client_secret
        __props__.__dict__["client_type"] = client_type
        __props__.__dict__["id_token_ttl"] = id_token_ttl
        __props__.__dict__["key"] = key
        __props__.__dict__["name"] = name
        __props__.__dict__["namespace"] = namespace
        __props__.__dict__["redirect_uris"] = redirect_uris
        return OidcClient(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessTokenTtl")
    def access_token_ttl(self) -> pulumi.Output[int]:
        """
        The time-to-live for access tokens obtained by the client.
        """
        return pulumi.get(self, "access_token_ttl")

    @property
    @pulumi.getter
    def assignments(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of assignment resources associated with the client.
        """
        return pulumi.get(self, "assignments")

    @property
    @pulumi.getter(name="clientId")
    def client_id(self) -> pulumi.Output[str]:
        """
        The Client ID returned by Vault.
        """
        return pulumi.get(self, "client_id")

    @property
    @pulumi.getter(name="clientSecret")
    def client_secret(self) -> pulumi.Output[str]:
        """
        The Client Secret Key returned by Vault.
        For public OpenID Clients `client_secret` is set to an empty string `""`
        """
        return pulumi.get(self, "client_secret")

    @property
    @pulumi.getter(name="clientType")
    def client_type(self) -> pulumi.Output[str]:
        """
        The client type based on its ability to maintain confidentiality of credentials.
        The following client types are supported: `confidential`, `public`. Defaults to `confidential`.
        """
        return pulumi.get(self, "client_type")

    @property
    @pulumi.getter(name="idTokenTtl")
    def id_token_ttl(self) -> pulumi.Output[int]:
        """
        The time-to-live for ID tokens obtained by the client. 
        The value should be less than the `verification_ttl` on the key.
        """
        return pulumi.get(self, "id_token_ttl")

    @property
    @pulumi.getter
    def key(self) -> pulumi.Output[str]:
        """
        A reference to a named key resource in Vault.
        This cannot be modified after creation. If not provided, the `default`
        key is used.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the client.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def namespace(self) -> pulumi.Output[Optional[str]]:
        """
        The namespace to provision the resource in.
        The value should not contain leading or trailing forward slashes.
        The `namespace` is always relative to the provider's configured [namespace](https://www.terraform.io/docs/providers/vault/index.html#namespace).
        *Available only for Vault Enterprise*.
        """
        return pulumi.get(self, "namespace")

    @property
    @pulumi.getter(name="redirectUris")
    def redirect_uris(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Redirection URI values used by the client. 
        One of these values must exactly match the `redirect_uri` parameter value
        used in each authentication request.
        """
        return pulumi.get(self, "redirect_uris")

