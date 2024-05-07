# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VolumeAttachArgs', 'VolumeAttach']

@pulumi.input_type
class VolumeAttachArgs:
    def __init__(__self__, *,
                 host_name: pulumi.Input[str],
                 volume_id: pulumi.Input[str],
                 attach_mode: Optional[pulumi.Input[str]] = None,
                 device: Optional[pulumi.Input[str]] = None,
                 initiator: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 multipath: Optional[pulumi.Input[bool]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 wwnn: Optional[pulumi.Input[str]] = None,
                 wwpns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a VolumeAttach resource.
        :param pulumi.Input[str] host_name: The host to attach the volume to.
        :param pulumi.Input[str] volume_id: The ID of the Volume to attach to an Instance.
        :param pulumi.Input[str] attach_mode: Specify whether to attach the volume as Read-Only
               (`ro`) or Read-Write (`rw`). Only values of `ro` and `rw` are accepted.
               If left unspecified, the Block Storage API will apply a default of `rw`.
        :param pulumi.Input[str] device: The device to tell the Block Storage service this
               volume will be attached as. This is purely for informational purposes.
               You can specify `auto` or a device such as `/dev/vdc`.
        :param pulumi.Input[str] initiator: The iSCSI initiator string to make the connection.
        :param pulumi.Input[str] ip_address: The IP address of the `host_name` above.
        :param pulumi.Input[bool] multipath: Whether to connect to this volume via multipath.
        :param pulumi.Input[str] os_type: The iSCSI initiator OS type.
        :param pulumi.Input[str] platform: The iSCSI initiator platform.
        :param pulumi.Input[str] region: The region in which to obtain the V3 Block Storage
               client. A Block Storage client is needed to create a volume attachment.
               If omitted, the `region` argument of the provider is used. Changing this
               creates a new volume attachment.
        :param pulumi.Input[str] wwnn: A wwnn name. Used for Fibre Channel connections.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] wwpns: An array of wwpn strings. Used for Fibre Channel
               connections.
        """
        pulumi.set(__self__, "host_name", host_name)
        pulumi.set(__self__, "volume_id", volume_id)
        if attach_mode is not None:
            pulumi.set(__self__, "attach_mode", attach_mode)
        if device is not None:
            pulumi.set(__self__, "device", device)
        if initiator is not None:
            pulumi.set(__self__, "initiator", initiator)
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if multipath is not None:
            pulumi.set(__self__, "multipath", multipath)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if wwnn is not None:
            pulumi.set(__self__, "wwnn", wwnn)
        if wwpns is not None:
            pulumi.set(__self__, "wwpns", wwpns)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Input[str]:
        """
        The host to attach the volume to.
        """
        return pulumi.get(self, "host_name")

    @host_name.setter
    def host_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "host_name", value)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> pulumi.Input[str]:
        """
        The ID of the Volume to attach to an Instance.
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "volume_id", value)

    @property
    @pulumi.getter(name="attachMode")
    def attach_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Specify whether to attach the volume as Read-Only
        (`ro`) or Read-Write (`rw`). Only values of `ro` and `rw` are accepted.
        If left unspecified, the Block Storage API will apply a default of `rw`.
        """
        return pulumi.get(self, "attach_mode")

    @attach_mode.setter
    def attach_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attach_mode", value)

    @property
    @pulumi.getter
    def device(self) -> Optional[pulumi.Input[str]]:
        """
        The device to tell the Block Storage service this
        volume will be attached as. This is purely for informational purposes.
        You can specify `auto` or a device such as `/dev/vdc`.
        """
        return pulumi.get(self, "device")

    @device.setter
    def device(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device", value)

    @property
    @pulumi.getter
    def initiator(self) -> Optional[pulumi.Input[str]]:
        """
        The iSCSI initiator string to make the connection.
        """
        return pulumi.get(self, "initiator")

    @initiator.setter
    def initiator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "initiator", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the `host_name` above.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter
    def multipath(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to connect to this volume via multipath.
        """
        return pulumi.get(self, "multipath")

    @multipath.setter
    def multipath(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "multipath", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[str]]:
        """
        The iSCSI initiator OS type.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input[str]]:
        """
        The iSCSI initiator platform.
        """
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "platform", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to obtain the V3 Block Storage
        client. A Block Storage client is needed to create a volume attachment.
        If omitted, the `region` argument of the provider is used. Changing this
        creates a new volume attachment.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def wwnn(self) -> Optional[pulumi.Input[str]]:
        """
        A wwnn name. Used for Fibre Channel connections.
        """
        return pulumi.get(self, "wwnn")

    @wwnn.setter
    def wwnn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "wwnn", value)

    @property
    @pulumi.getter
    def wwpns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of wwpn strings. Used for Fibre Channel
        connections.
        """
        return pulumi.get(self, "wwpns")

    @wwpns.setter
    def wwpns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "wwpns", value)


