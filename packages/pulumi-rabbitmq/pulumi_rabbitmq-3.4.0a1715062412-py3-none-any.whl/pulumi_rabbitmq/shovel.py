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

__all__ = ['ShovelArgs', 'Shovel']

@pulumi.input_type
class ShovelArgs:
    def __init__(__self__, *,
                 info: pulumi.Input['ShovelInfoArgs'],
                 vhost: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Shovel resource.
        :param pulumi.Input['ShovelInfoArgs'] info: The settings of the dynamic shovel. The structure is
               described below.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        :param pulumi.Input[str] name: The shovel name.
        """
        pulumi.set(__self__, "info", info)
        pulumi.set(__self__, "vhost", vhost)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def info(self) -> pulumi.Input['ShovelInfoArgs']:
        """
        The settings of the dynamic shovel. The structure is
        described below.
        """
        return pulumi.get(self, "info")

    @info.setter
    def info(self, value: pulumi.Input['ShovelInfoArgs']):
        pulumi.set(self, "info", value)

    @property
    @pulumi.getter
    def vhost(self) -> pulumi.Input[str]:
        """
        The vhost to create the resource in.
        """
        return pulumi.get(self, "vhost")

    @vhost.setter
    def vhost(self, value: pulumi.Input[str]):
        pulumi.set(self, "vhost", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The shovel name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ShovelState:
    def __init__(__self__, *,
                 info: Optional[pulumi.Input['ShovelInfoArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 vhost: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Shovel resources.
        :param pulumi.Input['ShovelInfoArgs'] info: The settings of the dynamic shovel. The structure is
               described below.
        :param pulumi.Input[str] name: The shovel name.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        """
        if info is not None:
            pulumi.set(__self__, "info", info)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if vhost is not None:
            pulumi.set(__self__, "vhost", vhost)

    @property
    @pulumi.getter
    def info(self) -> Optional[pulumi.Input['ShovelInfoArgs']]:
        """
        The settings of the dynamic shovel. The structure is
        described below.
        """
        return pulumi.get(self, "info")

    @info.setter
    def info(self, value: Optional[pulumi.Input['ShovelInfoArgs']]):
        pulumi.set(self, "info", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The shovel name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def vhost(self) -> Optional[pulumi.Input[str]]:
        """
        The vhost to create the resource in.
        """
        return pulumi.get(self, "vhost")

    @vhost.setter
    def vhost(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vhost", value)


class Shovel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 info: Optional[pulumi.Input[pulumi.InputType['ShovelInfoArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 vhost: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        The ``Shovel`` resource creates and manages a dynamic shovel.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_rabbitmq as rabbitmq

        test = rabbitmq.VHost("test", name="test")
        test_exchange = rabbitmq.Exchange("test",
            name="test_exchange",
            vhost=test.name,
            settings=rabbitmq.ExchangeSettingsArgs(
                type="fanout",
                durable=False,
                auto_delete=True,
            ))
        test_queue = rabbitmq.Queue("test",
            name="test_queue",
            vhost=test.name,
            settings=rabbitmq.QueueSettingsArgs(
                durable=False,
                auto_delete=True,
            ))
        shovel_test = rabbitmq.Shovel("shovelTest",
            name="shovelTest",
            vhost=test.name,
            info=rabbitmq.ShovelInfoArgs(
                source_uri="amqp:///test",
                source_exchange=test_exchange.name,
                source_exchange_key="test",
                destination_uri="amqp:///test",
                destination_queue=test_queue.name,
            ))
        ```

        ## Import

        Shovels can be imported using the `name` and `vhost`

        E.g.

        ```sh
        $ pulumi import rabbitmq:index/shovel:Shovel test shovelTest@test
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ShovelInfoArgs']] info: The settings of the dynamic shovel. The structure is
               described below.
        :param pulumi.Input[str] name: The shovel name.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ShovelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The ``Shovel`` resource creates and manages a dynamic shovel.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_rabbitmq as rabbitmq

        test = rabbitmq.VHost("test", name="test")
        test_exchange = rabbitmq.Exchange("test",
            name="test_exchange",
            vhost=test.name,
            settings=rabbitmq.ExchangeSettingsArgs(
                type="fanout",
                durable=False,
                auto_delete=True,
            ))
        test_queue = rabbitmq.Queue("test",
            name="test_queue",
            vhost=test.name,
            settings=rabbitmq.QueueSettingsArgs(
                durable=False,
                auto_delete=True,
            ))
        shovel_test = rabbitmq.Shovel("shovelTest",
            name="shovelTest",
            vhost=test.name,
            info=rabbitmq.ShovelInfoArgs(
                source_uri="amqp:///test",
                source_exchange=test_exchange.name,
                source_exchange_key="test",
                destination_uri="amqp:///test",
                destination_queue=test_queue.name,
            ))
        ```

        ## Import

        Shovels can be imported using the `name` and `vhost`

        E.g.

        ```sh
        $ pulumi import rabbitmq:index/shovel:Shovel test shovelTest@test
        ```

        :param str resource_name: The name of the resource.
        :param ShovelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ShovelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 info: Optional[pulumi.Input[pulumi.InputType['ShovelInfoArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 vhost: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ShovelArgs.__new__(ShovelArgs)

            if info is None and not opts.urn:
                raise TypeError("Missing required property 'info'")
            __props__.__dict__["info"] = info
            __props__.__dict__["name"] = name
            if vhost is None and not opts.urn:
                raise TypeError("Missing required property 'vhost'")
            __props__.__dict__["vhost"] = vhost
        super(Shovel, __self__).__init__(
            'rabbitmq:index/shovel:Shovel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            info: Optional[pulumi.Input[pulumi.InputType['ShovelInfoArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            vhost: Optional[pulumi.Input[str]] = None) -> 'Shovel':
        """
        Get an existing Shovel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ShovelInfoArgs']] info: The settings of the dynamic shovel. The structure is
               described below.
        :param pulumi.Input[str] name: The shovel name.
        :param pulumi.Input[str] vhost: The vhost to create the resource in.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ShovelState.__new__(_ShovelState)

        __props__.__dict__["info"] = info
        __props__.__dict__["name"] = name
        __props__.__dict__["vhost"] = vhost
        return Shovel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def info(self) -> pulumi.Output['outputs.ShovelInfo']:
        """
        The settings of the dynamic shovel. The structure is
        described below.
        """
        return pulumi.get(self, "info")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The shovel name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def vhost(self) -> pulumi.Output[str]:
        """
        The vhost to create the resource in.
        """
        return pulumi.get(self, "vhost")

