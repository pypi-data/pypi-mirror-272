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
    'GetEventsResult',
    'AwaitableGetEventsResult',
    'get_events',
    'get_events_output',
]

@pulumi.output_type
class GetEventsResult:
    """
    A collection of values returned by getEvents.
    """
    def __init__(__self__, earliest_start_time_epoch_millis=None, events=None, id=None, latest_start_time_epoch_millis=None, limit=None, offset=None):
        if earliest_start_time_epoch_millis and not isinstance(earliest_start_time_epoch_millis, int):
            raise TypeError("Expected argument 'earliest_start_time_epoch_millis' to be a int")
        pulumi.set(__self__, "earliest_start_time_epoch_millis", earliest_start_time_epoch_millis)
        if events and not isinstance(events, list):
            raise TypeError("Expected argument 'events' to be a list")
        pulumi.set(__self__, "events", events)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if latest_start_time_epoch_millis and not isinstance(latest_start_time_epoch_millis, int):
            raise TypeError("Expected argument 'latest_start_time_epoch_millis' to be a int")
        pulumi.set(__self__, "latest_start_time_epoch_millis", latest_start_time_epoch_millis)
        if limit and not isinstance(limit, int):
            raise TypeError("Expected argument 'limit' to be a int")
        pulumi.set(__self__, "limit", limit)
        if offset and not isinstance(offset, int):
            raise TypeError("Expected argument 'offset' to be a int")
        pulumi.set(__self__, "offset", offset)

    @property
    @pulumi.getter(name="earliestStartTimeEpochMillis")
    def earliest_start_time_epoch_millis(self) -> int:
        """
        Earliest start time in epoch milliseconds.
        """
        return pulumi.get(self, "earliest_start_time_epoch_millis")

    @property
    @pulumi.getter
    def events(self) -> Sequence['outputs.GetEventsEventResult']:
        """
        List of all events in Wavefront. For each event you will see a list of attributes.
        """
        return pulumi.get(self, "events")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="latestStartTimeEpochMillis")
    def latest_start_time_epoch_millis(self) -> int:
        """
        Latest start time in epoch milliseconds.
        """
        return pulumi.get(self, "latest_start_time_epoch_millis")

    @property
    @pulumi.getter
    def limit(self) -> Optional[int]:
        return pulumi.get(self, "limit")

    @property
    @pulumi.getter
    def offset(self) -> Optional[int]:
        return pulumi.get(self, "offset")


class AwaitableGetEventsResult(GetEventsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventsResult(
            earliest_start_time_epoch_millis=self.earliest_start_time_epoch_millis,
            events=self.events,
            id=self.id,
            latest_start_time_epoch_millis=self.latest_start_time_epoch_millis,
            limit=self.limit,
            offset=self.offset)


def get_events(earliest_start_time_epoch_millis: Optional[int] = None,
               latest_start_time_epoch_millis: Optional[int] = None,
               limit: Optional[int] = None,
               offset: Optional[int] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventsResult:
    """
    Use this data source to get information about all Wavefront events.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    # Get the information about all events
    example = wavefront.get_events(limit=10,
        offset=0,
        latest_start_time_epoch_millis=1665427195,
        earliest_start_time_epoch_millis=1665427195)
    ```


    :param int earliest_start_time_epoch_millis: The earliest start time in epoch milliseconds.
    :param int latest_start_time_epoch_millis: The latest start time in epoch milliseconds.
    :param int limit: Limit is the maximum number of results to be returned. Defaults to 100.
    :param int offset: Offset is the offset from the first result to be returned. Defaults to 0.
    """
    __args__ = dict()
    __args__['earliestStartTimeEpochMillis'] = earliest_start_time_epoch_millis
    __args__['latestStartTimeEpochMillis'] = latest_start_time_epoch_millis
    __args__['limit'] = limit
    __args__['offset'] = offset
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('wavefront:index/getEvents:getEvents', __args__, opts=opts, typ=GetEventsResult).value

    return AwaitableGetEventsResult(
        earliest_start_time_epoch_millis=pulumi.get(__ret__, 'earliest_start_time_epoch_millis'),
        events=pulumi.get(__ret__, 'events'),
        id=pulumi.get(__ret__, 'id'),
        latest_start_time_epoch_millis=pulumi.get(__ret__, 'latest_start_time_epoch_millis'),
        limit=pulumi.get(__ret__, 'limit'),
        offset=pulumi.get(__ret__, 'offset'))


@_utilities.lift_output_func(get_events)
def get_events_output(earliest_start_time_epoch_millis: Optional[pulumi.Input[int]] = None,
                      latest_start_time_epoch_millis: Optional[pulumi.Input[int]] = None,
                      limit: Optional[pulumi.Input[Optional[int]]] = None,
                      offset: Optional[pulumi.Input[Optional[int]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEventsResult]:
    """
    Use this data source to get information about all Wavefront events.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_wavefront as wavefront

    # Get the information about all events
    example = wavefront.get_events(limit=10,
        offset=0,
        latest_start_time_epoch_millis=1665427195,
        earliest_start_time_epoch_millis=1665427195)
    ```


    :param int earliest_start_time_epoch_millis: The earliest start time in epoch milliseconds.
    :param int latest_start_time_epoch_millis: The latest start time in epoch milliseconds.
    :param int limit: Limit is the maximum number of results to be returned. Defaults to 100.
    :param int offset: Offset is the offset from the first result to be returned. Defaults to 0.
    """
    ...
