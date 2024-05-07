# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['TargetArgs', 'Target']

@pulumi.input_type
class TargetArgs:
    def __init__(__self__, *,
                 target: pulumi.Input[str],
                 upstream_id: pulumi.Input[str],
                 weight: pulumi.Input[int],
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Target resource.
        :param pulumi.Input[str] target: is the target address (IP or hostname) and port. If omitted the port defaults to 8000.
        :param pulumi.Input[str] upstream_id: is the id of the upstream to apply this target to.
        :param pulumi.Input[int] weight: is the weight this target gets within the upstream load balancer (0-1000, defaults to 100).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list set of strings associated with the Plugin for grouping and filtering
        """
        pulumi.set(__self__, "target", target)
        pulumi.set(__self__, "upstream_id", upstream_id)
        pulumi.set(__self__, "weight", weight)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        is the target address (IP or hostname) and port. If omitted the port defaults to 8000.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="upstreamId")
    def upstream_id(self) -> pulumi.Input[str]:
        """
        is the id of the upstream to apply this target to.
        """
        return pulumi.get(self, "upstream_id")

    @upstream_id.setter
    def upstream_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "upstream_id", value)

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Input[int]:
        """
        is the weight this target gets within the upstream load balancer (0-1000, defaults to 100).
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: pulumi.Input[int]):
        pulumi.set(self, "weight", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list set of strings associated with the Plugin for grouping and filtering
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _TargetState:
    def __init__(__self__, *,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 upstream_id: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering Target resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list set of strings associated with the Plugin for grouping and filtering
        :param pulumi.Input[str] target: is the target address (IP or hostname) and port. If omitted the port defaults to 8000.
        :param pulumi.Input[str] upstream_id: is the id of the upstream to apply this target to.
        :param pulumi.Input[int] weight: is the weight this target gets within the upstream load balancer (0-1000, defaults to 100).
        """
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if upstream_id is not None:
            pulumi.set(__self__, "upstream_id", upstream_id)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list set of strings associated with the Plugin for grouping and filtering
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        """
        is the target address (IP or hostname) and port. If omitted the port defaults to 8000.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="upstreamId")
    def upstream_id(self) -> Optional[pulumi.Input[str]]:
        """
        is the id of the upstream to apply this target to.
        """
        return pulumi.get(self, "upstream_id")

    @upstream_id.setter
    def upstream_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "upstream_id", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        is the weight this target gets within the upstream load balancer (0-1000, defaults to 100).
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)


class Target(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 upstream_id: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_kong as kong

        target = kong.Target("target",
            target="sample_target:80",
            weight=10,
            upstream_id=upstream["id"])
        ```

        ## Import

        To import a target use a combination of the upstream id and the target id as follows:

        ```sh
        $ pulumi import kong:index/target:Target <target_identifier> <upstream_id>/<target_id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list set of strings associated with the Plugin for grouping and filtering
        :param pulumi.Input[str] target: is the target address (IP or hostname) and port. If omitted the port defaults to 8000.
        :param pulumi.Input[str] upstream_id: is the id of the upstream to apply this target to.
        :param pulumi.Input[int] weight: is the weight this target gets within the upstream load balancer (0-1000, defaults to 100).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TargetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ```python
        import pulumi
        import pulumi_kong as kong

        target = kong.Target("target",
            target="sample_target:80",
            weight=10,
            upstream_id=upstream["id"])
        ```

        ## Import

        To import a target use a combination of the upstream id and the target id as follows:

        ```sh
        $ pulumi import kong:index/target:Target <target_identifier> <upstream_id>/<target_id>
        ```

        :param str resource_name: The name of the resource.
        :param TargetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TargetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 upstream_id: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = TargetArgs.__new__(TargetArgs)

            __props__.__dict__["tags"] = tags
            if target is None and not opts.urn:
                raise TypeError("Missing required property 'target'")
            __props__.__dict__["target"] = target
            if upstream_id is None and not opts.urn:
                raise TypeError("Missing required property 'upstream_id'")
            __props__.__dict__["upstream_id"] = upstream_id
            if weight is None and not opts.urn:
                raise TypeError("Missing required property 'weight'")
            __props__.__dict__["weight"] = weight
        super(Target, __self__).__init__(
            'kong:index/target:Target',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            target: Optional[pulumi.Input[str]] = None,
            upstream_id: Optional[pulumi.Input[str]] = None,
            weight: Optional[pulumi.Input[int]] = None) -> 'Target':
        """
        Get an existing Target resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list set of strings associated with the Plugin for grouping and filtering
        :param pulumi.Input[str] target: is the target address (IP or hostname) and port. If omitted the port defaults to 8000.
        :param pulumi.Input[str] upstream_id: is the id of the upstream to apply this target to.
        :param pulumi.Input[int] weight: is the weight this target gets within the upstream load balancer (0-1000, defaults to 100).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TargetState.__new__(_TargetState)

        __props__.__dict__["tags"] = tags
        __props__.__dict__["target"] = target
        __props__.__dict__["upstream_id"] = upstream_id
        __props__.__dict__["weight"] = weight
        return Target(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list set of strings associated with the Plugin for grouping and filtering
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output[str]:
        """
        is the target address (IP or hostname) and port. If omitted the port defaults to 8000.
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter(name="upstreamId")
    def upstream_id(self) -> pulumi.Output[str]:
        """
        is the id of the upstream to apply this target to.
        """
        return pulumi.get(self, "upstream_id")

    @property
    @pulumi.getter
    def weight(self) -> pulumi.Output[int]:
        """
        is the weight this target gets within the upstream load balancer (0-1000, defaults to 100).
        """
        return pulumi.get(self, "weight")

