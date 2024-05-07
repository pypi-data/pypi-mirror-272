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

__all__ = [
    'GetPolicyResult',
    'AwaitableGetPolicyResult',
    'get_policy',
    'get_policy_output',
]

@pulumi.output_type
class GetPolicyResult:
    """
    A collection of values returned by getPolicy.
    """
    def __init__(__self__, controls=None, id=None, name=None, published_copy=None, requires=None, rules=None, strategy=None):
        if controls and not isinstance(controls, list):
            raise TypeError("Expected argument 'controls' to be a list")
        pulumi.set(__self__, "controls", controls)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if published_copy and not isinstance(published_copy, str):
            raise TypeError("Expected argument 'published_copy' to be a str")
        pulumi.set(__self__, "published_copy", published_copy)
        if requires and not isinstance(requires, list):
            raise TypeError("Expected argument 'requires' to be a list")
        pulumi.set(__self__, "requires", requires)
        if rules and not isinstance(rules, list):
            raise TypeError("Expected argument 'rules' to be a list")
        pulumi.set(__self__, "rules", rules)
        if strategy and not isinstance(strategy, str):
            raise TypeError("Expected argument 'strategy' to be a str")
        pulumi.set(__self__, "strategy", strategy)

    @property
    @pulumi.getter
    def controls(self) -> Optional[Sequence[str]]:
        """
        Specifies the controls.
        """
        return pulumi.get(self, "controls")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publishedCopy")
    def published_copy(self) -> Optional[str]:
        return pulumi.get(self, "published_copy")

    @property
    @pulumi.getter
    def requires(self) -> Optional[Sequence[str]]:
        """
        Specifies the protocol.
        """
        return pulumi.get(self, "requires")

    @property
    @pulumi.getter
    def rules(self) -> Optional[Sequence['outputs.GetPolicyRuleResult']]:
        """
        Rules defined in the policy.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter
    def strategy(self) -> Optional[str]:
        """
        Specifies the match strategy.
        """
        return pulumi.get(self, "strategy")


class AwaitableGetPolicyResult(GetPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPolicyResult(
            controls=self.controls,
            id=self.id,
            name=self.name,
            published_copy=self.published_copy,
            requires=self.requires,
            rules=self.rules,
            strategy=self.strategy)


def get_policy(controls: Optional[Sequence[str]] = None,
               name: Optional[str] = None,
               published_copy: Optional[str] = None,
               requires: Optional[Sequence[str]] = None,
               rules: Optional[Sequence[pulumi.InputType['GetPolicyRuleArgs']]] = None,
               strategy: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPolicyResult:
    """
    Use this data source (`ltm.Policy`) to get the ltm policy details available on BIG-IP

    ## Example Usage

    ```python
    import pulumi
    import pulumi_f5bigip as f5bigip

    test = f5bigip.ltm.get_policy(name="/Common/test-policy")
    pulumi.export("bigipPolicy", test.rules)
    ```


    :param Sequence[str] controls: Specifies the controls.
    :param str name: Name of the policy which includes partion ( /partition/policy-name )
    :param Sequence[str] requires: Specifies the protocol.
    :param Sequence[pulumi.InputType['GetPolicyRuleArgs']] rules: Rules defined in the policy.
    :param str strategy: Specifies the match strategy.
    """
    __args__ = dict()
    __args__['controls'] = controls
    __args__['name'] = name
    __args__['publishedCopy'] = published_copy
    __args__['requires'] = requires
    __args__['rules'] = rules
    __args__['strategy'] = strategy
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('f5bigip:ltm/getPolicy:getPolicy', __args__, opts=opts, typ=GetPolicyResult).value

    return AwaitableGetPolicyResult(
        controls=pulumi.get(__ret__, 'controls'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        published_copy=pulumi.get(__ret__, 'published_copy'),
        requires=pulumi.get(__ret__, 'requires'),
        rules=pulumi.get(__ret__, 'rules'),
        strategy=pulumi.get(__ret__, 'strategy'))


@_utilities.lift_output_func(get_policy)
def get_policy_output(controls: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                      name: Optional[pulumi.Input[str]] = None,
                      published_copy: Optional[pulumi.Input[Optional[str]]] = None,
                      requires: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                      rules: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetPolicyRuleArgs']]]]] = None,
                      strategy: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPolicyResult]:
    """
    Use this data source (`ltm.Policy`) to get the ltm policy details available on BIG-IP

    ## Example Usage

    ```python
    import pulumi
    import pulumi_f5bigip as f5bigip

    test = f5bigip.ltm.get_policy(name="/Common/test-policy")
    pulumi.export("bigipPolicy", test.rules)
    ```


    :param Sequence[str] controls: Specifies the controls.
    :param str name: Name of the policy which includes partion ( /partition/policy-name )
    :param Sequence[str] requires: Specifies the protocol.
    :param Sequence[pulumi.InputType['GetPolicyRuleArgs']] rules: Rules defined in the policy.
    :param str strategy: Specifies the match strategy.
    """
    ...
