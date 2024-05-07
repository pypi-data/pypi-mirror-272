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
    'GetDatastoresResult',
    'AwaitableGetDatastoresResult',
    'get_datastores',
    'get_datastores_output',
]

@pulumi.output_type
class GetDatastoresResult:
    """
    A collection of values returned by getDatastores.
    """
    def __init__(__self__, actives=None, content_types=None, datastore_ids=None, enableds=None, id=None, node_name=None, shareds=None, space_availables=None, space_totals=None, space_useds=None, types=None):
        if actives and not isinstance(actives, list):
            raise TypeError("Expected argument 'actives' to be a list")
        pulumi.set(__self__, "actives", actives)
        if content_types and not isinstance(content_types, list):
            raise TypeError("Expected argument 'content_types' to be a list")
        pulumi.set(__self__, "content_types", content_types)
        if datastore_ids and not isinstance(datastore_ids, list):
            raise TypeError("Expected argument 'datastore_ids' to be a list")
        pulumi.set(__self__, "datastore_ids", datastore_ids)
        if enableds and not isinstance(enableds, list):
            raise TypeError("Expected argument 'enableds' to be a list")
        pulumi.set(__self__, "enableds", enableds)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if node_name and not isinstance(node_name, str):
            raise TypeError("Expected argument 'node_name' to be a str")
        pulumi.set(__self__, "node_name", node_name)
        if shareds and not isinstance(shareds, list):
            raise TypeError("Expected argument 'shareds' to be a list")
        pulumi.set(__self__, "shareds", shareds)
        if space_availables and not isinstance(space_availables, list):
            raise TypeError("Expected argument 'space_availables' to be a list")
        pulumi.set(__self__, "space_availables", space_availables)
        if space_totals and not isinstance(space_totals, list):
            raise TypeError("Expected argument 'space_totals' to be a list")
        pulumi.set(__self__, "space_totals", space_totals)
        if space_useds and not isinstance(space_useds, list):
            raise TypeError("Expected argument 'space_useds' to be a list")
        pulumi.set(__self__, "space_useds", space_useds)
        if types and not isinstance(types, list):
            raise TypeError("Expected argument 'types' to be a list")
        pulumi.set(__self__, "types", types)

    @property
    @pulumi.getter
    def actives(self) -> Sequence[bool]:
        """
        Whether the datastore is active.
        """
        return pulumi.get(self, "actives")

    @property
    @pulumi.getter(name="contentTypes")
    def content_types(self) -> Sequence[Sequence[str]]:
        """
        The allowed content types.
        """
        return pulumi.get(self, "content_types")

    @property
    @pulumi.getter(name="datastoreIds")
    def datastore_ids(self) -> Sequence[str]:
        """
        The datastore identifiers.
        """
        return pulumi.get(self, "datastore_ids")

    @property
    @pulumi.getter
    def enableds(self) -> Sequence[bool]:
        """
        Whether the datastore is enabled.
        """
        return pulumi.get(self, "enableds")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="nodeName")
    def node_name(self) -> str:
        return pulumi.get(self, "node_name")

    @property
    @pulumi.getter
    def shareds(self) -> Sequence[bool]:
        """
        Whether the datastore is shared.
        """
        return pulumi.get(self, "shareds")

    @property
    @pulumi.getter(name="spaceAvailables")
    def space_availables(self) -> Sequence[int]:
        """
        The available space in bytes.
        """
        return pulumi.get(self, "space_availables")

    @property
    @pulumi.getter(name="spaceTotals")
    def space_totals(self) -> Sequence[int]:
        """
        The total space in bytes.
        """
        return pulumi.get(self, "space_totals")

    @property
    @pulumi.getter(name="spaceUseds")
    def space_useds(self) -> Sequence[int]:
        """
        The used space in bytes.
        """
        return pulumi.get(self, "space_useds")

    @property
    @pulumi.getter
    def types(self) -> Sequence[str]:
        """
        The storage types.
        """
        return pulumi.get(self, "types")


class AwaitableGetDatastoresResult(GetDatastoresResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDatastoresResult(
            actives=self.actives,
            content_types=self.content_types,
            datastore_ids=self.datastore_ids,
            enableds=self.enableds,
            id=self.id,
            node_name=self.node_name,
            shareds=self.shareds,
            space_availables=self.space_availables,
            space_totals=self.space_totals,
            space_useds=self.space_useds,
            types=self.types)


def get_datastores(node_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDatastoresResult:
    """
    Retrieves information about all the datastores available to a specific node.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    first_node = proxmoxve.Storage.get_datastores(node_name="first-node")
    ```
    <!--End PulumiCodeChooser -->


    :param str node_name: A node name.
    """
    __args__ = dict()
    __args__['nodeName'] = node_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('proxmoxve:Storage/getDatastores:getDatastores', __args__, opts=opts, typ=GetDatastoresResult).value

    return AwaitableGetDatastoresResult(
        actives=pulumi.get(__ret__, 'actives'),
        content_types=pulumi.get(__ret__, 'content_types'),
        datastore_ids=pulumi.get(__ret__, 'datastore_ids'),
        enableds=pulumi.get(__ret__, 'enableds'),
        id=pulumi.get(__ret__, 'id'),
        node_name=pulumi.get(__ret__, 'node_name'),
        shareds=pulumi.get(__ret__, 'shareds'),
        space_availables=pulumi.get(__ret__, 'space_availables'),
        space_totals=pulumi.get(__ret__, 'space_totals'),
        space_useds=pulumi.get(__ret__, 'space_useds'),
        types=pulumi.get(__ret__, 'types'))


@_utilities.lift_output_func(get_datastores)
def get_datastores_output(node_name: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDatastoresResult]:
    """
    Retrieves information about all the datastores available to a specific node.

    ## Example Usage

    <!--Start PulumiCodeChooser -->
    ```python
    import pulumi
    import pulumi_proxmoxve as proxmoxve

    first_node = proxmoxve.Storage.get_datastores(node_name="first-node")
    ```
    <!--End PulumiCodeChooser -->


    :param str node_name: A node name.
    """
    ...
