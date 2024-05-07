# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['QosBandwidthLimitRuleArgs', 'QosBandwidthLimitRule']

@pulumi.input_type
class QosBandwidthLimitRuleArgs:
    def __init__(__self__, *,
                 max_kbps: pulumi.Input[int],
                 qos_policy_id: pulumi.Input[str],
                 direction: Optional[pulumi.Input[str]] = None,
                 max_burst_kbps: Optional[pulumi.Input[int]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a QosBandwidthLimitRule resource.
        :param pulumi.Input[int] max_kbps: The maximum kilobits per second of a QoS bandwidth limit rule. Changing this updates the
               maximum kilobits per second of the existing QoS bandwidth limit rule.
        :param pulumi.Input[str] qos_policy_id: The QoS policy reference. Changing this creates a new QoS bandwidth limit rule.
        :param pulumi.Input[str] direction: The direction of traffic. Defaults to "egress". Changing this updates the direction of the
               existing QoS bandwidth limit rule.
        :param pulumi.Input[int] max_burst_kbps: The maximum burst size in kilobits of a QoS bandwidth limit rule. Changing this updates the
               maximum burst size in kilobits of the existing QoS bandwidth limit rule.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create a Neutron QoS bandwidth limit rule. If omitted, the
               `region` argument of the provider is used. Changing this creates a new QoS bandwidth limit rule.
        """
        pulumi.set(__self__, "max_kbps", max_kbps)
        pulumi.set(__self__, "qos_policy_id", qos_policy_id)
        if direction is not None:
            pulumi.set(__self__, "direction", direction)
        if max_burst_kbps is not None:
            pulumi.set(__self__, "max_burst_kbps", max_burst_kbps)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter(name="maxKbps")
    def max_kbps(self) -> pulumi.Input[int]:
        """
        The maximum kilobits per second of a QoS bandwidth limit rule. Changing this updates the
        maximum kilobits per second of the existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "max_kbps")

    @max_kbps.setter
    def max_kbps(self, value: pulumi.Input[int]):
        pulumi.set(self, "max_kbps", value)

    @property
    @pulumi.getter(name="qosPolicyId")
    def qos_policy_id(self) -> pulumi.Input[str]:
        """
        The QoS policy reference. Changing this creates a new QoS bandwidth limit rule.
        """
        return pulumi.get(self, "qos_policy_id")

    @qos_policy_id.setter
    def qos_policy_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "qos_policy_id", value)

    @property
    @pulumi.getter
    def direction(self) -> Optional[pulumi.Input[str]]:
        """
        The direction of traffic. Defaults to "egress". Changing this updates the direction of the
        existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "direction")

    @direction.setter
    def direction(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "direction", value)

    @property
    @pulumi.getter(name="maxBurstKbps")
    def max_burst_kbps(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum burst size in kilobits of a QoS bandwidth limit rule. Changing this updates the
        maximum burst size in kilobits of the existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "max_burst_kbps")

    @max_burst_kbps.setter
    def max_burst_kbps(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_burst_kbps", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to obtain the V2 Networking client.
        A Networking client is needed to create a Neutron QoS bandwidth limit rule. If omitted, the
        `region` argument of the provider is used. Changing this creates a new QoS bandwidth limit rule.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _QosBandwidthLimitRuleState:
    def __init__(__self__, *,
                 direction: Optional[pulumi.Input[str]] = None,
                 max_burst_kbps: Optional[pulumi.Input[int]] = None,
                 max_kbps: Optional[pulumi.Input[int]] = None,
                 qos_policy_id: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering QosBandwidthLimitRule resources.
        :param pulumi.Input[str] direction: The direction of traffic. Defaults to "egress". Changing this updates the direction of the
               existing QoS bandwidth limit rule.
        :param pulumi.Input[int] max_burst_kbps: The maximum burst size in kilobits of a QoS bandwidth limit rule. Changing this updates the
               maximum burst size in kilobits of the existing QoS bandwidth limit rule.
        :param pulumi.Input[int] max_kbps: The maximum kilobits per second of a QoS bandwidth limit rule. Changing this updates the
               maximum kilobits per second of the existing QoS bandwidth limit rule.
        :param pulumi.Input[str] qos_policy_id: The QoS policy reference. Changing this creates a new QoS bandwidth limit rule.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create a Neutron QoS bandwidth limit rule. If omitted, the
               `region` argument of the provider is used. Changing this creates a new QoS bandwidth limit rule.
        """
        if direction is not None:
            pulumi.set(__self__, "direction", direction)
        if max_burst_kbps is not None:
            pulumi.set(__self__, "max_burst_kbps", max_burst_kbps)
        if max_kbps is not None:
            pulumi.set(__self__, "max_kbps", max_kbps)
        if qos_policy_id is not None:
            pulumi.set(__self__, "qos_policy_id", qos_policy_id)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def direction(self) -> Optional[pulumi.Input[str]]:
        """
        The direction of traffic. Defaults to "egress". Changing this updates the direction of the
        existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "direction")

    @direction.setter
    def direction(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "direction", value)

    @property
    @pulumi.getter(name="maxBurstKbps")
    def max_burst_kbps(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum burst size in kilobits of a QoS bandwidth limit rule. Changing this updates the
        maximum burst size in kilobits of the existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "max_burst_kbps")

    @max_burst_kbps.setter
    def max_burst_kbps(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_burst_kbps", value)

    @property
    @pulumi.getter(name="maxKbps")
    def max_kbps(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum kilobits per second of a QoS bandwidth limit rule. Changing this updates the
        maximum kilobits per second of the existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "max_kbps")

    @max_kbps.setter
    def max_kbps(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_kbps", value)

    @property
    @pulumi.getter(name="qosPolicyId")
    def qos_policy_id(self) -> Optional[pulumi.Input[str]]:
        """
        The QoS policy reference. Changing this creates a new QoS bandwidth limit rule.
        """
        return pulumi.get(self, "qos_policy_id")

    @qos_policy_id.setter
    def qos_policy_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qos_policy_id", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to obtain the V2 Networking client.
        A Networking client is needed to create a Neutron QoS bandwidth limit rule. If omitted, the
        `region` argument of the provider is used. Changing this creates a new QoS bandwidth limit rule.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


class QosBandwidthLimitRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 direction: Optional[pulumi.Input[str]] = None,
                 max_burst_kbps: Optional[pulumi.Input[int]] = None,
                 max_kbps: Optional[pulumi.Input[int]] = None,
                 qos_policy_id: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a V2 Neutron QoS bandwidth limit rule resource within OpenStack.

        ## Example Usage

        ### Create a QoS Policy with some bandwidth limit rule

        ```python
        import pulumi
        import pulumi_openstack as openstack

        qos_policy1 = openstack.networking.QosPolicy("qos_policy_1",
            name="qos_policy_1",
            description="bw_limit")
        bw_limit_rule1 = openstack.networking.QosBandwidthLimitRule("bw_limit_rule_1",
            qos_policy_id=qos_policy1.id,
            max_kbps=3000,
            max_burst_kbps=300,
            direction="egress")
        ```

        ## Import

        QoS bandwidth limit rules can be imported using the `qos_policy_id/bandwidth_limit_rule` format, e.g.

        ```sh
        $ pulumi import openstack:networking/qosBandwidthLimitRule:QosBandwidthLimitRule bw_limit_rule_1 d6ae28ce-fcb5-4180-aa62-d260a27e09ae/46dfb556-b92f-48ce-94c5-9a9e2140de94
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] direction: The direction of traffic. Defaults to "egress". Changing this updates the direction of the
               existing QoS bandwidth limit rule.
        :param pulumi.Input[int] max_burst_kbps: The maximum burst size in kilobits of a QoS bandwidth limit rule. Changing this updates the
               maximum burst size in kilobits of the existing QoS bandwidth limit rule.
        :param pulumi.Input[int] max_kbps: The maximum kilobits per second of a QoS bandwidth limit rule. Changing this updates the
               maximum kilobits per second of the existing QoS bandwidth limit rule.
        :param pulumi.Input[str] qos_policy_id: The QoS policy reference. Changing this creates a new QoS bandwidth limit rule.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create a Neutron QoS bandwidth limit rule. If omitted, the
               `region` argument of the provider is used. Changing this creates a new QoS bandwidth limit rule.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: QosBandwidthLimitRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a V2 Neutron QoS bandwidth limit rule resource within OpenStack.

        ## Example Usage

        ### Create a QoS Policy with some bandwidth limit rule

        ```python
        import pulumi
        import pulumi_openstack as openstack

        qos_policy1 = openstack.networking.QosPolicy("qos_policy_1",
            name="qos_policy_1",
            description="bw_limit")
        bw_limit_rule1 = openstack.networking.QosBandwidthLimitRule("bw_limit_rule_1",
            qos_policy_id=qos_policy1.id,
            max_kbps=3000,
            max_burst_kbps=300,
            direction="egress")
        ```

        ## Import

        QoS bandwidth limit rules can be imported using the `qos_policy_id/bandwidth_limit_rule` format, e.g.

        ```sh
        $ pulumi import openstack:networking/qosBandwidthLimitRule:QosBandwidthLimitRule bw_limit_rule_1 d6ae28ce-fcb5-4180-aa62-d260a27e09ae/46dfb556-b92f-48ce-94c5-9a9e2140de94
        ```

        :param str resource_name: The name of the resource.
        :param QosBandwidthLimitRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(QosBandwidthLimitRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 direction: Optional[pulumi.Input[str]] = None,
                 max_burst_kbps: Optional[pulumi.Input[int]] = None,
                 max_kbps: Optional[pulumi.Input[int]] = None,
                 qos_policy_id: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = QosBandwidthLimitRuleArgs.__new__(QosBandwidthLimitRuleArgs)

            __props__.__dict__["direction"] = direction
            __props__.__dict__["max_burst_kbps"] = max_burst_kbps
            if max_kbps is None and not opts.urn:
                raise TypeError("Missing required property 'max_kbps'")
            __props__.__dict__["max_kbps"] = max_kbps
            if qos_policy_id is None and not opts.urn:
                raise TypeError("Missing required property 'qos_policy_id'")
            __props__.__dict__["qos_policy_id"] = qos_policy_id
            __props__.__dict__["region"] = region
        super(QosBandwidthLimitRule, __self__).__init__(
            'openstack:networking/qosBandwidthLimitRule:QosBandwidthLimitRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            direction: Optional[pulumi.Input[str]] = None,
            max_burst_kbps: Optional[pulumi.Input[int]] = None,
            max_kbps: Optional[pulumi.Input[int]] = None,
            qos_policy_id: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None) -> 'QosBandwidthLimitRule':
        """
        Get an existing QosBandwidthLimitRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] direction: The direction of traffic. Defaults to "egress". Changing this updates the direction of the
               existing QoS bandwidth limit rule.
        :param pulumi.Input[int] max_burst_kbps: The maximum burst size in kilobits of a QoS bandwidth limit rule. Changing this updates the
               maximum burst size in kilobits of the existing QoS bandwidth limit rule.
        :param pulumi.Input[int] max_kbps: The maximum kilobits per second of a QoS bandwidth limit rule. Changing this updates the
               maximum kilobits per second of the existing QoS bandwidth limit rule.
        :param pulumi.Input[str] qos_policy_id: The QoS policy reference. Changing this creates a new QoS bandwidth limit rule.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create a Neutron QoS bandwidth limit rule. If omitted, the
               `region` argument of the provider is used. Changing this creates a new QoS bandwidth limit rule.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _QosBandwidthLimitRuleState.__new__(_QosBandwidthLimitRuleState)

        __props__.__dict__["direction"] = direction
        __props__.__dict__["max_burst_kbps"] = max_burst_kbps
        __props__.__dict__["max_kbps"] = max_kbps
        __props__.__dict__["qos_policy_id"] = qos_policy_id
        __props__.__dict__["region"] = region
        return QosBandwidthLimitRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def direction(self) -> pulumi.Output[Optional[str]]:
        """
        The direction of traffic. Defaults to "egress". Changing this updates the direction of the
        existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "direction")

    @property
    @pulumi.getter(name="maxBurstKbps")
    def max_burst_kbps(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum burst size in kilobits of a QoS bandwidth limit rule. Changing this updates the
        maximum burst size in kilobits of the existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "max_burst_kbps")

    @property
    @pulumi.getter(name="maxKbps")
    def max_kbps(self) -> pulumi.Output[int]:
        """
        The maximum kilobits per second of a QoS bandwidth limit rule. Changing this updates the
        maximum kilobits per second of the existing QoS bandwidth limit rule.
        """
        return pulumi.get(self, "max_kbps")

    @property
    @pulumi.getter(name="qosPolicyId")
    def qos_policy_id(self) -> pulumi.Output[str]:
        """
        The QoS policy reference. Changing this creates a new QoS bandwidth limit rule.
        """
        return pulumi.get(self, "qos_policy_id")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region in which to obtain the V2 Networking client.
        A Networking client is needed to create a Neutron QoS bandwidth limit rule. If omitted, the
        `region` argument of the provider is used. Changing this creates a new QoS bandwidth limit rule.
        """
        return pulumi.get(self, "region")

