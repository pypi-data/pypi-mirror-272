import logging
import time

import ai.h2o.featurestore.api.v1.CoreService_pb2 as pb

from ..access_type import AccessType
from ..collections.feature_sets import FeatureSets
from ..collections.feature_views import FeatureViews
from ..utils import Utils
from .user import User


class Project:
    def __init__(self, stub, project):
        self._project = project
        self._stub = stub
        self.feature_sets = FeatureSets(stub, project)
        self.feature_views = FeatureViews(stub, project)

    @property
    def id(self):
        return self._project.id

    @property
    def name(self):
        return self._project.name

    @property
    def description(self):
        return self._project.description

    @description.setter
    def description(self, value):
        update_request = pb.UpdateProjectRequest(
            project_id=self._project.id, description=value, fields_to_update=[pb.PROJECT_DESCRIPTION]
        )
        self._project = self._stub.UpdateProject(update_request).updated_project

    @property
    def secret(self):
        return self._project.secret

    @secret.setter
    def secret(self, value):
        update_request = pb.UpdateProjectRequest(
            project_id=self._project.id, secret=value, fields_to_update=[pb.PROJECT_SECRET]
        )
        self._project = self._stub.UpdateProject(update_request).updated_project

    @property
    def locked(self):
        return self._project.locked

    @locked.setter
    def locked(self, value):
        update_request = pb.UpdateProjectRequest(
            project_id=self._project.id, locked=value, fields_to_update=[pb.PROJECT_LOCKED]
        )
        self._project = self._stub.UpdateProject(update_request).updated_project

    @property
    def author(self):
        return User(self._project.author)

    @property
    def custom_data(self):
        return self._project.custom_data

    @custom_data.setter
    def custom_data(self, value):
        update_request = pb.UpdateProjectRequest(
            project_id=self._project.id, custom_data=value, fields_to_update=[pb.PROJECT_CUSTOM_DATA]
        )
        self._project = self._stub.UpdateProject(update_request).updated_project

    def delete(self, wait_for_completion=False):
        """Deletes the project."""
        request = pb.DeleteProjectRequest()
        request.project.CopyFrom(self._project)
        self._stub.DeleteProject(request)
        exists_request = pb.ProjectExistsRequest()
        exists_request.project_id = self._project.id
        if wait_for_completion:
            while self._stub.ProjectExists(exists_request).exists:
                time.sleep(1)
                logging.debug(f"Waiting for project '{self._project.name}' deletion...")
        logging.info(f"Project '{self._project.name}' is deleted")

    def add_owners(self, user_emails):
        """Add additional owner/owners to project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.add_owners(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._add_permissions(user_emails, pb.PermissionType.Owner)

    def add_editors(self, user_emails):
        """Add additional editor/editors to project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.add_editors(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._add_permissions(user_emails, pb.PermissionType.Editor)

    def add_consumers(self, user_emails):
        """Add additional consumer/consumers to project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.add_consumers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._add_permissions(user_emails, pb.PermissionType.Consumer)

    def add_sensitive_consumers(self, user_emails):
        """Add additional sensitive consumer/consumers to project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.add_sensitive_consumers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._add_permissions(user_emails, pb.PermissionType.SensitiveConsumer)

    def add_viewers(self, user_emails):
        """Add additional viewer/viewers to project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.add_viewers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._add_permissions(user_emails, pb.PermissionType.Viewer)

    def remove_owners(self, user_emails):
        """Remove owner/owners from project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.remove_owners(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._remove_permissions(user_emails, pb.PermissionType.Owner)

    def remove_editors(self, user_emails):
        """Remove editor/editors from project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.remove_editors(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._remove_permissions(user_emails, pb.PermissionType.Editor)

    def remove_consumers(self, user_emails):
        """Remove consumer/consumers from project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.remove_consumers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._remove_permissions(user_emails, pb.PermissionType.Consumer)

    def remove_sensitive_consumers(self, user_emails):
        """Remove sensitive consumer/consumers from project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.remove_sensitive_consumers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._remove_permissions(user_emails, pb.PermissionType.SensitiveConsumer)

    def remove_viewers(self, user_emails):
        """Remove viewer/viewers from project.

        Args:
            user_emails: (list[str]]) A collection of user emails.

        Returns:
            Project: An existing project with the latest information.

        Typical example:
            project.remove_viewers(["bob@h2o.ai", "alice@h2o.ai"])

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#project-permission-api
        """
        return self._remove_permissions(user_emails, pb.PermissionType.Viewer)

    @property
    def owners(self):
        request = pb.GetOwnersRequest(resource_id=self._project.id)
        response = self._stub.GetProjectOwners(request)
        return [User(owner) for owner in response.owners]

    def _add_permissions(self, user_emails, permission):
        request = pb.ProjectPermissionRequest()
        request.project.CopyFrom(self._project)
        request.user_emails.extend(user_emails)
        request.permission = permission
        self._stub.AddProjectPermission(request)
        return self

    def _remove_permissions(self, user_emails, permission):
        request = pb.ProjectPermissionRequest()
        request.project.CopyFrom(self._project)
        request.user_emails.extend(user_emails)
        request.permission = permission
        self._stub.RemoveProjectPermission(request)
        return self

    def _refresh(self):
        request = pb.GetProjectRequest()
        request.project_name = self._project.name
        response = self._stub.GetProject(request)
        self._project = response.project

    def request_access(self, access_type, reason):
        """Request project permissions.

        Args:
            access_type: (PermissionType) Object represents type of permission.
                OWNER | EDITOR | CONSUMER | SENSITIVE_CONSUMER
            reason: (str) A reason for permission request.

        Returns:
            str: A permission id.

        Typical example:
            my_request_id = project.request_access(AccessType.CONSUMER, "Preparing the best model")

        For more details:
            https://docs.h2o.ai/feature-store/latest-stable/docs/api/permissions.html#requesting-permissions-to-a-project
        """
        request = pb.SubmitPendingPermissionRequest()
        request.resource_id = self._project.id
        request.permission = AccessType.to_proto_permission(access_type)
        request.reason = reason
        response = self._stub.SubmitPendingProjectPermission(request)
        return response.permission_id

    @property
    def current_permission(self):
        """Lists current access rights."""
        request = pb.GetActivePermissionRequest(resource_id=self._project.id)
        response = self._stub.GetActiveProjectPermission(request)
        return AccessType.from_proto_active_permission(response.permission)

    def __repr__(self):
        return Utils.pretty_print_proto(self._project)

    def __str__(self):
        return (
            f"Project name    : {self.name} \n"
            f"Description     : {self.description} \n"
            f"Secret          : {self.secret} \n"
            f"Locked          : {self.locked} \n"
            f"Author            \n{Utils.output_indent_spacing(str(self.author), '  ')}"
            f"Created         : {Utils.proto_to_dict(self._project).get('created_date_time')} \n"
            f"Last updated    : {Utils.proto_to_dict(self._project).get('last_update_date_time')} \n"
        )
