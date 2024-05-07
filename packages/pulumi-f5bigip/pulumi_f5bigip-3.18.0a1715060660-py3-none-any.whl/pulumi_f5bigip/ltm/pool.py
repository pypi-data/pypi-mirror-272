# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PoolArgs', 'Pool']

@pulumi.input_type
class PoolArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 allow_nat: Optional[pulumi.Input[str]] = None,
                 allow_snat: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 load_balancing_mode: Optional[pulumi.Input[str]] = None,
                 minimum_active_members: Optional[pulumi.Input[int]] = None,
                 monitors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 reselect_tries: Optional[pulumi.Input[int]] = None,
                 service_down_action: Optional[pulumi.Input[str]] = None,
                 slow_ramp_time: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Pool resource.
        :param pulumi.Input[str] name: Name of the pool,it should be `full path`.The full path is the combination of the `partition + name` of the pool.(For example `/Common/my-pool`)
        :param pulumi.Input[str] allow_nat: Specifies whether NATs are automatically enabled or disabled for any connections using this pool, [ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] allow_snat: Specifies whether SNATs are automatically enabled or disabled for any connections using this pool,[ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] description: Specifies descriptive text that identifies the pool.
        :param pulumi.Input[str] load_balancing_mode: Specifies the load balancing method. The default is Round Robin.
        :param pulumi.Input[int] minimum_active_members: Specifies whether the system load balances traffic according to the priority number assigned to the pool member,Default Value is `0` meaning `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] monitors: List of monitor names to associate with the pool
        :param pulumi.Input[int] reselect_tries: Specifies the number of times the system tries to contact a new pool member after a passive failure.
        :param pulumi.Input[str] service_down_action: Specifies how the system should respond when the target pool member becomes unavailable. The default is `None`, Possible values: `[none, reset, reselect, drop]`.
        :param pulumi.Input[int] slow_ramp_time: Specifies the duration during which the system sends less traffic to a newly-enabled pool member.
        """
        pulumi.set(__self__, "name", name)
        if allow_nat is not None:
            pulumi.set(__self__, "allow_nat", allow_nat)
        if allow_snat is not None:
            pulumi.set(__self__, "allow_snat", allow_snat)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if load_balancing_mode is not None:
            pulumi.set(__self__, "load_balancing_mode", load_balancing_mode)
        if minimum_active_members is not None:
            pulumi.set(__self__, "minimum_active_members", minimum_active_members)
        if monitors is not None:
            pulumi.set(__self__, "monitors", monitors)
        if reselect_tries is not None:
            pulumi.set(__self__, "reselect_tries", reselect_tries)
        if service_down_action is not None:
            pulumi.set(__self__, "service_down_action", service_down_action)
        if slow_ramp_time is not None:
            pulumi.set(__self__, "slow_ramp_time", slow_ramp_time)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the pool,it should be `full path`.The full path is the combination of the `partition + name` of the pool.(For example `/Common/my-pool`)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="allowNat")
    def allow_nat(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether NATs are automatically enabled or disabled for any connections using this pool, [ Default : `yes`, Possible Values `yes` or `no`].
        """
        return pulumi.get(self, "allow_nat")

    @allow_nat.setter
    def allow_nat(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_nat", value)

    @property
    @pulumi.getter(name="allowSnat")
    def allow_snat(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether SNATs are automatically enabled or disabled for any connections using this pool,[ Default : `yes`, Possible Values `yes` or `no`].
        """
        return pulumi.get(self, "allow_snat")

    @allow_snat.setter
    def allow_snat(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_snat", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies descriptive text that identifies the pool.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="loadBalancingMode")
    def load_balancing_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the load balancing method. The default is Round Robin.
        """
        return pulumi.get(self, "load_balancing_mode")

    @load_balancing_mode.setter
    def load_balancing_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancing_mode", value)

    @property
    @pulumi.getter(name="minimumActiveMembers")
    def minimum_active_members(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies whether the system load balances traffic according to the priority number assigned to the pool member,Default Value is `0` meaning `disabled`.
        """
        return pulumi.get(self, "minimum_active_members")

    @minimum_active_members.setter
    def minimum_active_members(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "minimum_active_members", value)

    @property
    @pulumi.getter
    def monitors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of monitor names to associate with the pool
        """
        return pulumi.get(self, "monitors")

    @monitors.setter
    def monitors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "monitors", value)

    @property
    @pulumi.getter(name="reselectTries")
    def reselect_tries(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of times the system tries to contact a new pool member after a passive failure.
        """
        return pulumi.get(self, "reselect_tries")

    @reselect_tries.setter
    def reselect_tries(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "reselect_tries", value)

    @property
    @pulumi.getter(name="serviceDownAction")
    def service_down_action(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how the system should respond when the target pool member becomes unavailable. The default is `None`, Possible values: `[none, reset, reselect, drop]`.
        """
        return pulumi.get(self, "service_down_action")

    @service_down_action.setter
    def service_down_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_down_action", value)

    @property
    @pulumi.getter(name="slowRampTime")
    def slow_ramp_time(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the duration during which the system sends less traffic to a newly-enabled pool member.
        """
        return pulumi.get(self, "slow_ramp_time")

    @slow_ramp_time.setter
    def slow_ramp_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "slow_ramp_time", value)


@pulumi.input_type
class _PoolState:
    def __init__(__self__, *,
                 allow_nat: Optional[pulumi.Input[str]] = None,
                 allow_snat: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 load_balancing_mode: Optional[pulumi.Input[str]] = None,
                 minimum_active_members: Optional[pulumi.Input[int]] = None,
                 monitors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reselect_tries: Optional[pulumi.Input[int]] = None,
                 service_down_action: Optional[pulumi.Input[str]] = None,
                 slow_ramp_time: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Pool resources.
        :param pulumi.Input[str] allow_nat: Specifies whether NATs are automatically enabled or disabled for any connections using this pool, [ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] allow_snat: Specifies whether SNATs are automatically enabled or disabled for any connections using this pool,[ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] description: Specifies descriptive text that identifies the pool.
        :param pulumi.Input[str] load_balancing_mode: Specifies the load balancing method. The default is Round Robin.
        :param pulumi.Input[int] minimum_active_members: Specifies whether the system load balances traffic according to the priority number assigned to the pool member,Default Value is `0` meaning `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] monitors: List of monitor names to associate with the pool
        :param pulumi.Input[str] name: Name of the pool,it should be `full path`.The full path is the combination of the `partition + name` of the pool.(For example `/Common/my-pool`)
        :param pulumi.Input[int] reselect_tries: Specifies the number of times the system tries to contact a new pool member after a passive failure.
        :param pulumi.Input[str] service_down_action: Specifies how the system should respond when the target pool member becomes unavailable. The default is `None`, Possible values: `[none, reset, reselect, drop]`.
        :param pulumi.Input[int] slow_ramp_time: Specifies the duration during which the system sends less traffic to a newly-enabled pool member.
        """
        if allow_nat is not None:
            pulumi.set(__self__, "allow_nat", allow_nat)
        if allow_snat is not None:
            pulumi.set(__self__, "allow_snat", allow_snat)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if load_balancing_mode is not None:
            pulumi.set(__self__, "load_balancing_mode", load_balancing_mode)
        if minimum_active_members is not None:
            pulumi.set(__self__, "minimum_active_members", minimum_active_members)
        if monitors is not None:
            pulumi.set(__self__, "monitors", monitors)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if reselect_tries is not None:
            pulumi.set(__self__, "reselect_tries", reselect_tries)
        if service_down_action is not None:
            pulumi.set(__self__, "service_down_action", service_down_action)
        if slow_ramp_time is not None:
            pulumi.set(__self__, "slow_ramp_time", slow_ramp_time)

    @property
    @pulumi.getter(name="allowNat")
    def allow_nat(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether NATs are automatically enabled or disabled for any connections using this pool, [ Default : `yes`, Possible Values `yes` or `no`].
        """
        return pulumi.get(self, "allow_nat")

    @allow_nat.setter
    def allow_nat(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_nat", value)

    @property
    @pulumi.getter(name="allowSnat")
    def allow_snat(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether SNATs are automatically enabled or disabled for any connections using this pool,[ Default : `yes`, Possible Values `yes` or `no`].
        """
        return pulumi.get(self, "allow_snat")

    @allow_snat.setter
    def allow_snat(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allow_snat", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies descriptive text that identifies the pool.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="loadBalancingMode")
    def load_balancing_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the load balancing method. The default is Round Robin.
        """
        return pulumi.get(self, "load_balancing_mode")

    @load_balancing_mode.setter
    def load_balancing_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "load_balancing_mode", value)

    @property
    @pulumi.getter(name="minimumActiveMembers")
    def minimum_active_members(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies whether the system load balances traffic according to the priority number assigned to the pool member,Default Value is `0` meaning `disabled`.
        """
        return pulumi.get(self, "minimum_active_members")

    @minimum_active_members.setter
    def minimum_active_members(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "minimum_active_members", value)

    @property
    @pulumi.getter
    def monitors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of monitor names to associate with the pool
        """
        return pulumi.get(self, "monitors")

    @monitors.setter
    def monitors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "monitors", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the pool,it should be `full path`.The full path is the combination of the `partition + name` of the pool.(For example `/Common/my-pool`)
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="reselectTries")
    def reselect_tries(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the number of times the system tries to contact a new pool member after a passive failure.
        """
        return pulumi.get(self, "reselect_tries")

    @reselect_tries.setter
    def reselect_tries(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "reselect_tries", value)

    @property
    @pulumi.getter(name="serviceDownAction")
    def service_down_action(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how the system should respond when the target pool member becomes unavailable. The default is `None`, Possible values: `[none, reset, reselect, drop]`.
        """
        return pulumi.get(self, "service_down_action")

    @service_down_action.setter
    def service_down_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_down_action", value)

    @property
    @pulumi.getter(name="slowRampTime")
    def slow_ramp_time(self) -> Optional[pulumi.Input[int]]:
        """
        Specifies the duration during which the system sends less traffic to a newly-enabled pool member.
        """
        return pulumi.get(self, "slow_ramp_time")

    @slow_ramp_time.setter
    def slow_ramp_time(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "slow_ramp_time", value)


class Pool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_nat: Optional[pulumi.Input[str]] = None,
                 allow_snat: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 load_balancing_mode: Optional[pulumi.Input[str]] = None,
                 minimum_active_members: Optional[pulumi.Input[int]] = None,
                 monitors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reselect_tries: Optional[pulumi.Input[int]] = None,
                 service_down_action: Optional[pulumi.Input[str]] = None,
                 slow_ramp_time: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        `ltm.Pool` Manages F5 BIG-IP LTM pools via iControl REST API.

        For resources should be named with their `full path`. The full path is the combination of the `partition + name` of the resource or  `partition + directory + name`.
        For example `/Common/my-pool`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_f5bigip as f5bigip

        monitor = f5bigip.ltm.Monitor("monitor",
            name="/Common/terraform_monitor",
            parent="/Common/http")
        pool = f5bigip.ltm.Pool("pool",
            name="/Common/Axiom_Environment_APP1_Pool",
            load_balancing_mode="round-robin",
            minimum_active_members=1,
            monitors=[monitor.name])
        ```

        ## Importing

        An existing pool can be imported into this resource by supplying pool Name in `full path` as `id`.
        An example is below:
        ```sh
        $ terraform import bigip_ltm_pool.k8s_prod_import /Common/k8prod_Pool

        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allow_nat: Specifies whether NATs are automatically enabled or disabled for any connections using this pool, [ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] allow_snat: Specifies whether SNATs are automatically enabled or disabled for any connections using this pool,[ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] description: Specifies descriptive text that identifies the pool.
        :param pulumi.Input[str] load_balancing_mode: Specifies the load balancing method. The default is Round Robin.
        :param pulumi.Input[int] minimum_active_members: Specifies whether the system load balances traffic according to the priority number assigned to the pool member,Default Value is `0` meaning `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] monitors: List of monitor names to associate with the pool
        :param pulumi.Input[str] name: Name of the pool,it should be `full path`.The full path is the combination of the `partition + name` of the pool.(For example `/Common/my-pool`)
        :param pulumi.Input[int] reselect_tries: Specifies the number of times the system tries to contact a new pool member after a passive failure.
        :param pulumi.Input[str] service_down_action: Specifies how the system should respond when the target pool member becomes unavailable. The default is `None`, Possible values: `[none, reset, reselect, drop]`.
        :param pulumi.Input[int] slow_ramp_time: Specifies the duration during which the system sends less traffic to a newly-enabled pool member.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        `ltm.Pool` Manages F5 BIG-IP LTM pools via iControl REST API.

        For resources should be named with their `full path`. The full path is the combination of the `partition + name` of the resource or  `partition + directory + name`.
        For example `/Common/my-pool`.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_f5bigip as f5bigip

        monitor = f5bigip.ltm.Monitor("monitor",
            name="/Common/terraform_monitor",
            parent="/Common/http")
        pool = f5bigip.ltm.Pool("pool",
            name="/Common/Axiom_Environment_APP1_Pool",
            load_balancing_mode="round-robin",
            minimum_active_members=1,
            monitors=[monitor.name])
        ```

        ## Importing

        An existing pool can be imported into this resource by supplying pool Name in `full path` as `id`.
        An example is below:
        ```sh
        $ terraform import bigip_ltm_pool.k8s_prod_import /Common/k8prod_Pool

        ```

        :param str resource_name: The name of the resource.
        :param PoolArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PoolArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_nat: Optional[pulumi.Input[str]] = None,
                 allow_snat: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 load_balancing_mode: Optional[pulumi.Input[str]] = None,
                 minimum_active_members: Optional[pulumi.Input[int]] = None,
                 monitors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 reselect_tries: Optional[pulumi.Input[int]] = None,
                 service_down_action: Optional[pulumi.Input[str]] = None,
                 slow_ramp_time: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PoolArgs.__new__(PoolArgs)

            __props__.__dict__["allow_nat"] = allow_nat
            __props__.__dict__["allow_snat"] = allow_snat
            __props__.__dict__["description"] = description
            __props__.__dict__["load_balancing_mode"] = load_balancing_mode
            __props__.__dict__["minimum_active_members"] = minimum_active_members
            __props__.__dict__["monitors"] = monitors
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["reselect_tries"] = reselect_tries
            __props__.__dict__["service_down_action"] = service_down_action
            __props__.__dict__["slow_ramp_time"] = slow_ramp_time
        super(Pool, __self__).__init__(
            'f5bigip:ltm/pool:Pool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allow_nat: Optional[pulumi.Input[str]] = None,
            allow_snat: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            load_balancing_mode: Optional[pulumi.Input[str]] = None,
            minimum_active_members: Optional[pulumi.Input[int]] = None,
            monitors: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            reselect_tries: Optional[pulumi.Input[int]] = None,
            service_down_action: Optional[pulumi.Input[str]] = None,
            slow_ramp_time: Optional[pulumi.Input[int]] = None) -> 'Pool':
        """
        Get an existing Pool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allow_nat: Specifies whether NATs are automatically enabled or disabled for any connections using this pool, [ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] allow_snat: Specifies whether SNATs are automatically enabled or disabled for any connections using this pool,[ Default : `yes`, Possible Values `yes` or `no`].
        :param pulumi.Input[str] description: Specifies descriptive text that identifies the pool.
        :param pulumi.Input[str] load_balancing_mode: Specifies the load balancing method. The default is Round Robin.
        :param pulumi.Input[int] minimum_active_members: Specifies whether the system load balances traffic according to the priority number assigned to the pool member,Default Value is `0` meaning `disabled`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] monitors: List of monitor names to associate with the pool
        :param pulumi.Input[str] name: Name of the pool,it should be `full path`.The full path is the combination of the `partition + name` of the pool.(For example `/Common/my-pool`)
        :param pulumi.Input[int] reselect_tries: Specifies the number of times the system tries to contact a new pool member after a passive failure.
        :param pulumi.Input[str] service_down_action: Specifies how the system should respond when the target pool member becomes unavailable. The default is `None`, Possible values: `[none, reset, reselect, drop]`.
        :param pulumi.Input[int] slow_ramp_time: Specifies the duration during which the system sends less traffic to a newly-enabled pool member.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PoolState.__new__(_PoolState)

        __props__.__dict__["allow_nat"] = allow_nat
        __props__.__dict__["allow_snat"] = allow_snat
        __props__.__dict__["description"] = description
        __props__.__dict__["load_balancing_mode"] = load_balancing_mode
        __props__.__dict__["minimum_active_members"] = minimum_active_members
        __props__.__dict__["monitors"] = monitors
        __props__.__dict__["name"] = name
        __props__.__dict__["reselect_tries"] = reselect_tries
        __props__.__dict__["service_down_action"] = service_down_action
        __props__.__dict__["slow_ramp_time"] = slow_ramp_time
        return Pool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowNat")
    def allow_nat(self) -> pulumi.Output[str]:
        """
        Specifies whether NATs are automatically enabled or disabled for any connections using this pool, [ Default : `yes`, Possible Values `yes` or `no`].
        """
        return pulumi.get(self, "allow_nat")

    @property
    @pulumi.getter(name="allowSnat")
    def allow_snat(self) -> pulumi.Output[str]:
        """
        Specifies whether SNATs are automatically enabled or disabled for any connections using this pool,[ Default : `yes`, Possible Values `yes` or `no`].
        """
        return pulumi.get(self, "allow_snat")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies descriptive text that identifies the pool.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="loadBalancingMode")
    def load_balancing_mode(self) -> pulumi.Output[str]:
        """
        Specifies the load balancing method. The default is Round Robin.
        """
        return pulumi.get(self, "load_balancing_mode")

    @property
    @pulumi.getter(name="minimumActiveMembers")
    def minimum_active_members(self) -> pulumi.Output[int]:
        """
        Specifies whether the system load balances traffic according to the priority number assigned to the pool member,Default Value is `0` meaning `disabled`.
        """
        return pulumi.get(self, "minimum_active_members")

    @property
    @pulumi.getter
    def monitors(self) -> pulumi.Output[Sequence[str]]:
        """
        List of monitor names to associate with the pool
        """
        return pulumi.get(self, "monitors")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the pool,it should be `full path`.The full path is the combination of the `partition + name` of the pool.(For example `/Common/my-pool`)
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="reselectTries")
    def reselect_tries(self) -> pulumi.Output[int]:
        """
        Specifies the number of times the system tries to contact a new pool member after a passive failure.
        """
        return pulumi.get(self, "reselect_tries")

    @property
    @pulumi.getter(name="serviceDownAction")
    def service_down_action(self) -> pulumi.Output[str]:
        """
        Specifies how the system should respond when the target pool member becomes unavailable. The default is `None`, Possible values: `[none, reset, reselect, drop]`.
        """
        return pulumi.get(self, "service_down_action")

    @property
    @pulumi.getter(name="slowRampTime")
    def slow_ramp_time(self) -> pulumi.Output[int]:
        """
        Specifies the duration during which the system sends less traffic to a newly-enabled pool member.
        """
        return pulumi.get(self, "slow_ramp_time")

