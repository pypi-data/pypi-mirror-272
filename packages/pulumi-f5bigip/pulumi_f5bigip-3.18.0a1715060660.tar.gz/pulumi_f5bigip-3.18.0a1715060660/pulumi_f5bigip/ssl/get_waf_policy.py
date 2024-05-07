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
    'GetWafPolicyResult',
    'AwaitableGetWafPolicyResult',
    'get_waf_policy',
    'get_waf_policy_output',
]

@pulumi.output_type
class GetWafPolicyResult:
    """
    A collection of values returned by getWafPolicy.
    """
    def __init__(__self__, id=None, policy_id=None, policy_json=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy_id and not isinstance(policy_id, str):
            raise TypeError("Expected argument 'policy_id' to be a str")
        pulumi.set(__self__, "policy_id", policy_id)
        if policy_json and not isinstance(policy_json, str):
            raise TypeError("Expected argument 'policy_json' to be a str")
        pulumi.set(__self__, "policy_json", policy_json)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="policyId")
    def policy_id(self) -> str:
        return pulumi.get(self, "policy_id")

    @property
    @pulumi.getter(name="policyJson")
    def policy_json(self) -> str:
        """
        Exported WAF policy JSON
        """
        return pulumi.get(self, "policy_json")


class AwaitableGetWafPolicyResult(GetWafPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWafPolicyResult(
            id=self.id,
            policy_id=self.policy_id,
            policy_json=self.policy_json)


def get_waf_policy(policy_id: Optional[str] = None,
                   policy_json: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWafPolicyResult:
    """
    Use this data source (`WafPolicy`) to get the details of exist WAF policy BIG-IP.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_f5bigip as f5bigip

    existpolicy = f5bigip.ssl.get_waf_policy(policy_id="xxxxx")
    ```


    :param str policy_id: ID of the WAF policy deployed in the BIG-IP.
    :param str policy_json: Exported WAF policy JSON
    """
    __args__ = dict()
    __args__['policyId'] = policy_id
    __args__['policyJson'] = policy_json
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('f5bigip:ssl/getWafPolicy:getWafPolicy', __args__, opts=opts, typ=GetWafPolicyResult).value

    return AwaitableGetWafPolicyResult(
        id=pulumi.get(__ret__, 'id'),
        policy_id=pulumi.get(__ret__, 'policy_id'),
        policy_json=pulumi.get(__ret__, 'policy_json'))


@_utilities.lift_output_func(get_waf_policy)
def get_waf_policy_output(policy_id: Optional[pulumi.Input[str]] = None,
                          policy_json: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWafPolicyResult]:
    """
    Use this data source (`WafPolicy`) to get the details of exist WAF policy BIG-IP.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_f5bigip as f5bigip

    existpolicy = f5bigip.ssl.get_waf_policy(policy_id="xxxxx")
    ```


    :param str policy_id: ID of the WAF policy deployed in the BIG-IP.
    :param str policy_json: Exported WAF policy JSON
    """
    ...
