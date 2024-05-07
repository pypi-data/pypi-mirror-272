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
    'GetUserResult',
    'AwaitableGetUserResult',
    'get_user',
    'get_user_output',
]

@pulumi.output_type
class GetUserResult:
    """
    A collection of values returned by getUser.
    """
    def __init__(__self__, description=None, email=None, id=None, job_title=None, name=None, role=None, time_zone=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if email and not isinstance(email, str):
            raise TypeError("Expected argument 'email' to be a str")
        pulumi.set(__self__, "email", email)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if job_title and not isinstance(job_title, str):
            raise TypeError("Expected argument 'job_title' to be a str")
        pulumi.set(__self__, "job_title", job_title)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role and not isinstance(role, str):
            raise TypeError("Expected argument 'role' to be a str")
        pulumi.set(__self__, "role", role)
        if time_zone and not isinstance(time_zone, str):
            raise TypeError("Expected argument 'time_zone' to be a str")
        pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        The human-friendly description of the found user.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def email(self) -> str:
        return pulumi.get(self, "email")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="jobTitle")
    def job_title(self) -> str:
        """
        The job title of the found user.
        """
        return pulumi.get(self, "job_title")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The short name of the found user.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def role(self) -> str:
        """
        The role of the found user.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> str:
        """
        The timezone of the found user.
        """
        return pulumi.get(self, "time_zone")


class AwaitableGetUserResult(GetUserResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserResult(
            description=self.description,
            email=self.email,
            id=self.id,
            job_title=self.job_title,
            name=self.name,
            role=self.role,
            time_zone=self.time_zone)


def get_user(email: Optional[str] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserResult:
    """
    Use this data source to get information about a specific [user](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODIzMw-list-users) that you can use for other PagerDuty resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    me = pagerduty.get_user(email="me@example.com")
    foo = pagerduty.EscalationPolicy("foo",
        name="Engineering Escalation Policy",
        num_loops=2,
        rules=[pagerduty.EscalationPolicyRuleArgs(
            escalation_delay_in_minutes=10,
            targets=[pagerduty.EscalationPolicyRuleTargetArgs(
                type="user",
                id=me.id,
            )],
        )])
    ```


    :param str email: The email to use to find a user in the PagerDuty API.
    """
    __args__ = dict()
    __args__['email'] = email
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('pagerduty:index/getUser:getUser', __args__, opts=opts, typ=GetUserResult).value

    return AwaitableGetUserResult(
        description=pulumi.get(__ret__, 'description'),
        email=pulumi.get(__ret__, 'email'),
        id=pulumi.get(__ret__, 'id'),
        job_title=pulumi.get(__ret__, 'job_title'),
        name=pulumi.get(__ret__, 'name'),
        role=pulumi.get(__ret__, 'role'),
        time_zone=pulumi.get(__ret__, 'time_zone'))


@_utilities.lift_output_func(get_user)
def get_user_output(email: Optional[pulumi.Input[str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserResult]:
    """
    Use this data source to get information about a specific [user](https://developer.pagerduty.com/api-reference/b3A6Mjc0ODIzMw-list-users) that you can use for other PagerDuty resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    me = pagerduty.get_user(email="me@example.com")
    foo = pagerduty.EscalationPolicy("foo",
        name="Engineering Escalation Policy",
        num_loops=2,
        rules=[pagerduty.EscalationPolicyRuleArgs(
            escalation_delay_in_minutes=10,
            targets=[pagerduty.EscalationPolicyRuleTargetArgs(
                type="user",
                id=me.id,
            )],
        )])
    ```


    :param str email: The email to use to find a user in the PagerDuty API.
    """
    ...
