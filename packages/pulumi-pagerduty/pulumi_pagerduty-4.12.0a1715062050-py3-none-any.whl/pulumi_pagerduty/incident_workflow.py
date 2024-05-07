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

__all__ = ['IncidentWorkflowArgs', 'IncidentWorkflow']

@pulumi.input_type
class IncidentWorkflowArgs:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 steps: Optional[pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]]] = None,
                 team: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a IncidentWorkflow resource.
        :param pulumi.Input[str] description: The description of the workflow.
        :param pulumi.Input[str] name: The name of the workflow.
        :param pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]] steps: The steps in the workflow.
        :param pulumi.Input[str] team: A team ID. If specified then workflow edit permissions will be scoped to members of this team.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if steps is not None:
            pulumi.set(__self__, "steps", steps)
        if team is not None:
            pulumi.set(__self__, "team", team)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the workflow.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the workflow.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def steps(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]]]:
        """
        The steps in the workflow.
        """
        return pulumi.get(self, "steps")

    @steps.setter
    def steps(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]]]):
        pulumi.set(self, "steps", value)

    @property
    @pulumi.getter
    def team(self) -> Optional[pulumi.Input[str]]:
        """
        A team ID. If specified then workflow edit permissions will be scoped to members of this team.
        """
        return pulumi.get(self, "team")

    @team.setter
    def team(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team", value)


@pulumi.input_type
class _IncidentWorkflowState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 steps: Optional[pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]]] = None,
                 team: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IncidentWorkflow resources.
        :param pulumi.Input[str] description: The description of the workflow.
        :param pulumi.Input[str] name: The name of the workflow.
        :param pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]] steps: The steps in the workflow.
        :param pulumi.Input[str] team: A team ID. If specified then workflow edit permissions will be scoped to members of this team.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if steps is not None:
            pulumi.set(__self__, "steps", steps)
        if team is not None:
            pulumi.set(__self__, "team", team)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the workflow.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the workflow.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def steps(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]]]:
        """
        The steps in the workflow.
        """
        return pulumi.get(self, "steps")

    @steps.setter
    def steps(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['IncidentWorkflowStepArgs']]]]):
        pulumi.set(self, "steps", value)

    @property
    @pulumi.getter
    def team(self) -> Optional[pulumi.Input[str]]:
        """
        A team ID. If specified then workflow edit permissions will be scoped to members of this team.
        """
        return pulumi.get(self, "team")

    @team.setter
    def team(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "team", value)


class IncidentWorkflow(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 steps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IncidentWorkflowStepArgs']]]]] = None,
                 team: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        An [Incident Workflow](https://support.pagerduty.com/docs/incident-workflows) is a series of steps which can be executed on an incident.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        my_first_workflow = pagerduty.IncidentWorkflow("my_first_workflow",
            name="Example Incident Workflow",
            description="This Incident Workflow is an example",
            steps=[pagerduty.IncidentWorkflowStepArgs(
                name="Send Status Update",
                action="pagerduty.com:incident-workflows:send-status-update:1",
                inputs=[pagerduty.IncidentWorkflowStepInputArgs(
                    name="Message",
                    value="Example status message sent on {{current_date}}",
                )],
            )])
        ```

        ## Import

        Incident workflows can be imported using the `id`, e.g.

        ```sh
        $ pulumi import pagerduty:index/incidentWorkflow:IncidentWorkflow major_incident_workflow PLBP09X
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the workflow.
        :param pulumi.Input[str] name: The name of the workflow.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IncidentWorkflowStepArgs']]]] steps: The steps in the workflow.
        :param pulumi.Input[str] team: A team ID. If specified then workflow edit permissions will be scoped to members of this team.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[IncidentWorkflowArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        An [Incident Workflow](https://support.pagerduty.com/docs/incident-workflows) is a series of steps which can be executed on an incident.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        my_first_workflow = pagerduty.IncidentWorkflow("my_first_workflow",
            name="Example Incident Workflow",
            description="This Incident Workflow is an example",
            steps=[pagerduty.IncidentWorkflowStepArgs(
                name="Send Status Update",
                action="pagerduty.com:incident-workflows:send-status-update:1",
                inputs=[pagerduty.IncidentWorkflowStepInputArgs(
                    name="Message",
                    value="Example status message sent on {{current_date}}",
                )],
            )])
        ```

        ## Import

        Incident workflows can be imported using the `id`, e.g.

        ```sh
        $ pulumi import pagerduty:index/incidentWorkflow:IncidentWorkflow major_incident_workflow PLBP09X
        ```

        :param str resource_name: The name of the resource.
        :param IncidentWorkflowArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IncidentWorkflowArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 steps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IncidentWorkflowStepArgs']]]]] = None,
                 team: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IncidentWorkflowArgs.__new__(IncidentWorkflowArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["steps"] = steps
            __props__.__dict__["team"] = team
        super(IncidentWorkflow, __self__).__init__(
            'pagerduty:index/incidentWorkflow:IncidentWorkflow',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            steps: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IncidentWorkflowStepArgs']]]]] = None,
            team: Optional[pulumi.Input[str]] = None) -> 'IncidentWorkflow':
        """
        Get an existing IncidentWorkflow resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the workflow.
        :param pulumi.Input[str] name: The name of the workflow.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['IncidentWorkflowStepArgs']]]] steps: The steps in the workflow.
        :param pulumi.Input[str] team: A team ID. If specified then workflow edit permissions will be scoped to members of this team.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IncidentWorkflowState.__new__(_IncidentWorkflowState)

        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["steps"] = steps
        __props__.__dict__["team"] = team
        return IncidentWorkflow(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the workflow.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the workflow.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def steps(self) -> pulumi.Output[Sequence['outputs.IncidentWorkflowStep']]:
        """
        The steps in the workflow.
        """
        return pulumi.get(self, "steps")

    @property
    @pulumi.getter
    def team(self) -> pulumi.Output[Optional[str]]:
        """
        A team ID. If specified then workflow edit permissions will be scoped to members of this team.
        """
        return pulumi.get(self, "team")

