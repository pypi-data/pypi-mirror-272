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

__all__ = [
    'GetUsbResult',
    'AwaitableGetUsbResult',
    'get_usb',
    'get_usb_output',
]

@pulumi.output_type
class GetUsbResult:
    """
    A collection of values returned by getUsb.
    """
    def __init__(__self__, comment=None, id=None, maps=None, name=None):
        if comment and not isinstance(comment, str):
            raise TypeError("Expected argument 'comment' to be a str")
        pulumi.set(__self__, "comment", comment)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if maps and not isinstance(maps, list):
            raise TypeError("Expected argument 'maps' to be a list")
        pulumi.set(__self__, "maps", maps)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def comment(self) -> str:
        """
        The comment of this USB hardware mapping.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The unique identifier of this USB hardware mapping data source.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def maps(self) -> Sequence['outputs.GetUsbMapResult']:
        """
        The actual map of devices for the hardware mapping.
        """
        return pulumi.get(self, "maps")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of this USB hardware mapping.
        """
        return pulumi.get(self, "name")


class AwaitableGetUsbResult(GetUsbResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUsbResult(
            comment=self.comment,
            id=self.id,
            maps=self.maps,
            name=self.name)


def get_usb(name: Optional[str] = None,
            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUsbResult:
    """
    Retrieves a USB hardware mapping from a Proxmox VE cluster.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    example = proxmoxve.Hardware.mapping.get_usb(name="example")
    pulumi.export("dataProxmoxVirtualEnvironmentHardwareMappingUsb", example)
    ```
    <!--End PulumiCodeChooser -->


    :param str name: The name of this USB hardware mapping.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('proxmoxve:Hardware/mapping/getUsb:getUsb', __args__, opts=opts, typ=GetUsbResult).value

    return AwaitableGetUsbResult(
        comment=pulumi.get(__ret__, 'comment'),
        id=pulumi.get(__ret__, 'id'),
        maps=pulumi.get(__ret__, 'maps'),
        name=pulumi.get(__ret__, 'name'))


@_utilities.lift_output_func(get_usb)
def get_usb_output(name: Optional[pulumi.Input[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUsbResult]:
    """
    Retrieves a USB hardware mapping from a Proxmox VE cluster.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    example = proxmoxve.Hardware.mapping.get_usb(name="example")
    pulumi.export("dataProxmoxVirtualEnvironmentHardwareMappingUsb", example)
    ```
    <!--End PulumiCodeChooser -->


    :param str name: The name of this USB hardware mapping.
    """
    ...
