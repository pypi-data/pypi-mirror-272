# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['SubscriptionArgs', 'Subscription']

@pulumi.input_type
class SubscriptionArgs:
    def __init__(__self__, *,
                 conninfo: pulumi.Input[str],
                 publications: pulumi.Input[Sequence[pulumi.Input[str]]],
                 create_slot: Optional[pulumi.Input[bool]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 slot_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Subscription resource.
        :param pulumi.Input[str] conninfo: The connection string to the publisher. It should follow the [keyword/value format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] publications: Names of the publications on the publisher to subscribe to
        :param pulumi.Input[bool] create_slot: Specifies whether the command should create the replication slot on the publisher. Default behavior is true
        :param pulumi.Input[str] database: Which database to create the subscription on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the publication.
        :param pulumi.Input[str] slot_name: Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name
        """
        pulumi.set(__self__, "conninfo", conninfo)
        pulumi.set(__self__, "publications", publications)
        if create_slot is not None:
            pulumi.set(__self__, "create_slot", create_slot)
        if database is not None:
            pulumi.set(__self__, "database", database)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if slot_name is not None:
            pulumi.set(__self__, "slot_name", slot_name)

    @property
    @pulumi.getter
    def conninfo(self) -> pulumi.Input[str]:
        """
        The connection string to the publisher. It should follow the [keyword/value format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
        """
        return pulumi.get(self, "conninfo")

    @conninfo.setter
    def conninfo(self, value: pulumi.Input[str]):
        pulumi.set(self, "conninfo", value)

    @property
    @pulumi.getter
    def publications(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Names of the publications on the publisher to subscribe to
        """
        return pulumi.get(self, "publications")

    @publications.setter
    def publications(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "publications", value)

    @property
    @pulumi.getter(name="createSlot")
    def create_slot(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the command should create the replication slot on the publisher. Default behavior is true
        """
        return pulumi.get(self, "create_slot")

    @create_slot.setter
    def create_slot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "create_slot", value)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        Which database to create the subscription on. Defaults to provider database.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the publication.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="slotName")
    def slot_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name
        """
        return pulumi.get(self, "slot_name")

    @slot_name.setter
    def slot_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "slot_name", value)


@pulumi.input_type
class _SubscriptionState:
    def __init__(__self__, *,
                 conninfo: Optional[pulumi.Input[str]] = None,
                 create_slot: Optional[pulumi.Input[bool]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 publications: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 slot_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Subscription resources.
        :param pulumi.Input[str] conninfo: The connection string to the publisher. It should follow the [keyword/value format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
        :param pulumi.Input[bool] create_slot: Specifies whether the command should create the replication slot on the publisher. Default behavior is true
        :param pulumi.Input[str] database: Which database to create the subscription on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the publication.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] publications: Names of the publications on the publisher to subscribe to
        :param pulumi.Input[str] slot_name: Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name
        """
        if conninfo is not None:
            pulumi.set(__self__, "conninfo", conninfo)
        if create_slot is not None:
            pulumi.set(__self__, "create_slot", create_slot)
        if database is not None:
            pulumi.set(__self__, "database", database)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if publications is not None:
            pulumi.set(__self__, "publications", publications)
        if slot_name is not None:
            pulumi.set(__self__, "slot_name", slot_name)

    @property
    @pulumi.getter
    def conninfo(self) -> Optional[pulumi.Input[str]]:
        """
        The connection string to the publisher. It should follow the [keyword/value format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
        """
        return pulumi.get(self, "conninfo")

    @conninfo.setter
    def conninfo(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "conninfo", value)

    @property
    @pulumi.getter(name="createSlot")
    def create_slot(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the command should create the replication slot on the publisher. Default behavior is true
        """
        return pulumi.get(self, "create_slot")

    @create_slot.setter
    def create_slot(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "create_slot", value)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        Which database to create the subscription on. Defaults to provider database.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the publication.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def publications(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Names of the publications on the publisher to subscribe to
        """
        return pulumi.get(self, "publications")

    @publications.setter
    def publications(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "publications", value)

    @property
    @pulumi.getter(name="slotName")
    def slot_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name
        """
        return pulumi.get(self, "slot_name")

    @slot_name.setter
    def slot_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "slot_name", value)


class Subscription(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 conninfo: Optional[pulumi.Input[str]] = None,
                 create_slot: Optional[pulumi.Input[bool]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 publications: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 slot_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The `Subscription` resource creates and manages a publication on a PostgreSQL
        server.

        ## Usage

        ```python
        import pulumi
        import pulumi_postgresql as postgresql

        subscription = postgresql.Subscription("subscription",
            name="subscription",
            conninfo="host=localhost port=5432 dbname=mydb user=postgres password=postgres",
            publications=["publication"])
        ```

        ## Postgres documentation

        - https://www.postgresql.org/docs/current/sql-createsubscription.html

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] conninfo: The connection string to the publisher. It should follow the [keyword/value format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
        :param pulumi.Input[bool] create_slot: Specifies whether the command should create the replication slot on the publisher. Default behavior is true
        :param pulumi.Input[str] database: Which database to create the subscription on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the publication.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] publications: Names of the publications on the publisher to subscribe to
        :param pulumi.Input[str] slot_name: Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SubscriptionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The `Subscription` resource creates and manages a publication on a PostgreSQL
        server.

        ## Usage

        ```python
        import pulumi
        import pulumi_postgresql as postgresql

        subscription = postgresql.Subscription("subscription",
            name="subscription",
            conninfo="host=localhost port=5432 dbname=mydb user=postgres password=postgres",
            publications=["publication"])
        ```

        ## Postgres documentation

        - https://www.postgresql.org/docs/current/sql-createsubscription.html

        :param str resource_name: The name of the resource.
        :param SubscriptionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SubscriptionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 conninfo: Optional[pulumi.Input[str]] = None,
                 create_slot: Optional[pulumi.Input[bool]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 publications: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 slot_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SubscriptionArgs.__new__(SubscriptionArgs)

            if conninfo is None and not opts.urn:
                raise TypeError("Missing required property 'conninfo'")
            __props__.__dict__["conninfo"] = None if conninfo is None else pulumi.Output.secret(conninfo)
            __props__.__dict__["create_slot"] = create_slot
            __props__.__dict__["database"] = database
            __props__.__dict__["name"] = name
            if publications is None and not opts.urn:
                raise TypeError("Missing required property 'publications'")
            __props__.__dict__["publications"] = publications
            __props__.__dict__["slot_name"] = slot_name
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["conninfo"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(Subscription, __self__).__init__(
            'postgresql:index/subscription:Subscription',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            conninfo: Optional[pulumi.Input[str]] = None,
            create_slot: Optional[pulumi.Input[bool]] = None,
            database: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            publications: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            slot_name: Optional[pulumi.Input[str]] = None) -> 'Subscription':
        """
        Get an existing Subscription resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] conninfo: The connection string to the publisher. It should follow the [keyword/value format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
        :param pulumi.Input[bool] create_slot: Specifies whether the command should create the replication slot on the publisher. Default behavior is true
        :param pulumi.Input[str] database: Which database to create the subscription on. Defaults to provider database.
        :param pulumi.Input[str] name: The name of the publication.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] publications: Names of the publications on the publisher to subscribe to
        :param pulumi.Input[str] slot_name: Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SubscriptionState.__new__(_SubscriptionState)

        __props__.__dict__["conninfo"] = conninfo
        __props__.__dict__["create_slot"] = create_slot
        __props__.__dict__["database"] = database
        __props__.__dict__["name"] = name
        __props__.__dict__["publications"] = publications
        __props__.__dict__["slot_name"] = slot_name
        return Subscription(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def conninfo(self) -> pulumi.Output[str]:
        """
        The connection string to the publisher. It should follow the [keyword/value format](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
        """
        return pulumi.get(self, "conninfo")

    @property
    @pulumi.getter(name="createSlot")
    def create_slot(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the command should create the replication slot on the publisher. Default behavior is true
        """
        return pulumi.get(self, "create_slot")

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        Which database to create the subscription on. Defaults to provider database.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the publication.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def publications(self) -> pulumi.Output[Sequence[str]]:
        """
        Names of the publications on the publisher to subscribe to
        """
        return pulumi.get(self, "publications")

    @property
    @pulumi.getter(name="slotName")
    def slot_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the replication slot to use. The default behavior is to use the name of the subscription for the slot name
        """
        return pulumi.get(self, "slot_name")