@pulumi.input_type
class _VolumeAttachState:
    def __init__(__self__, *,
                 attach_mode: Optional[pulumi.Input[str]] = None,
                 data: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 device: Optional[pulumi.Input[str]] = None,
                 driver_volume_type: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 initiator: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 mount_point_base: Optional[pulumi.Input[str]] = None,
                 multipath: Optional[pulumi.Input[bool]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 wwnn: Optional[pulumi.Input[str]] = None,
                 wwpns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering VolumeAttach resources.
        :param pulumi.Input[str] attach_mode: Specify whether to attach the volume as Read-Only
               (`ro`) or Read-Write (`rw`). Only values of `ro` and `rw` are accepted.
               If left unspecified, the Block Storage API will apply a default of `rw`.
        :param pulumi.Input[Mapping[str, Any]] data: This is a map of key/value pairs that contain the connection
               information. You will want to pass this information to a provisioner
               script to finalize the connection. See below for more information.
        :param pulumi.Input[str] device: The device to tell the Block Storage service this
               volume will be attached as. This is purely for informational purposes.
               You can specify `auto` or a device such as `/dev/vdc`.
        :param pulumi.Input[str] driver_volume_type: The storage driver that the volume is based on.
        :param pulumi.Input[str] host_name: The host to attach the volume to.
        :param pulumi.Input[str] initiator: The iSCSI initiator string to make the connection.
        :param pulumi.Input[str] ip_address: The IP address of the `host_name` above.
        :param pulumi.Input[str] mount_point_base: A mount point base name for shared storage.
        :param pulumi.Input[bool] multipath: Whether to connect to this volume via multipath.
        :param pulumi.Input[str] os_type: The iSCSI initiator OS type.
        :param pulumi.Input[str] platform: The iSCSI initiator platform.
        :param pulumi.Input[str] region: The region in which to obtain the V3 Block Storage
               client. A Block Storage client is needed to create a volume attachment.
               If omitted, the `region` argument of the provider is used. Changing this
               creates a new volume attachment.
        :param pulumi.Input[str] volume_id: The ID of the Volume to attach to an Instance.
        :param pulumi.Input[str] wwnn: A wwnn name. Used for Fibre Channel connections.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] wwpns: An array of wwpn strings. Used for Fibre Channel
               connections.
        """
        if attach_mode is not None:
            pulumi.set(__self__, "attach_mode", attach_mode)
        if data is not None:
            pulumi.set(__self__, "data", data)
        if device is not None:
            pulumi.set(__self__, "device", device)
        if driver_volume_type is not None:
            pulumi.set(__self__, "driver_volume_type", driver_volume_type)
        if host_name is not None:
            pulumi.set(__self__, "host_name", host_name)
        if initiator is not None:
            pulumi.set(__self__, "initiator", initiator)
        if ip_address is not None:
            pulumi.set(__self__, "ip_address", ip_address)
        if mount_point_base is not None:
            pulumi.set(__self__, "mount_point_base", mount_point_base)
        if multipath is not None:
            pulumi.set(__self__, "multipath", multipath)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if volume_id is not None:
            pulumi.set(__self__, "volume_id", volume_id)
        if wwnn is not None:
            pulumi.set(__self__, "wwnn", wwnn)
        if wwpns is not None:
            pulumi.set(__self__, "wwpns", wwpns)

    @property
    @pulumi.getter(name="attachMode")
    def attach_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Specify whether to attach the volume as Read-Only
        (`ro`) or Read-Write (`rw`). Only values of `ro` and `rw` are accepted.
        If left unspecified, the Block Storage API will apply a default of `rw`.
        """
        return pulumi.get(self, "attach_mode")

    @attach_mode.setter
    def attach_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attach_mode", value)

    @property
    @pulumi.getter
    def data(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        This is a map of key/value pairs that contain the connection
        information. You will want to pass this information to a provisioner
        script to finalize the connection. See below for more information.
        """
        return pulumi.get(self, "data")

    @data.setter
    def data(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "data", value)

    @property
    @pulumi.getter
    def device(self) -> Optional[pulumi.Input[str]]:
        """
        The device to tell the Block Storage service this
        volume will be attached as. This is purely for informational purposes.
        You can specify `auto` or a device such as `/dev/vdc`.
        """
        return pulumi.get(self, "device")

    @device.setter
    def device(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "device", value)

    @property
    @pulumi.getter(name="driverVolumeType")
    def driver_volume_type(self) -> Optional[pulumi.Input[str]]:
        """
        The storage driver that the volume is based on.
        """
        return pulumi.get(self, "driver_volume_type")

    @driver_volume_type.setter
    def driver_volume_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "driver_volume_type", value)

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> Optional[pulumi.Input[str]]:
        """
        The host to attach the volume to.
        """
        return pulumi.get(self, "host_name")

    @host_name.setter
    def host_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host_name", value)

    @property
    @pulumi.getter
    def initiator(self) -> Optional[pulumi.Input[str]]:
        """
        The iSCSI initiator string to make the connection.
        """
        return pulumi.get(self, "initiator")

    @initiator.setter
    def initiator(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "initiator", value)

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IP address of the `host_name` above.
        """
        return pulumi.get(self, "ip_address")

    @ip_address.setter
    def ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ip_address", value)

    @property
    @pulumi.getter(name="mountPointBase")
    def mount_point_base(self) -> Optional[pulumi.Input[str]]:
        """
        A mount point base name for shared storage.
        """
        return pulumi.get(self, "mount_point_base")

    @mount_point_base.setter
    def mount_point_base(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mount_point_base", value)

    @property
    @pulumi.getter
    def multipath(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to connect to this volume via multipath.
        """
        return pulumi.get(self, "multipath")

    @multipath.setter
    def multipath(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "multipath", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[str]]:
        """
        The iSCSI initiator OS type.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input[str]]:
        """
        The iSCSI initiator platform.
        """
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "platform", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to obtain the V3 Block Storage
        client. A Block Storage client is needed to create a volume attachment.
        If omitted, the `region` argument of the provider is used. Changing this
        creates a new volume attachment.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Volume to attach to an Instance.
        """
        return pulumi.get(self, "volume_id")

    @volume_id.setter
    def volume_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "volume_id", value)

    @property
    @pulumi.getter
    def wwnn(self) -> Optional[pulumi.Input[str]]:
        """
        A wwnn name. Used for Fibre Channel connections.
        """
        return pulumi.get(self, "wwnn")

    @wwnn.setter
    def wwnn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "wwnn", value)

    @property
    @pulumi.getter
    def wwpns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of wwpn strings. Used for Fibre Channel
        connections.
        """
        return pulumi.get(self, "wwpns")

    @wwpns.setter
    def wwpns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "wwpns", value)


class VolumeAttach(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attach_mode: Optional[pulumi.Input[str]] = None,
                 device: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 initiator: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 multipath: Optional[pulumi.Input[bool]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 wwnn: Optional[pulumi.Input[str]] = None,
                 wwpns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        > **Note:** This resource usually requires admin privileges.

        > **Note:** This resource does not actually attach a volume to an instance.
        Please use the `compute.VolumeAttach` resource for that.

        > **Note:** All arguments including the `data` computed attribute will be
        stored in the raw state as plain-text. Read more about sensitive data in
        state.

        Creates a general purpose attachment connection to a Block
        Storage volume using the OpenStack Block Storage (Cinder) v3 API.

        Depending on your Block Storage service configuration, this
        resource can assist in attaching a volume to a non-OpenStack resource
        such as a bare-metal server or a remote virtual machine in a
        different cloud provider.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_openstack as openstack

        volume1 = openstack.blockstorage.Volume("volume_1",
            name="volume_1",
            size=1)
        va1 = openstack.blockstorage.VolumeAttach("va_1",
            volume_id=volume1.id,
            device="auto",
            host_name="devstack",
            ip_address="192.168.255.10",
            initiator="iqn.1993-08.org.debian:01:e9861fb1859",
            os_type="linux2",
            platform="x86_64")
        ```

        ## Volume Connection Data

        Upon creation of this resource, a `data` exported attribute will be available.
        This attribute is a set of key/value pairs that contains the information
        required to complete the block storage connection.

        As an example, creating an iSCSI-based volume will return the following:

        This information can then be fed into a provisioner or a template shell script,
        where the final result would look something like:

        The contents of `data` will vary from each Block Storage service. You must have
        a good understanding of how the service is configured and how to make the
        appropriate final connection. However, if used correctly, this has the
        flexibility to be able to attach OpenStack Block Storage volumes to
        non-OpenStack resources.

        ## Import

        It is not possible to import this resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attach_mode: Specify whether to attach the volume as Read-Only
               (`ro`) or Read-Write (`rw`). Only values of `ro` and `rw` are accepted.
               If left unspecified, the Block Storage API will apply a default of `rw`.
        :param pulumi.Input[str] device: The device to tell the Block Storage service this
               volume will be attached as. This is purely for informational purposes.
               You can specify `auto` or a device such as `/dev/vdc`.
        :param pulumi.Input[str] host_name: The host to attach the volume to.
        :param pulumi.Input[str] initiator: The iSCSI initiator string to make the connection.
        :param pulumi.Input[str] ip_address: The IP address of the `host_name` above.
        :param pulumi.Input[bool] multipath: Whether to connect to this volume via multipath.
        :param pulumi.Input[str] os_type: The iSCSI initiator OS type.
        :param pulumi.Input[str] platform: The iSCSI initiator platform.
        :param pulumi.Input[str] region: The region in which to obtain the V3 Block Storage
               client. A Block Storage client is needed to create a volume attachment.
               If omitted, the `region` argument of the provider is used. Changing this
               creates a new volume attachment.
        :param pulumi.Input[str] volume_id: The ID of the Volume to attach to an Instance.
        :param pulumi.Input[str] wwnn: A wwnn name. Used for Fibre Channel connections.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] wwpns: An array of wwpn strings. Used for Fibre Channel
               connections.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VolumeAttachArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        > **Note:** This resource usually requires admin privileges.

        > **Note:** This resource does not actually attach a volume to an instance.
        Please use the `compute.VolumeAttach` resource for that.

        > **Note:** All arguments including the `data` computed attribute will be
        stored in the raw state as plain-text. Read more about sensitive data in
        state.

        Creates a general purpose attachment connection to a Block
        Storage volume using the OpenStack Block Storage (Cinder) v3 API.

        Depending on your Block Storage service configuration, this
        resource can assist in attaching a volume to a non-OpenStack resource
        such as a bare-metal server or a remote virtual machine in a
        different cloud provider.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_openstack as openstack

        volume1 = openstack.blockstorage.Volume("volume_1",
            name="volume_1",
            size=1)
        va1 = openstack.blockstorage.VolumeAttach("va_1",
            volume_id=volume1.id,
            device="auto",
            host_name="devstack",
            ip_address="192.168.255.10",
            initiator="iqn.1993-08.org.debian:01:e9861fb1859",
            os_type="linux2",
            platform="x86_64")
        ```

        ## Volume Connection Data

        Upon creation of this resource, a `data` exported attribute will be available.
        This attribute is a set of key/value pairs that contains the information
        required to complete the block storage connection.

        As an example, creating an iSCSI-based volume will return the following:

        This information can then be fed into a provisioner or a template shell script,
        where the final result would look something like:

        The contents of `data` will vary from each Block Storage service. You must have
        a good understanding of how the service is configured and how to make the
        appropriate final connection. However, if used correctly, this has the
        flexibility to be able to attach OpenStack Block Storage volumes to
        non-OpenStack resources.

        ## Import

        It is not possible to import this resource.

        :param str resource_name: The name of the resource.
        :param VolumeAttachArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VolumeAttachArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attach_mode: Optional[pulumi.Input[str]] = None,
                 device: Optional[pulumi.Input[str]] = None,
                 host_name: Optional[pulumi.Input[str]] = None,
                 initiator: Optional[pulumi.Input[str]] = None,
                 ip_address: Optional[pulumi.Input[str]] = None,
                 multipath: Optional[pulumi.Input[bool]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 volume_id: Optional[pulumi.Input[str]] = None,
                 wwnn: Optional[pulumi.Input[str]] = None,
                 wwpns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VolumeAttachArgs.__new__(VolumeAttachArgs)

            __props__.__dict__["attach_mode"] = attach_mode
            __props__.__dict__["device"] = device
            if host_name is None and not opts.urn:
                raise TypeError("Missing required property 'host_name'")
            __props__.__dict__["host_name"] = host_name
            __props__.__dict__["initiator"] = initiator
            __props__.__dict__["ip_address"] = ip_address
            __props__.__dict__["multipath"] = multipath
            __props__.__dict__["os_type"] = os_type
            __props__.__dict__["platform"] = platform
            __props__.__dict__["region"] = region
            if volume_id is None and not opts.urn:
                raise TypeError("Missing required property 'volume_id'")
            __props__.__dict__["volume_id"] = volume_id
            __props__.__dict__["wwnn"] = wwnn
            __props__.__dict__["wwpns"] = wwpns
            __props__.__dict__["data"] = None
            __props__.__dict__["driver_volume_type"] = None
            __props__.__dict__["mount_point_base"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["data"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(VolumeAttach, __self__).__init__(
            'openstack:blockstorage/volumeAttach:VolumeAttach',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attach_mode: Optional[pulumi.Input[str]] = None,
            data: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            device: Optional[pulumi.Input[str]] = None,
            driver_volume_type: Optional[pulumi.Input[str]] = None,
            host_name: Optional[pulumi.Input[str]] = None,
            initiator: Optional[pulumi.Input[str]] = None,
            ip_address: Optional[pulumi.Input[str]] = None,
            mount_point_base: Optional[pulumi.Input[str]] = None,
            multipath: Optional[pulumi.Input[bool]] = None,
            os_type: Optional[pulumi.Input[str]] = None,
            platform: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None,
            volume_id: Optional[pulumi.Input[str]] = None,
            wwnn: Optional[pulumi.Input[str]] = None,
            wwpns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'VolumeAttach':
        """
        Get an existing VolumeAttach resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attach_mode: Specify whether to attach the volume as Read-Only
               (`ro`) or Read-Write (`rw`). Only values of `ro` and `rw` are accepted.
               If left unspecified, the Block Storage API will apply a default of `rw`.
        :param pulumi.Input[Mapping[str, Any]] data: This is a map of key/value pairs that contain the connection
               information. You will want to pass this information to a provisioner
               script to finalize the connection. See below for more information.
        :param pulumi.Input[str] device: The device to tell the Block Storage service this
               volume will be attached as. This is purely for informational purposes.
               You can specify `auto` or a device such as `/dev/vdc`.
        :param pulumi.Input[str] driver_volume_type: The storage driver that the volume is based on.
        :param pulumi.Input[str] host_name: The host to attach the volume to.
        :param pulumi.Input[str] initiator: The iSCSI initiator string to make the connection.
        :param pulumi.Input[str] ip_address: The IP address of the `host_name` above.
        :param pulumi.Input[str] mount_point_base: A mount point base name for shared storage.
        :param pulumi.Input[bool] multipath: Whether to connect to this volume via multipath.
        :param pulumi.Input[str] os_type: The iSCSI initiator OS type.
        :param pulumi.Input[str] platform: The iSCSI initiator platform.
        :param pulumi.Input[str] region: The region in which to obtain the V3 Block Storage
               client. A Block Storage client is needed to create a volume attachment.
               If omitted, the `region` argument of the provider is used. Changing this
               creates a new volume attachment.
        :param pulumi.Input[str] volume_id: The ID of the Volume to attach to an Instance.
        :param pulumi.Input[str] wwnn: A wwnn name. Used for Fibre Channel connections.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] wwpns: An array of wwpn strings. Used for Fibre Channel
               connections.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VolumeAttachState.__new__(_VolumeAttachState)

        __props__.__dict__["attach_mode"] = attach_mode
        __props__.__dict__["data"] = data
        __props__.__dict__["device"] = device
        __props__.__dict__["driver_volume_type"] = driver_volume_type
        __props__.__dict__["host_name"] = host_name
        __props__.__dict__["initiator"] = initiator
        __props__.__dict__["ip_address"] = ip_address
        __props__.__dict__["mount_point_base"] = mount_point_base
        __props__.__dict__["multipath"] = multipath
        __props__.__dict__["os_type"] = os_type
        __props__.__dict__["platform"] = platform
        __props__.__dict__["region"] = region
        __props__.__dict__["volume_id"] = volume_id
        __props__.__dict__["wwnn"] = wwnn
        __props__.__dict__["wwpns"] = wwpns
        return VolumeAttach(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachMode")
    def attach_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Specify whether to attach the volume as Read-Only
        (`ro`) or Read-Write (`rw`). Only values of `ro` and `rw` are accepted.
        If left unspecified, the Block Storage API will apply a default of `rw`.
        """
        return pulumi.get(self, "attach_mode")

    @property
    @pulumi.getter
    def data(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        This is a map of key/value pairs that contain the connection
        information. You will want to pass this information to a provisioner
        script to finalize the connection. See below for more information.
        """
        return pulumi.get(self, "data")

    @property
    @pulumi.getter
    def device(self) -> pulumi.Output[Optional[str]]:
        """
        The device to tell the Block Storage service this
        volume will be attached as. This is purely for informational purposes.
        You can specify `auto` or a device such as `/dev/vdc`.
        """
        return pulumi.get(self, "device")

    @property
    @pulumi.getter(name="driverVolumeType")
    def driver_volume_type(self) -> pulumi.Output[str]:
        """
        The storage driver that the volume is based on.
        """
        return pulumi.get(self, "driver_volume_type")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        The host to attach the volume to.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter
    def initiator(self) -> pulumi.Output[Optional[str]]:
        """
        The iSCSI initiator string to make the connection.
        """
        return pulumi.get(self, "initiator")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[Optional[str]]:
        """
        The IP address of the `host_name` above.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter(name="mountPointBase")
    def mount_point_base(self) -> pulumi.Output[str]:
        """
        A mount point base name for shared storage.
        """
        return pulumi.get(self, "mount_point_base")

    @property
    @pulumi.getter
    def multipath(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to connect to this volume via multipath.
        """
        return pulumi.get(self, "multipath")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[Optional[str]]:
        """
        The iSCSI initiator OS type.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter
    def platform(self) -> pulumi.Output[Optional[str]]:
        """
        The iSCSI initiator platform.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region in which to obtain the V3 Block Storage
        client. A Block Storage client is needed to create a volume attachment.
        If omitted, the `region` argument of the provider is used. Changing this
        creates a new volume attachment.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> pulumi.Output[str]:
        """
        The ID of the Volume to attach to an Instance.
        """
        return pulumi.get(self, "volume_id")

    @property
    @pulumi.getter
    def wwnn(self) -> pulumi.Output[Optional[str]]:
        """
        A wwnn name. Used for Fibre Channel connections.
        """
        return pulumi.get(self, "wwnn")

    @property
    @pulumi.getter
    def wwpns(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        An array of wwpn strings. Used for Fibre Channel
        connections.
        """
        return pulumi.get(self, "wwpns")

