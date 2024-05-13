from slurpit.apis.baseapi import BaseAPI
from slurpit.models.planning import Planning

class PlanningAPI(BaseAPI):
    def __init__(self, base_url, api_key):
        """
        Initializes a new instance of the PlanningAPI class, which extends BaseAPI. This class is designed to interact with the planning-related endpoints of an API, managing planning entries.

        Args:
            base_url (str): The root URL for the API endpoints.
            api_key (str): The API key used for authenticating requests.
        """
        self.base_url = base_url
        super().__init__(api_key)

    def get_plannings(self, export_csv: bool = False):
        """
        Fetches all planning entries from the API and optionally exports the data to a CSV format.
        
        Args:
            export_csv (bool): If True, returns the planning data in CSV format as bytes.
                            If False, returns a list of Planning objects.

        Returns:
            list[Planning] | bytes | None: A list of Planning objects if successful, bytes if exporting to CSV,
                                        None otherwise.
        """
        url = f"{self.base_url}/planning"
        try:
            response = self.get(url)
            if response:
                plannings_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(plannings_data)
                else:
                    return [Planning(**item) for item in plannings_data]
        except Exception as e:
            print(f"Response error: {e}")

        return None

    
    def search(self, search_data: dict, export_csv: bool = False):
        """
        A more flexible way to search over the unique planning data and optionally exports the data to CSV format.

        Args:
            search_data (dict): A dictionary of search criteria.
            export_csv (bool): If True, returns the search results in CSV format as bytes.
                            If False, returns the search results as a dictionary.

        Returns:
            dict | bytes | None: The search results as a dictionary if successful, bytes if exporting to CSV,
                                None otherwise.
        """
        url = f"{self.base_url}/planning/search"
        try:
            response = self.post(url, search_data)
            if response:
                search_result = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(search_result)
                else:
                    return search_result
        except Exception as e:
            print(f"Response error: {e}")

        return None

    
    def regenerate_unique(self, planning_data):
        """
        When the keys of a planning are changed it's required to regenerate the existing data if you want to use the Unique Results

        Args:
            planning_data (dict): The data of the planning entry that needs to regenerate unique attributes.

        Returns:
            dict: Updated information of the planning entry, or None if an error occurs.
        """
        url = f"{self.base_url}/planning/regenerate_unique"
        try:
            response = self.post(url, planning_data)
            if response:
                update_info = response.json()
                return update_info
        except Exception as e:
            print(f"Response error: {e}")
        return None
