# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'GetAlertChannelResult',
    'AwaitableGetAlertChannelResult',
    'get_alert_channel',
    'get_alert_channel_output',
]

@pulumi.output_type
class GetAlertChannelResult:
    """
    A collection of values returned by getAlertChannel.
    """
    def __init__(__self__, account_id=None, config=None, id=None, name=None, policy_ids=None, type=None):
        if account_id and not isinstance(account_id, int):
            raise TypeError("Expected argument 'account_id' to be a int")
        pulumi.set(__self__, "account_id", account_id)
        if config and not isinstance(config, dict):
            raise TypeError("Expected argument 'config' to be a dict")
        pulumi.set(__self__, "config", config)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if policy_ids and not isinstance(policy_ids, list):
            raise TypeError("Expected argument 'policy_ids' to be a list")
        pulumi.set(__self__, "policy_ids", policy_ids)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="accountId")
    def account_id(self) -> int:
        return pulumi.get(self, "account_id")

    @property
    @pulumi.getter
    def config(self) -> 'outputs.GetAlertChannelConfigResult':
        """
        Alert channel configuration.
        """
        return pulumi.get(self, "config")

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
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="policyIds")
    def policy_ids(self) -> Sequence[int]:
        """
        A list of policy IDs associated with the alert channel.
        """
        return pulumi.get(self, "policy_ids")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Alert channel type, either: `email`, `opsgenie`, `pagerduty`, `slack`, `victorops`, or `webhook`.
        """
        return pulumi.get(self, "type")


class AwaitableGetAlertChannelResult(GetAlertChannelResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAlertChannelResult(
            account_id=self.account_id,
            config=self.config,
            id=self.id,
            name=self.name,
            policy_ids=self.policy_ids,
            type=self.type)


def get_alert_channel(account_id: Optional[int] = None,
                      name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAlertChannelResult:
    """
    Use this data source to get information about a specific alert channel in New Relic that already exists.

    > **WARNING:** The `AlertChannel` data source is deprecated and will be removed in the next major release.


    :param int account_id: The New Relic account ID to operate on.  This allows you to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
    :param str name: The name of the alert channel in New Relic.
    """
    __args__ = dict()
    __args__['accountId'] = account_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('newrelic:index/getAlertChannel:getAlertChannel', __args__, opts=opts, typ=GetAlertChannelResult).value

    return AwaitableGetAlertChannelResult(
        account_id=pulumi.get(__ret__, 'account_id'),
        config=pulumi.get(__ret__, 'config'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        policy_ids=pulumi.get(__ret__, 'policy_ids'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_alert_channel)
def get_alert_channel_output(account_id: Optional[pulumi.Input[Optional[int]]] = None,
                             name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAlertChannelResult]:
    """
    Use this data source to get information about a specific alert channel in New Relic that already exists.

    > **WARNING:** The `AlertChannel` data source is deprecated and will be removed in the next major release.


    :param int account_id: The New Relic account ID to operate on.  This allows you to override the `account_id` attribute set on the provider. Defaults to the environment variable `NEW_RELIC_ACCOUNT_ID`.
    :param str name: The name of the alert channel in New Relic.
    """
    ...
