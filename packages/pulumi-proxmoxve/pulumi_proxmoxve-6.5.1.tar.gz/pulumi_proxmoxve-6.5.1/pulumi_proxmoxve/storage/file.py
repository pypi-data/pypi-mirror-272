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

__all__ = ['FileArgs', 'File']

@pulumi.input_type
class FileArgs:
    def __init__(__self__, *,
                 datastore_id: pulumi.Input[str],
                 node_name: pulumi.Input[str],
                 content_type: Optional[pulumi.Input[str]] = None,
                 overwrite: Optional[pulumi.Input[bool]] = None,
                 source_file: Optional[pulumi.Input['FileSourceFileArgs']] = None,
                 source_raw: Optional[pulumi.Input['FileSourceRawArgs']] = None,
                 timeout_upload: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a File resource.
        :param pulumi.Input[str] datastore_id: The datastore id.
        :param pulumi.Input[str] node_name: The node name.
        :param pulumi.Input[str] content_type: The content type. If not specified, the content
               type will be inferred from the file extension. Valid values are:
        :param pulumi.Input[bool] overwrite: Whether to overwrite an existing file (defaults to
               `true`).
        :param pulumi.Input['FileSourceFileArgs'] source_file: The source file (conflicts with `source_raw`),
               could be a local file or a URL. If the source file is a URL, the file will
               be downloaded and stored locally before uploading it to Proxmox VE.
        :param pulumi.Input['FileSourceRawArgs'] source_raw: The raw source (conflicts with `source_file`).
        :param pulumi.Input[int] timeout_upload: Timeout for uploading ISO/VSTMPL files in
               seconds (defaults to 1800).
        """
        pulumi.set(__self__, "datastore_id", datastore_id)
        pulumi.set(__self__, "node_name", node_name)
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if overwrite is not None:
            pulumi.set(__self__, "overwrite", overwrite)
        if source_file is not None:
            pulumi.set(__self__, "source_file", source_file)
        if source_raw is not None:
            pulumi.set(__self__, "source_raw", source_raw)
        if timeout_upload is not None:
            pulumi.set(__self__, "timeout_upload", timeout_upload)

    @property
    @pulumi.getter(name="datastoreId")
    def datastore_id(self) -> pulumi.Input[str]:
        """
        The datastore id.
        """
        return pulumi.get(self, "datastore_id")

    @datastore_id.setter
    def datastore_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "datastore_id", value)

    @property
    @pulumi.getter(name="nodeName")
    def node_name(self) -> pulumi.Input[str]:
        """
        The node name.
        """
        return pulumi.get(self, "node_name")

    @node_name.setter
    def node_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "node_name", value)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        """
        The content type. If not specified, the content
        type will be inferred from the file extension. Valid values are:
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter
    def overwrite(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to overwrite an existing file (defaults to
        `true`).
        """
        return pulumi.get(self, "overwrite")

    @overwrite.setter
    def overwrite(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "overwrite", value)

    @property
    @pulumi.getter(name="sourceFile")
    def source_file(self) -> Optional[pulumi.Input['FileSourceFileArgs']]:
        """
        The source file (conflicts with `source_raw`),
        could be a local file or a URL. If the source file is a URL, the file will
        be downloaded and stored locally before uploading it to Proxmox VE.
        """
        return pulumi.get(self, "source_file")

    @source_file.setter
    def source_file(self, value: Optional[pulumi.Input['FileSourceFileArgs']]):
        pulumi.set(self, "source_file", value)

    @property
    @pulumi.getter(name="sourceRaw")
    def source_raw(self) -> Optional[pulumi.Input['FileSourceRawArgs']]:
        """
        The raw source (conflicts with `source_file`).
        """
        return pulumi.get(self, "source_raw")

    @source_raw.setter
    def source_raw(self, value: Optional[pulumi.Input['FileSourceRawArgs']]):
        pulumi.set(self, "source_raw", value)

    @property
    @pulumi.getter(name="timeoutUpload")
    def timeout_upload(self) -> Optional[pulumi.Input[int]]:
        """
        Timeout for uploading ISO/VSTMPL files in
        seconds (defaults to 1800).
        """
        return pulumi.get(self, "timeout_upload")

    @timeout_upload.setter
    def timeout_upload(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_upload", value)


@pulumi.input_type
class _FileState:
    def __init__(__self__, *,
                 content_type: Optional[pulumi.Input[str]] = None,
                 datastore_id: Optional[pulumi.Input[str]] = None,
                 file_modification_date: Optional[pulumi.Input[str]] = None,
                 file_name: Optional[pulumi.Input[str]] = None,
                 file_size: Optional[pulumi.Input[int]] = None,
                 file_tag: Optional[pulumi.Input[str]] = None,
                 node_name: Optional[pulumi.Input[str]] = None,
                 overwrite: Optional[pulumi.Input[bool]] = None,
                 source_file: Optional[pulumi.Input['FileSourceFileArgs']] = None,
                 source_raw: Optional[pulumi.Input['FileSourceRawArgs']] = None,
                 timeout_upload: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering File resources.
        :param pulumi.Input[str] content_type: The content type. If not specified, the content
               type will be inferred from the file extension. Valid values are:
        :param pulumi.Input[str] datastore_id: The datastore id.
        :param pulumi.Input[str] file_modification_date: The file modification date (RFC 3339).
        :param pulumi.Input[str] file_name: The file name.
        :param pulumi.Input[int] file_size: The file size in bytes.
        :param pulumi.Input[str] file_tag: The file tag.
        :param pulumi.Input[str] node_name: The node name.
        :param pulumi.Input[bool] overwrite: Whether to overwrite an existing file (defaults to
               `true`).
        :param pulumi.Input['FileSourceFileArgs'] source_file: The source file (conflicts with `source_raw`),
               could be a local file or a URL. If the source file is a URL, the file will
               be downloaded and stored locally before uploading it to Proxmox VE.
        :param pulumi.Input['FileSourceRawArgs'] source_raw: The raw source (conflicts with `source_file`).
        :param pulumi.Input[int] timeout_upload: Timeout for uploading ISO/VSTMPL files in
               seconds (defaults to 1800).
        """
        if content_type is not None:
            pulumi.set(__self__, "content_type", content_type)
        if datastore_id is not None:
            pulumi.set(__self__, "datastore_id", datastore_id)
        if file_modification_date is not None:
            pulumi.set(__self__, "file_modification_date", file_modification_date)
        if file_name is not None:
            pulumi.set(__self__, "file_name", file_name)
        if file_size is not None:
            pulumi.set(__self__, "file_size", file_size)
        if file_tag is not None:
            pulumi.set(__self__, "file_tag", file_tag)
        if node_name is not None:
            pulumi.set(__self__, "node_name", node_name)
        if overwrite is not None:
            pulumi.set(__self__, "overwrite", overwrite)
        if source_file is not None:
            pulumi.set(__self__, "source_file", source_file)
        if source_raw is not None:
            pulumi.set(__self__, "source_raw", source_raw)
        if timeout_upload is not None:
            pulumi.set(__self__, "timeout_upload", timeout_upload)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> Optional[pulumi.Input[str]]:
        """
        The content type. If not specified, the content
        type will be inferred from the file extension. Valid values are:
        """
        return pulumi.get(self, "content_type")

    @content_type.setter
    def content_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content_type", value)

    @property
    @pulumi.getter(name="datastoreId")
    def datastore_id(self) -> Optional[pulumi.Input[str]]:
        """
        The datastore id.
        """
        return pulumi.get(self, "datastore_id")

    @datastore_id.setter
    def datastore_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "datastore_id", value)

    @property
    @pulumi.getter(name="fileModificationDate")
    def file_modification_date(self) -> Optional[pulumi.Input[str]]:
        """
        The file modification date (RFC 3339).
        """
        return pulumi.get(self, "file_modification_date")

    @file_modification_date.setter
    def file_modification_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_modification_date", value)

    @property
    @pulumi.getter(name="fileName")
    def file_name(self) -> Optional[pulumi.Input[str]]:
        """
        The file name.
        """
        return pulumi.get(self, "file_name")

    @file_name.setter
    def file_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_name", value)

    @property
    @pulumi.getter(name="fileSize")
    def file_size(self) -> Optional[pulumi.Input[int]]:
        """
        The file size in bytes.
        """
        return pulumi.get(self, "file_size")

    @file_size.setter
    def file_size(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "file_size", value)

    @property
    @pulumi.getter(name="fileTag")
    def file_tag(self) -> Optional[pulumi.Input[str]]:
        """
        The file tag.
        """
        return pulumi.get(self, "file_tag")

    @file_tag.setter
    def file_tag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "file_tag", value)

    @property
    @pulumi.getter(name="nodeName")
    def node_name(self) -> Optional[pulumi.Input[str]]:
        """
        The node name.
        """
        return pulumi.get(self, "node_name")

    @node_name.setter
    def node_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node_name", value)

    @property
    @pulumi.getter
    def overwrite(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether to overwrite an existing file (defaults to
        `true`).
        """
        return pulumi.get(self, "overwrite")

    @overwrite.setter
    def overwrite(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "overwrite", value)

    @property
    @pulumi.getter(name="sourceFile")
    def source_file(self) -> Optional[pulumi.Input['FileSourceFileArgs']]:
        """
        The source file (conflicts with `source_raw`),
        could be a local file or a URL. If the source file is a URL, the file will
        be downloaded and stored locally before uploading it to Proxmox VE.
        """
        return pulumi.get(self, "source_file")

    @source_file.setter
    def source_file(self, value: Optional[pulumi.Input['FileSourceFileArgs']]):
        pulumi.set(self, "source_file", value)

    @property
    @pulumi.getter(name="sourceRaw")
    def source_raw(self) -> Optional[pulumi.Input['FileSourceRawArgs']]:
        """
        The raw source (conflicts with `source_file`).
        """
        return pulumi.get(self, "source_raw")

    @source_raw.setter
    def source_raw(self, value: Optional[pulumi.Input['FileSourceRawArgs']]):
        pulumi.set(self, "source_raw", value)

    @property
    @pulumi.getter(name="timeoutUpload")
    def timeout_upload(self) -> Optional[pulumi.Input[int]]:
        """
        Timeout for uploading ISO/VSTMPL files in
        seconds (defaults to 1800).
        """
        return pulumi.get(self, "timeout_upload")

    @timeout_upload.setter
    def timeout_upload(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "timeout_upload", value)


class File(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 datastore_id: Optional[pulumi.Input[str]] = None,
                 node_name: Optional[pulumi.Input[str]] = None,
                 overwrite: Optional[pulumi.Input[bool]] = None,
                 source_file: Optional[pulumi.Input[pulumi.InputType['FileSourceFileArgs']]] = None,
                 source_raw: Optional[pulumi.Input[pulumi.InputType['FileSourceRawArgs']]] = None,
                 timeout_upload: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Manages a file.

        ## Example Usage

        ### Backups (`dump`)

        > The resource with this content type uses SSH access to the node. You might need to configure the `ssh` option in the `provider` section.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        backup = proxmoxve.storage.File("backup",
            content_type="dump",
            datastore_id="local",
            node_name="pve",
            source_file=proxmoxve.storage.FileSourceFileArgs(
                path="vzdump-lxc-100-2023_11_08-23_10_05.tar",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### Images

        > Consider using `Download.File` resource instead. Using this resource for images is less efficient (requires to transfer uploaded image to node) though still supported.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        ubuntu_container_template = proxmoxve.storage.File("ubuntuContainerTemplate",
            content_type="iso",
            datastore_id="local",
            node_name="pve",
            source_file=proxmoxve.storage.FileSourceFileArgs(
                path="https://cloud-images.ubuntu.com/jammy/20230929/jammy-server-cloudimg-amd64-disk-kvm.img",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### Container Template (`vztmpl`)

        > Consider using `Download.File` resource instead. Using this resource for container images is less efficient (requires to transfer uploaded image to node) though still supported.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        ubuntu_container_template = proxmoxve.storage.File("ubuntuContainerTemplate",
            content_type="vztmpl",
            datastore_id="local",
            node_name="first-node",
            source_file=proxmoxve.storage.FileSourceFileArgs(
                path="https://download.proxmox.com/images/system/ubuntu-20.04-standard_20.04-1_amd64.tar.gz",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Important Notes

        The Proxmox VE API endpoint for file uploads does not support chunked transfer
        encoding, which means that we must first store the source file as a temporary
        file locally before uploading it.

        You must ensure that you have at least `Size-in-MB * 2 + 1` MB of storage space
        available (twice the size plus overhead because a multipart payload needs to be
        created as another temporary file).

        By default, if the specified file already exists, the resource will
        unconditionally replace it and take ownership of the resource. On destruction,
        the file will be deleted as if it did not exist before. If you want to prevent
        the resource from replacing the file, set `overwrite` to `false`.

        ## Import

        Instances can be imported using the `node_name`, `datastore_id`, `content_type`

        and the `file_name` in the following format:

        text

        node_name:datastore_id/content_type/file_name

        Example:

        bash

        ```sh
        $ pulumi import proxmoxve:Storage/file:File cloud_config pve/local:snippets/example.cloud-config.yaml
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content_type: The content type. If not specified, the content
               type will be inferred from the file extension. Valid values are:
        :param pulumi.Input[str] datastore_id: The datastore id.
        :param pulumi.Input[str] node_name: The node name.
        :param pulumi.Input[bool] overwrite: Whether to overwrite an existing file (defaults to
               `true`).
        :param pulumi.Input[pulumi.InputType['FileSourceFileArgs']] source_file: The source file (conflicts with `source_raw`),
               could be a local file or a URL. If the source file is a URL, the file will
               be downloaded and stored locally before uploading it to Proxmox VE.
        :param pulumi.Input[pulumi.InputType['FileSourceRawArgs']] source_raw: The raw source (conflicts with `source_file`).
        :param pulumi.Input[int] timeout_upload: Timeout for uploading ISO/VSTMPL files in
               seconds (defaults to 1800).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FileArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a file.

        ## Example Usage

        ### Backups (`dump`)

        > The resource with this content type uses SSH access to the node. You might need to configure the `ssh` option in the `provider` section.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        backup = proxmoxve.storage.File("backup",
            content_type="dump",
            datastore_id="local",
            node_name="pve",
            source_file=proxmoxve.storage.FileSourceFileArgs(
                path="vzdump-lxc-100-2023_11_08-23_10_05.tar",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### Images

        > Consider using `Download.File` resource instead. Using this resource for images is less efficient (requires to transfer uploaded image to node) though still supported.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        ubuntu_container_template = proxmoxve.storage.File("ubuntuContainerTemplate",
            content_type="iso",
            datastore_id="local",
            node_name="pve",
            source_file=proxmoxve.storage.FileSourceFileArgs(
                path="https://cloud-images.ubuntu.com/jammy/20230929/jammy-server-cloudimg-amd64-disk-kvm.img",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ### Container Template (`vztmpl`)

        > Consider using `Download.File` resource instead. Using this resource for container images is less efficient (requires to transfer uploaded image to node) though still supported.

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        ubuntu_container_template = proxmoxve.storage.File("ubuntuContainerTemplate",
            content_type="vztmpl",
            datastore_id="local",
            node_name="first-node",
            source_file=proxmoxve.storage.FileSourceFileArgs(
                path="https://download.proxmox.com/images/system/ubuntu-20.04-standard_20.04-1_amd64.tar.gz",
            ))
        ```
        <!--End PulumiCodeChooser -->

        ## Important Notes

        The Proxmox VE API endpoint for file uploads does not support chunked transfer
        encoding, which means that we must first store the source file as a temporary
        file locally before uploading it.

        You must ensure that you have at least `Size-in-MB * 2 + 1` MB of storage space
        available (twice the size plus overhead because a multipart payload needs to be
        created as another temporary file).

        By default, if the specified file already exists, the resource will
        unconditionally replace it and take ownership of the resource. On destruction,
        the file will be deleted as if it did not exist before. If you want to prevent
        the resource from replacing the file, set `overwrite` to `false`.

        ## Import

        Instances can be imported using the `node_name`, `datastore_id`, `content_type`

        and the `file_name` in the following format:

        text

        node_name:datastore_id/content_type/file_name

        Example:

        bash

        ```sh
        $ pulumi import proxmoxve:Storage/file:File cloud_config pve/local:snippets/example.cloud-config.yaml
        ```

        :param str resource_name: The name of the resource.
        :param FileArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FileArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content_type: Optional[pulumi.Input[str]] = None,
                 datastore_id: Optional[pulumi.Input[str]] = None,
                 node_name: Optional[pulumi.Input[str]] = None,
                 overwrite: Optional[pulumi.Input[bool]] = None,
                 source_file: Optional[pulumi.Input[pulumi.InputType['FileSourceFileArgs']]] = None,
                 source_raw: Optional[pulumi.Input[pulumi.InputType['FileSourceRawArgs']]] = None,
                 timeout_upload: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FileArgs.__new__(FileArgs)

            __props__.__dict__["content_type"] = content_type
            if datastore_id is None and not opts.urn:
                raise TypeError("Missing required property 'datastore_id'")
            __props__.__dict__["datastore_id"] = datastore_id
            if node_name is None and not opts.urn:
                raise TypeError("Missing required property 'node_name'")
            __props__.__dict__["node_name"] = node_name
            __props__.__dict__["overwrite"] = overwrite
            __props__.__dict__["source_file"] = source_file
            __props__.__dict__["source_raw"] = source_raw
            __props__.__dict__["timeout_upload"] = timeout_upload
            __props__.__dict__["file_modification_date"] = None
            __props__.__dict__["file_name"] = None
            __props__.__dict__["file_size"] = None
            __props__.__dict__["file_tag"] = None
        super(File, __self__).__init__(
            'proxmoxve:Storage/file:File',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            content_type: Optional[pulumi.Input[str]] = None,
            datastore_id: Optional[pulumi.Input[str]] = None,
            file_modification_date: Optional[pulumi.Input[str]] = None,
            file_name: Optional[pulumi.Input[str]] = None,
            file_size: Optional[pulumi.Input[int]] = None,
            file_tag: Optional[pulumi.Input[str]] = None,
            node_name: Optional[pulumi.Input[str]] = None,
            overwrite: Optional[pulumi.Input[bool]] = None,
            source_file: Optional[pulumi.Input[pulumi.InputType['FileSourceFileArgs']]] = None,
            source_raw: Optional[pulumi.Input[pulumi.InputType['FileSourceRawArgs']]] = None,
            timeout_upload: Optional[pulumi.Input[int]] = None) -> 'File':
        """
        Get an existing File resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content_type: The content type. If not specified, the content
               type will be inferred from the file extension. Valid values are:
        :param pulumi.Input[str] datastore_id: The datastore id.
        :param pulumi.Input[str] file_modification_date: The file modification date (RFC 3339).
        :param pulumi.Input[str] file_name: The file name.
        :param pulumi.Input[int] file_size: The file size in bytes.
        :param pulumi.Input[str] file_tag: The file tag.
        :param pulumi.Input[str] node_name: The node name.
        :param pulumi.Input[bool] overwrite: Whether to overwrite an existing file (defaults to
               `true`).
        :param pulumi.Input[pulumi.InputType['FileSourceFileArgs']] source_file: The source file (conflicts with `source_raw`),
               could be a local file or a URL. If the source file is a URL, the file will
               be downloaded and stored locally before uploading it to Proxmox VE.
        :param pulumi.Input[pulumi.InputType['FileSourceRawArgs']] source_raw: The raw source (conflicts with `source_file`).
        :param pulumi.Input[int] timeout_upload: Timeout for uploading ISO/VSTMPL files in
               seconds (defaults to 1800).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FileState.__new__(_FileState)

        __props__.__dict__["content_type"] = content_type
        __props__.__dict__["datastore_id"] = datastore_id
        __props__.__dict__["file_modification_date"] = file_modification_date
        __props__.__dict__["file_name"] = file_name
        __props__.__dict__["file_size"] = file_size
        __props__.__dict__["file_tag"] = file_tag
        __props__.__dict__["node_name"] = node_name
        __props__.__dict__["overwrite"] = overwrite
        __props__.__dict__["source_file"] = source_file
        __props__.__dict__["source_raw"] = source_raw
        __props__.__dict__["timeout_upload"] = timeout_upload
        return File(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="contentType")
    def content_type(self) -> pulumi.Output[str]:
        """
        The content type. If not specified, the content
        type will be inferred from the file extension. Valid values are:
        """
        return pulumi.get(self, "content_type")

    @property
    @pulumi.getter(name="datastoreId")
    def datastore_id(self) -> pulumi.Output[str]:
        """
        The datastore id.
        """
        return pulumi.get(self, "datastore_id")

    @property
    @pulumi.getter(name="fileModificationDate")
    def file_modification_date(self) -> pulumi.Output[str]:
        """
        The file modification date (RFC 3339).
        """
        return pulumi.get(self, "file_modification_date")

    @property
    @pulumi.getter(name="fileName")
    def file_name(self) -> pulumi.Output[str]:
        """
        The file name.
        """
        return pulumi.get(self, "file_name")

    @property
    @pulumi.getter(name="fileSize")
    def file_size(self) -> pulumi.Output[int]:
        """
        The file size in bytes.
        """
        return pulumi.get(self, "file_size")

    @property
    @pulumi.getter(name="fileTag")
    def file_tag(self) -> pulumi.Output[str]:
        """
        The file tag.
        """
        return pulumi.get(self, "file_tag")

    @property
    @pulumi.getter(name="nodeName")
    def node_name(self) -> pulumi.Output[str]:
        """
        The node name.
        """
        return pulumi.get(self, "node_name")

    @property
    @pulumi.getter
    def overwrite(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether to overwrite an existing file (defaults to
        `true`).
        """
        return pulumi.get(self, "overwrite")

    @property
    @pulumi.getter(name="sourceFile")
    def source_file(self) -> pulumi.Output[Optional['outputs.FileSourceFile']]:
        """
        The source file (conflicts with `source_raw`),
        could be a local file or a URL. If the source file is a URL, the file will
        be downloaded and stored locally before uploading it to Proxmox VE.
        """
        return pulumi.get(self, "source_file")

    @property
    @pulumi.getter(name="sourceRaw")
    def source_raw(self) -> pulumi.Output[Optional['outputs.FileSourceRaw']]:
        """
        The raw source (conflicts with `source_file`).
        """
        return pulumi.get(self, "source_raw")

    @property
    @pulumi.getter(name="timeoutUpload")
    def timeout_upload(self) -> pulumi.Output[Optional[int]]:
        """
        Timeout for uploading ISO/VSTMPL files in
        seconds (defaults to 1800).
        """
        return pulumi.get(self, "timeout_upload")

