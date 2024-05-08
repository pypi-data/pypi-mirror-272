"""Classes to handle API queries/searches"""
import aiohttp
from tmticket.model import Venue, Event, Attraction, Classification

class BaseQuery:
    """Base query/parent class for specific search types."""
    attr_map = {
        'start_date_time': 'startDateTime',
        'end_date_time': 'endDateTime',
        'onsale_start_date_time': 'onsaleStartDateTime',
        'onsale_end_date_time': 'onsaleEndDateTime',
        'country_code': 'countryCode',
        'state_code': 'stateCode',
        'venue_id': 'venueId',
        'attraction_id': 'attractionId',
        'segment_id': 'segmentId',
        'segment_name': 'segmentName',
        'classification_name': 'classificationName',
        'classification_id': 'classificationId',
        'market_id': 'marketId',
        'promoter_id': 'promoterId',
        'dma_id': 'dmaId',
        'include_tba': 'includeTBA',
        'include_tbd': 'includeTBD',
        'client_visibility': 'clientVisibility',
        'include_test': 'includeTest',
        'keyword': 'keyword',
        'id': 'id',
        'sort': 'sort',
        'page': 'page',
        'size': 'size',
        'locale': 'locale',
        'latlong': 'latlong',
        'radius': 'radius'
    }

    def __init__(self, api_client, method, model):
        self.api_client = api_client
        self.method = method
        self.model = model

    async def __get(self, **kwargs):
        """Asynchronously sends final request to `ApiClient`"""
        url = f"{self.api_client.url}/{self.method}"
        async with self.api_client.session.get(url, params={**self.api_client.api_key, **kwargs}) as response:
            if response.status == 200:
                return await response.json()
            else:
                response.raise_for_status()

    async def _get(self, keyword=None, entity_id=None, sort=None, include_test=None, page=None, size=None, locale=None, **kwargs):
        """Asynchronously handles basic API search request"""
        search_args = {
            'keyword': keyword,
            'id': entity_id,
            'sort': sort,
            'include_test': include_test,
            'page': page,
            'size': size,
            'locale': locale,
            **kwargs
        }
        params = self._search_params(**search_args)
        return await self.__get(**params)

    async def by_id(self, entity_id):
        """Asynchronously get a specific object by its ID"""
        return await self._get(entity_id=entity_id)

    def _search_params(self, **kwargs):
        """Maps parameter names to API-friendly parameters"""
        return {self.attr_map.get(k, k): v for k, v in kwargs.items() if v is not None}

class AttractionQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'attractions', Attraction)

    async def find(self, **kwargs):
        return await self._get(**kwargs)

class ClassificationQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'classifications', Classification)

    async def find(self, **kwargs):
        return await self._get(**kwargs)

    def segment_by_id(self, segment_id):
        """Return a ``Segment`` matching this ID"""
        return self.by_id(segment_id).segment

    def genre_by_id(self, genre_id):
        """Return a ``Genre`` matching this ID"""
        genre = None
        resp = self.by_id(genre_id)
        if resp.segment:
            for genre in resp.segment.genres:
                if genre.id == genre_id:
                    return genre

    def subgenre_by_id(self, subgenre_id):
        """Return a ``SubGenre`` matching this ID"""
        subgenre = None
        resp = self.by_id(subgenre_id)
        if resp.segment:
            subgenres = [subg for genre in resp.segment.genres for subg in genre.subgenres]
            for subg in subgenres:
                if subg.id == subgenre_id:
                    return subg


class EventQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'events', Event)

    async def find(self, **kwargs):
        return await self._get(**kwargs)

class VenueQuery(BaseQuery):
    def __init__(self, api_client):
        super().__init__(api_client, 'venues', Venue)

    async def find(self, **kwargs):
        return await self._get(**kwargs)
