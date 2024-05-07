# -*- coding: utf-8 -*-
from ...intunecdlib.BaseBackupModule import BaseBackupModule


class WindowsFeatureUpdatesBackupModule(BaseBackupModule):
    """A class used to backup Intune Windows Feature Update profiles

    Attributes:
        CONFIG_ENDPOINT (str): The endpoint to get the data from
        LOG_MESSAGE (str): The message to log when backing up the data
    """

    CONFIG_ENDPOINT = "/beta/deviceManagement/windowsFeatureUpdateProfiles"
    LOG_MESSAGE = "Backing up Windows Feature Update Profile: "

    def __init__(self, *args, **kwargs):
        """Initializes the WindowsFeatureUpdatesBackupModule class

        Args:
            *args: The positional arguments to pass to the base class's __init__ method.
            **kwargs: The keyword arguments to pass to the base class's __init__ method.
        """
        super().__init__(*args, **kwargs)
        self.path = f"{self.path}/Feature Updates/"
        self.audit_filter = "componentName eq 'SoftwareUpdateConfiguration'"
        self.assignment_endpoint = "deviceManagement/windowsFeatureUpdateProfiles/"
        self.assignment_extra_url = "/assignments"

    def main(self) -> dict[str, any]:
        """The main method to backup the Windows Feature Update profiles

        Returns:
            dict[str, any]: The results of the backup
        """
        try:
            self.graph_data = self.make_graph_request(
                endpoint=self.endpoint + self.CONFIG_ENDPOINT
            )
        except Exception as e:
            self.log(
                tag="error",
                msg=f"Error getting Windows Feature Update data from {self.endpoint + self.CONFIG_ENDPOINT}: {e}",
            )
            return None

        try:
            self.results = self.process_data(
                data=self.graph_data["value"],
                filetype=self.filetype,
                path=self.path,
                name_key="displayName",
                log_message=self.LOG_MESSAGE,
                audit_compare_info={"type": "resourceId", "value_key": "id"},
            )
        except Exception as e:
            self.log(
                tag="error", msg=f"Error processing Windows Feature Update data: {e}"
            )
            return None

        return self.results
