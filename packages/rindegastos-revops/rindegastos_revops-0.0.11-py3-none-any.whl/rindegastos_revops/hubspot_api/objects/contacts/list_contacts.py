from ..list import List
from ....hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from typing import Optional

class ContactsList():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 archived:bool,
                 properties:List):
        
        self.contacts_list = List(
            client=client,
            object_endpoint = Endpoints.CONTACTS,
            archived = archived,
            properties = properties)

    def records(self, test:Optional[bool]):
        object_records = self.contacts_list.all_pages_df(test)
        return object_records