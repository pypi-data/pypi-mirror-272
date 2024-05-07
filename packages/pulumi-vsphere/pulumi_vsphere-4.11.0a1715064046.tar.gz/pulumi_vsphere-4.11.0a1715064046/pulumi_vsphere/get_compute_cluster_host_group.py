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
    'GetComputeClusterHostGroupResult',
    'AwaitableGetComputeClusterHostGroupResult',
    'get_compute_cluster_host_group',
    'get_compute_cluster_host_group_output',
]

@pulumi.output_type
class GetComputeClusterHostGroupResult:
    """
    A collection of values returned by getComputeClusterHostGroup.
    """
    def __init__(__self__, compute_cluster_id=None, host_system_ids=None, id=None, name=None):
        if compute_cluster_id and not isinstance(compute_cluster_id, str):
            raise TypeError("Expected argument 'compute_cluster_id' to be a str")
        pulumi.set(__self__, "compute_cluster_id", compute_cluster_id)
        if host_system_ids and not isinstance(host_system_ids, list):
            raise TypeError("Expected argument 'host_system_ids' to be a list")
        pulumi.set(__self__, "host_system_ids", host_system_ids)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="computeClusterId")
    def compute_cluster_id(self) -> str:
        return pulumi.get(self, "compute_cluster_id")

    @property
    @pulumi.getter(name="hostSystemIds")
    def host_system_ids(self) -> Sequence[str]:
        """
        The [managed object reference ID][docs-about-morefs] of
        the ESXi hosts in the host group.
        """
        return pulumi.get(self, "host_system_ids")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


class AwaitableGetComputeClusterHostGroupResult(GetComputeClusterHostGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetComputeClusterHostGroupResult(
            compute_cluster_id=self.compute_cluster_id,
            host_system_ids=self.host_system_ids,
            id=self.id,
            name=self.name)


def get_compute_cluster_host_group(compute_cluster_id: Optional[str] = None,
                                   name: Optional[str] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetComputeClusterHostGroupResult:
    """
    The `ComputeClusterHostGroup` data source can be used to discover
    the IDs ESXi hosts in a host group and return host group attributes to other
    resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    datacenter = vsphere.get_datacenter(name=vsphere_datacenter)
    cluster = vsphere.get_compute_cluster(name=vsphere_cluster,
        datacenter_id=datacenter.id)
    host_group1 = vsphere.get_compute_cluster_host_group(name="host_group1",
        compute_cluster_id=cluster.id)
    host_rule1 = vsphere.ComputeClusterVmHostRule("host_rule1",
        compute_cluster_id=cluster.id,
        name="terraform-host-rule1",
        vm_group_name="vm_group1",
        affinity_host_group_name=host_group1.name)
    ```


    :param str compute_cluster_id: The [managed object reference ID][docs-about-morefs]
           of the compute cluster for the host group.
           
           [docs-about-morefs]: /docs/providers/vsphere/index.html#use-of-managed-object-references-by-the-vsphere-provider
    :param str name: The name of the host group.
    """
    __args__ = dict()
    __args__['computeClusterId'] = compute_cluster_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('vsphere:index/getComputeClusterHostGroup:getComputeClusterHostGroup', __args__, opts=opts, typ=GetComputeClusterHostGroupResult).value

    return AwaitableGetComputeClusterHostGroupResult(
        compute_cluster_id=pulumi.get(__ret__, 'compute_cluster_id'),
        host_system_ids=pulumi.get(__ret__, 'host_system_ids'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'))


@_utilities.lift_output_func(get_compute_cluster_host_group)
def get_compute_cluster_host_group_output(compute_cluster_id: Optional[pulumi.Input[str]] = None,
                                          name: Optional[pulumi.Input[str]] = None,
                                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetComputeClusterHostGroupResult]:
    """
    The `ComputeClusterHostGroup` data source can be used to discover
    the IDs ESXi hosts in a host group and return host group attributes to other
    resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_vsphere as vsphere

    datacenter = vsphere.get_datacenter(name=vsphere_datacenter)
    cluster = vsphere.get_compute_cluster(name=vsphere_cluster,
        datacenter_id=datacenter.id)
    host_group1 = vsphere.get_compute_cluster_host_group(name="host_group1",
        compute_cluster_id=cluster.id)
    host_rule1 = vsphere.ComputeClusterVmHostRule("host_rule1",
        compute_cluster_id=cluster.id,
        name="terraform-host-rule1",
        vm_group_name="vm_group1",
        affinity_host_group_name=host_group1.name)
    ```


    :param str compute_cluster_id: The [managed object reference ID][docs-about-morefs]
           of the compute cluster for the host group.
           
           [docs-about-morefs]: /docs/providers/vsphere/index.html#use-of-managed-object-references-by-the-vsphere-provider
    :param str name: The name of the host group.
    """
    ...
