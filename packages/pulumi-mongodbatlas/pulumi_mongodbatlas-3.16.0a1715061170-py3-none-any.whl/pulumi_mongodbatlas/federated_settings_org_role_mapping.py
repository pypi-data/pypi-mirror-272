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

__all__ = ['FederatedSettingsOrgRoleMappingArgs', 'FederatedSettingsOrgRoleMapping']

@pulumi.input_type
class FederatedSettingsOrgRoleMappingArgs:
    def __init__(__self__, *,
                 external_group_name: pulumi.Input[str],
                 federation_settings_id: pulumi.Input[str],
                 org_id: pulumi.Input[str],
                 role_assignments: pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]):
        """
        The set of arguments for constructing a FederatedSettingsOrgRoleMapping resource.
        :param pulumi.Input[str] external_group_name: Unique human-readable label that identifies the identity provider group to which this role mapping applies.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]] role_assignments: Atlas roles and the unique identifiers of the groups and organizations associated with each role.
        """
        pulumi.set(__self__, "external_group_name", external_group_name)
        pulumi.set(__self__, "federation_settings_id", federation_settings_id)
        pulumi.set(__self__, "org_id", org_id)
        pulumi.set(__self__, "role_assignments", role_assignments)

    @property
    @pulumi.getter(name="externalGroupName")
    def external_group_name(self) -> pulumi.Input[str]:
        """
        Unique human-readable label that identifies the identity provider group to which this role mapping applies.
        """
        return pulumi.get(self, "external_group_name")

    @external_group_name.setter
    def external_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "external_group_name", value)

    @property
    @pulumi.getter(name="federationSettingsId")
    def federation_settings_id(self) -> pulumi.Input[str]:
        """
        Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        """
        return pulumi.get(self, "federation_settings_id")

    @federation_settings_id.setter
    def federation_settings_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "federation_settings_id", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Input[str]:
        """
        Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="roleAssignments")
    def role_assignments(self) -> pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]:
        """
        Atlas roles and the unique identifiers of the groups and organizations associated with each role.
        """
        return pulumi.get(self, "role_assignments")

    @role_assignments.setter
    def role_assignments(self, value: pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]):
        pulumi.set(self, "role_assignments", value)


@pulumi.input_type
class _FederatedSettingsOrgRoleMappingState:
    def __init__(__self__, *,
                 external_group_name: Optional[pulumi.Input[str]] = None,
                 federation_settings_id: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role_assignments: Optional[pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]] = None):
        """
        Input properties used for looking up and filtering FederatedSettingsOrgRoleMapping resources.
        :param pulumi.Input[str] external_group_name: Unique human-readable label that identifies the identity provider group to which this role mapping applies.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]] role_assignments: Atlas roles and the unique identifiers of the groups and organizations associated with each role.
        """
        if external_group_name is not None:
            pulumi.set(__self__, "external_group_name", external_group_name)
        if federation_settings_id is not None:
            pulumi.set(__self__, "federation_settings_id", federation_settings_id)
        if org_id is not None:
            pulumi.set(__self__, "org_id", org_id)
        if role_assignments is not None:
            pulumi.set(__self__, "role_assignments", role_assignments)

    @property
    @pulumi.getter(name="externalGroupName")
    def external_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Unique human-readable label that identifies the identity provider group to which this role mapping applies.
        """
        return pulumi.get(self, "external_group_name")

    @external_group_name.setter
    def external_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "external_group_name", value)

    @property
    @pulumi.getter(name="federationSettingsId")
    def federation_settings_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        """
        return pulumi.get(self, "federation_settings_id")

    @federation_settings_id.setter
    def federation_settings_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "federation_settings_id", value)

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> Optional[pulumi.Input[str]]:
        """
        Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        """
        return pulumi.get(self, "org_id")

    @org_id.setter
    def org_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "org_id", value)

    @property
    @pulumi.getter(name="roleAssignments")
    def role_assignments(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]]:
        """
        Atlas roles and the unique identifiers of the groups and organizations associated with each role.
        """
        return pulumi.get(self, "role_assignments")

    @role_assignments.setter
    def role_assignments(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]]):
        pulumi.set(self, "role_assignments", value)


class FederatedSettingsOrgRoleMapping(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 external_group_name: Optional[pulumi.Input[str]] = None,
                 federation_settings_id: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role_assignments: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]]] = None,
                 __props__=None):
        """
        `FederatedSettingsOrgRoleMapping` provides an Role Mapping resource. This allows organization role mapping to be created.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        org_group_role_mapping_import = mongodbatlas.FederatedSettingsOrgRoleMapping("org_group_role_mapping_import",
            federation_settings_id="627a9687f7f7f7f774de306f14",
            org_id="627a9683e7f7f7ff7fe306f14",
            external_group_name="myGrouptest",
            role_assignments=[
                mongodbatlas.FederatedSettingsOrgRoleMappingRoleAssignmentArgs(
                    org_id="627a9683e7f7f7ff7fe306f14",
                    roles=[
                        "ORG_MEMBER",
                        "ORG_GROUP_CREATOR",
                        "ORG_BILLING_ADMIN",
                    ],
                ),
                mongodbatlas.FederatedSettingsOrgRoleMappingRoleAssignmentArgs(
                    group_id="628aa20d7f7f7f7f7098b81b8",
                    roles=[
                        "GROUP_OWNER",
                        "GROUP_DATA_ACCESS_ADMIN",
                        "GROUP_SEARCH_INDEX_EDITOR",
                        "GROUP_DATA_ACCESS_READ_ONLY",
                    ],
                ),
                mongodbatlas.FederatedSettingsOrgRoleMappingRoleAssignmentArgs(
                    group_id="628aa20d7f7f7f7f7078b81b8",
                    roles=[
                        "GROUP_OWNER",
                        "GROUP_DATA_ACCESS_ADMIN",
                        "GROUP_SEARCH_INDEX_EDITOR",
                        "GROUP_DATA_ACCESS_READ_ONLY",
                        "GROUP_DATA_ACCESS_READ_WRITE",
                    ],
                ),
            ])
        ```

        ## Import

        FederatedSettingsOrgRoleMapping can be imported using federation_settings_id-org_id-role_mapping_id, e.g.

        ```sh
        $ pulumi import mongodbatlas:index/federatedSettingsOrgRoleMapping:FederatedSettingsOrgRoleMapping org_group_role_mapping_import 6287a663c7f7f7f71c441c6c-627a96837f7f7f7e306f14-628ae97f7f7468ea3727
        ```
        For more information see: [MongoDB Atlas API Reference.](https://www.mongodb.com/docs/atlas/reference/api/federation-configuration/)

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] external_group_name: Unique human-readable label that identifies the identity provider group to which this role mapping applies.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]] role_assignments: Atlas roles and the unique identifiers of the groups and organizations associated with each role.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FederatedSettingsOrgRoleMappingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        `FederatedSettingsOrgRoleMapping` provides an Role Mapping resource. This allows organization role mapping to be created.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_mongodbatlas as mongodbatlas

        org_group_role_mapping_import = mongodbatlas.FederatedSettingsOrgRoleMapping("org_group_role_mapping_import",
            federation_settings_id="627a9687f7f7f7f774de306f14",
            org_id="627a9683e7f7f7ff7fe306f14",
            external_group_name="myGrouptest",
            role_assignments=[
                mongodbatlas.FederatedSettingsOrgRoleMappingRoleAssignmentArgs(
                    org_id="627a9683e7f7f7ff7fe306f14",
                    roles=[
                        "ORG_MEMBER",
                        "ORG_GROUP_CREATOR",
                        "ORG_BILLING_ADMIN",
                    ],
                ),
                mongodbatlas.FederatedSettingsOrgRoleMappingRoleAssignmentArgs(
                    group_id="628aa20d7f7f7f7f7098b81b8",
                    roles=[
                        "GROUP_OWNER",
                        "GROUP_DATA_ACCESS_ADMIN",
                        "GROUP_SEARCH_INDEX_EDITOR",
                        "GROUP_DATA_ACCESS_READ_ONLY",
                    ],
                ),
                mongodbatlas.FederatedSettingsOrgRoleMappingRoleAssignmentArgs(
                    group_id="628aa20d7f7f7f7f7078b81b8",
                    roles=[
                        "GROUP_OWNER",
                        "GROUP_DATA_ACCESS_ADMIN",
                        "GROUP_SEARCH_INDEX_EDITOR",
                        "GROUP_DATA_ACCESS_READ_ONLY",
                        "GROUP_DATA_ACCESS_READ_WRITE",
                    ],
                ),
            ])
        ```

        ## Import

        FederatedSettingsOrgRoleMapping can be imported using federation_settings_id-org_id-role_mapping_id, e.g.

        ```sh
        $ pulumi import mongodbatlas:index/federatedSettingsOrgRoleMapping:FederatedSettingsOrgRoleMapping org_group_role_mapping_import 6287a663c7f7f7f71c441c6c-627a96837f7f7f7e306f14-628ae97f7f7468ea3727
        ```
        For more information see: [MongoDB Atlas API Reference.](https://www.mongodb.com/docs/atlas/reference/api/federation-configuration/)

        :param str resource_name: The name of the resource.
        :param FederatedSettingsOrgRoleMappingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FederatedSettingsOrgRoleMappingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 external_group_name: Optional[pulumi.Input[str]] = None,
                 federation_settings_id: Optional[pulumi.Input[str]] = None,
                 org_id: Optional[pulumi.Input[str]] = None,
                 role_assignments: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FederatedSettingsOrgRoleMappingArgs.__new__(FederatedSettingsOrgRoleMappingArgs)

            if external_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'external_group_name'")
            __props__.__dict__["external_group_name"] = external_group_name
            if federation_settings_id is None and not opts.urn:
                raise TypeError("Missing required property 'federation_settings_id'")
            __props__.__dict__["federation_settings_id"] = federation_settings_id
            if org_id is None and not opts.urn:
                raise TypeError("Missing required property 'org_id'")
            __props__.__dict__["org_id"] = org_id
            if role_assignments is None and not opts.urn:
                raise TypeError("Missing required property 'role_assignments'")
            __props__.__dict__["role_assignments"] = role_assignments
        super(FederatedSettingsOrgRoleMapping, __self__).__init__(
            'mongodbatlas:index/federatedSettingsOrgRoleMapping:FederatedSettingsOrgRoleMapping',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            external_group_name: Optional[pulumi.Input[str]] = None,
            federation_settings_id: Optional[pulumi.Input[str]] = None,
            org_id: Optional[pulumi.Input[str]] = None,
            role_assignments: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]]] = None) -> 'FederatedSettingsOrgRoleMapping':
        """
        Get an existing FederatedSettingsOrgRoleMapping resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] external_group_name: Unique human-readable label that identifies the identity provider group to which this role mapping applies.
        :param pulumi.Input[str] federation_settings_id: Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        :param pulumi.Input[str] org_id: Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['FederatedSettingsOrgRoleMappingRoleAssignmentArgs']]]] role_assignments: Atlas roles and the unique identifiers of the groups and organizations associated with each role.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FederatedSettingsOrgRoleMappingState.__new__(_FederatedSettingsOrgRoleMappingState)

        __props__.__dict__["external_group_name"] = external_group_name
        __props__.__dict__["federation_settings_id"] = federation_settings_id
        __props__.__dict__["org_id"] = org_id
        __props__.__dict__["role_assignments"] = role_assignments
        return FederatedSettingsOrgRoleMapping(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="externalGroupName")
    def external_group_name(self) -> pulumi.Output[str]:
        """
        Unique human-readable label that identifies the identity provider group to which this role mapping applies.
        """
        return pulumi.get(self, "external_group_name")

    @property
    @pulumi.getter(name="federationSettingsId")
    def federation_settings_id(self) -> pulumi.Output[str]:
        """
        Unique 24-hexadecimal digit string that identifies the federated authentication configuration.
        """
        return pulumi.get(self, "federation_settings_id")

    @property
    @pulumi.getter(name="orgId")
    def org_id(self) -> pulumi.Output[str]:
        """
        Unique 24-hexadecimal digit string that identifies the organization that contains your projects.
        """
        return pulumi.get(self, "org_id")

    @property
    @pulumi.getter(name="roleAssignments")
    def role_assignments(self) -> pulumi.Output[Sequence['outputs.FederatedSettingsOrgRoleMappingRoleAssignment']]:
        """
        Atlas roles and the unique identifiers of the groups and organizations associated with each role.
        """
        return pulumi.get(self, "role_assignments")

