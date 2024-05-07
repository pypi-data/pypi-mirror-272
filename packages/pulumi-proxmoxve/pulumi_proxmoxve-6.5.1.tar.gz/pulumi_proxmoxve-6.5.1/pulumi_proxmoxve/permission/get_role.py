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
    'GetRoleResult',
    'AwaitableGetRoleResult',
    'get_role',
    'get_role_output',
]

@pulumi.output_type
class GetRoleResult:
    """
    A collection of values returned by getRole.
    """
    def __init__(__self__, id=None, privileges=None, role_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if privileges and not isinstance(privileges, list):
            raise TypeError("Expected argument 'privileges' to be a list")
        pulumi.set(__self__, "privileges", privileges)
        if role_id and not isinstance(role_id, str):
            raise TypeError("Expected argument 'role_id' to be a str")
        pulumi.set(__self__, "role_id", role_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def privileges(self) -> Sequence[str]:
        """
        The role privileges
        """
        return pulumi.get(self, "privileges")

    @property
    @pulumi.getter(name="roleId")
    def role_id(self) -> str:
        return pulumi.get(self, "role_id")


class AwaitableGetRoleResult(GetRoleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoleResult(
            id=self.id,
            privileges=self.privileges,
            role_id=self.role_id)


def get_role(role_id: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRoleResult:
    """
    Retrieves information about a specific role.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    operations_role = proxmoxve.Permission.get_role(role_id="operations")
    ```
    <!--End PulumiCodeChooser -->


    :param str role_id: The role identifier.
    """
    __args__ = dict()
    __args__['roleId'] = role_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('proxmoxve:Permission/getRole:getRole', __args__, opts=opts, typ=GetRoleResult).value

    return AwaitableGetRoleResult(
        id=pulumi.get(__ret__, 'id'),
        privileges=pulumi.get(__ret__, 'privileges'),
        role_id=pulumi.get(__ret__, 'role_id'))


@_utilities.lift_output_func(get_role)
def get_role_output(role_id: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRoleResult]:
    """
    Retrieves information about a specific role.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    operations_role = proxmoxve.Permission.get_role(role_id="operations")
    ```
    <!--End PulumiCodeChooser -->


    :param str role_id: The role identifier.
    """
    ...
