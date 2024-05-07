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
    'GetVersionResult',
    'AwaitableGetVersionResult',
    'get_version',
    'get_version_output',
]

@pulumi.output_type
class GetVersionResult:
    """
    A collection of values returned by getVersion.
    """
    def __init__(__self__, id=None, release=None, repository_id=None, version=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if release and not isinstance(release, str):
            raise TypeError("Expected argument 'release' to be a str")
        pulumi.set(__self__, "release", release)
        if repository_id and not isinstance(repository_id, str):
            raise TypeError("Expected argument 'repository_id' to be a str")
        pulumi.set(__self__, "repository_id", repository_id)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Placeholder identifier attribute.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def release(self) -> str:
        """
        The current Proxmox VE point release in `x.y` format.
        """
        return pulumi.get(self, "release")

    @property
    @pulumi.getter(name="repositoryId")
    def repository_id(self) -> str:
        """
        The short git revision from which this version was build.
        """
        return pulumi.get(self, "repository_id")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        The full pve-manager package version of this node.
        """
        return pulumi.get(self, "version")


class AwaitableGetVersionResult(GetVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVersionResult(
            id=self.id,
            release=self.release,
            repository_id=self.repository_id,
            version=self.version)


def get_version(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVersionResult:
    """
    Retrieves API version details.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    example = proxmoxve.Network.get_version()
    pulumi.export("dataProxmoxVirtualEnvironmentVersion", {
        "release": example.release,
        "repository_id": example.repository_id,
        "version": example.version,
    })
    ```
    <!--End PulumiCodeChooser -->
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('proxmoxve:Network/getVersion:getVersion', __args__, opts=opts, typ=GetVersionResult).value

    return AwaitableGetVersionResult(
        id=pulumi.get(__ret__, 'id'),
        release=pulumi.get(__ret__, 'release'),
        repository_id=pulumi.get(__ret__, 'repository_id'),
        version=pulumi.get(__ret__, 'version'))


@_utilities.lift_output_func(get_version)
def get_version_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVersionResult]:
    """
    Retrieves API version details.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    example = proxmoxve.Network.get_version()
    pulumi.export("dataProxmoxVirtualEnvironmentVersion", {
        "release": example.release,
        "repository_id": example.repository_id,
        "version": example.version,
    })
    ```
    <!--End PulumiCodeChooser -->
    """
    ...
