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

__all__ = ['PoolArgs', 'Pool']

@pulumi.input_type
class PoolArgs:
    def __init__(__self__, *,
                 lb_method: pulumi.Input[str],
                 protocol: pulumi.Input[str],
                 admin_state_up: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 loadbalancer_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 persistence: Optional[pulumi.Input['PoolPersistenceArgs']] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Pool resource.
        :param pulumi.Input[str] lb_method: The load balancing algorithm to
               distribute traffic to the pool's members. Must be one of
               ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP, or SOURCE_IP_PORT (supported only
               in Octavia).
        :param pulumi.Input[str] protocol: The protocol - can either be TCP, HTTP, HTTPS, PROXY,
               UDP (supported only in Octavia), PROXYV2 (**Octavia minor version >= 2.22**)
               or SCTP (**Octavia minor version >= 2.23**). Changing this creates a new pool.
        :param pulumi.Input[bool] admin_state_up: The administrative state of the pool.
               A valid value is true (UP) or false (DOWN).
        :param pulumi.Input[str] description: Human-readable description for the pool.
        :param pulumi.Input[str] listener_id: The Listener on which the members of the pool
               will be associated with. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] loadbalancer_id: The load balancer on which to provision this
               pool. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] name: Human-readable name for the pool.
        :param pulumi.Input['PoolPersistenceArgs'] persistence: Omit this field to prevent session persistence.  Indicates
               whether connections in the same session will be processed by the same Pool
               member or not. Changing this creates a new pool.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create an . If omitted, the
               `region` argument of the provider is used. Changing this creates a new
               pool.
        :param pulumi.Input[str] tenant_id: Required for admins. The UUID of the tenant who owns
               the pool.  Only administrative users can specify a tenant UUID
               other than their own. Changing this creates a new pool.
        """
        pulumi.set(__self__, "lb_method", lb_method)
        pulumi.set(__self__, "protocol", protocol)
        if admin_state_up is not None:
            pulumi.set(__self__, "admin_state_up", admin_state_up)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if listener_id is not None:
            pulumi.set(__self__, "listener_id", listener_id)
        if loadbalancer_id is not None:
            pulumi.set(__self__, "loadbalancer_id", loadbalancer_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if persistence is not None:
            pulumi.set(__self__, "persistence", persistence)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="lbMethod")
    def lb_method(self) -> pulumi.Input[str]:
        """
        The load balancing algorithm to
        distribute traffic to the pool's members. Must be one of
        ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP, or SOURCE_IP_PORT (supported only
        in Octavia).
        """
        return pulumi.get(self, "lb_method")

    @lb_method.setter
    def lb_method(self, value: pulumi.Input[str]):
        pulumi.set(self, "lb_method", value)

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Input[str]:
        """
        The protocol - can either be TCP, HTTP, HTTPS, PROXY,
        UDP (supported only in Octavia), PROXYV2 (**Octavia minor version >= 2.22**)
        or SCTP (**Octavia minor version >= 2.23**). Changing this creates a new pool.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: pulumi.Input[str]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter(name="adminStateUp")
    def admin_state_up(self) -> Optional[pulumi.Input[bool]]:
        """
        The administrative state of the pool.
        A valid value is true (UP) or false (DOWN).
        """
        return pulumi.get(self, "admin_state_up")

    @admin_state_up.setter
    def admin_state_up(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "admin_state_up", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Human-readable description for the pool.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Listener on which the members of the pool
        will be associated with. Changing this creates a new pool.
        Note:  One of LoadbalancerID or ListenerID must be provided.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter(name="loadbalancerId")
    def loadbalancer_id(self) -> Optional[pulumi.Input[str]]:
        """
        The load balancer on which to provision this
        pool. Changing this creates a new pool.
        Note:  One of LoadbalancerID or ListenerID must be provided.
        """
        return pulumi.get(self, "loadbalancer_id")

    @loadbalancer_id.setter
    def loadbalancer_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "loadbalancer_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Human-readable name for the pool.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def persistence(self) -> Optional[pulumi.Input['PoolPersistenceArgs']]:
        """
        Omit this field to prevent session persistence.  Indicates
        whether connections in the same session will be processed by the same Pool
        member or not. Changing this creates a new pool.
        """
        return pulumi.get(self, "persistence")

    @persistence.setter
    def persistence(self, value: Optional[pulumi.Input['PoolPersistenceArgs']]):
        pulumi.set(self, "persistence", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to obtain the V2 Networking client.
        A Networking client is needed to create an . If omitted, the
        `region` argument of the provider is used. Changing this creates a new
        pool.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        Required for admins. The UUID of the tenant who owns
        the pool.  Only administrative users can specify a tenant UUID
        other than their own. Changing this creates a new pool.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


@pulumi.input_type
class _PoolState:
    def __init__(__self__, *,
                 admin_state_up: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 lb_method: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 loadbalancer_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 persistence: Optional[pulumi.Input['PoolPersistenceArgs']] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Pool resources.
        :param pulumi.Input[bool] admin_state_up: The administrative state of the pool.
               A valid value is true (UP) or false (DOWN).
        :param pulumi.Input[str] description: Human-readable description for the pool.
        :param pulumi.Input[str] lb_method: The load balancing algorithm to
               distribute traffic to the pool's members. Must be one of
               ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP, or SOURCE_IP_PORT (supported only
               in Octavia).
        :param pulumi.Input[str] listener_id: The Listener on which the members of the pool
               will be associated with. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] loadbalancer_id: The load balancer on which to provision this
               pool. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] name: Human-readable name for the pool.
        :param pulumi.Input['PoolPersistenceArgs'] persistence: Omit this field to prevent session persistence.  Indicates
               whether connections in the same session will be processed by the same Pool
               member or not. Changing this creates a new pool.
        :param pulumi.Input[str] protocol: The protocol - can either be TCP, HTTP, HTTPS, PROXY,
               UDP (supported only in Octavia), PROXYV2 (**Octavia minor version >= 2.22**)
               or SCTP (**Octavia minor version >= 2.23**). Changing this creates a new pool.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create an . If omitted, the
               `region` argument of the provider is used. Changing this creates a new
               pool.
        :param pulumi.Input[str] tenant_id: Required for admins. The UUID of the tenant who owns
               the pool.  Only administrative users can specify a tenant UUID
               other than their own. Changing this creates a new pool.
        """
        if admin_state_up is not None:
            pulumi.set(__self__, "admin_state_up", admin_state_up)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if lb_method is not None:
            pulumi.set(__self__, "lb_method", lb_method)
        if listener_id is not None:
            pulumi.set(__self__, "listener_id", listener_id)
        if loadbalancer_id is not None:
            pulumi.set(__self__, "loadbalancer_id", loadbalancer_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if persistence is not None:
            pulumi.set(__self__, "persistence", persistence)
        if protocol is not None:
            pulumi.set(__self__, "protocol", protocol)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="adminStateUp")
    def admin_state_up(self) -> Optional[pulumi.Input[bool]]:
        """
        The administrative state of the pool.
        A valid value is true (UP) or false (DOWN).
        """
        return pulumi.get(self, "admin_state_up")

    @admin_state_up.setter
    def admin_state_up(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "admin_state_up", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Human-readable description for the pool.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="lbMethod")
    def lb_method(self) -> Optional[pulumi.Input[str]]:
        """
        The load balancing algorithm to
        distribute traffic to the pool's members. Must be one of
        ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP, or SOURCE_IP_PORT (supported only
        in Octavia).
        """
        return pulumi.get(self, "lb_method")

    @lb_method.setter
    def lb_method(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lb_method", value)

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Listener on which the members of the pool
        will be associated with. Changing this creates a new pool.
        Note:  One of LoadbalancerID or ListenerID must be provided.
        """
        return pulumi.get(self, "listener_id")

    @listener_id.setter
    def listener_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "listener_id", value)

    @property
    @pulumi.getter(name="loadbalancerId")
    def loadbalancer_id(self) -> Optional[pulumi.Input[str]]:
        """
        The load balancer on which to provision this
        pool. Changing this creates a new pool.
        Note:  One of LoadbalancerID or ListenerID must be provided.
        """
        return pulumi.get(self, "loadbalancer_id")

    @loadbalancer_id.setter
    def loadbalancer_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "loadbalancer_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Human-readable name for the pool.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def persistence(self) -> Optional[pulumi.Input['PoolPersistenceArgs']]:
        """
        Omit this field to prevent session persistence.  Indicates
        whether connections in the same session will be processed by the same Pool
        member or not. Changing this creates a new pool.
        """
        return pulumi.get(self, "persistence")

    @persistence.setter
    def persistence(self, value: Optional[pulumi.Input['PoolPersistenceArgs']]):
        pulumi.set(self, "persistence", value)

    @property
    @pulumi.getter
    def protocol(self) -> Optional[pulumi.Input[str]]:
        """
        The protocol - can either be TCP, HTTP, HTTPS, PROXY,
        UDP (supported only in Octavia), PROXYV2 (**Octavia minor version >= 2.22**)
        or SCTP (**Octavia minor version >= 2.23**). Changing this creates a new pool.
        """
        return pulumi.get(self, "protocol")

    @protocol.setter
    def protocol(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "protocol", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to obtain the V2 Networking client.
        A Networking client is needed to create an . If omitted, the
        `region` argument of the provider is used. Changing this creates a new
        pool.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[pulumi.Input[str]]:
        """
        Required for admins. The UUID of the tenant who owns
        the pool.  Only administrative users can specify a tenant UUID
        other than their own. Changing this creates a new pool.
        """
        return pulumi.get(self, "tenant_id")

    @tenant_id.setter
    def tenant_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "tenant_id", value)


