# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from spaceone.api.identity.v2 import project_pb2 as spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2

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
        + f' but the generated code in spaceone/api/identity/v2/project_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
        + f' This warning will become an error in {EXPECTED_ERROR_RELEASE},'
        + f' scheduled for release on {SCHEDULED_RELEASE_DATE}.',
        RuntimeWarning
    )


class ProjectStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.create = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/create',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.CreateProjectRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.update = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/update',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UpdateProjectRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.update_project_type = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/update_project_type',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UpdateProjectTypeRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.change_project_group = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/change_project_group',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ChangeProjectGroupRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.delete = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/delete',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectRequest.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                _registered_method=True)
        self.add_users = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/add_users',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UsersProjectRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.remove_users = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/remove_users',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UsersProjectRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.add_user_groups = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/add_user_groups',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UserGroupsProjectRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.remove_user_groups = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/remove_user_groups',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UserGroupsProjectRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.get = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/get',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectRequest.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
                _registered_method=True)
        self.list = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/list',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectSearchQuery.SerializeToString,
                response_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectsInfo.FromString,
                _registered_method=True)
        self.stat = channel.unary_unary(
                '/spaceone.api.identity.v2.Project/stat',
                request_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectStatQuery.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_struct__pb2.Struct.FromString,
                _registered_method=True)


class ProjectServicer(object):
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

    def update_project_type(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def change_project_group(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def delete(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def add_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remove_users(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def add_user_groups(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def remove_user_groups(self, request, context):
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


def add_ProjectServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'create': grpc.unary_unary_rpc_method_handler(
                    servicer.create,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.CreateProjectRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'update': grpc.unary_unary_rpc_method_handler(
                    servicer.update,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UpdateProjectRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'update_project_type': grpc.unary_unary_rpc_method_handler(
                    servicer.update_project_type,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UpdateProjectTypeRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'change_project_group': grpc.unary_unary_rpc_method_handler(
                    servicer.change_project_group,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ChangeProjectGroupRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'delete': grpc.unary_unary_rpc_method_handler(
                    servicer.delete,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectRequest.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'add_users': grpc.unary_unary_rpc_method_handler(
                    servicer.add_users,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UsersProjectRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'remove_users': grpc.unary_unary_rpc_method_handler(
                    servicer.remove_users,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UsersProjectRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'add_user_groups': grpc.unary_unary_rpc_method_handler(
                    servicer.add_user_groups,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UserGroupsProjectRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'remove_user_groups': grpc.unary_unary_rpc_method_handler(
                    servicer.remove_user_groups,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UserGroupsProjectRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'get': grpc.unary_unary_rpc_method_handler(
                    servicer.get,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectRequest.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.SerializeToString,
            ),
            'list': grpc.unary_unary_rpc_method_handler(
                    servicer.list,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectSearchQuery.FromString,
                    response_serializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectsInfo.SerializeToString,
            ),
            'stat': grpc.unary_unary_rpc_method_handler(
                    servicer.stat,
                    request_deserializer=spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectStatQuery.FromString,
                    response_serializer=google_dot_protobuf_dot_struct__pb2.Struct.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'spaceone.api.identity.v2.Project', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Project(object):
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
            '/spaceone.api.identity.v2.Project/create',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.CreateProjectRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
            '/spaceone.api.identity.v2.Project/update',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UpdateProjectRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
    def update_project_type(request,
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
            '/spaceone.api.identity.v2.Project/update_project_type',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UpdateProjectTypeRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
    def change_project_group(request,
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
            '/spaceone.api.identity.v2.Project/change_project_group',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ChangeProjectGroupRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
            '/spaceone.api.identity.v2.Project/delete',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectRequest.SerializeToString,
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
    def add_users(request,
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
            '/spaceone.api.identity.v2.Project/add_users',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UsersProjectRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
    def remove_users(request,
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
            '/spaceone.api.identity.v2.Project/remove_users',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UsersProjectRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
    def add_user_groups(request,
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
            '/spaceone.api.identity.v2.Project/add_user_groups',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UserGroupsProjectRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
    def remove_user_groups(request,
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
            '/spaceone.api.identity.v2.Project/remove_user_groups',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.UserGroupsProjectRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
            '/spaceone.api.identity.v2.Project/get',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectRequest.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectInfo.FromString,
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
            '/spaceone.api.identity.v2.Project/list',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectSearchQuery.SerializeToString,
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectsInfo.FromString,
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
            '/spaceone.api.identity.v2.Project/stat',
            spaceone_dot_api_dot_identity_dot_v2_dot_project__pb2.ProjectStatQuery.SerializeToString,
            google_dot_protobuf_dot_struct__pb2.Struct.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
