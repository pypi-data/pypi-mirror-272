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
    'GetPoolsResult',
    'AwaitableGetPoolsResult',
    'get_pools',
    'get_pools_output',
]

@pulumi.output_type
class GetPoolsResult:
    """
    A collection of values returned by getPools.
    """
    def __init__(__self__, id=None, pool_ids=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if pool_ids and not isinstance(pool_ids, list):
            raise TypeError("Expected argument 'pool_ids' to be a list")
        pulumi.set(__self__, "pool_ids", pool_ids)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="poolIds")
    def pool_ids(self) -> Sequence[str]:
        """
        The pool identifiers.
        """
        return pulumi.get(self, "pool_ids")


class AwaitableGetPoolsResult(GetPoolsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPoolsResult(
            id=self.id,
            pool_ids=self.pool_ids)


def get_pools(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPoolsResult:
    """
    Retrieves the identifiers for all the available resource pools.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    available_pools = proxmoxve.Permission.get_pools()
    ```
    <!--End PulumiCodeChooser -->
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('proxmoxve:Permission/getPools:getPools', __args__, opts=opts, typ=GetPoolsResult).value

    return AwaitableGetPoolsResult(
        id=pulumi.get(__ret__, 'id'),
        pool_ids=pulumi.get(__ret__, 'pool_ids'))


@_utilities.lift_output_func(get_pools)
def get_pools_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPoolsResult]:
    """
    Retrieves the identifiers for all the available resource pools.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    available_pools = proxmoxve.Permission.get_pools()
    ```
    <!--End PulumiCodeChooser -->
    """
    ...
