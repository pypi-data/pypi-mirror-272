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

__all__ = [
    'GetGuestOsCustomizationResult',
    'AwaitableGetGuestOsCustomizationResult',
    'get_guest_os_customization',
    'get_guest_os_customization_output',
]

@pulumi.output_type
class GetGuestOsCustomizationResult:
    """
    A collection of values returned by getGuestOsCustomization.
    """
    def __init__(__self__, change_version=None, description=None, id=None, last_update_time=None, name=None, specs=None, type=None):
        if change_version and not isinstance(change_version, str):
            raise TypeError("Expected argument 'change_version' to be a str")
        pulumi.set(__self__, "change_version", change_version)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_update_time and not isinstance(last_update_time, str):
            raise TypeError("Expected argument 'last_update_time' to be a str")
        pulumi.set(__self__, "last_update_time", last_update_time)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if specs and not isinstance(specs, list):
            raise TypeError("Expected argument 'specs' to be a list")
        pulumi.set(__self__, "specs", specs)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="changeVersion")
    def change_version(self) -> str:
        """
        The number of last changed version to the customization specification.
        """
        return pulumi.get(self, "change_version")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The description for the customization specification.
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
    @pulumi.getter(name="lastUpdateTime")
    def last_update_time(self) -> str:
        """
        The time of last modification to the customization specification.
        """
        return pulumi.get(self, "last_update_time")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def specs(self) -> Sequence['outputs.GetGuestOsCustomizationSpecResult']:
        """
        Container object for the guest operating system properties to be customized. See virtual machine customizations
        """
        return pulumi.get(self, "specs")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of customization specification: One among: Windows, Linux.
        """
        return pulumi.get(self, "type")


class AwaitableGetGuestOsCustomizationResult(GetGuestOsCustomizationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGuestOsCustomizationResult(
            change_version=self.change_version,
            description=self.description,
            id=self.id,
            last_update_time=self.last_update_time,
            name=self.name,
            specs=self.specs,
            type=self.type)


def get_guest_os_customization(name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGuestOsCustomizationResult:
    """
    The `GuestOsCustomization` data source can be used to discover the details about a customization specification for a guest operating system.

    Suggested change
    > **NOTE:** The name attribute is the unique identifier for the customization specification per vCenter Server instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    gosc1 = vsphere.get_guest_os_customization(name="linux-spec")
    ```


    :param str name: The name of the customization specification is the unique identifier per vCenter Server instance.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('vsphere:index/getGuestOsCustomization:getGuestOsCustomization', __args__, opts=opts, typ=GetGuestOsCustomizationResult).value

    return AwaitableGetGuestOsCustomizationResult(
        change_version=pulumi.get(__ret__, 'change_version'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        last_update_time=pulumi.get(__ret__, 'last_update_time'),
        name=pulumi.get(__ret__, 'name'),
        specs=pulumi.get(__ret__, 'specs'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_guest_os_customization)
def get_guest_os_customization_output(name: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGuestOsCustomizationResult]:
    """
    The `GuestOsCustomization` data source can be used to discover the details about a customization specification for a guest operating system.

    Suggested change
    > **NOTE:** The name attribute is the unique identifier for the customization specification per vCenter Server instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    gosc1 = vsphere.get_guest_os_customization(name="linux-spec")
    ```


    :param str name: The name of the customization specification is the unique identifier per vCenter Server instance.
    """
    ...
