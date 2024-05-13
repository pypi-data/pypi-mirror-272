from slurpit.apis.baseapi import BaseAPI

class ScraperAPI(BaseAPI):
    def __init__(self, base_url, api_key):
        """
        Initializes a new instance of the ScraperAPI class, which extends BaseAPI. This class is designed to interact with scraper-related endpoints of an API.

        Args:
            base_url (str): The root URL for the API endpoints.
            api_key (str): The API key used for authenticating requests.
        """
        self.base_url = base_url
        super().__init__(api_key)

    def scrape(self, batch_id: int, offset: int = 0, limit: int = 1000, export_csv: bool = False):
        """
        Retrieves scraped data for a specific batch ID from the scraper endpoint and optionally exports the data to CSV format.

        Args:
            batch_id (int): The ID of the batch to retrieve data for.
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The maximum number of records to retrieve. Defaults to 1000.
            export_csv (bool): If True, returns the scraped data in CSV format as bytes. If False, returns it as a dictionary.

        Returns:
            dict | bytes | None: A dictionary containing scraped data if successful, bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/scraper/{batch_id}"
        params = {'offset': offset, 'limit': limit}
        try:
            response = self.get(url, params=params)
            if response:
                collected_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(collected_data)
                else:
                    return collected_data
        except Exception as e:
            print(f"Response error: {e}")
        return None
    
    def scrape_planning(self, planning_id: int, offset: int = 0, limit: int = 1000, export_csv: bool = False):
        """
        Retrieve all unique data for a given planning ID from the scraper endpoint and optionally exports the data to CSV format.

        Args:
            planning_id (int): The ID of the planning to retrieve data for.
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The maximum number of records to retrieve. Defaults to 1000.
            export_csv (bool): If True, returns the scraped planning data in CSV format as bytes. If False, returns it as a dictionary.

        Returns:
            dict | bytes | None: A dictionary containing scraped planning data if successful, bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/scraper/planning/{planning_id}"
        params = {'offset': offset, 'limit': limit}
        try:
            response = self.get(url, params=params)
            if response:
                scraped_planning = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(scraped_planning)
                else:
                    return scraped_planning
        except Exception as e:
            print(f"Response error: {e}")
        return None
   
    def scrape_planning_ips(self, planning_id: int, date: str = None):
        """
        Retrieves IP addresses related to a specific planning ID and date from the scraper endpoint.

        Args:
            planning_id (int): The ID of the planning to retrieve IP addresses for.
            date (str, optional): The date for which to retrieve IP addresses. Defaults to None.

        Returns:
            dict | None: A dictionary containing IP addresses related to the planning if the request is successful; None otherwise.
        """
        url = f"{self.base_url}/scraper/planning_ips/{planning_id}/{date}"
        params = {'date': date}
        try:
            response = self.get(url, params=params)
            if response:
                planning_ips = response.json()
                return planning_ips
        except Exception as e:
            print(f"Response error: {e}")
        return None
    
    def scrape_planning_ipam(self, planning_id: int, date: str = None):
        """
        Retrieve all IPs for a given planning id new then given datetime value

        Args:
            planning_id (int): The ID of the planning to retrieve IP addresses for.
            date (str, optional): The date for which to retrieve IP addresses. Defaults to None.

        Returns:
            dict | None: A dictionary containing IP addresses related to the planning if the request is successful; None otherwise.
        """
        url = f"{self.base_url}/scraper/planning_ipam/{planning_id}/{date}"
        params = {'date': date}
        try:
            response = self.get(url, params=params)
            if response:
                planning_ipams = response.json()
                return planning_ipams
        except Exception as e:
            print(f"Response error: {e}")
        return None
    
    def scrape_planning_by_hostname(self, planning_id: int, hostname: str, offset: int = 0, limit: int = 1000, export_csv: bool = False):
        """
        Retrieves all unique data for a specific planning ID and hostname from the scraper endpoint, optionally exporting the data to CSV.

        Args:
            planning_id (int): The ID of the planning to retrieve data for.
            hostname (str): The hostname to filter the data by.
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The maximum number of records to retrieve. Defaults to 1000.
            export_csv (bool): If True, returns the data in CSV format as bytes. If False, returns it as a dictionary.

        Returns:
            dict | bytes | None: A dictionary containing scraped planning data if successful, bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/scraper/planning/{planning_id}/{hostname}"
        params = {'offset': offset, 'limit': limit}
        try:
            response = self.get(url, params=params)
            if response:
                scraped_planning = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(scraped_planning)
                else:
                    return scraped_planning
        except Exception as e:
            print(f"Response error: {e}")
        return None

    
    def scrape_device(self, hostname: str, offset: int = 0, limit: int = 1000, export_csv: bool = False):
        """
        Retrieves scraped data for a specific hostname from the scraper endpoint, optionally exporting the data to CSV.

        Args:
            hostname (str): The hostname to retrieve data for.
            offset (int, optional): The offset for pagination. Defaults to 0.
            limit (int, optional): The maximum number of records to retrieve. Defaults to 1000.
            export_csv (bool): If True, returns the data in CSV format as bytes. If False, returns it as a dictionary.

        Returns:
            dict | bytes | None: A dictionary containing scraped data if successful, bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/scraper/device/{hostname}"
        params = {'offset': offset, 'limit': limit}
        try:
            response = self.get(url, params=params)
            if response:
                scraped_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(scraped_data)
                else:
                    return scraped_data
        except Exception as e:
            print(f"Response error: {e}")
        return 

    
    def scrape_batches_latest(self, export_csv: bool = False):
        """
        Retrieves the latest batch IDs and their corresponding planning IDs, optionally exporting the data to CSV.

        Args:
            export_csv (bool): If True, returns the data in CSV format as bytes. If False, returns it as a dictionary.

        Returns:
            dict | bytes | None: A dictionary containing the latest scraped batches if successful, bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/scraper/batches/latest"
        try:
            response = self.get(url)
            if response:
                scraped_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(scraped_data)
                else:
                    return scraped_data
        except Exception as e:
            print(f"Response error: {e}")
        return None

    
    def scrape_batches(self, planning_id: int, hostname: str, export_csv: bool = False):
        """
        Retrieves a list of all batch IDs and timestamps for the specified hostname and planning ID, optionally exporting the data to CSV.

        Args:
            planning_id (int): The ID of the planning to retrieve data for.
            hostname (str): The hostname to retrieve data for.
            export_csv (bool): If True, returns the data in CSV format as bytes. If False, returns it as a dictionary.

        Returns:
            dict | bytes | None: A dictionary containing scraped batches if successful, bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/scraper/batches/hostname/{hostname}/{planning_id}"
        try:
            response = self.get(url)
            if response:
                scraped_data = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(scraped_data)
                else:
                    return scraped_data
        except Exception as e:
            print(f"Response error: {e}")
        return None

    
    def start_scraper(self, scraper_info: dict):
        """
        Start the Data Collector

        Args:
            scraper_info (dict): Information required to start the scraper.

        Returns:
            dict | None: A dictionary containing the result of the scraper initiation if successful; None otherwise.
        """
        url = f"{self.base_url}/scraper"
        try:
            response = self.post(url, scraper_info)
            if response:
                started_result = response.json()
                return started_result
        except Exception as e:
            print(f"Response error: {e}")
        return None
    
    def clean_logs(self, datetime: str):
        """
        Cleans results and logging older than given datetime.

        Args:
            datetime (str): The datetime to clean logs for. (yyyy-mm-dd hh:mm)

        Returns:
            dict | None: A dictionary containing the result of the log cleaning if successful; None otherwise.
        """
        request_data = {
            "datetime": datetime
        }
        url = f"{self.base_url}/scraper/clean"
        try:
            response = self.post(url, request_data)
            if response:
                clean_result = response.json()
                return clean_result
        except Exception as e:
            print(f"Response error: {e}")
        return None
    
    def get_status(self):
        """
        Retrieves the status of the scraper.

        Returns:
            dict | None: A dictionary containing the status of the scraper if successful; None otherwise.
        """
        url = f"{self.base_url}/scraper/status"
        try:
            response = self.get(url)
            if response:
                scraper_status = response.json()
                return scraper_status
        except Exception as e:
            print(f"Response error: {e}")
        return None


    def get_queue_list(self, export_csv: bool = False):
        """
        Gives a list of currently queued tasks for the scraper

        Args:
            export_csv (bool): If True, returns the crawlers data in CSV format as bytes. If False, returns list of crawlers.

        Returns:
            list[dict] | bytes | None: A list of crawlers if successful, bytes if exporting to CSV, None otherwise.
        """
        url = f"{self.base_url}/scraper/queue/list"
        try:
            response = self.post(url, None)
            if response:
                queue_list = response.json()
                if export_csv:
                    return self.json_to_csv_bytes(queue_list)
                else:
                    return queue_list
        except Exception as e:
            print(f"Response error: {e}")

        return None
    
    def clear_queue(self):
        """
        Clears the queue of the scraper by sending a DELETE request to the queue list endpoint.

        Returns:
            dict | None: The result of clearing the queue if successful, None otherwise.
        """
        url = f"{self.base_url}/scraper/queue/clear"
        
        try:
            response = self.delete(url)
            
            if response:
                clear_result = response.json()
                return clear_result
        except Exception as e:
            print(f"Response error: {e}")

        return None
    