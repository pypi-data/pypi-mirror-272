from ..list import List
from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from typing import Optional

class CompaniesList():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 archived:bool,
                 properties:List):
        
        self.companies_list = List(
            client=client,
            object_endpoint = Endpoints.COMPANIES,
            archived = archived,
            properties = properties)

    def records(self, test:Optional[bool]):
        object_records = self.companies_list.all_pages_df(test)
        return object_records