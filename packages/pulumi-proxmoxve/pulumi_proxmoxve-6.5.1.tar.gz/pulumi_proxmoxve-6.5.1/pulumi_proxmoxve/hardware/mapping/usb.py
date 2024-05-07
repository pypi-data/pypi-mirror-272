# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['UsbArgs', 'Usb']

@pulumi.input_type
class UsbArgs:
    def __init__(__self__, *,
                 maps: pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]],
                 comment: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Usb resource.
        :param pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]] maps: The actual map of devices for the hardware mapping.
        :param pulumi.Input[str] comment: The comment of the mapped USB device.
        :param pulumi.Input[str] name: The name of this hardware mapping.
        """
        pulumi.set(__self__, "maps", maps)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def maps(self) -> pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]]:
        """
        The actual map of devices for the hardware mapping.
        """
        return pulumi.get(self, "maps")

    @maps.setter
    def maps(self, value: pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]]):
        pulumi.set(self, "maps", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        The comment of the mapped USB device.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of this hardware mapping.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _UsbState:
    def __init__(__self__, *,
                 comment: Optional[pulumi.Input[str]] = None,
                 maps: Optional[pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Usb resources.
        :param pulumi.Input[str] comment: The comment of the mapped USB device.
        :param pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]] maps: The actual map of devices for the hardware mapping.
        :param pulumi.Input[str] name: The name of this hardware mapping.
        """
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if maps is not None:
            pulumi.set(__self__, "maps", maps)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        The comment of the mapped USB device.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def maps(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]]]:
        """
        The actual map of devices for the hardware mapping.
        """
        return pulumi.get(self, "maps")

    @maps.setter
    def maps(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UsbMapArgs']]]]):
        pulumi.set(self, "maps", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of this hardware mapping.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class Usb(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 maps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UsbMapArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a USB hardware mapping in a Proxmox VE cluster.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        example = proxmoxve.hardware.mapping.Usb("example",
            comment="This is a comment",
            maps=[proxmoxve.hardware.mapping.UsbMapArgs(
                comment="This is a device specific comment",
                id="8087:0a2b",
                node="pve",
                path="1-8.2",
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        #!/usr/bin/env sh

        A USB hardware mapping can be imported using their name, e.g.:

        ```sh
        $ pulumi import proxmoxve:Hardware/mapping/usb:Usb example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: The comment of the mapped USB device.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UsbMapArgs']]]] maps: The actual map of devices for the hardware mapping.
        :param pulumi.Input[str] name: The name of this hardware mapping.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UsbArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a USB hardware mapping in a Proxmox VE cluster.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        example = proxmoxve.hardware.mapping.Usb("example",
            comment="This is a comment",
            maps=[proxmoxve.hardware.mapping.UsbMapArgs(
                comment="This is a device specific comment",
                id="8087:0a2b",
                node="pve",
                path="1-8.2",
            )])
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        #!/usr/bin/env sh

        A USB hardware mapping can be imported using their name, e.g.:

        ```sh
        $ pulumi import proxmoxve:Hardware/mapping/usb:Usb example example
        ```

        :param str resource_name: The name of the resource.
        :param UsbArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UsbArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 maps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UsbMapArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UsbArgs.__new__(UsbArgs)

            __props__.__dict__["comment"] = comment
            if maps is None and not opts.urn:
                raise TypeError("Missing required property 'maps'")
            __props__.__dict__["maps"] = maps
            __props__.__dict__["name"] = name
        super(Usb, __self__).__init__(
            'proxmoxve:Hardware/mapping/usb:Usb',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            comment: Optional[pulumi.Input[str]] = None,
            maps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UsbMapArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'Usb':
        """
        Get an existing Usb resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] comment: The comment of the mapped USB device.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UsbMapArgs']]]] maps: The actual map of devices for the hardware mapping.
        :param pulumi.Input[str] name: The name of this hardware mapping.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UsbState.__new__(_UsbState)

        __props__.__dict__["comment"] = comment
        __props__.__dict__["maps"] = maps
        __props__.__dict__["name"] = name
        return Usb(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        The comment of the mapped USB device.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def maps(self) -> pulumi.Output[Sequence['outputs.UsbMap']]:
        """
        The actual map of devices for the hardware mapping.
        """
        return pulumi.get(self, "maps")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of this hardware mapping.
        """
        return pulumi.get(self, "name")

