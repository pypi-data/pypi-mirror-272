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
from ._inputs import *

__all__ = ['HostsArgs', 'Hosts']

@pulumi.input_type
class HostsArgs:
    def __init__(__self__, *,
                 entry: pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]],
                 node_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a Hosts resource.
        :param pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]] entry: A host entry (multiple blocks supported).
        :param pulumi.Input[str] node_name: A node name.
        """
        pulumi.set(__self__, "entry", entry)
        pulumi.set(__self__, "node_name", node_name)

    @property
    @pulumi.getter
    def entry(self) -> pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]:
        """
        A host entry (multiple blocks supported).
        """
        return pulumi.get(self, "entry")

    @entry.setter
    def entry(self, value: pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]):
        pulumi.set(self, "entry", value)

    @property
    @pulumi.getter(name="nodeName")
    def node_name(self) -> pulumi.Input[str]:
        """
        A node name.
        """
        return pulumi.get(self, "node_name")

    @node_name.setter
    def node_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "node_name", value)


@pulumi.input_type
class _HostsState:
    def __init__(__self__, *,
                 addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 digest: Optional[pulumi.Input[str]] = None,
                 entries: Optional[pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]] = None,
                 entry: Optional[pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]] = None,
                 hostnames: Optional[pulumi.Input[Sequence[pulumi.Input[Sequence[pulumi.Input[str]]]]]] = None,
                 node_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Hosts resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] addresses: The IP addresses.
        :param pulumi.Input[str] digest: The SHA1 digest.
        :param pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]] entries: The host entries (conversion of `addresses` and `hostnames` into
               objects).
        :param pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]] entry: A host entry (multiple blocks supported).
        :param pulumi.Input[Sequence[pulumi.Input[Sequence[pulumi.Input[str]]]]] hostnames: The hostnames.
        :param pulumi.Input[str] node_name: A node name.
        """
        if addresses is not None:
            pulumi.set(__self__, "addresses", addresses)
        if digest is not None:
            pulumi.set(__self__, "digest", digest)
        if entries is not None:
            pulumi.set(__self__, "entries", entries)
        if entry is not None:
            pulumi.set(__self__, "entry", entry)
        if hostnames is not None:
            pulumi.set(__self__, "hostnames", hostnames)
        if node_name is not None:
            pulumi.set(__self__, "node_name", node_name)

    @property
    @pulumi.getter
    def addresses(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IP addresses.
        """
        return pulumi.get(self, "addresses")

    @addresses.setter
    def addresses(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "addresses", value)

    @property
    @pulumi.getter
    def digest(self) -> Optional[pulumi.Input[str]]:
        """
        The SHA1 digest.
        """
        return pulumi.get(self, "digest")

    @digest.setter
    def digest(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "digest", value)

    @property
    @pulumi.getter
    def entries(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]]:
        """
        The host entries (conversion of `addresses` and `hostnames` into
        objects).
        """
        return pulumi.get(self, "entries")

    @entries.setter
    def entries(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]]):
        pulumi.set(self, "entries", value)

    @property
    @pulumi.getter
    def entry(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]]:
        """
        A host entry (multiple blocks supported).
        """
        return pulumi.get(self, "entry")

    @entry.setter
    def entry(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['HostsEntryArgs']]]]):
        pulumi.set(self, "entry", value)

    @property
    @pulumi.getter
    def hostnames(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Sequence[pulumi.Input[str]]]]]]:
        """
        The hostnames.
        """
        return pulumi.get(self, "hostnames")

    @hostnames.setter
    def hostnames(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Sequence[pulumi.Input[str]]]]]]):
        pulumi.set(self, "hostnames", value)

    @property
    @pulumi.getter(name="nodeName")
    def node_name(self) -> Optional[pulumi.Input[str]]:
        """
        A node name.
        """
        return pulumi.get(self, "node_name")

    @node_name.setter
    def node_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node_name", value)


class Hosts(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 entry: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostsEntryArgs']]]]] = None,
                 node_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages the host entries on a specific node.

        ## Import

        Instances can be imported using the `node_name`, e.g.,

        bash

        ```sh
        $ pulumi import proxmoxve:index/hosts:Hosts first_node_host_entries first-node
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostsEntryArgs']]]] entry: A host entry (multiple blocks supported).
        :param pulumi.Input[str] node_name: A node name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HostsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the host entries on a specific node.

        ## Import

        Instances can be imported using the `node_name`, e.g.,

        bash

        ```sh
        $ pulumi import proxmoxve:index/hosts:Hosts first_node_host_entries first-node
        ```

        :param str resource_name: The name of the resource.
        :param HostsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HostsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 entry: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostsEntryArgs']]]]] = None,
                 node_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HostsArgs.__new__(HostsArgs)

            if entry is None and not opts.urn:
                raise TypeError("Missing required property 'entry'")
            __props__.__dict__["entry"] = entry
            if node_name is None and not opts.urn:
                raise TypeError("Missing required property 'node_name'")
            __props__.__dict__["node_name"] = node_name
            __props__.__dict__["addresses"] = None
            __props__.__dict__["digest"] = None
            __props__.__dict__["entries"] = None
            __props__.__dict__["hostnames"] = None
        super(Hosts, __self__).__init__(
            'proxmoxve:index/hosts:Hosts',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            addresses: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            digest: Optional[pulumi.Input[str]] = None,
            entries: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostsEntryArgs']]]]] = None,
            entry: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostsEntryArgs']]]]] = None,
            hostnames: Optional[pulumi.Input[Sequence[pulumi.Input[Sequence[pulumi.Input[str]]]]]] = None,
            node_name: Optional[pulumi.Input[str]] = None) -> 'Hosts':
        """
        Get an existing Hosts resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] addresses: The IP addresses.
        :param pulumi.Input[str] digest: The SHA1 digest.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostsEntryArgs']]]] entries: The host entries (conversion of `addresses` and `hostnames` into
               objects).
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['HostsEntryArgs']]]] entry: A host entry (multiple blocks supported).
        :param pulumi.Input[Sequence[pulumi.Input[Sequence[pulumi.Input[str]]]]] hostnames: The hostnames.
        :param pulumi.Input[str] node_name: A node name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HostsState.__new__(_HostsState)

        __props__.__dict__["addresses"] = addresses
        __props__.__dict__["digest"] = digest
        __props__.__dict__["entries"] = entries
        __props__.__dict__["entry"] = entry
        __props__.__dict__["hostnames"] = hostnames
        __props__.__dict__["node_name"] = node_name
        return Hosts(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def addresses(self) -> pulumi.Output[Sequence[str]]:
        """
        The IP addresses.
        """
        return pulumi.get(self, "addresses")

    @property
    @pulumi.getter
    def digest(self) -> pulumi.Output[str]:
        """
        The SHA1 digest.
        """
        return pulumi.get(self, "digest")

    @property
    @pulumi.getter
    def entries(self) -> pulumi.Output[Sequence['outputs.HostsEntry']]:
        """
        The host entries (conversion of `addresses` and `hostnames` into
        objects).
        """
        return pulumi.get(self, "entries")

    @property
    @pulumi.getter
    def entry(self) -> pulumi.Output[Sequence['outputs.HostsEntry']]:
        """
        A host entry (multiple blocks supported).
        """
        return pulumi.get(self, "entry")

    @property
    @pulumi.getter
    def hostnames(self) -> pulumi.Output[Sequence[Sequence[str]]]:
        """
        The hostnames.
        """
        return pulumi.get(self, "hostnames")

    @property
    @pulumi.getter(name="nodeName")
    def node_name(self) -> pulumi.Output[str]:
        """
        A node name.
        """
        return pulumi.get(self, "node_name")

