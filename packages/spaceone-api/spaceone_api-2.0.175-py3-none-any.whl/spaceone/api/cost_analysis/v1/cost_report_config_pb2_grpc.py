# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from spaceone.api.cost_analysis.v1 import cost_report_config_pb2 as spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2

GRPC_GENERATED_VERSION = '1.63.0'
GRPC_VERSION = grpc.__version__
EXPECTED_ERROR_RELEASE = '1.65.0'
SCHEDULED_RELEASE_DATE = 'June 25, 2024'
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    warnings.warn(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in spaceone/api/cost_analysis/v1/cost_report_config_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class CostReportConfigStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/create',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CreateCostReportConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
                _registered_method=True)
        self.update = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/update',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.UpdateCostReportConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
                _registered_method=True)
        self.update_recipients = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/update_recipients',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.UpdateCostReportConfigRecipientsRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
                _registered_method=True)
        self.enable = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/enable',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
                _registered_method=True)
        self.disable = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/disable',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
                _registered_method=True)
        self.delete = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/delete',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.run = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/run',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/get',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
                _registered_method=True)
        self.list = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/list',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigsInfo.FromString,
                _registered_method=True)
        self.stat = channel.unary_unary(
                '/spaceone.api.cost_analysis.v1.CostReportConfig/stat',
                request_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigStatQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigsInfo.FromString,
                _registered_method=True)


class CostReportConfigServicer(object):
    """Missing associated documentation comment in .proto file."""

    def create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def update_recipients(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def enable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def disable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def run(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def list(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CostReportConfigServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CreateCostReportConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.UpdateCostReportConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.SerializeToString,
            ),
            'update_recipients': grpc.unary_unary_rpc_method_handler(
                    servicer.update_recipients,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.UpdateCostReportConfigRecipientsRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.SerializeToString,
            ),
            'enable': grpc.unary_unary_rpc_method_handler(
                    servicer.enable,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.SerializeToString,
            ),
            'disable': grpc.unary_unary_rpc_method_handler(
                    servicer.disable,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'run': grpc.unary_unary_rpc_method_handler(
                    servicer.run,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigStatQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigsInfo.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.cost_analysis.v1.CostReportConfig', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CostReportConfig(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/create',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CreateCostReportConfigRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/update',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.UpdateCostReportConfigRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def update_recipients(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/update_recipients',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.UpdateCostReportConfigRecipientsRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def enable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/enable',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def disable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/disable',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/delete',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def run(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/run',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/get',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigRequest.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def list(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/list',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigQuery.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigsInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def stat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/spaceone.api.cost_analysis.v1.CostReportConfig/stat',
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigStatQuery.SerializeToString,
            spaceone_dot_api_dot_cost__analysis_dot_v1_dot_cost__report__config__pb2.CostReportConfigsInfo.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
