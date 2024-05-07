# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['DoArgs', 'Do']

@pulumi.input_type
class DoArgs:
    def __init__(__self__, *,
                 do_json: pulumi.Input[str],
                 bigip_address: Optional[pulumi.Input[str]] = None,
                 bigip_password: Optional[pulumi.Input[str]] = None,
                 bigip_port: Optional[pulumi.Input[str]] = None,
                 bigip_token_auth: Optional[pulumi.Input[bool]] = None,
                 bigip_user: Optional[pulumi.Input[str]] = None,
                 tenant_name: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Do resource.
        :param pulumi.Input[str] do_json: Name of the of the Declarative DO JSON file
        :param pulumi.Input[str] bigip_address: IP Address of BIGIP Host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] bigip_password: Password of BIGIP host to be used for this resource
        :param pulumi.Input[str] bigip_port: Port number of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[bool] bigip_token_auth: Enable to use an external authentication source (LDAP, TACACS, etc)
        :param pulumi.Input[str] bigip_user: UserName of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] tenant_name: unique identifier for DO resource
        :param pulumi.Input[int] timeout: DO json
        """
        pulumi.set(__self__, "do_json", do_json)
        if bigip_address is not None:
            pulumi.set(__self__, "bigip_address", bigip_address)
        if bigip_password is not None:
            pulumi.set(__self__, "bigip_password", bigip_password)
        if bigip_port is not None:
            pulumi.set(__self__, "bigip_port", bigip_port)
        if bigip_token_auth is not None:
            pulumi.set(__self__, "bigip_token_auth", bigip_token_auth)
        if bigip_user is not None:
            pulumi.set(__self__, "bigip_user", bigip_user)
        if tenant_name is not None:
            warnings.warn("""this attribute is no longer in use""", DeprecationWarning)
            pulumi.log.warn("""tenant_name is deprecated: this attribute is no longer in use""")
        if tenant_name is not None:
            pulumi.set(__self__, "tenant_name", tenant_name)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)

    @property
    @pulumi.getter(name="doJson")
    def do_json(self) -> pulumi.Input[str]:
        """
        Name of the of the Declarative DO JSON file
        """
        return pulumi.get(self, "do_json")

    @do_json.setter
    def do_json(self, value: pulumi.Input[str]):
        pulumi.set(self, "do_json", value)

    @property
    @pulumi.getter(name="bigipAddress")
    def bigip_address(self) -> Optional[pulumi.Input[str]]:
        """
        IP Address of BIGIP Host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_address")

    @bigip_address.setter
    def bigip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_address", value)

    @property
    @pulumi.getter(name="bigipPassword")
    def bigip_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password of BIGIP host to be used for this resource
        """
        return pulumi.get(self, "bigip_password")

    @bigip_password.setter
    def bigip_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_password", value)

    @property
    @pulumi.getter(name="bigipPort")
    def bigip_port(self) -> Optional[pulumi.Input[str]]:
        """
        Port number of BIGIP host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_port")

    @bigip_port.setter
    def bigip_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_port", value)

    @property
    @pulumi.getter(name="bigipTokenAuth")
    def bigip_token_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable to use an external authentication source (LDAP, TACACS, etc)
        """
        return pulumi.get(self, "bigip_token_auth")

    @bigip_token_auth.setter
    def bigip_token_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bigip_token_auth", value)

    @property
    @pulumi.getter(name="bigipUser")
    def bigip_user(self) -> Optional[pulumi.Input[str]]:
        """
        UserName of BIGIP host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_user")

    @bigip_user.setter
    def bigip_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_user", value)

    @property
    @pulumi.getter(name="tenantName")
    def tenant_name(self) -> Optional[pulumi.Input[str]]:
        """
        unique identifier for DO resource
        """
        warnings.warn("""this attribute is no longer in use""", DeprecationWarning)
        pulumi.log.warn("""tenant_name is deprecated: this attribute is no longer in use""")

        return pulumi.get(self, "tenant_name")

    @tenant_name.setter
    def tenant_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_name", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        """
        DO json
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)


