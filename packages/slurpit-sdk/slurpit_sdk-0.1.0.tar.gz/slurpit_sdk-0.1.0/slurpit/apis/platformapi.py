from slurpit.apis.baseapi import BaseAPI
from slurpit.models.platform import Platform

class PlatformAPI(BaseAPI):
    def __init__(self, base_url, api_key):
        """
        Initializes a new instance of the PlatformAPI class, which extends BaseAPI. This class is designed to interact with platform-related endpoints of an API.

        Args:
            base_url (str): The root URL for the API endpoints.
            api_key (str): The API key used for authenticating requests.
        """
        self.base_url = base_url
        super().__init__(api_key)

    def ping(self):
        """
        Sends a 'ping' request to the platform's ping endpoint and returns a Platform instance if successful.

        Returns:
            Platform | None: A Platform object initialized with the data from the API response if the request is successful; None otherwise.
        """
        url = f"{self.base_url}/platform/ping" 
        try:
            response = self.get(url)
            if response:
                platform_data = response.json()  
                return Platform(**platform_data)  
        except Exception as e:
            print(f"Error retrieving platform data: {e}")  
        
        return None 