class Pool(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin_state_up: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 lb_method: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 loadbalancer_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 persistence: Optional[pulumi.Input[pulumi.InputType['PoolPersistenceArgs']]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a V2 pool resource within OpenStack.

        > **Note:** This resource has attributes that depend on octavia minor versions.
        Please ensure your Openstack cloud supports the required minor version.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_openstack as openstack

        pool1 = openstack.loadbalancer.Pool("pool_1",
            protocol="HTTP",
            lb_method="ROUND_ROBIN",
            listener_id="d9415786-5f1a-428b-b35f-2f1523e146d2",
            persistence=openstack.loadbalancer.PoolPersistenceArgs(
                type="APP_COOKIE",
                cookie_name="testCookie",
            ))
        ```

        ## Import

        Load Balancer Pool can be imported using the Pool ID, e.g.:

        ```sh
        $ pulumi import openstack:loadbalancer/pool:Pool pool_1 60ad9ee4-249a-4d60-a45b-aa60e046c513
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] admin_state_up: The administrative state of the pool.
               A valid value is true (UP) or false (DOWN).
        :param pulumi.Input[str] description: Human-readable description for the pool.
        :param pulumi.Input[str] lb_method: The load balancing algorithm to
               distribute traffic to the pool's members. Must be one of
               ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP, or SOURCE_IP_PORT (supported only
               in Octavia).
        :param pulumi.Input[str] listener_id: The Listener on which the members of the pool
               will be associated with. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] loadbalancer_id: The load balancer on which to provision this
               pool. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] name: Human-readable name for the pool.
        :param pulumi.Input[pulumi.InputType['PoolPersistenceArgs']] persistence: Omit this field to prevent session persistence.  Indicates
               whether connections in the same session will be processed by the same Pool
               member or not. Changing this creates a new pool.
        :param pulumi.Input[str] protocol: The protocol - can either be TCP, HTTP, HTTPS, PROXY,
               UDP (supported only in Octavia), PROXYV2 (**Octavia minor version >= 2.22**)
               or SCTP (**Octavia minor version >= 2.23**). Changing this creates a new pool.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create an . If omitted, the
               `region` argument of the provider is used. Changing this creates a new
               pool.
        :param pulumi.Input[str] tenant_id: Required for admins. The UUID of the tenant who owns
               the pool.  Only administrative users can specify a tenant UUID
               other than their own. Changing this creates a new pool.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PoolArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a V2 pool resource within OpenStack.

        > **Note:** This resource has attributes that depend on octavia minor versions.
        Please ensure your Openstack cloud supports the required minor version.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_openstack as openstack

        pool1 = openstack.loadbalancer.Pool("pool_1",
            protocol="HTTP",
            lb_method="ROUND_ROBIN",
            listener_id="d9415786-5f1a-428b-b35f-2f1523e146d2",
            persistence=openstack.loadbalancer.PoolPersistenceArgs(
                type="APP_COOKIE",
                cookie_name="testCookie",
            ))
        ```

        ## Import

        Load Balancer Pool can be imported using the Pool ID, e.g.:

        ```sh
        $ pulumi import openstack:loadbalancer/pool:Pool pool_1 60ad9ee4-249a-4d60-a45b-aa60e046c513
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
                 admin_state_up: Optional[pulumi.Input[bool]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 lb_method: Optional[pulumi.Input[str]] = None,
                 listener_id: Optional[pulumi.Input[str]] = None,
                 loadbalancer_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 persistence: Optional[pulumi.Input[pulumi.InputType['PoolPersistenceArgs']]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 tenant_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PoolArgs.__new__(PoolArgs)

            __props__.__dict__["admin_state_up"] = admin_state_up
            __props__.__dict__["description"] = description
            if lb_method is None and not opts.urn:
                raise TypeError("Missing required property 'lb_method'")
            __props__.__dict__["lb_method"] = lb_method
            __props__.__dict__["listener_id"] = listener_id
            __props__.__dict__["loadbalancer_id"] = loadbalancer_id
            __props__.__dict__["name"] = name
            __props__.__dict__["persistence"] = persistence
            if protocol is None and not opts.urn:
                raise TypeError("Missing required property 'protocol'")
            __props__.__dict__["protocol"] = protocol
            __props__.__dict__["region"] = region
            __props__.__dict__["tenant_id"] = tenant_id
        super(Pool, __self__).__init__(
            'openstack:loadbalancer/pool:Pool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            admin_state_up: Optional[pulumi.Input[bool]] = None,
            description: Optional[pulumi.Input[str]] = None,
            lb_method: Optional[pulumi.Input[str]] = None,
            listener_id: Optional[pulumi.Input[str]] = None,
            loadbalancer_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            persistence: Optional[pulumi.Input[pulumi.InputType['PoolPersistenceArgs']]] = None,
            protocol: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            tenant_id: Optional[pulumi.Input[str]] = None) -> 'Pool':
        """
        Get an existing Pool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] admin_state_up: The administrative state of the pool.
               A valid value is true (UP) or false (DOWN).
        :param pulumi.Input[str] description: Human-readable description for the pool.
        :param pulumi.Input[str] lb_method: The load balancing algorithm to
               distribute traffic to the pool's members. Must be one of
               ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP, or SOURCE_IP_PORT (supported only
               in Octavia).
        :param pulumi.Input[str] listener_id: The Listener on which the members of the pool
               will be associated with. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] loadbalancer_id: The load balancer on which to provision this
               pool. Changing this creates a new pool.
               Note:  One of LoadbalancerID or ListenerID must be provided.
        :param pulumi.Input[str] name: Human-readable name for the pool.
        :param pulumi.Input[pulumi.InputType['PoolPersistenceArgs']] persistence: Omit this field to prevent session persistence.  Indicates
               whether connections in the same session will be processed by the same Pool
               member or not. Changing this creates a new pool.
        :param pulumi.Input[str] protocol: The protocol - can either be TCP, HTTP, HTTPS, PROXY,
               UDP (supported only in Octavia), PROXYV2 (**Octavia minor version >= 2.22**)
               or SCTP (**Octavia minor version >= 2.23**). Changing this creates a new pool.
        :param pulumi.Input[str] region: The region in which to obtain the V2 Networking client.
               A Networking client is needed to create an . If omitted, the
               `region` argument of the provider is used. Changing this creates a new
               pool.
        :param pulumi.Input[str] tenant_id: Required for admins. The UUID of the tenant who owns
               the pool.  Only administrative users can specify a tenant UUID
               other than their own. Changing this creates a new pool.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PoolState.__new__(_PoolState)

        __props__.__dict__["admin_state_up"] = admin_state_up
        __props__.__dict__["description"] = description
        __props__.__dict__["lb_method"] = lb_method
        __props__.__dict__["listener_id"] = listener_id
        __props__.__dict__["loadbalancer_id"] = loadbalancer_id
        __props__.__dict__["name"] = name
        __props__.__dict__["persistence"] = persistence
        __props__.__dict__["protocol"] = protocol
        __props__.__dict__["region"] = region
        __props__.__dict__["tenant_id"] = tenant_id
        return Pool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="adminStateUp")
    def admin_state_up(self) -> pulumi.Output[Optional[bool]]:
        """
        The administrative state of the pool.
        A valid value is true (UP) or false (DOWN).
        """
        return pulumi.get(self, "admin_state_up")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Human-readable description for the pool.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="lbMethod")
    def lb_method(self) -> pulumi.Output[str]:
        """
        The load balancing algorithm to
        distribute traffic to the pool's members. Must be one of
        ROUND_ROBIN, LEAST_CONNECTIONS, SOURCE_IP, or SOURCE_IP_PORT (supported only
        in Octavia).
        """
        return pulumi.get(self, "lb_method")

    @property
    @pulumi.getter(name="listenerId")
    def listener_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Listener on which the members of the pool
        will be associated with. Changing this creates a new pool.
        Note:  One of LoadbalancerID or ListenerID must be provided.
        """
        return pulumi.get(self, "listener_id")

    @property
    @pulumi.getter(name="loadbalancerId")
    def loadbalancer_id(self) -> pulumi.Output[Optional[str]]:
        """
        The load balancer on which to provision this
        pool. Changing this creates a new pool.
        Note:  One of LoadbalancerID or ListenerID must be provided.
        """
        return pulumi.get(self, "loadbalancer_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Human-readable name for the pool.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def persistence(self) -> pulumi.Output['outputs.PoolPersistence']:
        """
        Omit this field to prevent session persistence.  Indicates
        whether connections in the same session will be processed by the same Pool
        member or not. Changing this creates a new pool.
        """
        return pulumi.get(self, "persistence")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        The protocol - can either be TCP, HTTP, HTTPS, PROXY,
        UDP (supported only in Octavia), PROXYV2 (**Octavia minor version >= 2.22**)
        or SCTP (**Octavia minor version >= 2.23**). Changing this creates a new pool.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region in which to obtain the V2 Networking client.
        A Networking client is needed to create an . If omitted, the
        `region` argument of the provider is used. Changing this creates a new
        pool.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[str]:
        """
        Required for admins. The UUID of the tenant who owns
        the pool.  Only administrative users can specify a tenant UUID
        other than their own. Changing this creates a new pool.
        """
        return pulumi.get(self, "tenant_id")