@pulumi.input_type
class _DoState:
    def __init__(__self__, *,
                 bigip_address: Optional[pulumi.Input[str]] = None,
                 bigip_password: Optional[pulumi.Input[str]] = None,
                 bigip_port: Optional[pulumi.Input[str]] = None,
                 bigip_token_auth: Optional[pulumi.Input[bool]] = None,
                 bigip_user: Optional[pulumi.Input[str]] = None,
                 do_json: Optional[pulumi.Input[str]] = None,
                 tenant_name: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Do resources.
        :param pulumi.Input[str] bigip_address: IP Address of BIGIP Host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] bigip_password: Password of BIGIP host to be used for this resource
        :param pulumi.Input[str] bigip_port: Port number of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[bool] bigip_token_auth: Enable to use an external authentication source (LDAP, TACACS, etc)
        :param pulumi.Input[str] bigip_user: UserName of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] do_json: Name of the of the Declarative DO JSON file
        :param pulumi.Input[str] tenant_name: unique identifier for DO resource
        :param pulumi.Input[int] timeout: DO json
        """
        if bigip_address is not None:
            pulumi.set(__self__, "bigip_address", bigip_address)
        if bigip_password is not None:
            pulumi.set(__self__, "bigip_password", bigip_password)
        if bigip_port is not None:
            pulumi.set(__self__, "bigip_port", bigip_port)
        if bigip_token_auth is not None:
            pulumi.set(__self__, "bigip_token_auth", bigip_token_auth)
        if bigip_user is not None:
            pulumi.set(__self__, "bigip_user", bigip_user)
        if do_json is not None:
            pulumi.set(__self__, "do_json", do_json)
        if tenant_name is not None:
            warnings.warn("""this attribute is no longer in use""", DeprecationWarning)
            pulumi.log.warn("""tenant_name is deprecated: this attribute is no longer in use""")
        if tenant_name is not None:
            pulumi.set(__self__, "tenant_name", tenant_name)
        if timeout is not None:
            pulumi.set(__self__, "timeout", timeout)

    @property
    @pulumi.getter(name="bigipAddress")
    def bigip_address(self) -> Optional[pulumi.Input[str]]:
        """
        IP Address of BIGIP Host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_address")

    @bigip_address.setter
    def bigip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_address", value)

    @property
    @pulumi.getter(name="bigipPassword")
    def bigip_password(self) -> Optional[pulumi.Input[str]]:
        """
        Password of BIGIP host to be used for this resource
        """
        return pulumi.get(self, "bigip_password")

    @bigip_password.setter
    def bigip_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_password", value)

    @property
    @pulumi.getter(name="bigipPort")
    def bigip_port(self) -> Optional[pulumi.Input[str]]:
        """
        Port number of BIGIP host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_port")

    @bigip_port.setter
    def bigip_port(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_port", value)

    @property
    @pulumi.getter(name="bigipTokenAuth")
    def bigip_token_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable to use an external authentication source (LDAP, TACACS, etc)
        """
        return pulumi.get(self, "bigip_token_auth")

    @bigip_token_auth.setter
    def bigip_token_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bigip_token_auth", value)

    @property
    @pulumi.getter(name="bigipUser")
    def bigip_user(self) -> Optional[pulumi.Input[str]]:
        """
        UserName of BIGIP host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_user")

    @bigip_user.setter
    def bigip_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bigip_user", value)

    @property
    @pulumi.getter(name="doJson")
    def do_json(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the of the Declarative DO JSON file
        """
        return pulumi.get(self, "do_json")

    @do_json.setter
    def do_json(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "do_json", value)

    @property
    @pulumi.getter(name="tenantName")
    def tenant_name(self) -> Optional[pulumi.Input[str]]:
        """
        unique identifier for DO resource
        """
        warnings.warn("""this attribute is no longer in use""", DeprecationWarning)
        pulumi.log.warn("""tenant_name is deprecated: this attribute is no longer in use""")

        return pulumi.get(self, "tenant_name")

    @tenant_name.setter
    def tenant_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_name", value)

    @property
    @pulumi.getter
    def timeout(self) -> Optional[pulumi.Input[int]]:
        """
        DO json
        """
        return pulumi.get(self, "timeout")

    @timeout.setter
    def timeout(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout", value)


class Do(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bigip_address: Optional[pulumi.Input[str]] = None,
                 bigip_password: Optional[pulumi.Input[str]] = None,
                 bigip_port: Optional[pulumi.Input[str]] = None,
                 bigip_token_auth: Optional[pulumi.Input[bool]] = None,
                 bigip_user: Optional[pulumi.Input[str]] = None,
                 do_json: Optional[pulumi.Input[str]] = None,
                 tenant_name: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Create a Do resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bigip_address: IP Address of BIGIP Host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] bigip_password: Password of BIGIP host to be used for this resource
        :param pulumi.Input[str] bigip_port: Port number of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[bool] bigip_token_auth: Enable to use an external authentication source (LDAP, TACACS, etc)
        :param pulumi.Input[str] bigip_user: UserName of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] do_json: Name of the of the Declarative DO JSON file
        :param pulumi.Input[str] tenant_name: unique identifier for DO resource
        :param pulumi.Input[int] timeout: DO json
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DoArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Do resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param DoArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DoArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bigip_address: Optional[pulumi.Input[str]] = None,
                 bigip_password: Optional[pulumi.Input[str]] = None,
                 bigip_port: Optional[pulumi.Input[str]] = None,
                 bigip_token_auth: Optional[pulumi.Input[bool]] = None,
                 bigip_user: Optional[pulumi.Input[str]] = None,
                 do_json: Optional[pulumi.Input[str]] = None,
                 tenant_name: Optional[pulumi.Input[str]] = None,
                 timeout: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DoArgs.__new__(DoArgs)

            __props__.__dict__["bigip_address"] = bigip_address
            __props__.__dict__["bigip_password"] = None if bigip_password is None else pulumi.Output.secret(bigip_password)
            __props__.__dict__["bigip_port"] = bigip_port
            __props__.__dict__["bigip_token_auth"] = None if bigip_token_auth is None else pulumi.Output.secret(bigip_token_auth)
            __props__.__dict__["bigip_user"] = bigip_user
            if do_json is None and not opts.urn:
                raise TypeError("Missing required property 'do_json'")
            __props__.__dict__["do_json"] = do_json
            __props__.__dict__["tenant_name"] = tenant_name
            __props__.__dict__["timeout"] = timeout
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["bigipPassword", "bigipTokenAuth"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Do, __self__).__init__(
            'f5bigip:index/do:Do',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bigip_address: Optional[pulumi.Input[str]] = None,
            bigip_password: Optional[pulumi.Input[str]] = None,
            bigip_port: Optional[pulumi.Input[str]] = None,
            bigip_token_auth: Optional[pulumi.Input[bool]] = None,
            bigip_user: Optional[pulumi.Input[str]] = None,
            do_json: Optional[pulumi.Input[str]] = None,
            tenant_name: Optional[pulumi.Input[str]] = None,
            timeout: Optional[pulumi.Input[int]] = None) -> 'Do':
        """
        Get an existing Do resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bigip_address: IP Address of BIGIP Host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] bigip_password: Password of BIGIP host to be used for this resource
        :param pulumi.Input[str] bigip_port: Port number of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[bool] bigip_token_auth: Enable to use an external authentication source (LDAP, TACACS, etc)
        :param pulumi.Input[str] bigip_user: UserName of BIGIP host to be used for this resource,this is optional parameter.
               whenever we specify this parameter it gets overwrite provider configuration
        :param pulumi.Input[str] do_json: Name of the of the Declarative DO JSON file
        :param pulumi.Input[str] tenant_name: unique identifier for DO resource
        :param pulumi.Input[int] timeout: DO json
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DoState.__new__(_DoState)

        __props__.__dict__["bigip_address"] = bigip_address
        __props__.__dict__["bigip_password"] = bigip_password
        __props__.__dict__["bigip_port"] = bigip_port
        __props__.__dict__["bigip_token_auth"] = bigip_token_auth
        __props__.__dict__["bigip_user"] = bigip_user
        __props__.__dict__["do_json"] = do_json
        __props__.__dict__["tenant_name"] = tenant_name
        __props__.__dict__["timeout"] = timeout
        return Do(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bigipAddress")
    def bigip_address(self) -> pulumi.Output[Optional[str]]:
        """
        IP Address of BIGIP Host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_address")

    @property
    @pulumi.getter(name="bigipPassword")
    def bigip_password(self) -> pulumi.Output[Optional[str]]:
        """
        Password of BIGIP host to be used for this resource
        """
        return pulumi.get(self, "bigip_password")

    @property
    @pulumi.getter(name="bigipPort")
    def bigip_port(self) -> pulumi.Output[Optional[str]]:
        """
        Port number of BIGIP host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_port")

    @property
    @pulumi.getter(name="bigipTokenAuth")
    def bigip_token_auth(self) -> pulumi.Output[Optional[bool]]:
        """
        Enable to use an external authentication source (LDAP, TACACS, etc)
        """
        return pulumi.get(self, "bigip_token_auth")

    @property
    @pulumi.getter(name="bigipUser")
    def bigip_user(self) -> pulumi.Output[Optional[str]]:
        """
        UserName of BIGIP host to be used for this resource,this is optional parameter.
        whenever we specify this parameter it gets overwrite provider configuration
        """
        return pulumi.get(self, "bigip_user")

    @property
    @pulumi.getter(name="doJson")
    def do_json(self) -> pulumi.Output[str]:
        """
        Name of the of the Declarative DO JSON file
        """
        return pulumi.get(self, "do_json")

    @property
    @pulumi.getter(name="tenantName")
    def tenant_name(self) -> pulumi.Output[Optional[str]]:
        """
        unique identifier for DO resource
        """
        warnings.warn("""this attribute is no longer in use""", DeprecationWarning)
        pulumi.log.warn("""tenant_name is deprecated: this attribute is no longer in use""")

        return pulumi.get(self, "tenant_name")

    @property
    @pulumi.getter
    def timeout(self) -> pulumi.Output[Optional[int]]:
        """
        DO json
        """
        return pulumi.get(self, "timeout")

