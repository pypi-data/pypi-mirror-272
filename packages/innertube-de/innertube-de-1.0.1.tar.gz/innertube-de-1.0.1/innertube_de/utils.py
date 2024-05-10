import re

from datetime import time, date

from typing import (
    Optional,
    Callable,
    List,
    Any,
    Dict,
    Union
)

from innertube_de.errors import AccessError

from innertube_de.items import (
    Item,
    RadioItem,
    ChannelItem,
    YouTubeVideoItem,
    YouTubeMusicVideoItem,
    ArtistItem,
    AlbumItem,
    EPItem,
    YouTubePlaylistItem,
    YouTubeMusicPlaylistItem,
    SingleItem,
    SongItem,
    ProfileItem,
    PodcastItem,
    EpisodeItem
)

from innertube_de.endpoints import (
    ContinuationEndpoint,
    WatchEndpoint,
    BrowseEndpoint,
    YouTubeBrowseEndpoint,
    UrlEndpoint,
    SearchEndpoint,
    Endpoint
)

from innertube_de.types import (
    EndpointType,
    ItemType
)


def return_on_input_none(func: Callable) -> Callable:
    def inner(*args, **kwargs) -> Optional[str]:
        if len(args) > 2:
            raise TypeError("The function must receive only one argument.")
        elif len(args) > 1 and args[1] is None or len(args) == 1 and args[0] is None:
            return
        else:
            return func(*args, **kwargs)
    return inner


def get(ds: Union[List, Dict], *keys) -> Any:
    try:
        return ds if len(keys) == 0 else get(ds[keys[0]], *keys[1:])
    except (KeyError, TypeError, IndexError) as error:
        raise AccessError(data=ds, prefix=f"{error.__class__.__name__}: {error.args[0]}. ")


def clc_int(string: str) -> int:
    patterns = [
        r'(\d+)(?:\.(\d+))?([KMB])',
        r'(\d+)\s(plays|views|video|songs|song|subscribers)'
    ]

    result: Optional[str] = None
    for pattern in patterns:
        regex = re.compile(pattern)
        func_match = regex.search(string)
        if func_match is not None:
            result = func_match.group()

    if result is None:
        raise ValueError(f"Invalid input: {string}")

    last_char = result[-1]
    if last_char.isupper():
        match last_char:
            case "B":
                factor = 1000000000
            case "M":
                factor = 1000000
            case "K":
                factor = 1000
            case _:
                raise ValueError(f"Invalid character: {last_char}. Expected character: 'B', 'M' or 'K'")
        return int(float(result[:-1]) * factor)
    else:
        return int(result.split()[0])


def clc_views(string: str) -> int:
    return int(string.split()[0].replace(",", ""))


def clc_length(string: str) -> time:
    time_list = list(map(int, [x for x in string.split(":")]))
    match len(time_list):
        case 3:
            return time(hour=time_list[0], minute=time_list[1], second=time_list[2])
        case 2:
            return time(minute=time_list[0], second=time_list[1])
        case _:
            raise ValueError(f"Unexpected time format: {string}")


def clc_publication_date(string: str) -> date:
    month, day, year = string.split()
    return date(month=get_month_num(month), day=int(day[:-1]), year=int(year))


@return_on_input_none
def get_publication_date(data: Dict) -> Optional[date]:
    return date(month=data["month"], day=data["day"], year=data["year"])


@return_on_input_none
def get_length(data: Dict) -> Optional[time]:
    return time(hour=data["hour"], minute=data["minute"], second=data["second"])


@return_on_input_none
def get_item_type(string: str) -> Optional[ItemType]:
    if string.lower() == "fans might also like":
        return ItemType.ARTIST
    if _match("song", string):
        return ItemType.SONG
    if _match("single", string):
        return ItemType.SINGLE
    if _match("video", string):
        return ItemType.YOUTUBE_MUSIC_VIDEO
    if _match("playlist", string):
        return ItemType.YOUTUBE_MUSIC_PLAYLIST
    if _match("album", string):
        return ItemType.ALBUM
    if _match("artist", string):
        return ItemType.ARTIST
    if _match("episode", string):
        return ItemType.EPISODE
    if _match("profile", string):
        return ItemType.PROFILE
    if _match("podcast", string):
        return ItemType.PODCAST
    if _match("ep", string):
        return ItemType.EP


def _match(seq: str, title: str) -> bool:
    return re.search(seq, title, re.IGNORECASE) is not None


def to_int(el: Optional[str] = None) -> Optional[int]:
    return int(el) if isinstance(el, str) and el.isdigit() else None


def get_month_num(month: str) -> int:
    match month.lower():
        case "jan":
            return 1
        case "feb":
            return 2
        case "mar":
            return 3
        case "apr":
            return 4
        case "may":
            return 5
        case "jun":
            return 6
        case "jul":
            return 7
        case "aug":
            return 8
        case "sep":
            return 9
        case "oct":
            return 10
        case "nov":
            return 11
        case "dec":
            return 12
        case _:
            raise ValueError(f"Invalid input: {month}. Expected input: 'jan', 'feb', ..., 'dec'")


@return_on_input_none
def get_items(data: List) -> List[Item]:
    return [get_item(item_data) for item_data in data]


@return_on_input_none
def get_item(data: Dict) -> Item:
    match data["type"]:
        case ItemType.RADIO.value:
            item = RadioItem()
        case ItemType.ARTIST.value:
            item = ArtistItem()
        case ItemType.YOUTUBE_VIDEO.value:
            item = YouTubeVideoItem()
        case ItemType.YOUTUBE_MUSIC_VIDEO.value:
            item = YouTubeMusicVideoItem()
        case ItemType.ALBUM.value:
            item = AlbumItem()
        case ItemType.EP.value:
            item = EPItem()
        case ItemType.YOUTUBE_PLAYLIST.value:
            item = YouTubePlaylistItem()
        case ItemType.YOUTUBE_MUSIC_PLAYLIST.value:
            item = YouTubeMusicPlaylistItem()
        case ItemType.SINGLE.value:
            item = SingleItem()
        case ItemType.SONG.value:
            item = SongItem()
        case ItemType.PROFILE.value:
            item = ProfileItem()
        case ItemType.PODCAST.value:
            item = PodcastItem()
        case ItemType.EPISODE.value:
            item = EpisodeItem()
        case ItemType.CHANNEL.value:
            item = ChannelItem()
        case None:
            item = Item()
        case _:
            raise ValueError(
                f"Invalid key type: {data['type']}. Expected key type: "
                f"{', '.join([str(x) for x in ItemType.__members__.values()])}"
            )
    item.load(data)
    return item


@return_on_input_none
def get_endpoint(data: Dict) -> Endpoint:
    match data["type"]:
        case EndpointType.URL.value:
            endpoint = UrlEndpoint()
        case EndpointType.BROWSE.value:
            endpoint = BrowseEndpoint()
        case EndpointType.YOUTUBE_BROWSE.value:
            endpoint = YouTubeBrowseEndpoint()
        case EndpointType.SEARCH.value:
            endpoint = SearchEndpoint()
        case EndpointType.WATCH.value:
            endpoint = WatchEndpoint()
        case EndpointType.CONTINUATION.value:
            endpoint = ContinuationEndpoint()
        case _:
            raise ValueError(
                f"Invalid data type: {data['type']}. Expected data type: "
                f"{', '.join([str(x) for x in EndpointType.__members__.values()])}"
            )
    endpoint.load(data)
    return endpoint
