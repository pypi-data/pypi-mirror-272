""" Class representing the OpenGateClient """

import openpyxl
import requests
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from .datapoints.datapoints import DataPointsBuilder
from .datasets.datasets import DataSetsBuilder
from .timeseries.timeseries import TimeSeriesBuilder
from .entities.entities import EntitiesBuilder
from .provision_processor.provision_processor import ProvisionProcessorBuilder
from .operations.operations import OperationsBuilder
from .ai_models.ai_models import AIModelsBuilder
from .ai_pipelines.ai_pipelines import AIPipelinesBuilder
from .ai_transformers.ai_transformers import AITransformersBuilder
from .rules.rules import RulesBuilder
from .collection.iot_collection import IotCollectionBuilder
from .collection.iot_bulk_collection import IotBulkCollectionBuilder


class OpenGateClient:
    """ Class representing the OpenGateClient """

    def __init__(self, url: str | None = None, user: str | None = None, password: str | None = None,
                 api_key: str | None = None) -> None:
        self.url: str = url
        self.user: str = user
        self.password: str | None = password
        self.api_key: str | None = api_key
        self.headers: dict[str, str] = {}
        self.client: OpenGateClient = self
        self.entity_type: str | None = None
        disable_warnings(InsecureRequestWarning)

        if not url:
            raise ValueError('You have not provided a URL')

        if user and password:
            data_user = {
                'email': self.user,
                'password': self.password
            }
            try:
                login_url = self.url + '/north/v80/provision/users/login'
                request = requests.post(login_url, json=data_user, timeout=5000, verify=False)
                request.raise_for_status()
                response_json = request.json()
                if 'user' in response_json:
                    self.headers.update({
                        'Authorization': f'Bearer {response_json["user"]["jwt"]}',
                    })
                else:
                    raise ValueError('Empty response received')

            except requests.exceptions.HTTPError as err:
                raise requests.exceptions.HTTPError(f'Request failed: {err}')
            except requests.exceptions.RequestException as error:
                raise requests.exceptions.RequestException(f'Connection failed: {error}')
        elif api_key:
            self.headers.update({
                'X-ApiKey': self.api_key
            })
        else:
            raise ValueError('You have not provided an API key or user and password')

    def data_sets(self) -> DataSetsBuilder:
        """ Represents the builder of datasets """
        return DataSetsBuilder(self)

    def timeseries(self) -> TimeSeriesBuilder:
        """ Represents the builder of timeseries """
        return TimeSeriesBuilder(self)

    def entities(self) -> EntitiesBuilder:
        """ Represents the builder of entities """
        return EntitiesBuilder(self)

    def provision_processor(self) -> ProvisionProcessorBuilder:
        """ Represents the builder of provision processors """
        return ProvisionProcessorBuilder(self)

    def operations(self) -> OperationsBuilder:
        """ Represents the builder of operations """
        return OperationsBuilder(self)

    def data_points_builder(self) -> DataPointsBuilder:
        """ Represents the builder of datapoints """
        return DataPointsBuilder(self)

    def ai_models_builder(self) -> AIModelsBuilder:
        """ Represents the builder of artificial intelligence models """
        return AIModelsBuilder(self)

    def ai_pipelines_builder(self) -> AIPipelinesBuilder:
        """ Represents the builder of artificial intelligence models """
        return AIPipelinesBuilder(self)

    def ai_transformers_builder(self) -> AITransformersBuilder:
        """ Represents the builder of artificial intelligence models """
        return AITransformersBuilder(self)

    def rules_builder(self) -> RulesBuilder:
        """ Represents the builder rules """
        return RulesBuilder(self)

    def new_iot_collection_builder(self) -> IotCollectionBuilder:
        """ Represents the builder iot collection builder """
        return IotCollectionBuilder(self)

    def new_iot_bulk_collection_builder(self) -> IotBulkCollectionBuilder:
        """ Represents the builder iot bulk collection builder """
        return IotBulkCollectionBuilder(self)
