from slurpit.apis.baseapi import BaseAPI
from slurpit.models.device import Device, Vendor

class DeviceAPI(BaseAPI):
    def __init__(self, base_url, api_key):
        """
        Initializes a new instance of DeviceAPI, extending the BaseAPI class.
        Sets up the base URL for API calls specific to devices and initializes authentication.

        Args:
            base_url (str): The root URL for the device-related API endpoints.
            api_key (str): The API key used for authenticating requests.
        """
        self.base_url = base_url
        super().__init__(api_key)

    def get_devices(self, offset: int = 0, limit: int = 1000, export_csv: bool = False):
        """
        Fetches a list of devices from the API with pagination and optionally exports the data to a CSV format.
        
        Args:
            offset (int): The starting index of the records to fetch.
            limit (int): The maximum number of records to return in one call.
            export_csv (bool): If True, returns the device data in CSV format as bytes.
                            If False, returns a list of Device objects.

        Returns:
            list[Device] | bytes | None: A list of Device instances if successful, bytes if exporting to CSV,
                                        None otherwise.
        """
        url = f"{self.base_url}/devices"
        params = {'offset': offset, 'limit': limit}
        try:
            response = self.get(url, params=params)
            if response:
                devices_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(devices_data)
                else:
                    return [Device(**item) for item in devices_data]
        except Exception as e:
            print(f"Response error: {e}")

        return None


    def get_device(self, device_id: int):
        """
        Fetches a single device by its ID.

        Args:
            device_id (int): The unique identifier of the device to retrieve.

        Returns:
            Device | None: A Device instance if successful, None otherwise.
        """
        url = f"{self.base_url}/devices/{device_id}"
        try:
            response = self.get(url)
            if response:
                device_data = response.json()
                return Device(**device_data)
        except Exception as e:
            print(f"Response error: {e}")
        return None

    def update_device(self, device_id: int, update_data: dict):
        """
        Updates a specific device using its ID.

        Args:
            device_id (int): The unique identifier of the device to update.
            update_data (dict): A dictionary containing the updated device attributes.

        Returns:
            Device | None: An updated Device instance if successful, None otherwise.
        """
        url = f"{self.base_url}/devices/{device_id}"
        try:
            response = self.put(url, update_data)
            if response:
                device_data = response.json()
                return Device(**device_data)
        except Exception as e:
            print(f"Response error: {e}")
        return None

    def create_device(self, device_data: dict):
        """
        Creates a new device in the system.

        Args:
            device_data (dict): A dictionary containing the device attributes.

        Returns:
            Device | None: A newly created Device instance if successful, None otherwise.
        """
        url = f"{self.base_url}/devices"
        try:
            response = self.post(url, device_data)
            if response:
                device_data = response.json()
                return Device(**device_data)
        except Exception as e:
            print(f"Response error: {e}")
        return None

    def delete_device(self, device_id: int):
        """
        Deletes a device using its ID.

        Args:
            device_id (int): The unique identifier of the device to delete.

        Returns:
            Device | None: A Device instance representing the deleted device if successful, None otherwise.
        """
        url = f"{self.base_url}/devices/{device_id}"
        try:
            response = self.delete(url)
            if response:
                device_data = response.json()
                return Device(**device_data)
        except Exception as e:
            print(f"Response error: {e}")
        return None

    def sync_device(self, device_data: dict):
        """
        Synchronizes a device with the given device data. Insert or Update a new device with the provided data.

        Args:
            device_data (dict): A dictionary containing the device attributes to be synchronized.

        Returns:
            None | Device: None if the synchronization is successful and 'success' is reported by the API, 
            otherwise returns a Device instance based on the returned data.
        """
        url = f"{self.base_url}/devices/sync"
        try:
            response = self.post(url, device_data)
            if response:
                device_data = response.json()
                if device_data.get('success'):
                    print("Sync response:", device_data['success'])
                    return None
                else:
                    return Device(**device_data)
        except Exception as e:
            print(f"Response error: {e}")
        return None

    def get_vendors(self, export_csv: bool = False):
        """
        Retrieves a list of vendors from the API and optionally exports the data to a CSV format.
        
        Args:
            export_csv (bool): If True, returns the vendor data in CSV format as bytes.
                            If False, returns a list of Vendor objects.

        Returns:
            list[Vendor] | bytes | None: A list of Vendor instances if successful, bytes if exporting to CSV,
                                        None otherwise.
        """
        url = f"{self.base_url}/devices/vendors"
        try:
            response = self.get(url)
            if response:
                vendors_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(vendors_data)
                else:
                    return [Vendor(**item) for item in vendors_data]
        except Exception as e:
            print(f"Response error: {e}")

        return None


    def get_types(self, export_csv: bool = False):
        """
        Retrieves a list of device types from the API and optionally exports the data to CSV format.
        
        Args:
            export_csv (bool): If True, returns the device type data in CSV format as bytes.
                            If False, returns a list of device types as strings.

        Returns:
            list[str] | bytes | None: A list of device types if successful, bytes if exporting to CSV,
                                    None otherwise.
        """
        url = f"{self.base_url}/devices/types"
        try:
            response = self.get(url)
            if response:
                types_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(types_data)
                else:
                    return types_data
        except Exception as e:
            print(f"Response error: {e}")

        return None


    def get_snapshots(self, hostname: str, date: str = None, export_csv: bool = False):
        """
        Retrieve latest data for a given hostname for all plannings, optionally filtered by date,
        and optionally exports the data to a CSV format.
        
        Args:
            hostname (str): The hostname of the device for which snapshots are required.
            date (str, optional): The specific date for which snapshots are required.
            export_csv (bool): If True, returns the snapshot data in CSV format as bytes.
                            If False, returns a list of snapshot data dictionaries.

        Returns:
            list[dict] | bytes | None: A list of snapshot data dictionaries if successful, 
                                    bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/devices/snapshot/all/{hostname}"
        params = {'date': date}
        try:
            response = self.get(url, params=params)
            if response:
                snapshots_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(snapshots_data)
                else:
                    return snapshots_data
        except Exception as e:
            print(f"Response error: {e}")

        return None


    def get_snapshot(self, hostname: str, planning_id: int, date: str = None):
        """
        Retrieves latest data for a given hostname and planning id, optionally filtered by date.

        Args:
            hostname (str): The hostname of the device.
            planning_id (int): The planning ID associated with the snapshot.
            date (str, optional): The specific date for which the snapshot is required.

        Returns:
            dict | None: Snapshot data as a dictionary if successful, None otherwise.
        """
        url = f"{self.base_url}/devices/snapshot/single/{hostname}/{planning_id}"
        params = {'date': date}
        try:
            response = self.get(url, params=params)
            if response:
                snapshot_data = response.json()
                return snapshot_data
        except Exception as e:
            print(f"Response error: {e}")
        return None

    def test_ssh(self, ssh_info: dict):
        """
        Tests SSH connectivity using the provided SSH information.

        Args:
            ssh_info (dict): A dictionary containing the SSH credentials and details.

        Returns:
            dict | None: SSH test response as a dictionary if successful, None otherwise.
        """
        url = f"{self.base_url}/devices/test/ssh"
        try:
            response = self.post(url, ssh_info)
            if response:
                ssh_response = response.json()
                return ssh_response
        except Exception as e:
            print(f"Response error: {e}")
        return None