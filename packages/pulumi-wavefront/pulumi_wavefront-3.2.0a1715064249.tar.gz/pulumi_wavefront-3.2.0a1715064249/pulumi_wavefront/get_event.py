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
    'GetEventResult',
    'AwaitableGetEventResult',
    'get_event',
    'get_event_output',
]

@pulumi.output_type
class GetEventResult:
    """
    A collection of values returned by getEvent.
    """
    def __init__(__self__, annotations=None, details=None, endtime_key=None, id=None, is_ephemeral=None, name=None, severity=None, start_time=None, tags=None, type=None):
        if annotations and not isinstance(annotations, dict):
            raise TypeError("Expected argument 'annotations' to be a dict")
        pulumi.set(__self__, "annotations", annotations)
        if details and not isinstance(details, str):
            raise TypeError("Expected argument 'details' to be a str")
        pulumi.set(__self__, "details", details)
        if endtime_key and not isinstance(endtime_key, int):
            raise TypeError("Expected argument 'endtime_key' to be a int")
        pulumi.set(__self__, "endtime_key", endtime_key)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_ephemeral and not isinstance(is_ephemeral, bool):
            raise TypeError("Expected argument 'is_ephemeral' to be a bool")
        pulumi.set(__self__, "is_ephemeral", is_ephemeral)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if severity and not isinstance(severity, str):
            raise TypeError("Expected argument 'severity' to be a str")
        pulumi.set(__self__, "severity", severity)
        if start_time and not isinstance(start_time, int):
            raise TypeError("Expected argument 'start_time' to be a int")
        pulumi.set(__self__, "start_time", start_time)
        if tags and not isinstance(tags, list):
            raise TypeError("Expected argument 'tags' to be a list")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def annotations(self) -> Mapping[str, str]:
        """
        Annotations associated with the event.
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter
    def details(self) -> str:
        """
        The description of the event.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter(name="endtimeKey")
    def endtime_key(self) -> int:
        return pulumi.get(self, "endtime_key")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of the event in Wavefront.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isEphemeral")
    def is_ephemeral(self) -> bool:
        """
        A Boolean flag. If set to `true`, creates a point-in-time event (i.e. with no duration).
        """
        return pulumi.get(self, "is_ephemeral")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the event in Wavefront.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        The severity category of the event.
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> int:
        """
        The start time of the event in epoch milliseconds.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def tags(self) -> Sequence[str]:
        """
        A set of tags assigned to the event.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the event.
        """
        return pulumi.get(self, "type")


class AwaitableGetEventResult(GetEventResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventResult(
            annotations=self.annotations,
            details=self.details,
            endtime_key=self.endtime_key,
            id=self.id,
            is_ephemeral=self.is_ephemeral,
            name=self.name,
            severity=self.severity,
            start_time=self.start_time,
            tags=self.tags,
            type=self.type)


def get_event(id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventResult:
    """
    Use this data source to get information about a certain Wavefront event.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    # Get the information about a Wavefront event by its ID.
    example = wavefront.get_event(id="sample-event-id")
    ```


    :param str id: The ID associated with the event data to be fetched.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('wavefront:index/getEvent:getEvent', __args__, opts=opts, typ=GetEventResult).value

    return AwaitableGetEventResult(
        annotations=pulumi.get(__ret__, 'annotations'),
        details=pulumi.get(__ret__, 'details'),
        endtime_key=pulumi.get(__ret__, 'endtime_key'),
        id=pulumi.get(__ret__, 'id'),
        is_ephemeral=pulumi.get(__ret__, 'is_ephemeral'),
        name=pulumi.get(__ret__, 'name'),
        severity=pulumi.get(__ret__, 'severity'),
        start_time=pulumi.get(__ret__, 'start_time'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_event)
def get_event_output(id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventResult]:
    """
    Use this data source to get information about a certain Wavefront event.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    # Get the information about a Wavefront event by its ID.
    example = wavefront.get_event(id="sample-event-id")
    ```


    :param str id: The ID associated with the event data to be fetched.
    """
    ...
