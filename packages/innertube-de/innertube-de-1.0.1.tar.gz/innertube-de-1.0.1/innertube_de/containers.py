from dataclasses import dataclass
from typing import List, Dict, Optional
from innertube_de.endpoints import Endpoint
from innertube_de.items import Item
from innertube_de.types import ShelfType
from innertube_de.utils import get_endpoint, get_item, get_items


@dataclass(kw_only=True)
class Shelf(List[Item]):
    title: Optional[str] = None
    endpoint: Optional[Endpoint] = None

    def dump(self) -> Dict:
        return dict(
            type=ShelfType.SHELF.value,
            title=self.title,
            endpoint=None if self.endpoint is None else self.endpoint.dump(),
            items=[item.dump() for item in self],
        )

    def load(self, data: Dict) -> None:
        self.title = data["title"]
        self.endpoint = None if data["endpoint"] is None else get_endpoint(data["endpoint"])
        for item in get_items(data["items"]):
            self.append(item)


@dataclass(kw_only=True)
class CardShelf(Shelf):
    item: Optional[Item] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update(dict(
            type=ShelfType.CARD_SHELF.value,
            item=None if self.item is None else self.item.dump()
        ))
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.item = get_item(data["item"])


@dataclass(kw_only=True)
class Container(List[Shelf]):
    header: Optional[Item] = None 

    def dump(self) -> Dict:
        return dict(
            header=None if self.header is None else self.header.dump(),
            contents=[shelf.dump() for shelf in self]
        )

    def load(self, data: Dict) -> None:
        self.header = None if data["header"] is None else get_item(data["header"])
        for shelf_data in data["contents"]:
            match shelf_data["type"]:
                case ShelfType.SHELF.value:
                    shelf = Shelf()
                case ShelfType.CARD_SHELF.value:
                    shelf = CardShelf()
                case _:
                    raise TypeError(
                        f"Invalid type: {shelf_data['type']}. "
                        f"Expected type: {ShelfType.SHELF.value} or {ShelfType.CARD_SHELF.value}"
                    )
            shelf.load(shelf_data)
            self.append(shelf)
