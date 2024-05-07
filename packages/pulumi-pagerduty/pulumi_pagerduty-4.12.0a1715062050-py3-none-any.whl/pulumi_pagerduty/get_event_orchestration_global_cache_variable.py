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
    'GetEventOrchestrationGlobalCacheVariableResult',
    'AwaitableGetEventOrchestrationGlobalCacheVariableResult',
    'get_event_orchestration_global_cache_variable',
    'get_event_orchestration_global_cache_variable_output',
]

@pulumi.output_type
class GetEventOrchestrationGlobalCacheVariableResult:
    """
    A collection of values returned by getEventOrchestrationGlobalCacheVariable.
    """
    def __init__(__self__, conditions=None, configurations=None, disabled=None, event_orchestration=None, id=None, name=None):
        if conditions and not isinstance(conditions, list):
            raise TypeError("Expected argument 'conditions' to be a list")
        pulumi.set(__self__, "conditions", conditions)
        if configurations and not isinstance(configurations, list):
            raise TypeError("Expected argument 'configurations' to be a list")
        pulumi.set(__self__, "configurations", configurations)
        if disabled and not isinstance(disabled, bool):
            raise TypeError("Expected argument 'disabled' to be a bool")
        pulumi.set(__self__, "disabled", disabled)
        if event_orchestration and not isinstance(event_orchestration, str):
            raise TypeError("Expected argument 'event_orchestration' to be a str")
        pulumi.set(__self__, "event_orchestration", event_orchestration)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def conditions(self) -> Sequence['outputs.GetEventOrchestrationGlobalCacheVariableConditionResult']:
        """
        Conditions to be evaluated in order to determine whether or not to update the Cache Variable's stored value.
        """
        return pulumi.get(self, "conditions")

    @property
    @pulumi.getter
    def configurations(self) -> Sequence['outputs.GetEventOrchestrationGlobalCacheVariableConfigurationResult']:
        """
        A configuration object to define what and how values will be stored in the Cache Variable.
        """
        return pulumi.get(self, "configurations")

    @property
    @pulumi.getter
    def disabled(self) -> bool:
        """
        Indicates whether the Cache Variable is disabled and would therefore not be evaluated.
        """
        return pulumi.get(self, "disabled")

    @property
    @pulumi.getter(name="eventOrchestration")
    def event_orchestration(self) -> str:
        return pulumi.get(self, "event_orchestration")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")


class AwaitableGetEventOrchestrationGlobalCacheVariableResult(GetEventOrchestrationGlobalCacheVariableResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventOrchestrationGlobalCacheVariableResult(
            conditions=self.conditions,
            configurations=self.configurations,
            disabled=self.disabled,
            event_orchestration=self.event_orchestration,
            id=self.id,
            name=self.name)


def get_event_orchestration_global_cache_variable(event_orchestration: Optional[str] = None,
                                                  id: Optional[str] = None,
                                                  name: Optional[str] = None,
                                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventOrchestrationGlobalCacheVariableResult:
    """
    Use this data source to get information about a specific [Cache Variable](https://support.pagerduty.com/docs/event-orchestration-variables) for a Global Event Orchestration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    event_orchestration = pagerduty.EventOrchestration("event_orchestration", name="Test Event Orchestration")
    cache_variable = pagerduty.get_event_orchestration_global_cache_variable_output(event_orchestration=event_orchestration.id,
        name="example_cache_variable")
    ```


    :param str event_orchestration: ID of the Global Event Orchestration to which this Cache Variable belongs.
    :param str id: ID of the Cache Variable associated with the Global Event Orchestration. Specify either `id` or `name`. If both are specified `id` takes precedence.
    :param str name: Name of the Cache Variable associated with the Global Event Orchestration. Specify either `id` or `name`. If both are specified `id` takes precedence.
    """
    __args__ = dict()
    __args__['eventOrchestration'] = event_orchestration
    __args__['id'] = id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('pagerduty:index/getEventOrchestrationGlobalCacheVariable:getEventOrchestrationGlobalCacheVariable', __args__, opts=opts, typ=GetEventOrchestrationGlobalCacheVariableResult).value

    return AwaitableGetEventOrchestrationGlobalCacheVariableResult(
        conditions=pulumi.get(__ret__, 'conditions'),
        configurations=pulumi.get(__ret__, 'configurations'),
        disabled=pulumi.get(__ret__, 'disabled'),
        event_orchestration=pulumi.get(__ret__, 'event_orchestration'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'))


@_utilities.lift_output_func(get_event_orchestration_global_cache_variable)
def get_event_orchestration_global_cache_variable_output(event_orchestration: Optional[pulumi.Input[str]] = None,
                                                         id: Optional[pulumi.Input[Optional[str]]] = None,
                                                         name: Optional[pulumi.Input[Optional[str]]] = None,
                                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventOrchestrationGlobalCacheVariableResult]:
    """
    Use this data source to get information about a specific [Cache Variable](https://support.pagerduty.com/docs/event-orchestration-variables) for a Global Event Orchestration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    event_orchestration = pagerduty.EventOrchestration("event_orchestration", name="Test Event Orchestration")
    cache_variable = pagerduty.get_event_orchestration_global_cache_variable_output(event_orchestration=event_orchestration.id,
        name="example_cache_variable")
    ```


    :param str event_orchestration: ID of the Global Event Orchestration to which this Cache Variable belongs.
    :param str id: ID of the Cache Variable associated with the Global Event Orchestration. Specify either `id` or `name`. If both are specified `id` takes precedence.
    :param str name: Name of the Cache Variable associated with the Global Event Orchestration. Specify either `id` or `name`. If both are specified `id` takes precedence.
    """
    ...
