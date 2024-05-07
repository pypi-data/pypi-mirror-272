# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['DnsArgs', 'Dns']

@pulumi.input_type
class DnsArgs:
    def __init__(__self__, *,
                 description: pulumi.Input[str],
                 name_servers: pulumi.Input[Sequence[pulumi.Input[str]]],
                 number_of_dots: Optional[pulumi.Input[int]] = None,
                 searches: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Dns resource.
        :param pulumi.Input[str] description: Provide description for your DNS server
        :param pulumi.Input[Sequence[pulumi.Input[str]]] name_servers: Specifies the name servers that the system uses to validate DNS lookups, and resolve host names.
        :param pulumi.Input[int] number_of_dots: Configures the number of dots needed in a name before an initial absolute query will be made.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] searches: Specifies the domains that the system searches for local domain lookups, to resolve local host names.
        """
        pulumi.set(__self__, "description", description)
        pulumi.set(__self__, "name_servers", name_servers)
        if number_of_dots is not None:
            pulumi.set(__self__, "number_of_dots", number_of_dots)
        if searches is not None:
            pulumi.set(__self__, "searches", searches)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        Provide description for your DNS server
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="nameServers")
    def name_servers(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Specifies the name servers that the system uses to validate DNS lookups, and resolve host names.
        """
        return pulumi.get(self, "name_servers")

    @name_servers.setter
    def name_servers(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "name_servers", value)

    @property
    @pulumi.getter(name="numberOfDots")
    def number_of_dots(self) -> Optional[pulumi.Input[int]]:
        """
        Configures the number of dots needed in a name before an initial absolute query will be made.
        """
        return pulumi.get(self, "number_of_dots")

    @number_of_dots.setter
    def number_of_dots(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "number_of_dots", value)

    @property
    @pulumi.getter
    def searches(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the domains that the system searches for local domain lookups, to resolve local host names.
        """
        return pulumi.get(self, "searches")

    @searches.setter
    def searches(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "searches", value)


@pulumi.input_type
class _DnsState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 name_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 number_of_dots: Optional[pulumi.Input[int]] = None,
                 searches: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Dns resources.
        :param pulumi.Input[str] description: Provide description for your DNS server
        :param pulumi.Input[Sequence[pulumi.Input[str]]] name_servers: Specifies the name servers that the system uses to validate DNS lookups, and resolve host names.
        :param pulumi.Input[int] number_of_dots: Configures the number of dots needed in a name before an initial absolute query will be made.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] searches: Specifies the domains that the system searches for local domain lookups, to resolve local host names.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name_servers is not None:
            pulumi.set(__self__, "name_servers", name_servers)
        if number_of_dots is not None:
            pulumi.set(__self__, "number_of_dots", number_of_dots)
        if searches is not None:
            pulumi.set(__self__, "searches", searches)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Provide description for your DNS server
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="nameServers")
    def name_servers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the name servers that the system uses to validate DNS lookups, and resolve host names.
        """
        return pulumi.get(self, "name_servers")

    @name_servers.setter
    def name_servers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "name_servers", value)

    @property
    @pulumi.getter(name="numberOfDots")
    def number_of_dots(self) -> Optional[pulumi.Input[int]]:
        """
        Configures the number of dots needed in a name before an initial absolute query will be made.
        """
        return pulumi.get(self, "number_of_dots")

    @number_of_dots.setter
    def number_of_dots(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "number_of_dots", value)

    @property
    @pulumi.getter
    def searches(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the domains that the system searches for local domain lookups, to resolve local host names.
        """
        return pulumi.get(self, "searches")

    @searches.setter
    def searches(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "searches", value)


class Dns(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 number_of_dots: Optional[pulumi.Input[int]] = None,
                 searches: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        `sys.Dns` Configures DNS Name server on F5 BIG-IP

        ## Example Usage

        ```python
        import pulumi
        import pulumi_f5bigip as f5bigip

        dns1 = f5bigip.sys.Dns("dns1",
            description="/Common/DNS1",
            name_servers=["1.1.1.1"],
            searches=["f5.com"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Provide description for your DNS server
        :param pulumi.Input[Sequence[pulumi.Input[str]]] name_servers: Specifies the name servers that the system uses to validate DNS lookups, and resolve host names.
        :param pulumi.Input[int] number_of_dots: Configures the number of dots needed in a name before an initial absolute query will be made.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] searches: Specifies the domains that the system searches for local domain lookups, to resolve local host names.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DnsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        `sys.Dns` Configures DNS Name server on F5 BIG-IP

        ## Example Usage

        ```python
        import pulumi
        import pulumi_f5bigip as f5bigip

        dns1 = f5bigip.sys.Dns("dns1",
            description="/Common/DNS1",
            name_servers=["1.1.1.1"],
            searches=["f5.com"])
        ```

        :param str resource_name: The name of the resource.
        :param DnsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DnsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 number_of_dots: Optional[pulumi.Input[int]] = None,
                 searches: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DnsArgs.__new__(DnsArgs)

            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            if name_servers is None and not opts.urn:
                raise TypeError("Missing required property 'name_servers'")
            __props__.__dict__["name_servers"] = name_servers
            __props__.__dict__["number_of_dots"] = number_of_dots
            __props__.__dict__["searches"] = searches
        super(Dns, __self__).__init__(
            'f5bigip:sys/dns:Dns',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            name_servers: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            number_of_dots: Optional[pulumi.Input[int]] = None,
            searches: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'Dns':
        """
        Get an existing Dns resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: Provide description for your DNS server
        :param pulumi.Input[Sequence[pulumi.Input[str]]] name_servers: Specifies the name servers that the system uses to validate DNS lookups, and resolve host names.
        :param pulumi.Input[int] number_of_dots: Configures the number of dots needed in a name before an initial absolute query will be made.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] searches: Specifies the domains that the system searches for local domain lookups, to resolve local host names.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DnsState.__new__(_DnsState)

        __props__.__dict__["description"] = description
        __props__.__dict__["name_servers"] = name_servers
        __props__.__dict__["number_of_dots"] = number_of_dots
        __props__.__dict__["searches"] = searches
        return Dns(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Provide description for your DNS server
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="nameServers")
    def name_servers(self) -> pulumi.Output[Sequence[str]]:
        """
        Specifies the name servers that the system uses to validate DNS lookups, and resolve host names.
        """
        return pulumi.get(self, "name_servers")

    @property
    @pulumi.getter(name="numberOfDots")
    def number_of_dots(self) -> pulumi.Output[int]:
        """
        Configures the number of dots needed in a name before an initial absolute query will be made.
        """
        return pulumi.get(self, "number_of_dots")

    @property
    @pulumi.getter
    def searches(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        Specifies the domains that the system searches for local domain lookups, to resolve local host names.
        """
        return pulumi.get(self, "searches")

