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

__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:
    def __init__(__self__, *,
                 user_id: pulumi.Input[str],
                 acls: Optional[pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 keys: Optional[pulumi.Input[str]] = None,
                 last_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] user_id: The user identifier.
        :param pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]] acls: The access control list (multiple blocks supported).
        :param pulumi.Input[str] comment: The user comment.
        :param pulumi.Input[str] email: The user's email address.
        :param pulumi.Input[bool] enabled: Whether the user account is enabled.
        :param pulumi.Input[str] expiration_date: The user account's expiration date (RFC 3339).
        :param pulumi.Input[str] first_name: The user's first name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: The user's groups.
        :param pulumi.Input[str] keys: The user's keys.
        :param pulumi.Input[str] last_name: The user's last name.
        :param pulumi.Input[str] password: The user's password. Required for PVE or PAM realms.
        """
        pulumi.set(__self__, "user_id", user_id)
        if acls is not None:
            pulumi.set(__self__, "acls", acls)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if expiration_date is not None:
            pulumi.set(__self__, "expiration_date", expiration_date)
        if first_name is not None:
            pulumi.set(__self__, "first_name", first_name)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if keys is not None:
            pulumi.set(__self__, "keys", keys)
        if last_name is not None:
            pulumi.set(__self__, "last_name", last_name)
        if password is not None:
            pulumi.set(__self__, "password", password)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Input[str]:
        """
        The user identifier.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_id", value)

    @property
    @pulumi.getter
    def acls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]]]:
        """
        The access control list (multiple blocks supported).
        """
        return pulumi.get(self, "acls")

    @acls.setter
    def acls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]]]):
        pulumi.set(self, "acls", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        The user comment.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        The user's email address.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user account is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> Optional[pulumi.Input[str]]:
        """
        The user account's expiration date (RFC 3339).
        """
        return pulumi.get(self, "expiration_date")

    @expiration_date.setter
    def expiration_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration_date", value)

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user's first name.
        """
        return pulumi.get(self, "first_name")

    @first_name.setter
    def first_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "first_name", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The user's groups.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter
    def keys(self) -> Optional[pulumi.Input[str]]:
        """
        The user's keys.
        """
        return pulumi.get(self, "keys")

    @keys.setter
    def keys(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "keys", value)

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user's last name.
        """
        return pulumi.get(self, "last_name")

    @last_name.setter
    def last_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The user's password. Required for PVE or PAM realms.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)


@pulumi.input_type
class _UserState:
    def __init__(__self__, *,
                 acls: Optional[pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 keys: Optional[pulumi.Input[str]] = None,
                 last_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering User resources.
        :param pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]] acls: The access control list (multiple blocks supported).
        :param pulumi.Input[str] comment: The user comment.
        :param pulumi.Input[str] email: The user's email address.
        :param pulumi.Input[bool] enabled: Whether the user account is enabled.
        :param pulumi.Input[str] expiration_date: The user account's expiration date (RFC 3339).
        :param pulumi.Input[str] first_name: The user's first name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: The user's groups.
        :param pulumi.Input[str] keys: The user's keys.
        :param pulumi.Input[str] last_name: The user's last name.
        :param pulumi.Input[str] password: The user's password. Required for PVE or PAM realms.
        :param pulumi.Input[str] user_id: The user identifier.
        """
        if acls is not None:
            pulumi.set(__self__, "acls", acls)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if expiration_date is not None:
            pulumi.set(__self__, "expiration_date", expiration_date)
        if first_name is not None:
            pulumi.set(__self__, "first_name", first_name)
        if groups is not None:
            pulumi.set(__self__, "groups", groups)
        if keys is not None:
            pulumi.set(__self__, "keys", keys)
        if last_name is not None:
            pulumi.set(__self__, "last_name", last_name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if user_id is not None:
            pulumi.set(__self__, "user_id", user_id)

    @property
    @pulumi.getter
    def acls(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]]]:
        """
        The access control list (multiple blocks supported).
        """
        return pulumi.get(self, "acls")

    @acls.setter
    def acls(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserAclArgs']]]]):
        pulumi.set(self, "acls", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        """
        The user comment.
        """
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        The user's email address.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the user account is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> Optional[pulumi.Input[str]]:
        """
        The user account's expiration date (RFC 3339).
        """
        return pulumi.get(self, "expiration_date")

    @expiration_date.setter
    def expiration_date(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "expiration_date", value)

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user's first name.
        """
        return pulumi.get(self, "first_name")

    @first_name.setter
    def first_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "first_name", value)

    @property
    @pulumi.getter
    def groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The user's groups.
        """
        return pulumi.get(self, "groups")

    @groups.setter
    def groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "groups", value)

    @property
    @pulumi.getter
    def keys(self) -> Optional[pulumi.Input[str]]:
        """
        The user's keys.
        """
        return pulumi.get(self, "keys")

    @keys.setter
    def keys(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "keys", value)

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user's last name.
        """
        return pulumi.get(self, "last_name")

    @last_name.setter
    def last_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The user's password. Required for PVE or PAM realms.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The user identifier.
        """
        return pulumi.get(self, "user_id")

    @user_id.setter
    def user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_id", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acls: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserAclArgs']]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 keys: Optional[pulumi.Input[str]] = None,
                 last_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a user.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        operations_monitoring = proxmoxve.permission.Role("operationsMonitoring",
            role_id="operations-monitoring",
            privileges=["VM.Monitor"])
        operations_automation = proxmoxve.permission.User("operationsAutomation",
            acls=[proxmoxve.permission.UserAclArgs(
                path="/vms/1234",
                propagate=True,
                role_id=operations_monitoring.role_id,
            )],
            comment="Managed by Terraform",
            password="a-strong-password",
            user_id="operations-automation@pve")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Instances can be imported using the `user_id`, e.g.,

        bash

        ```sh
        $ pulumi import proxmoxve:Permission/user:User operations_automation operations-automation@pve
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserAclArgs']]]] acls: The access control list (multiple blocks supported).
        :param pulumi.Input[str] comment: The user comment.
        :param pulumi.Input[str] email: The user's email address.
        :param pulumi.Input[bool] enabled: Whether the user account is enabled.
        :param pulumi.Input[str] expiration_date: The user account's expiration date (RFC 3339).
        :param pulumi.Input[str] first_name: The user's first name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: The user's groups.
        :param pulumi.Input[str] keys: The user's keys.
        :param pulumi.Input[str] last_name: The user's last name.
        :param pulumi.Input[str] password: The user's password. Required for PVE or PAM realms.
        :param pulumi.Input[str] user_id: The user identifier.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a user.

        ## Example Usage

        <!--Start PulumiCodeChooser -->
        ```python
        import pulumi
        import pulumi_proxmoxve as proxmoxve

        operations_monitoring = proxmoxve.permission.Role("operationsMonitoring",
            role_id="operations-monitoring",
            privileges=["VM.Monitor"])
        operations_automation = proxmoxve.permission.User("operationsAutomation",
            acls=[proxmoxve.permission.UserAclArgs(
                path="/vms/1234",
                propagate=True,
                role_id=operations_monitoring.role_id,
            )],
            comment="Managed by Terraform",
            password="a-strong-password",
            user_id="operations-automation@pve")
        ```
        <!--End PulumiCodeChooser -->

        ## Import

        Instances can be imported using the `user_id`, e.g.,

        bash

        ```sh
        $ pulumi import proxmoxve:Permission/user:User operations_automation operations-automation@pve
        ```

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 acls: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserAclArgs']]]]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 expiration_date: Optional[pulumi.Input[str]] = None,
                 first_name: Optional[pulumi.Input[str]] = None,
                 groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 keys: Optional[pulumi.Input[str]] = None,
                 last_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 user_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserArgs.__new__(UserArgs)

            __props__.__dict__["acls"] = acls
            __props__.__dict__["comment"] = comment
            __props__.__dict__["email"] = email
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["expiration_date"] = expiration_date
            __props__.__dict__["first_name"] = first_name
            __props__.__dict__["groups"] = groups
            __props__.__dict__["keys"] = keys
            __props__.__dict__["last_name"] = last_name
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            if user_id is None and not opts.urn:
                raise TypeError("Missing required property 'user_id'")
            __props__.__dict__["user_id"] = user_id
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["password"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(User, __self__).__init__(
            'proxmoxve:Permission/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            acls: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserAclArgs']]]]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            email: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            expiration_date: Optional[pulumi.Input[str]] = None,
            first_name: Optional[pulumi.Input[str]] = None,
            groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            keys: Optional[pulumi.Input[str]] = None,
            last_name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            user_id: Optional[pulumi.Input[str]] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserAclArgs']]]] acls: The access control list (multiple blocks supported).
        :param pulumi.Input[str] comment: The user comment.
        :param pulumi.Input[str] email: The user's email address.
        :param pulumi.Input[bool] enabled: Whether the user account is enabled.
        :param pulumi.Input[str] expiration_date: The user account's expiration date (RFC 3339).
        :param pulumi.Input[str] first_name: The user's first name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] groups: The user's groups.
        :param pulumi.Input[str] keys: The user's keys.
        :param pulumi.Input[str] last_name: The user's last name.
        :param pulumi.Input[str] password: The user's password. Required for PVE or PAM realms.
        :param pulumi.Input[str] user_id: The user identifier.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserState.__new__(_UserState)

        __props__.__dict__["acls"] = acls
        __props__.__dict__["comment"] = comment
        __props__.__dict__["email"] = email
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["expiration_date"] = expiration_date
        __props__.__dict__["first_name"] = first_name
        __props__.__dict__["groups"] = groups
        __props__.__dict__["keys"] = keys
        __props__.__dict__["last_name"] = last_name
        __props__.__dict__["password"] = password
        __props__.__dict__["user_id"] = user_id
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def acls(self) -> pulumi.Output[Optional[Sequence['outputs.UserAcl']]]:
        """
        The access control list (multiple blocks supported).
        """
        return pulumi.get(self, "acls")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        """
        The user comment.
        """
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[Optional[str]]:
        """
        The user's email address.
        """
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the user account is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="expirationDate")
    def expiration_date(self) -> pulumi.Output[Optional[str]]:
        """
        The user account's expiration date (RFC 3339).
        """
        return pulumi.get(self, "expiration_date")

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> pulumi.Output[Optional[str]]:
        """
        The user's first name.
        """
        return pulumi.get(self, "first_name")

    @property
    @pulumi.getter
    def groups(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The user's groups.
        """
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter
    def keys(self) -> pulumi.Output[Optional[str]]:
        """
        The user's keys.
        """
        return pulumi.get(self, "keys")

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> pulumi.Output[Optional[str]]:
        """
        The user's last name.
        """
        return pulumi.get(self, "last_name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[Optional[str]]:
        """
        The user's password. Required for PVE or PAM realms.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="userId")
    def user_id(self) -> pulumi.Output[str]:
        """
        The user identifier.
        """
        return pulumi.get(self, "user_id")

