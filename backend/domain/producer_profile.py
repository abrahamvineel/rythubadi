from dataclasses import dataclass, field, replace
from uuid import UUID
from domain.exceptions import UnauthorisedOperationError, NoProducerTypeError, InvalidProducerTypeError, ProductAlreadyExistsError
from domain.producer_type import ProducerType
from domain.product import Product

@dataclass(frozen=True)
class ProducerProfile:
    producer_id: UUID
    producer_types: frozenset[ProducerType]
    name: str
    products: frozenset[Product] = field(default_factory=frozenset)

    def __post_init__(self):
        if len(self.producer_types) == 0:
            raise NoProducerTypeError("Producer types are empty")
        elif all(not isinstance(types, ProducerType) for types in self.producer_types):
            raise InvalidProducerTypeError("Producer type is invalid")

    def check_ownership(self, requesting_producer_id: UUID) -> None:
        if requesting_producer_id != self.producer_id:
            raise UnauthorisedOperationError("Requesting producer id is not matching")
    
    def add_product(self, product: Product, requesting_producer_id: UUID):
        self.check_ownership(requesting_producer_id)
        if product in self.products:
            raise ProductAlreadyExistsError("Product already is already added")
        return replace(self, products=frozenset([*self.products, product]))
