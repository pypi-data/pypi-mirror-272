# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ReplicationSlotArgs', 'ReplicationSlot']

@pulumi.input_type
class ReplicationSlotArgs:
    def __init__(__self__, *,
                 plugin: pulumi.Input[str],
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ReplicationSlot resource.
        :param pulumi.Input[str] plugin: Sets the output plugin.
        :param pulumi.Input[str] database: Which database to create the replication slot on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the replication slot.
        """
        pulumi.set(__self__, "plugin", plugin)
        if database is not None:
            pulumi.set(__self__, "database", database)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def plugin(self) -> pulumi.Input[str]:
        """
        Sets the output plugin.
        """
        return pulumi.get(self, "plugin")

    @plugin.setter
    def plugin(self, value: pulumi.Input[str]):
        pulumi.set(self, "plugin", value)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        Which database to create the replication slot on. Defaults to provider database.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the replication slot.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ReplicationSlotState:
    def __init__(__self__, *,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 plugin: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ReplicationSlot resources.
        :param pulumi.Input[str] database: Which database to create the replication slot on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the replication slot.
        :param pulumi.Input[str] plugin: Sets the output plugin.
        """
        if database is not None:
            pulumi.set(__self__, "database", database)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if plugin is not None:
            pulumi.set(__self__, "plugin", plugin)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        Which database to create the replication slot on. Defaults to provider database.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the replication slot.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def plugin(self) -> Optional[pulumi.Input[str]]:
        """
        Sets the output plugin.
        """
        return pulumi.get(self, "plugin")

    @plugin.setter
    def plugin(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "plugin", value)


class ReplicationSlot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 plugin: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ``ReplicationSlot`` resource creates and manages a replication slot on a PostgreSQL
        server.

        ## Usage

        ```python
        import pulumi
        import pulumi_postgresql as postgresql

        my_slot = postgresql.ReplicationSlot("my_slot",
            name="my_slot",
            plugin="test_decoding")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: Which database to create the replication slot on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the replication slot.
        :param pulumi.Input[str] plugin: Sets the output plugin.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationSlotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``ReplicationSlot`` resource creates and manages a replication slot on a PostgreSQL
        server.

        ## Usage

        ```python
        import pulumi
        import pulumi_postgresql as postgresql

        my_slot = postgresql.ReplicationSlot("my_slot",
            name="my_slot",
            plugin="test_decoding")
        ```

        :param str resource_name: The name of the resource.
        :param ReplicationSlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationSlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 plugin: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicationSlotArgs.__new__(ReplicationSlotArgs)

            __props__.__dict__["database"] = database
            __props__.__dict__["name"] = name
            if plugin is None and not opts.urn:
                raise TypeError("Missing required property 'plugin'")
            __props__.__dict__["plugin"] = plugin
        super(ReplicationSlot, __self__).__init__(
            'postgresql:index/replicationSlot:ReplicationSlot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            database: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            plugin: Optional[pulumi.Input[str]] = None) -> 'ReplicationSlot':
        """
        Get an existing ReplicationSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: Which database to create the replication slot on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the replication slot.
        :param pulumi.Input[str] plugin: Sets the output plugin.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ReplicationSlotState.__new__(_ReplicationSlotState)

        __props__.__dict__["database"] = database
        __props__.__dict__["name"] = name
        __props__.__dict__["plugin"] = plugin
        return ReplicationSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        Which database to create the replication slot on. Defaults to provider database.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the replication slot.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def plugin(self) -> pulumi.Output[str]:
        """
        Sets the output plugin.
        """
        return pulumi.get(self, "plugin")

