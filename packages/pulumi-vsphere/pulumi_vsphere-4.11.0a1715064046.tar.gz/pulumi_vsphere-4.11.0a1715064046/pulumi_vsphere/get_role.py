# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

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
    def __init__(__self__, description=None, id=None, label=None, name=None, role_privileges=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if label and not isinstance(label, str):
            raise TypeError("Expected argument 'label' to be a str")
        pulumi.set(__self__, "label", label)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role_privileges and not isinstance(role_privileges, list):
            raise TypeError("Expected argument 'role_privileges' to be a list")
        pulumi.set(__self__, "role_privileges", role_privileges)

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the role.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def label(self) -> str:
        """
        The display label of the role.
        """
        return pulumi.get(self, "label")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="rolePrivileges")
    def role_privileges(self) -> Optional[Sequence[str]]:
        """
        The privileges associated with the role.
        """
        return pulumi.get(self, "role_privileges")


class AwaitableGetRoleResult(GetRoleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetRoleResult(
            description=self.description,
            id=self.id,
            label=self.label,
            name=self.name,
            role_privileges=self.role_privileges)


def get_role(description: Optional[str] = None,
             label: Optional[str] = None,
             name: Optional[str] = None,
             role_privileges: Optional[Sequence[str]] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetRoleResult:
    """
    The `Role` data source can be used to discover the `id` and privileges associated
    with a role given its name or display label.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    terraform_role = vsphere.get_role(label="Terraform to vSphere Integration Role")
    ```


    :param str description: The description of the role.
    :param str label: The label of the role.
    :param Sequence[str] role_privileges: The privileges associated with the role.
    """
    __args__ = dict()
    __args__['description'] = description
    __args__['label'] = label
    __args__['name'] = name
    __args__['rolePrivileges'] = role_privileges
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('vsphere:index/getRole:getRole', __args__, opts=opts, typ=GetRoleResult).value

    return AwaitableGetRoleResult(
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        label=pulumi.get(__ret__, 'label'),
        name=pulumi.get(__ret__, 'name'),
        role_privileges=pulumi.get(__ret__, 'role_privileges'))


@_utilities.lift_output_func(get_role)
def get_role_output(description: Optional[pulumi.Input[Optional[str]]] = None,
                    label: Optional[pulumi.Input[str]] = None,
                    name: Optional[pulumi.Input[Optional[str]]] = None,
                    role_privileges: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetRoleResult]:
    """
    The `Role` data source can be used to discover the `id` and privileges associated
    with a role given its name or display label.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    terraform_role = vsphere.get_role(label="Terraform to vSphere Integration Role")
    ```


    :param str description: The description of the role.
    :param str label: The label of the role.
    :param Sequence[str] role_privileges: The privileges associated with the role.
    """
    ...
