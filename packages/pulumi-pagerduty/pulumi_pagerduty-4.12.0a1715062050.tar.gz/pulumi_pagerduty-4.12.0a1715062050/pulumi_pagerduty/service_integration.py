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

__all__ = ['ServiceIntegrationArgs', 'ServiceIntegration']

@pulumi.input_type
class ServiceIntegrationArgs:
    def __init__(__self__, *,
                 service: pulumi.Input[str],
                 email_filter_mode: Optional[pulumi.Input[str]] = None,
                 email_filters: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailFilterArgs']]]] = None,
                 email_incident_creation: Optional[pulumi.Input[str]] = None,
                 email_parsers: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailParserArgs']]]] = None,
                 email_parsing_fallback: Optional[pulumi.Input[str]] = None,
                 integration_email: Optional[pulumi.Input[str]] = None,
                 integration_key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vendor: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ServiceIntegration resource.
        :param pulumi.Input[str] integration_email: This is the unique fully-qualified email address used for routing emails to this integration for processing.
        :param pulumi.Input[str] integration_key: This is the unique key used to route events to this integration when received via the PagerDuty Events API.
        """
        pulumi.set(__self__, "service", service)
        if email_filter_mode is not None:
            pulumi.set(__self__, "email_filter_mode", email_filter_mode)
        if email_filters is not None:
            pulumi.set(__self__, "email_filters", email_filters)
        if email_incident_creation is not None:
            pulumi.set(__self__, "email_incident_creation", email_incident_creation)
        if email_parsers is not None:
            pulumi.set(__self__, "email_parsers", email_parsers)
        if email_parsing_fallback is not None:
            pulumi.set(__self__, "email_parsing_fallback", email_parsing_fallback)
        if integration_email is not None:
            pulumi.set(__self__, "integration_email", integration_email)
        if integration_key is not None:
            pulumi.set(__self__, "integration_key", integration_key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if vendor is not None:
            pulumi.set(__self__, "vendor", vendor)

    @property
    @pulumi.getter
    def service(self) -> pulumi.Input[str]:
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: pulumi.Input[str]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter(name="emailFilterMode")
    def email_filter_mode(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "email_filter_mode")

    @email_filter_mode.setter
    def email_filter_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_filter_mode", value)

    @property
    @pulumi.getter(name="emailFilters")
    def email_filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailFilterArgs']]]]:
        return pulumi.get(self, "email_filters")

    @email_filters.setter
    def email_filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailFilterArgs']]]]):
        pulumi.set(self, "email_filters", value)

    @property
    @pulumi.getter(name="emailIncidentCreation")
    def email_incident_creation(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "email_incident_creation")

    @email_incident_creation.setter
    def email_incident_creation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_incident_creation", value)

    @property
    @pulumi.getter(name="emailParsers")
    def email_parsers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailParserArgs']]]]:
        return pulumi.get(self, "email_parsers")

    @email_parsers.setter
    def email_parsers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailParserArgs']]]]):
        pulumi.set(self, "email_parsers", value)

    @property
    @pulumi.getter(name="emailParsingFallback")
    def email_parsing_fallback(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "email_parsing_fallback")

    @email_parsing_fallback.setter
    def email_parsing_fallback(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_parsing_fallback", value)

    @property
    @pulumi.getter(name="integrationEmail")
    def integration_email(self) -> Optional[pulumi.Input[str]]:
        """
        This is the unique fully-qualified email address used for routing emails to this integration for processing.
        """
        return pulumi.get(self, "integration_email")

    @integration_email.setter
    def integration_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_email", value)

    @property
    @pulumi.getter(name="integrationKey")
    def integration_key(self) -> Optional[pulumi.Input[str]]:
        """
        This is the unique key used to route events to this integration when received via the PagerDuty Events API.
        """
        return pulumi.get(self, "integration_key")

    @integration_key.setter
    def integration_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def vendor(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "vendor")

    @vendor.setter
    def vendor(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vendor", value)


@pulumi.input_type
class _ServiceIntegrationState:
    def __init__(__self__, *,
                 email_filter_mode: Optional[pulumi.Input[str]] = None,
                 email_filters: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailFilterArgs']]]] = None,
                 email_incident_creation: Optional[pulumi.Input[str]] = None,
                 email_parsers: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailParserArgs']]]] = None,
                 email_parsing_fallback: Optional[pulumi.Input[str]] = None,
                 html_url: Optional[pulumi.Input[str]] = None,
                 integration_email: Optional[pulumi.Input[str]] = None,
                 integration_key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vendor: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ServiceIntegration resources.
        :param pulumi.Input[str] html_url: URL at which the entity is uniquely displayed in the Web app.
        :param pulumi.Input[str] integration_email: This is the unique fully-qualified email address used for routing emails to this integration for processing.
        :param pulumi.Input[str] integration_key: This is the unique key used to route events to this integration when received via the PagerDuty Events API.
        """
        if email_filter_mode is not None:
            pulumi.set(__self__, "email_filter_mode", email_filter_mode)
        if email_filters is not None:
            pulumi.set(__self__, "email_filters", email_filters)
        if email_incident_creation is not None:
            pulumi.set(__self__, "email_incident_creation", email_incident_creation)
        if email_parsers is not None:
            pulumi.set(__self__, "email_parsers", email_parsers)
        if email_parsing_fallback is not None:
            pulumi.set(__self__, "email_parsing_fallback", email_parsing_fallback)
        if html_url is not None:
            pulumi.set(__self__, "html_url", html_url)
        if integration_email is not None:
            pulumi.set(__self__, "integration_email", integration_email)
        if integration_key is not None:
            pulumi.set(__self__, "integration_key", integration_key)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if service is not None:
            pulumi.set(__self__, "service", service)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if vendor is not None:
            pulumi.set(__self__, "vendor", vendor)

    @property
    @pulumi.getter(name="emailFilterMode")
    def email_filter_mode(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "email_filter_mode")

    @email_filter_mode.setter
    def email_filter_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_filter_mode", value)

    @property
    @pulumi.getter(name="emailFilters")
    def email_filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailFilterArgs']]]]:
        return pulumi.get(self, "email_filters")

    @email_filters.setter
    def email_filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailFilterArgs']]]]):
        pulumi.set(self, "email_filters", value)

    @property
    @pulumi.getter(name="emailIncidentCreation")
    def email_incident_creation(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "email_incident_creation")

    @email_incident_creation.setter
    def email_incident_creation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_incident_creation", value)

    @property
    @pulumi.getter(name="emailParsers")
    def email_parsers(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailParserArgs']]]]:
        return pulumi.get(self, "email_parsers")

    @email_parsers.setter
    def email_parsers(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServiceIntegrationEmailParserArgs']]]]):
        pulumi.set(self, "email_parsers", value)

    @property
    @pulumi.getter(name="emailParsingFallback")
    def email_parsing_fallback(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "email_parsing_fallback")

    @email_parsing_fallback.setter
    def email_parsing_fallback(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email_parsing_fallback", value)

    @property
    @pulumi.getter(name="htmlUrl")
    def html_url(self) -> Optional[pulumi.Input[str]]:
        """
        URL at which the entity is uniquely displayed in the Web app.
        """
        return pulumi.get(self, "html_url")

    @html_url.setter
    def html_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "html_url", value)

    @property
    @pulumi.getter(name="integrationEmail")
    def integration_email(self) -> Optional[pulumi.Input[str]]:
        """
        This is the unique fully-qualified email address used for routing emails to this integration for processing.
        """
        return pulumi.get(self, "integration_email")

    @integration_email.setter
    def integration_email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_email", value)

    @property
    @pulumi.getter(name="integrationKey")
    def integration_key(self) -> Optional[pulumi.Input[str]]:
        """
        This is the unique key used to route events to this integration when received via the PagerDuty Events API.
        """
        return pulumi.get(self, "integration_key")

    @integration_key.setter
    def integration_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "integration_key", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def service(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "service")

    @service.setter
    def service(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def vendor(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "vendor")

    @vendor.setter
    def vendor(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vendor", value)


class ServiceIntegration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email_filter_mode: Optional[pulumi.Input[str]] = None,
                 email_filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceIntegrationEmailFilterArgs']]]]] = None,
                 email_incident_creation: Optional[pulumi.Input[str]] = None,
                 email_parsers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceIntegrationEmailParserArgs']]]]] = None,
                 email_parsing_fallback: Optional[pulumi.Input[str]] = None,
                 integration_email: Optional[pulumi.Input[str]] = None,
                 integration_key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vendor: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A [service integration](https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1services~1%7Bid%7D~1integrations/post) is an integration that belongs to a service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        example = pagerduty.User("example",
            name="Earline Greenholt",
            email="125.greenholt.earline@graham.name",
            teams=[example_pagerduty_team["id"]])
        foo = pagerduty.EscalationPolicy("foo",
            name="Engineering Escalation Policy",
            num_loops=2,
            rules=[pagerduty.EscalationPolicyRuleArgs(
                escalation_delay_in_minutes=10,
                targets=[pagerduty.EscalationPolicyRuleTargetArgs(
                    type="user",
                    id=example.id,
                )],
            )])
        example_service = pagerduty.Service("example",
            name="My Web App",
            auto_resolve_timeout="14400",
            acknowledgement_timeout="600",
            escalation_policy=example_pagerduty_escalation_policy["id"])
        example_service_integration = pagerduty.ServiceIntegration("example",
            name="Generic API Service Integration",
            type="generic_events_api_inbound_integration",
            service=example_service.id)
        apiv2 = pagerduty.ServiceIntegration("apiv2",
            name="API V2",
            type="events_api_v2_inbound_integration",
            service=example_service.id)
        email_x = pagerduty.ServiceIntegration("email_x",
            name="Email X",
            type="generic_email_inbound_integration",
            integration_email="ecommerce@subdomain.pagerduty.com",
            service=example_service.id)
        datadog = pagerduty.get_vendor(name="Datadog")
        datadog_service_integration = pagerduty.ServiceIntegration("datadog",
            name=datadog.name,
            service=example_service.id,
            vendor=datadog.id)
        cloudwatch = pagerduty.get_vendor(name="Cloudwatch")
        cloudwatch_service_integration = pagerduty.ServiceIntegration("cloudwatch",
            name=cloudwatch.name,
            service=example_service.id,
            vendor=cloudwatch.id)
        email = pagerduty.get_vendor(name="Email")
        email_service_integration = pagerduty.ServiceIntegration("email",
            name=email.name,
            service=example_service.id,
            vendor=email.id,
            integration_email="s1@your_account.pagerduty.com",
            email_incident_creation="use_rules",
            email_filter_mode="and-rules-email",
            email_filters=[
                pagerduty.ServiceIntegrationEmailFilterArgs(
                    body_mode="always",
                    body_regex=None,
                    from_email_mode="match",
                    from_email_regex="(@foo.test*)",
                    subject_mode="match",
                    subject_regex="(CRITICAL*)",
                ),
                pagerduty.ServiceIntegrationEmailFilterArgs(
                    body_mode="always",
                    body_regex=None,
                    from_email_mode="match",
                    from_email_regex="(@bar.com*)",
                    subject_mode="match",
                    subject_regex="(CRITICAL*)",
                ),
            ],
            email_parsers=[pagerduty.ServiceIntegrationEmailParserArgs(
                action="resolve",
                match_predicate=pagerduty.ServiceIntegrationEmailParserMatchPredicateArgs(
                    type="any",
                    predicates=[
                        pagerduty.ServiceIntegrationEmailParserMatchPredicatePredicateArgs(
                            matcher="foo",
                            part="subject",
                            type="contains",
                        ),
                        pagerduty.ServiceIntegrationEmailParserMatchPredicatePredicateArgs(
                            type="not",
                            predicates=[pagerduty.ServiceIntegrationEmailParserMatchPredicatePredicatePredicateArgs(
                                matcher="(bar*)",
                                part="body",
                                type="regex",
                            )],
                        ),
                    ],
                ),
                value_extractors=[
                    pagerduty.ServiceIntegrationEmailParserValueExtractorArgs(
                        ends_before="end",
                        part="subject",
                        starts_after="start",
                        type="between",
                        value_name="incident_key",
                    ),
                    pagerduty.ServiceIntegrationEmailParserValueExtractorArgs(
                        ends_before="end",
                        part="subject",
                        starts_after="start",
                        type="between",
                        value_name="FieldName1",
                    ),
                ],
            )])
        ```

        ## Import

        Services can be imported using their related `service` id and service integration `id` separated by a dot, e.g.

        ```sh
        $ pulumi import pagerduty:index/serviceIntegration:ServiceIntegration main PLSSSSS.PLIIIII
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] integration_email: This is the unique fully-qualified email address used for routing emails to this integration for processing.
        :param pulumi.Input[str] integration_key: This is the unique key used to route events to this integration when received via the PagerDuty Events API.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ServiceIntegrationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A [service integration](https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1services~1%7Bid%7D~1integrations/post) is an integration that belongs to a service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_pagerduty as pagerduty

        example = pagerduty.User("example",
            name="Earline Greenholt",
            email="125.greenholt.earline@graham.name",
            teams=[example_pagerduty_team["id"]])
        foo = pagerduty.EscalationPolicy("foo",
            name="Engineering Escalation Policy",
            num_loops=2,
            rules=[pagerduty.EscalationPolicyRuleArgs(
                escalation_delay_in_minutes=10,
                targets=[pagerduty.EscalationPolicyRuleTargetArgs(
                    type="user",
                    id=example.id,
                )],
            )])
        example_service = pagerduty.Service("example",
            name="My Web App",
            auto_resolve_timeout="14400",
            acknowledgement_timeout="600",
            escalation_policy=example_pagerduty_escalation_policy["id"])
        example_service_integration = pagerduty.ServiceIntegration("example",
            name="Generic API Service Integration",
            type="generic_events_api_inbound_integration",
            service=example_service.id)
        apiv2 = pagerduty.ServiceIntegration("apiv2",
            name="API V2",
            type="events_api_v2_inbound_integration",
            service=example_service.id)
        email_x = pagerduty.ServiceIntegration("email_x",
            name="Email X",
            type="generic_email_inbound_integration",
            integration_email="ecommerce@subdomain.pagerduty.com",
            service=example_service.id)
        datadog = pagerduty.get_vendor(name="Datadog")
        datadog_service_integration = pagerduty.ServiceIntegration("datadog",
            name=datadog.name,
            service=example_service.id,
            vendor=datadog.id)
        cloudwatch = pagerduty.get_vendor(name="Cloudwatch")
        cloudwatch_service_integration = pagerduty.ServiceIntegration("cloudwatch",
            name=cloudwatch.name,
            service=example_service.id,
            vendor=cloudwatch.id)
        email = pagerduty.get_vendor(name="Email")
        email_service_integration = pagerduty.ServiceIntegration("email",
            name=email.name,
            service=example_service.id,
            vendor=email.id,
            integration_email="s1@your_account.pagerduty.com",
            email_incident_creation="use_rules",
            email_filter_mode="and-rules-email",
            email_filters=[
                pagerduty.ServiceIntegrationEmailFilterArgs(
                    body_mode="always",
                    body_regex=None,
                    from_email_mode="match",
                    from_email_regex="(@foo.test*)",
                    subject_mode="match",
                    subject_regex="(CRITICAL*)",
                ),
                pagerduty.ServiceIntegrationEmailFilterArgs(
                    body_mode="always",
                    body_regex=None,
                    from_email_mode="match",
                    from_email_regex="(@bar.com*)",
                    subject_mode="match",
                    subject_regex="(CRITICAL*)",
                ),
            ],
            email_parsers=[pagerduty.ServiceIntegrationEmailParserArgs(
                action="resolve",
                match_predicate=pagerduty.ServiceIntegrationEmailParserMatchPredicateArgs(
                    type="any",
                    predicates=[
                        pagerduty.ServiceIntegrationEmailParserMatchPredicatePredicateArgs(
                            matcher="foo",
                            part="subject",
                            type="contains",
                        ),
                        pagerduty.ServiceIntegrationEmailParserMatchPredicatePredicateArgs(
                            type="not",
                            predicates=[pagerduty.ServiceIntegrationEmailParserMatchPredicatePredicatePredicateArgs(
                                matcher="(bar*)",
                                part="body",
                                type="regex",
                            )],
                        ),
                    ],
                ),
                value_extractors=[
                    pagerduty.ServiceIntegrationEmailParserValueExtractorArgs(
                        ends_before="end",
                        part="subject",
                        starts_after="start",
                        type="between",
                        value_name="incident_key",
                    ),
                    pagerduty.ServiceIntegrationEmailParserValueExtractorArgs(
                        ends_before="end",
                        part="subject",
                        starts_after="start",
                        type="between",
                        value_name="FieldName1",
                    ),
                ],
            )])
        ```

        ## Import

        Services can be imported using their related `service` id and service integration `id` separated by a dot, e.g.

        ```sh
        $ pulumi import pagerduty:index/serviceIntegration:ServiceIntegration main PLSSSSS.PLIIIII
        ```

        :param str resource_name: The name of the resource.
        :param ServiceIntegrationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ServiceIntegrationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 email_filter_mode: Optional[pulumi.Input[str]] = None,
                 email_filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceIntegrationEmailFilterArgs']]]]] = None,
                 email_incident_creation: Optional[pulumi.Input[str]] = None,
                 email_parsers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceIntegrationEmailParserArgs']]]]] = None,
                 email_parsing_fallback: Optional[pulumi.Input[str]] = None,
                 integration_email: Optional[pulumi.Input[str]] = None,
                 integration_key: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 service: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 vendor: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ServiceIntegrationArgs.__new__(ServiceIntegrationArgs)

            __props__.__dict__["email_filter_mode"] = email_filter_mode
            __props__.__dict__["email_filters"] = email_filters
            __props__.__dict__["email_incident_creation"] = email_incident_creation
            __props__.__dict__["email_parsers"] = email_parsers
            __props__.__dict__["email_parsing_fallback"] = email_parsing_fallback
            __props__.__dict__["integration_email"] = integration_email
            __props__.__dict__["integration_key"] = integration_key
            __props__.__dict__["name"] = name
            if service is None and not opts.urn:
                raise TypeError("Missing required property 'service'")
            __props__.__dict__["service"] = service
            __props__.__dict__["type"] = type
            __props__.__dict__["vendor"] = vendor
            __props__.__dict__["html_url"] = None
        super(ServiceIntegration, __self__).__init__(
            'pagerduty:index/serviceIntegration:ServiceIntegration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            email_filter_mode: Optional[pulumi.Input[str]] = None,
            email_filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceIntegrationEmailFilterArgs']]]]] = None,
            email_incident_creation: Optional[pulumi.Input[str]] = None,
            email_parsers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ServiceIntegrationEmailParserArgs']]]]] = None,
            email_parsing_fallback: Optional[pulumi.Input[str]] = None,
            html_url: Optional[pulumi.Input[str]] = None,
            integration_email: Optional[pulumi.Input[str]] = None,
            integration_key: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            service: Optional[pulumi.Input[str]] = None,
            type: Optional[pulumi.Input[str]] = None,
            vendor: Optional[pulumi.Input[str]] = None) -> 'ServiceIntegration':
        """
        Get an existing ServiceIntegration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] html_url: URL at which the entity is uniquely displayed in the Web app.
        :param pulumi.Input[str] integration_email: This is the unique fully-qualified email address used for routing emails to this integration for processing.
        :param pulumi.Input[str] integration_key: This is the unique key used to route events to this integration when received via the PagerDuty Events API.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ServiceIntegrationState.__new__(_ServiceIntegrationState)

        __props__.__dict__["email_filter_mode"] = email_filter_mode
        __props__.__dict__["email_filters"] = email_filters
        __props__.__dict__["email_incident_creation"] = email_incident_creation
        __props__.__dict__["email_parsers"] = email_parsers
        __props__.__dict__["email_parsing_fallback"] = email_parsing_fallback
        __props__.__dict__["html_url"] = html_url
        __props__.__dict__["integration_email"] = integration_email
        __props__.__dict__["integration_key"] = integration_key
        __props__.__dict__["name"] = name
        __props__.__dict__["service"] = service
        __props__.__dict__["type"] = type
        __props__.__dict__["vendor"] = vendor
        return ServiceIntegration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="emailFilterMode")
    def email_filter_mode(self) -> pulumi.Output[str]:
        return pulumi.get(self, "email_filter_mode")

    @property
    @pulumi.getter(name="emailFilters")
    def email_filters(self) -> pulumi.Output[Sequence['outputs.ServiceIntegrationEmailFilter']]:
        return pulumi.get(self, "email_filters")

    @property
    @pulumi.getter(name="emailIncidentCreation")
    def email_incident_creation(self) -> pulumi.Output[str]:
        return pulumi.get(self, "email_incident_creation")

    @property
    @pulumi.getter(name="emailParsers")
    def email_parsers(self) -> pulumi.Output[Optional[Sequence['outputs.ServiceIntegrationEmailParser']]]:
        return pulumi.get(self, "email_parsers")

    @property
    @pulumi.getter(name="emailParsingFallback")
    def email_parsing_fallback(self) -> pulumi.Output[str]:
        return pulumi.get(self, "email_parsing_fallback")

    @property
    @pulumi.getter(name="htmlUrl")
    def html_url(self) -> pulumi.Output[str]:
        """
        URL at which the entity is uniquely displayed in the Web app.
        """
        return pulumi.get(self, "html_url")

    @property
    @pulumi.getter(name="integrationEmail")
    def integration_email(self) -> pulumi.Output[str]:
        """
        This is the unique fully-qualified email address used for routing emails to this integration for processing.
        """
        return pulumi.get(self, "integration_email")

    @property
    @pulumi.getter(name="integrationKey")
    def integration_key(self) -> pulumi.Output[str]:
        """
        This is the unique key used to route events to this integration when received via the PagerDuty Events API.
        """
        return pulumi.get(self, "integration_key")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def service(self) -> pulumi.Output[str]:
        return pulumi.get(self, "service")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def vendor(self) -> pulumi.Output[str]:
        return pulumi.get(self, "vendor")

