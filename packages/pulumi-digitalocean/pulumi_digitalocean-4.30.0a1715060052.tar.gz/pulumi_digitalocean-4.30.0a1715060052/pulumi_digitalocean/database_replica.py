# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from ._enums import *

__all__ = ['DatabaseReplicaArgs', 'DatabaseReplica']

@pulumi.input_type
class DatabaseReplicaArgs:
    def __init__(__self__, *,
                 cluster_id: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 private_network_uuid: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[Union[str, 'Region']]] = None,
                 size: Optional[pulumi.Input[Union[str, 'DatabaseSlug']]] = None,
                 storage_size_mib: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a DatabaseReplica resource.
        :param pulumi.Input[str] cluster_id: The ID of the original source database cluster.
        :param pulumi.Input[str] name: The name for the database replica.
        :param pulumi.Input[str] private_network_uuid: The ID of the VPC where the database replica will be located.
        :param pulumi.Input[Union[str, 'Region']] region: DigitalOcean region where the replica will reside.
        :param pulumi.Input[Union[str, 'DatabaseSlug']] size: Database Droplet size associated with the replica (ex. `db-s-1vcpu-1gb`). Note that when resizing an existing replica, its size can only be increased. Decreasing its size is not supported.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag names to be applied to the database replica.
        """
        pulumi.set(__self__, "cluster_id", cluster_id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_network_uuid is not None:
            pulumi.set(__self__, "private_network_uuid", private_network_uuid)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if storage_size_mib is not None:
            pulumi.set(__self__, "storage_size_mib", storage_size_mib)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Input[str]:
        """
        The ID of the original source database cluster.
        """
        return pulumi.get(self, "cluster_id")

    @cluster_id.setter
    def cluster_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the database replica.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateNetworkUuid")
    def private_network_uuid(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC where the database replica will be located.
        """
        return pulumi.get(self, "private_network_uuid")

    @private_network_uuid.setter
    def private_network_uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_network_uuid", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[Union[str, 'Region']]]:
        """
        DigitalOcean region where the replica will reside.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[Union[str, 'Region']]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[Union[str, 'DatabaseSlug']]]:
        """
        Database Droplet size associated with the replica (ex. `db-s-1vcpu-1gb`). Note that when resizing an existing replica, its size can only be increased. Decreasing its size is not supported.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[Union[str, 'DatabaseSlug']]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter(name="storageSizeMib")
    def storage_size_mib(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_size_mib")

    @storage_size_mib.setter
    def storage_size_mib(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_size_mib", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of tag names to be applied to the database replica.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _DatabaseReplicaState:
    def __init__(__self__, *,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None,
                 private_host: Optional[pulumi.Input[str]] = None,
                 private_network_uuid: Optional[pulumi.Input[str]] = None,
                 private_uri: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[Union[str, 'Region']]] = None,
                 size: Optional[pulumi.Input[Union[str, 'DatabaseSlug']]] = None,
                 storage_size_mib: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 uri: Optional[pulumi.Input[str]] = None,
                 user: Optional[pulumi.Input[str]] = None,
                 uuid: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DatabaseReplica resources.
        :param pulumi.Input[str] cluster_id: The ID of the original source database cluster.
        :param pulumi.Input[str] database: Name of the replica's default database.
        :param pulumi.Input[str] host: Database replica's hostname.
        :param pulumi.Input[str] name: The name for the database replica.
        :param pulumi.Input[str] password: Password for the replica's default user.
        :param pulumi.Input[int] port: Network port that the database replica is listening on.
        :param pulumi.Input[str] private_host: Same as `host`, but only accessible from resources within the account and in the same region.
        :param pulumi.Input[str] private_network_uuid: The ID of the VPC where the database replica will be located.
        :param pulumi.Input[str] private_uri: Same as `uri`, but only accessible from resources within the account and in the same region.
        :param pulumi.Input[Union[str, 'Region']] region: DigitalOcean region where the replica will reside.
        :param pulumi.Input[Union[str, 'DatabaseSlug']] size: Database Droplet size associated with the replica (ex. `db-s-1vcpu-1gb`). Note that when resizing an existing replica, its size can only be increased. Decreasing its size is not supported.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag names to be applied to the database replica.
        :param pulumi.Input[str] uri: The full URI for connecting to the database replica.
        :param pulumi.Input[str] user: Username for the replica's default user.
        :param pulumi.Input[str] uuid: The UUID of the database replica. The uuid can be used to reference the database replica as the target database cluster in other resources. See example  "Create firewall rule for database replica" above.
        """
        if cluster_id is not None:
            pulumi.set(__self__, "cluster_id", cluster_id)
        if database is not None:
            pulumi.set(__self__, "database", database)
        if host is not None:
            pulumi.set(__self__, "host", host)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if port is not None:
            pulumi.set(__self__, "port", port)
        if private_host is not None:
            pulumi.set(__self__, "private_host", private_host)
        if private_network_uuid is not None:
            pulumi.set(__self__, "private_network_uuid", private_network_uuid)
        if private_uri is not None:
            pulumi.set(__self__, "private_uri", private_uri)
        if region is not None:
            pulumi.set(__self__, "region", region)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if storage_size_mib is not None:
            pulumi.set(__self__, "storage_size_mib", storage_size_mib)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if uri is not None:
            pulumi.set(__self__, "uri", uri)
        if user is not None:
            pulumi.set(__self__, "user", user)
        if uuid is not None:
            pulumi.set(__self__, "uuid", uuid)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the original source database cluster.
        """
        return pulumi.get(self, "cluster_id")

    @cluster_id.setter
    def cluster_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_id", value)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the replica's default database.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def host(self) -> Optional[pulumi.Input[str]]:
        """
        Database replica's hostname.
        """
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name for the database replica.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Password for the replica's default user.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        Network port that the database replica is listening on.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter(name="privateHost")
    def private_host(self) -> Optional[pulumi.Input[str]]:
        """
        Same as `host`, but only accessible from resources within the account and in the same region.
        """
        return pulumi.get(self, "private_host")

    @private_host.setter
    def private_host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_host", value)

    @property
    @pulumi.getter(name="privateNetworkUuid")
    def private_network_uuid(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the VPC where the database replica will be located.
        """
        return pulumi.get(self, "private_network_uuid")

    @private_network_uuid.setter
    def private_network_uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_network_uuid", value)

    @property
    @pulumi.getter(name="privateUri")
    def private_uri(self) -> Optional[pulumi.Input[str]]:
        """
        Same as `uri`, but only accessible from resources within the account and in the same region.
        """
        return pulumi.get(self, "private_uri")

    @private_uri.setter
    def private_uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_uri", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[Union[str, 'Region']]]:
        """
        DigitalOcean region where the replica will reside.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[Union[str, 'Region']]]):
        pulumi.set(self, "region", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[Union[str, 'DatabaseSlug']]]:
        """
        Database Droplet size associated with the replica (ex. `db-s-1vcpu-1gb`). Note that when resizing an existing replica, its size can only be increased. Decreasing its size is not supported.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[Union[str, 'DatabaseSlug']]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter(name="storageSizeMib")
    def storage_size_mib(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "storage_size_mib")

    @storage_size_mib.setter
    def storage_size_mib(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "storage_size_mib", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of tag names to be applied to the database replica.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def uri(self) -> Optional[pulumi.Input[str]]:
        """
        The full URI for connecting to the database replica.
        """
        return pulumi.get(self, "uri")

    @uri.setter
    def uri(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uri", value)

    @property
    @pulumi.getter
    def user(self) -> Optional[pulumi.Input[str]]:
        """
        Username for the replica's default user.
        """
        return pulumi.get(self, "user")

    @user.setter
    def user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user", value)

    @property
    @pulumi.getter
    def uuid(self) -> Optional[pulumi.Input[str]]:
        """
        The UUID of the database replica. The uuid can be used to reference the database replica as the target database cluster in other resources. See example  "Create firewall rule for database replica" above.
        """
        return pulumi.get(self, "uuid")

    @uuid.setter
    def uuid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uuid", value)


class DatabaseReplica(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_network_uuid: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[Union[str, 'Region']]] = None,
                 size: Optional[pulumi.Input[Union[str, 'DatabaseSlug']]] = None,
                 storage_size_mib: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a DigitalOcean database replica resource.

        ## Example Usage

        ### Create a new PostgreSQL database replica
        ```python
        import pulumi
        import pulumi_digitalocean as digitalocean

        postgres_example = digitalocean.DatabaseCluster("postgres-example",
            engine="pg",
            version="15",
            size=digitalocean.DatabaseSlug.D_B_1_VPCU1_GB,
            region=digitalocean.Region.NYC1,
            node_count=1)
        replica_example = digitalocean.DatabaseReplica("replica-example",
            cluster_id=postgres_example.id,
            size=digitalocean.DatabaseSlug.D_B_1_VPCU1_GB,
            region=digitalocean.Region.NYC1)
        pulumi.export("uUID", replica_example.uuid)
        # Create firewall rule for database replica
        example_fw = digitalocean.DatabaseFirewall("example-fw",
            cluster_id=replica_example.uuid,
            rules=[digitalocean.DatabaseFirewallRuleArgs(
                type="ip_addr",
                value="192.168.1.1",
            )])
        ```

        ## Import

        Database replicas can be imported using the `id` of the source database cluster

        and the `name` of the replica joined with a comma. For example:

        ```sh
        $ pulumi import digitalocean:index/databaseReplica:DatabaseReplica read-replica 245bcfd0-7f31-4ce6-a2bc-475a116cca97,read-replica
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: The ID of the original source database cluster.
        :param pulumi.Input[str] name: The name for the database replica.
        :param pulumi.Input[str] private_network_uuid: The ID of the VPC where the database replica will be located.
        :param pulumi.Input[Union[str, 'Region']] region: DigitalOcean region where the replica will reside.
        :param pulumi.Input[Union[str, 'DatabaseSlug']] size: Database Droplet size associated with the replica (ex. `db-s-1vcpu-1gb`). Note that when resizing an existing replica, its size can only be increased. Decreasing its size is not supported.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag names to be applied to the database replica.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DatabaseReplicaArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a DigitalOcean database replica resource.

        ## Example Usage

        ### Create a new PostgreSQL database replica
        ```python
        import pulumi
        import pulumi_digitalocean as digitalocean

        postgres_example = digitalocean.DatabaseCluster("postgres-example",
            engine="pg",
            version="15",
            size=digitalocean.DatabaseSlug.D_B_1_VPCU1_GB,
            region=digitalocean.Region.NYC1,
            node_count=1)
        replica_example = digitalocean.DatabaseReplica("replica-example",
            cluster_id=postgres_example.id,
            size=digitalocean.DatabaseSlug.D_B_1_VPCU1_GB,
            region=digitalocean.Region.NYC1)
        pulumi.export("uUID", replica_example.uuid)
        # Create firewall rule for database replica
        example_fw = digitalocean.DatabaseFirewall("example-fw",
            cluster_id=replica_example.uuid,
            rules=[digitalocean.DatabaseFirewallRuleArgs(
                type="ip_addr",
                value="192.168.1.1",
            )])
        ```

        ## Import

        Database replicas can be imported using the `id` of the source database cluster

        and the `name` of the replica joined with a comma. For example:

        ```sh
        $ pulumi import digitalocean:index/databaseReplica:DatabaseReplica read-replica 245bcfd0-7f31-4ce6-a2bc-475a116cca97,read-replica
        ```

        :param str resource_name: The name of the resource.
        :param DatabaseReplicaArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DatabaseReplicaArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_network_uuid: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[Union[str, 'Region']]] = None,
                 size: Optional[pulumi.Input[Union[str, 'DatabaseSlug']]] = None,
                 storage_size_mib: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DatabaseReplicaArgs.__new__(DatabaseReplicaArgs)

            if cluster_id is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_id'")
            __props__.__dict__["cluster_id"] = cluster_id
            __props__.__dict__["name"] = name
            __props__.__dict__["private_network_uuid"] = private_network_uuid
            __props__.__dict__["region"] = region
            __props__.__dict__["size"] = size
            __props__.__dict__["storage_size_mib"] = storage_size_mib
            __props__.__dict__["tags"] = tags
            __props__.__dict__["database"] = None
            __props__.__dict__["host"] = None
            __props__.__dict__["password"] = None
            __props__.__dict__["port"] = None
            __props__.__dict__["private_host"] = None
            __props__.__dict__["private_uri"] = None
            __props__.__dict__["uri"] = None
            __props__.__dict__["user"] = None
            __props__.__dict__["uuid"] = None
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["password", "privateUri", "uri"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(DatabaseReplica, __self__).__init__(
            'digitalocean:index/databaseReplica:DatabaseReplica',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cluster_id: Optional[pulumi.Input[str]] = None,
            database: Optional[pulumi.Input[str]] = None,
            host: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            port: Optional[pulumi.Input[int]] = None,
            private_host: Optional[pulumi.Input[str]] = None,
            private_network_uuid: Optional[pulumi.Input[str]] = None,
            private_uri: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[Union[str, 'Region']]] = None,
            size: Optional[pulumi.Input[Union[str, 'DatabaseSlug']]] = None,
            storage_size_mib: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            uri: Optional[pulumi.Input[str]] = None,
            user: Optional[pulumi.Input[str]] = None,
            uuid: Optional[pulumi.Input[str]] = None) -> 'DatabaseReplica':
        """
        Get an existing DatabaseReplica resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: The ID of the original source database cluster.
        :param pulumi.Input[str] database: Name of the replica's default database.
        :param pulumi.Input[str] host: Database replica's hostname.
        :param pulumi.Input[str] name: The name for the database replica.
        :param pulumi.Input[str] password: Password for the replica's default user.
        :param pulumi.Input[int] port: Network port that the database replica is listening on.
        :param pulumi.Input[str] private_host: Same as `host`, but only accessible from resources within the account and in the same region.
        :param pulumi.Input[str] private_network_uuid: The ID of the VPC where the database replica will be located.
        :param pulumi.Input[str] private_uri: Same as `uri`, but only accessible from resources within the account and in the same region.
        :param pulumi.Input[Union[str, 'Region']] region: DigitalOcean region where the replica will reside.
        :param pulumi.Input[Union[str, 'DatabaseSlug']] size: Database Droplet size associated with the replica (ex. `db-s-1vcpu-1gb`). Note that when resizing an existing replica, its size can only be increased. Decreasing its size is not supported.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag names to be applied to the database replica.
        :param pulumi.Input[str] uri: The full URI for connecting to the database replica.
        :param pulumi.Input[str] user: Username for the replica's default user.
        :param pulumi.Input[str] uuid: The UUID of the database replica. The uuid can be used to reference the database replica as the target database cluster in other resources. See example  "Create firewall rule for database replica" above.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DatabaseReplicaState.__new__(_DatabaseReplicaState)

        __props__.__dict__["cluster_id"] = cluster_id
        __props__.__dict__["database"] = database
        __props__.__dict__["host"] = host
        __props__.__dict__["name"] = name
        __props__.__dict__["password"] = password
        __props__.__dict__["port"] = port
        __props__.__dict__["private_host"] = private_host
        __props__.__dict__["private_network_uuid"] = private_network_uuid
        __props__.__dict__["private_uri"] = private_uri
        __props__.__dict__["region"] = region
        __props__.__dict__["size"] = size
        __props__.__dict__["storage_size_mib"] = storage_size_mib
        __props__.__dict__["tags"] = tags
        __props__.__dict__["uri"] = uri
        __props__.__dict__["user"] = user
        __props__.__dict__["uuid"] = uuid
        return DatabaseReplica(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Output[str]:
        """
        The ID of the original source database cluster.
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        Name of the replica's default database.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def host(self) -> pulumi.Output[str]:
        """
        Database replica's hostname.
        """
        return pulumi.get(self, "host")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name for the database replica.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        Password for the replica's default user.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[int]:
        """
        Network port that the database replica is listening on.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="privateHost")
    def private_host(self) -> pulumi.Output[str]:
        """
        Same as `host`, but only accessible from resources within the account and in the same region.
        """
        return pulumi.get(self, "private_host")

    @property
    @pulumi.getter(name="privateNetworkUuid")
    def private_network_uuid(self) -> pulumi.Output[str]:
        """
        The ID of the VPC where the database replica will be located.
        """
        return pulumi.get(self, "private_network_uuid")

    @property
    @pulumi.getter(name="privateUri")
    def private_uri(self) -> pulumi.Output[str]:
        """
        Same as `uri`, but only accessible from resources within the account and in the same region.
        """
        return pulumi.get(self, "private_uri")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[Optional[str]]:
        """
        DigitalOcean region where the replica will reside.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def size(self) -> pulumi.Output[Optional[str]]:
        """
        Database Droplet size associated with the replica (ex. `db-s-1vcpu-1gb`). Note that when resizing an existing replica, its size can only be increased. Decreasing its size is not supported.
        """
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="storageSizeMib")
    def storage_size_mib(self) -> pulumi.Output[str]:
        return pulumi.get(self, "storage_size_mib")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of tag names to be applied to the database replica.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def uri(self) -> pulumi.Output[str]:
        """
        The full URI for connecting to the database replica.
        """
        return pulumi.get(self, "uri")

    @property
    @pulumi.getter
    def user(self) -> pulumi.Output[str]:
        """
        Username for the replica's default user.
        """
        return pulumi.get(self, "user")

    @property
    @pulumi.getter
    def uuid(self) -> pulumi.Output[str]:
        """
        The UUID of the database replica. The uuid can be used to reference the database replica as the target database cluster in other resources. See example  "Create firewall rule for database replica" above.
        """
        return pulumi.get(self, "uuid")

