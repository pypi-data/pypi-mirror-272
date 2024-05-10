import logging

from datetime import time, date

from typing import (
    Optional,
    Tuple,
    Union,
    List,
    Dict,
    Callable,
    Any
)

from innertube_de.endpoints import (
    ContinuationEndpoint,
    Endpoint,
    BrowseEndpoint,
    YouTubeBrowseEndpoint,
    WatchEndpoint,
    UrlEndpoint,
    SearchEndpoint
)

from innertube_de.containers import (
    CardShelf,
    Shelf,
    Container
)

from innertube_de.items import (
    Item,
    RadioItem,
    YouTubeMusicVideoItem,
    YouTubeVideoItem,
    YouTubeMusicPlaylistItem,
    YouTubePlaylistItem,
    ChannelItem,
    AlbumItem,
    ArtistItem,
    SongItem,
    SingleItem,
    EPItem,
    PodcastItem,
    ProfileItem,
    EpisodeItem,
)

from innertube_de.types import (
    EndpointType,
    ContinuationStrucType,
    ItemStructType,
    ShelfStructType,
    ResultStructType,
    ItemType,
    TextDivisorType
)

from innertube_de.utils import (
    get_item_type,
    to_int,
    return_on_input_none,
    get,
    clc_length,
    clc_publication_date,
    clc_int,
    clc_views
)

from innertube_de.errors import (
    ErrorWrapper,
    AccessError,
    ExtractionError
)

log = logging.getLogger(__name__)


def extract(
        data: Dict,
        *,
        log_errors: bool = True,
        stack_info: bool = True,
        exc_info: bool = True,
        enable_exceptions: bool = True,
        include_all_urls: bool = True
) -> Container:
    innertube_de = InnerTubeDE(
        log_errors=log_errors,
        stack_info=stack_info,
        exc_info=exc_info,
        enable_exceptions=enable_exceptions,
        include_all_urls=include_all_urls
    )
    return innertube_de.extract(data)


class InnerTubeDE:
    def __init__(
            self,
            *,
            log_errors: bool = True,
            stack_info: bool = True,
            exc_info: bool = True,
            enable_exceptions: bool = True,
            include_all_urls: bool = False
    ) -> None:
        self.log_errors = log_errors
        self.stack_info = stack_info
        self.exc_info = exc_info
        self.enable_exceptions = enable_exceptions
        self.include_all_urls = include_all_urls

    @staticmethod
    def _handle_main_function(func: Callable) -> Callable:
        def inner(self, data: Dict) -> Container:
            if not isinstance(data, Dict):
                raise TypeError(f"Invalid input type: {type(data)}. Expected input type: Dict")
            try:
                result = func(self, data)
            except Exception:
                raise ExtractionError(
                    "An error occurred during the data extraction process. "
                    "Please open an issue at https://github.com/g3nsy/innertube-de/issues"
                    " and reports this log message."
                )
            else:
                return result

        return inner

    @_handle_main_function
    def extract(self, data: Dict) -> Container:
        header_data = self._get(data, "header", opt=True)
        if header_data is None:
            header = None
        else:
            header = self._extract_item(header_data)

        data_contents = self._extract_contents(data)
        container = Container(header=header)

        if data_contents is None:
            return container

        for entry in data_contents:
            shelf = self._extract_shelf(entry)
            if shelf is not None:
                container.append(shelf)

        return container

    @staticmethod
    def _handle_exception(func: Callable) -> Callable:
        def inner(*args, opt: bool = False, **kwargs) -> Optional[Any]:
            try:
                return func(*args, **kwargs)
            except Exception as error:
                if opt is False:
                    # _ErrorWrapper prevent the following from occurring:
                    # [2024-04-17 19:17:46,845 ERROR in extractor]: Executing function _clc_int ...
                    # [2024-04-17 19:17:46,845 ERROR in extractor]: Executing function _extract_item ...
                    # [2024-04-17 19:17:46,845 ERROR in extractor]: Executing function _extract_shelf ...
                    if args[0].log_errors is True and not isinstance(error, ErrorWrapper):
                        log.error(
                            f"Executing function {func.__name__} caused an exception: "
                            f"{error.__class__.__name__}"
                            f": {error.args[0]}" if error.args[0] is not None else "",
                            stack_info=False if args[0].enable_exceptions is True else args[0].stack_info,
                            exc_info=False if args[0].enable_exceptions is True else args[0].exc_info
                        )

                    if args[0].enable_exceptions is True:
                        if isinstance(error, ErrorWrapper):
                            raise error
                        else:
                            raise ErrorWrapper(error)
                return None

        return inner

    @_handle_exception
    def _extract_contents(self, data: Dict) -> Optional[List[Dict]]:
        if ContinuationStrucType.CONTINUATION in data:
            ds = self._get(data, ContinuationStrucType.CONTINUATION)
            if ContinuationStrucType.SECTION_LIST in ds:
                ds = self._get(ds, ContinuationStrucType.SECTION_LIST, "contents")

                if ShelfStructType.ITEM_SECTION in self._get(ds, 0):
                    shelves: List[Dict] = []
                    for entry in ds:
                        tmp = self._get(entry, ShelfStructType.ITEM_SECTION, "contents", 0)
                        if ItemStructType.CHANNEL_VIDEO_PLAYER in tmp:
                            shelves.append({ShelfStructType.CHANNEL_SHELF: {"contents": [tmp]}})
                        else:
                            shelves.append(tmp)
                    return shelves

                else:
                    return ds

            elif ContinuationStrucType.MUSIC_PLAYLIST_SHELF in ds:
                return [{
                    ShelfStructType.MUSIC_SHELF: self._get(
                        ds, ContinuationStrucType.MUSIC_PLAYLIST_SHELF
                    )
                }]

            elif ContinuationStrucType.MUSIC_SHELF in ds:
                return [{
                    ShelfStructType.MUSIC_SHELF: self._get(
                        ds, ContinuationStrucType.MUSIC_SHELF
                    )
                }]

            elif ShelfStructType.PLAYLIST_VIDEO_LIST_CONTINUATION in ds:
                return [ds]

            else:
                raise AccessError(data=ds)

        elif ResultStructType.ON_RESPONSE_RECEIVED_ENDPOINTS in data:
            tmp = self._get(
                data, ResultStructType.ON_RESPONSE_RECEIVED_ENDPOINTS, 0,
                "appendContinuationItemsAction", "continuationItems", opt=True
            )

            if tmp is not None:
                return tmp

        data = self._get(data, "contents", opt=True)
        if data is None:
            return None

        if ResultStructType.TWO_COLUMN_BROWSE_RESULT in data:
            ds = self._get(data, ResultStructType.TWO_COLUMN_BROWSE_RESULT)

            if "secondaryContents" in ds:
                return self._get(ds, "secondaryContents", "sectionListRenderer", "contents")

            elif "tabs" in ds:
                tmp = self._get(
                    ds, "tabs", 0, "tabRenderer", "content", "sectionListRenderer", "contents"
                )
                shelves: List[Dict] = []
                for entry in tmp:
                    if ItemStructType.CONTINUATION_ITEM in entry:
                        continue
                    tmp1 = self._get(entry, ShelfStructType.ITEM_SECTION, "contents", 0)
                    if ItemStructType.CHANNEL_VIDEO_PLAYER in tmp1:
                        shelves.append({ShelfStructType.CHANNEL_SHELF: {"contents": [tmp1]}})
                    else:
                        shelves.append(tmp1)
                return shelves
            else:
                raise AccessError(data=ds)

        elif ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS in data:
            tmp1 = self._get(
                data, ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS, "tabs", 0,
                "tabRenderer", "content", "sectionListRenderer", opt=True
            )

            if tmp1 is not None:
                tmp2 = self._get(tmp1, "contents", 0, opt=True)
                if tmp2 is not None:
                    if ShelfStructType.GRID in tmp2:
                        return self._get(tmp1, "contents")
                    elif ShelfStructType.MUSIC_PLAYLIST_SHELF in tmp2:
                        return [tmp2]
                    elif ShelfStructType.MUSIC_CAROUSEL_SHELF in tmp2:
                        return self._get(tmp1, "contents")
                    elif ShelfStructType.MUSIC_SHELF in tmp2:
                        return self._get(tmp1, "contents")
                    else:
                        raise AccessError(data=tmp2)
                else:
                    return None
            else:
                return None

        elif ResultStructType.TABBED_SEARCH_RESULTS in data:
            return self._get(
                data, ResultStructType.TABBED_SEARCH_RESULTS, "tabs", 0, "tabRenderer",
                "content", "sectionListRenderer", "contents"
            )

        elif ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT in data:
            tmp = self._get(
                data, ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT, "tabbedRenderer",
                "watchNextTabbedResultsRenderer", "tabs", 0, "tabRenderer", "content",
                "musicQueueRenderer", "content", ShelfStructType.PLAYLIST_PANEL, opt=True
            )
            if tmp is not None:
                return [{ShelfStructType.PLAYLIST_PANEL: tmp}]

        elif ResultStructType.TWO_COLUMN_SEARCH_RESULTS in data:
            contents = self._get(
                data, ResultStructType.TWO_COLUMN_SEARCH_RESULTS, "primaryContents",
                "sectionListRenderer", "contents", 0, "itemSectionRenderer", "contents"
            )

            results: List[Dict] = []
            shelf_contents: List[Dict] = []
            for entry in contents:
                key = list(entry.keys())[0]
                if ItemStructType.has_value(key):
                    shelf_contents.append(entry)
                elif ShelfStructType.has_value(key):
                    results.append(entry)
                    if len(shelf_contents) != 0:
                        results.append({ShelfStructType.CHANNEL_SHELF: {"contents": shelf_contents}})
                        shelf_contents.clear()
                else:
                    raise AccessError(data=entry, prefix=f"Key used: {key}. ")

            if len(shelf_contents) != 0:
                results.append({ShelfStructType.CHANNEL_SHELF: {"contents": shelf_contents}})

            secondary_contents = self._get(
                data, ResultStructType.TWO_COLUMN_SEARCH_RESULTS, "secondaryContents",
                "secondarySearchContainerRenderer", "contents", 0, "universalWatchCardRenderer",
                "sections", opt=True
            )

            if secondary_contents is not None:
                for entry in secondary_contents:
                    results.append(self._get(entry, "watchCardSectionSequenceRenderer", "lists", 0))

            return results

        elif ResultStructType.TWO_COLUMN_WATCH_NEXT_RESULTS in data:
            primary_content = self._get(
                data, ResultStructType.TWO_COLUMN_WATCH_NEXT_RESULTS, "results", "results", "contents"
            )

            custom_shelf = {
                ShelfStructType.NEXT_PRIMARY_SHELF: [{
                    ItemStructType.NEXT_PRIMARY_VIDEO: {
                        ItemType.YOUTUBE_VIDEO: self._get(
                            primary_content, 0, "videoPrimaryInfoRenderer"
                        ),
                        ItemType.CHANNEL: self._get(
                            primary_content, 1, "videoSecondaryInfoRenderer"
                        )
                    }
                }]
            }

            return [
                self._get(data, ResultStructType.TWO_COLUMN_WATCH_NEXT_RESULTS, "secondaryResults"),
                custom_shelf
            ]

        else:
            raise AccessError(data=data)

    @_handle_exception
    def _extract_shelf(self, entry: Dict) -> Optional[Shelf]:
        item_type = None

        if ShelfStructType.MUSIC_SHELF in entry:
            ds = self._get(entry, ShelfStructType.MUSIC_SHELF)
            name = self._get(ds, "title", "runs", 0, "text", opt=True)
            contents = self._get(ds, "contents")
            endpoint = self._extract_endpoint(self._get(ds, "bottomEndpoint", opt=True))
            if endpoint is None:
                endpoint = self._extract_endpoint(self._get(ds, "continuations", 0, opt=True))
            shelf = Shelf(title=name, endpoint=endpoint)
            item_type = get_item_type(name)

        elif ShelfStructType.MUSIC_PLAYLIST_SHELF in entry:
            ds = self._get(entry, ShelfStructType.MUSIC_PLAYLIST_SHELF)
            contents = self._get(ds, "contents")
            shelf = Shelf()

        elif ShelfStructType.MUSIC_CAROUSEL_SHELF in entry:
            ds = self._get(entry, ShelfStructType.MUSIC_CAROUSEL_SHELF)
            contents = self._get(ds, "contents")
            name = self._get(
                ds, "header", "musicCarouselShelfBasicHeaderRenderer", "title", "runs", 0, "text"
            )
            endpoint = self._extract_endpoint(
                self._get(
                    ds, "header", "musicCarouselShelfBasicHeaderRenderer", "title",
                    "runs", 0, "navigationEndpoint", opt=True
                )
            )
            shelf = Shelf(title=name, endpoint=endpoint)
            item_type = get_item_type(name)

        elif ShelfStructType.MUSIC_CARD_SHELF in entry:
            item = self._extract_item(entry)
            shelf = CardShelf(item=item)
            contents = self._get(entry, ShelfStructType.MUSIC_CARD_SHELF, "contents", opt=True)

        elif ShelfStructType.PLAYLIST_PANEL in entry:
            ds = self._get(entry, ShelfStructType.PLAYLIST_PANEL)
            name = self._get(ds, "title", opt=True)
            contents = self._get(ds, "contents")
            shelf = Shelf(title=name)
            item_type = get_item_type(name)

        elif ShelfStructType.GRID in entry:
            shelf = Shelf()
            contents = self._get(entry, ShelfStructType.GRID, "items")

        elif ShelfStructType.NEXT_PRIMARY_SHELF in entry:
            shelf = Shelf()
            contents = self._get(entry, ShelfStructType.NEXT_PRIMARY_SHELF)

        elif ShelfStructType.SHELF in entry:
            ds = self._get(entry, ShelfStructType.SHELF)
            name = self._get(ds, "title", "runs", 0, "text", opt=True)
            if name is None:
                name = self._get(ds, "title", "simpleText")
            endpoint = self._extract_endpoint(self._get(ds, "endpoint", opt=True), opt=True)
            if endpoint is None:
                endpoint = self._extract_endpoint(
                    self._get(
                        ds, "endpoint", "showEngagementPanelEndpoint", "engagementPanel",
                        "engagementPanelSectionListRenderer", "content", "sectionListRenderer",
                        "contents", 0, "itemSectionRenderer", "contents", 0, "continuationItemRenderer",
                        opt=True
                    )
                )
            # TODO: Improve this
            contents = self._get(ds, "content", "horizontalListRenderer", "items", opt=True)
            if contents is None:
                contents = self._get(ds, "content", "verticalListRenderer", "items", opt=True)
                if contents is None:
                    contents = self._get(ds, "content", "expandedShelfContentsRenderer", "items")
            shelf = Shelf(title=name, endpoint=endpoint)
            item_type = get_item_type(name)

        elif ShelfStructType.SECONDARY_RESULTS in entry:
            contents = self._get(entry, ShelfStructType.SECONDARY_RESULTS, "results")
            shelf = Shelf()

        elif ShelfStructType.PLAYLIST_VIDEO_LIST_CONTINUATION in entry:
            contents = self._get(entry, ShelfStructType.PLAYLIST_VIDEO_LIST_CONTINUATION, "contents")
            shelf = Shelf()

        elif ShelfStructType.PLAYLIST_VIDEO_LIST in entry:
            contents = self._get(entry, ShelfStructType.PLAYLIST_VIDEO_LIST, "contents")
            shelf = Shelf()

        elif ShelfStructType.CHANNEL_SHELF in entry:
            contents = self._get(entry, ShelfStructType.CHANNEL_SHELF, "contents")
            shelf = Shelf()

        elif ShelfStructType.REEL_SHELF in entry:
            ds = self._get(entry, ShelfStructType.REEL_SHELF)
            name = self._get(ds, "title", "runs", 0, "text", opt=True)
            if name is None:
                name = self._get(ds, "title", "simpleText")
            contents = self._get(ds, "items")
            shelf = Shelf(title=name)

        elif ShelfStructType.HORIZONTAL_CARD_LIST_RENDERER in entry:
            ds = self._get(entry, ShelfStructType.HORIZONTAL_CARD_LIST_RENDERER)
            name = self._get(ds, "header", "titleAndButtonListHeaderRenderer", "title", "simpleText", opt=True)
            if name is None:
                name = self._get(ds, "header", "richListHeaderRenderer", "title", "simpleText")
            contents = self._get(ds, "cards")
            shelf = Shelf(title=name)

        elif ShelfStructType.VERTICAL_WATCH_CARD_LIST in entry:
            ds = self._get(entry, ShelfStructType.VERTICAL_WATCH_CARD_LIST)
            contents = self._get(ds, "items")
            shelf = Shelf()

        elif (
                ShelfStructType.ITEM_SECTION in entry
                or ShelfStructType.MUSIC_DESCRIPTION_SHELF in entry
                or ShelfStructType.SHOWING_RESULTS_FOR in entry
                or ShelfStructType.RECOGNITION_SHELF in entry
        ):
            return None

        else:
            raise AccessError(data=entry)

        if contents is not None:
            for entry_item in contents:
                item = self._extract_item(entry_item, item_type)
                if item is not None:
                    shelf.append(item)
        return shelf

    @_handle_exception
    def _extract_item(self, entry_item: Dict, item_type: Optional[ItemType] = None) -> Optional[Item]:
        if ShelfStructType.MUSIC_CARD_SHELF in entry_item:
            ds = self._get(entry_item, ShelfStructType.MUSIC_CARD_SHELF)
            item_type = get_item_type(self._get(ds, "subtitle", "runs", 0, "text"))
            name = self._get(ds, "title", "runs", 0, "text")
            endpoint = self._extract_endpoint(self._get(ds, "title", "runs", 0, "navigationEndpoint"))
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )

            match item_type:
                case ItemType.ALBUM:
                    explicit = self._is_explicit(ds)
                    item = AlbumItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, explicit=explicit
                    )

                case ItemType.ARTIST:
                    subscribers = self._clc_int(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = ArtistItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers
                    )

                case ItemType.YOUTUBE_MUSIC_VIDEO:
                    views = self._clc_int(self._get(ds, "subtitle", "runs", -3, "text"))
                    length = self._clc_length(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = YouTubeMusicVideoItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, views=views, length=length
                    )

                case ItemType.EP:
                    explicit = self._is_explicit(ds)
                    item = EPItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, explicit=explicit
                    )

                case ItemType.SONG:
                    explicit = self._is_explicit(ds)
                    length = self._clc_length(self._get(ds, "subtitle", "runs", -1, "text"))
                    album_name = self._get(ds, "subtitle", "runs", -3, "text")
                    album_endpoint = self._extract_endpoint(
                        self._get(ds, "subtitle", "runs", -3, "navigationEndpoint")
                    )

                    album_item = AlbumItem(
                        title=album_name, thumbnail_urls=thumbnail_urls, endpoint=album_endpoint
                    )

                    item = SongItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        length=length, album_item=album_item, explicit=explicit
                    )

                case ItemType.EPISODE:
                    publication_date = self._clc_publication_date(self._get(ds, "subtitle", "runs", 2))
                    item = EpisodeItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        publication_date=publication_date
                    )

                case _:
                    item = Item(title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

        elif ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM)
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint", opt=True))
            if endpoint is None:
                endpoint = self._extract_endpoint(
                    self._get(
                        ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs", -1, "navigationEndpoint"
                    )
                )
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails", opt=True)
            )
            name = self._get(
                ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer", "text", "runs", 0, "text"
            )
            if item_type is None:
                item_type = get_item_type(
                    self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs", 0, "text", opt=True
                    )
                )
                if item_type is None:
                    item_type = ItemType.SONG

            match item_type:
                case ItemType.ARTIST:
                    subscribers = self._clc_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -1, "text", opt=True
                        ),
                        opt=True
                    )
                    item = ArtistItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers
                    )

                case ItemType.ALBUM:
                    explicit = self._is_explicit(ds)
                    release_year = to_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -1, "text"
                        )
                    )
                    artist_items = self._extract_artist_items(self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs"
                    ))
                    item = AlbumItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        release_year=release_year, explicit=explicit, artist_items=artist_items
                    )

                case ItemType.YOUTUBE_MUSIC_VIDEO:
                    length = self._clc_length(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text"
                        )
                    )

                    views = self._clc_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -3, "text", opt=True
                        ), opt=True
                    )

                    artist_items = self._extract_artist_items(self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs"
                    ))

                    item = YouTubeMusicVideoItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, length=length,
                        views=views, artist_items=artist_items
                    )

                case ItemType.YOUTUBE_MUSIC_PLAYLIST:
                    artist_items = self._extract_artist_items(self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs"
                    ))
                    tracks_num = to_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text", opt=True
                        )
                    )

                    views = self._clc_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text", opt=True
                        ),
                        opt=True
                    )

                    item = YouTubeMusicPlaylistItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        tracks_num=tracks_num, views=views, artist_items=artist_items
                    )

                case ItemType.SINGLE:
                    explicit = self._is_explicit(ds)
                    release_year = to_int(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text",
                            "runs", -1, "text", opt=True
                        )
                    )
                    item = SingleItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, release_year=release_year,
                        explicit=explicit
                    )

                case ItemType.SONG:
                    explicit = self._is_explicit(ds)
                    subtitle_items = self._extract_subtitle_items(self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs", opt=True
                    ))

                    if subtitle_items is not None:
                        artist_items, album_item = subtitle_items
                    else:
                        artist_items, album_item = (None, None)

                    if album_item is None:
                        album_item = self._extract_album_item(self._get(
                            ds, "flexColumns", -1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", opt=True
                        ))

                    length = self._clc_length(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", -1, "text", opt=True
                        ),
                        opt=True
                    )
                    if length is None:
                        length = self._clc_length(
                            self._get(
                                ds, "fixedColumns", 0, "musicResponsiveListItemFixedColumnRenderer",
                                "text", "runs", 0, "text", opt=True
                            )
                        )

                    tmp = self._get(
                        ds, "flexColumns", -1, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs", -1, opt=True
                    )
                    if tmp is None:
                        reproductions = None
                    elif self._get(tmp, "navigationEndpoint", opt=True) is None:
                        reproductions = self._clc_int(self._get(tmp, "text", opt=True))
                    else:
                        reproductions = self._clc_int(
                            self._get(
                                ds, "flexColumns", -2, "musicResponsiveListItemFlexColumnRenderer",
                                "text", "runs", -1, "text"
                            )
                        )
                    item = SongItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, length=length,
                        reproductions=reproductions, explicit=explicit, artist_items=artist_items,
                        album_item=album_item
                    )

                case ItemType.EPISODE:
                    artist_items = self._extract_artist_items(self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer", "text", "runs"
                    ))
                    item = EpisodeItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, artist_items=artist_items
                    )

                case ItemType.PODCAST:
                    item = PodcastItem(title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

                case ItemType.PROFILE:
                    item_handle = self._get(
                        ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs", -1, "text"
                    )
                    item = ProfileItem(title=name, thumbnail_urls=thumbnail_urls, handle=item_handle)

                case ItemType.EP:
                    explicit = self._is_explicit(ds)
                    artist_items = self._extract_artist_items(self._get(
                        ds, "flexColumns", 0, "musicResponsiveListItemFlexColumnRenderer",
                        "text", "runs"
                    ))
                    item = EPItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, explicit=explicit,
                        artist_items=artist_items
                    )

                case _:
                    return None

        elif ItemStructType.MUSIC_TWO_ROW_ITEM in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_TWO_ROW_ITEM)
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnailRenderer", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            name = self._get(ds, "title", "runs", 0, "text")
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            if item_type is None:
                try:
                    item_type = ItemType(
                        self._get(
                            ds, "flexColumns", 1, "musicResponsiveListItemFlexColumnRenderer",
                            "text", "runs", 0, "text", opt=True
                        )
                    )
                except ValueError:
                    item_type = None

            match item_type:
                case ItemType.ARTIST:
                    subscribers = self._clc_int(self._get(ds, "subtitle", "runs", 0, "text"))
                    item = ArtistItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers
                    )

                case ItemType.ALBUM:
                    explicit = self._is_explicit(ds)
                    release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))
                    item = AlbumItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        release_year=release_year, explicit=explicit
                    )

                case ItemType.EP:
                    explicit = self._is_explicit(ds)
                    release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))
                    item = EPItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        release_year=release_year, explicit=explicit
                    )

                case ItemType.YOUTUBE_MUSIC_VIDEO:
                    artist_items = self._extract_artist_items(self._get(
                        ds, "subtitle", "runs"
                    ))
                    views = self._clc_int(self._get(ds, "subtitle", "runs", -1, "text"))
                    item = YouTubeMusicVideoItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, views=views,
                        artist_items=artist_items
                    )

                case ItemType.YOUTUBE_MUSIC_PLAYLIST:
                    item = YouTubeMusicPlaylistItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls
                    )

                case ItemType.SINGLE:
                    explicit = self._is_explicit(ds)
                    release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))
                    item = SingleItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                        release_year=release_year, explicit=explicit
                    )

                case ItemType.SONG:
                    explicit = self._is_explicit(ds)
                    item = SongItem(
                        title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, explicit=explicit
                    )

                case _:
                    item = Item(title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls)

        elif ItemStructType.PLAYLIST_PANEL_VIDEO in entry_item:
            ds = self._get(entry_item, ItemStructType.PLAYLIST_PANEL_VIDEO)
            name = self._get(ds, "title", "runs", -1, "text")
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            length = self._clc_length(self._get(ds, "lengthText", "runs", -1, "text"))
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails"))
            tmp = self._get(ds, "thumbnail", "thumbnails", -1)
            width = self._get(tmp, "width")
            height = self._get(tmp, "height")
            if width / height == 1:
                explicit = self._is_explicit(ds)
                item = SongItem(
                    title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, length=length,
                    explicit=explicit
                )
            else:
                views = self._clc_int(self._get(ds, "longBylineText", "runs", -3, "text", opt=True), opt=True)
                item = YouTubeMusicVideoItem(
                    title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, length=length, views=views
                )

        elif ItemStructType.MUSIC_IMMERSIVE_HEADER in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_IMMERSIVE_HEADER)
            description = self._extract_description(self._get(ds, "description", "runs", opt=True))
            name = self._get(ds, "title", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            subscribers = to_int(self._get(
                ds, "subscriptionButton", "subscribeButtonRenderer",
                "subscriberCountText", "runs", 0, "text"
            ))
            item = ArtistItem(
                title=name, subscribers=subscribers, description=description, thumbnail_urls=thumbnail_urls
            )

        elif ItemStructType.MUSIC_DETAIL_HEADER in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_DETAIL_HEADER)
            try:
                item_type = ItemType(self._get(ds, "subtitle", "runs", 0, "text"))
            except ValueError:
                return None

            name = self._get(ds, "title", "runs", 0, "text")

            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "croppedSquareThumbnailRenderer", "thumbnail", "thumbnails")
            )

            release_year = to_int(self._get(ds, "subtitle", "runs", -1, "text", opt=True))

            if item_type is ItemType.YOUTUBE_MUSIC_PLAYLIST:
                tracks_num = clc_int(self._get(ds, "secondSubtitle", "runs", 2, "text"))
            else:
                tracks_num = clc_int(self._get(ds, "secondSubtitle", "runs", 0, "text"))

            description = self._extract_description(self._get(ds, "description", "runs", opt=True))

            # TODO extract length: X minutes, N hour (?), K seconds (?)
            match item_type:
                case ItemType.ALBUM:
                    explicit = self._is_explicit(ds)
                    item = AlbumItem(
                        title=name, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num,
                        release_year=release_year, description=description, explicit=explicit
                    )

                case ItemType.EP:
                    explicit = self._is_explicit(ds)
                    item = EPItem(
                        title=name, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num,
                        release_year=release_year, description=description, explicit=explicit
                    )

                case ItemType.SINGLE:
                    explicit = self._is_explicit(ds)
                    item = SingleItem(
                        title=name, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num,
                        release_year=release_year, description=description, explicit=explicit
                    )

                case ItemType.YOUTUBE_MUSIC_PLAYLIST:
                    views = self._clc_int(self._get(ds, "secondSubtitle", "runs", 0, "text"))
                    item = YouTubeMusicPlaylistItem(
                        title=name, thumbnail_urls=thumbnail_urls, tracks_num=tracks_num,
                        release_year=release_year, description=description, views=views
                    )

                case _:
                    # FIXME 
                    return None

        elif ItemStructType.MUSIC_VISUAL_HEADER in entry_item:
            ds = self._get(entry_item, ItemStructType.MUSIC_VISUAL_HEADER)
            name = self._get(ds, "title", "runs", -1, "text")
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            item = Item(title=name, thumbnail_urls=thumbnail_urls)

        elif ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM in entry_item:
            ds = self._get(entry_item)
            name = self._get(ds, "title", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(
                self._get(ds, "thumbnail", "musicThumbnailRenderer", "thumbnail", "thumbnails")
            )
            endpoint = self._extract_endpoint(self._get(ds, "title", "runs", 0, "navigationEndpoint"))
            item = Item(title=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

        elif ItemStructType.NEXT_PRIMARY_VIDEO in entry_item:
            ds = self._get(entry_item, ItemStructType.NEXT_PRIMARY_VIDEO)
            video_data = self._get(ds, ItemType.YOUTUBE_VIDEO)
            item_name = self._get(video_data, "title", "runs", 0, "text")
            item_views = self._clc_views(
                self._get(
                    video_data, "viewCount", "videoViewCountRenderer", "viewCount", "simpleText"
                )
            )

            item_endpoint = WatchEndpoint(
                video_id=self._get(
                    video_data, "videoActions", "menuRenderer", "topLevelButtons", 0,
                    "segmentedLikeDislikeButtonViewModel", "likeButtonViewModel", "likeButtonViewModel",
                    "toggleButtonViewModel", "toggleButtonViewModel", "defaultButtonViewModel",
                    "buttonViewModel", "onTap", "serialCommand", "commands", 1, "innertubeCommand",
                    "modalEndpoint", "modal", "modalWithTitleAndButtonRenderer", "button",
                    "buttonRenderer", "navigationEndpoint", "signInEndpoint", "nextEndpoint",
                    "likeEndpoint", "target", "videoId"
                )
            )

            item_description = self._extract_description(
                self._get(ds, ItemType.CHANNEL, "attributedDescription", opt=True)
            )

            channel_data = self._get(ds, ItemType.CHANNEL, "owner", "videoOwnerRenderer")
            channel_thumbnail_urls = self._extract_urls(self._get(channel_data, "thumbnail", "thumbnails"))
            channel_name = self._get(channel_data, "title", "runs", 0, "text")
            channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
            channel_subscribers = self._clc_int(self._get(channel_data, "subscriberCountText", "simpleText"))
            channel_item = ChannelItem(
                title=channel_name, thumbnail_urls=channel_thumbnail_urls,
                endpoint=channel_endpoint, subscribers=channel_subscribers
            )

            item = YouTubeVideoItem(
                title=item_name, views=item_views, endpoint=item_endpoint,
                channel_item=channel_item, description=item_description
            )

        elif ItemStructType.CHANNEL_VIDEO_PLAYER in entry_item:
            ds = self._get(entry_item, ItemStructType.CHANNEL_VIDEO_PLAYER)
            name = self._get(ds, "title", "runs", 0, "text")
            description = self._extract_description(self._get(ds, "description", "runs"))
            views = self._clc_views(self._get(ds, "viewCountText", "simpleText"))
            endpoint = self._extract_endpoint(self._get(ds, "title", "runs", 0, "navigationEndpoint"))
            item = YouTubeVideoItem(title=name, endpoint=endpoint, description=description, views=views)

        elif (
                ItemStructType.CHANNEL in entry_item
                or ItemStructType.VIDEO in entry_item
                or ItemStructType.PLAYLIST_VIDEO in entry_item
                or ItemStructType.PLAYLIST in entry_item
                or ItemStructType.RADIO in entry_item
                or ItemStructType.COMPACT_VIDEO in entry_item
                or ItemStructType.COMPACT_RADIO in entry_item
                or ItemStructType.COMPACT_PLAYLIST in entry_item
                or ItemStructType.GRID_VIDEO in entry_item
                or ItemStructType.GRID_CHANNEL in entry_item
                or ItemStructType.GRID_PLAYLIST in entry_item
        ):
            ds = self._get(entry_item, list(entry_item.keys())[0])
            name = self._get(ds, "title", "simpleText", opt=True)
            if name is None:
                name = self._get(ds, "title", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails", opt=True))
            if thumbnail_urls is None:
                thumbnail_urls = self._extract_urls(self._get(ds, "thumbnails", 0, "thumbnails"))
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))

            if (
                    ItemStructType.PLAYLIST_VIDEO in entry_item
                    or ItemStructType.COMPACT_PLAYLIST in entry_item
                    or ItemStructType.COMPACT_VIDEO in entry_item
                    or ItemStructType.GRID_VIDEO in entry_item
                    or ItemStructType.VIDEO in entry_item
            ):
                views = self._clc_views(self._get(ds, "viewCountText", "simpleText", opt=True))
                if views is None:
                    views = self._clc_int(self._get(ds, "videoInfo", "runs", 0, "text", opt=True))

                length = self._clc_length(self._get(ds, "lengthText", "simpleText", opt=True))
                if length is None:
                    length = self._clc_length(
                        self._get(
                            ds, "thumbnailOverlays", 0, "thumbnailOverlayTimeStatusRenderer",
                            "text", "simpleText", opt=True
                        )
                    )

                description = self._extract_description(
                    self._get(ds, "detailedMetadataSnippets", 0, "snippetText", "runs", opt=True)
                )
                published_time = self._get(ds, "publishedTimeText", "simpleText", opt=True)
                if published_time is None:
                    published_time = self._get(ds, "videoInfo", "runs", -1, "text", opt=True)

                channel_data = self._get(ds, "shortBylineText", "runs", 0, opt=True)
                if channel_data is None:
                    channel_data = self._get(ds, "longBylineText", "runs", 0, opt=True)

                if channel_data is not None:
                    channel_name = self._get(channel_data, "text")
                    channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
                    channel_thumbnail_urls = self._extract_urls(
                        self._get(
                            ds, "channelThumbnailSupportedRenderers", "channelThumbnailWithLinkRenderer",
                            "thumbnail", "thumbnails", opt=True
                        )
                    )
                    channel_item = ChannelItem(
                        title=channel_name, endpoint=channel_endpoint, thumbnail_urls=channel_thumbnail_urls
                    )
                else:
                    channel_item = None

                item = YouTubeVideoItem(
                    title=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint, views=views, length=length,
                    channel_item=channel_item, description=description, published_time=published_time
                )

            elif (
                    ItemStructType.CHANNEL in entry_item
                    or ItemStructType.GRID_CHANNEL in entry_item
            ):
                subscribers = self._clc_int(
                    self._get(ds, "subscriberCountText", "simpleText", opt=True), opt=True
                )
                videos_num = to_int(self._get(ds, "videoCountText", "runs", 0, "text", opt=True))

                item = ChannelItem(
                    title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, subscribers=subscribers,
                    videos_num=videos_num
                )

            elif ItemStructType.GRID_PLAYLIST in entry_item:
                videos_num = to_int(self._get(ds, "videoCountShortText", "simpleText"))
                channel_data = self._get(ds, "shortBylineText", "runs", 0, opt=True)
                channel_name = self._get(channel_data, "text")
                channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
                channel_item = ChannelItem(title=channel_name, endpoint=channel_endpoint)

                item = YouTubePlaylistItem(
                    title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls, channel_item=channel_item,
                    videos_num=videos_num
                )

            elif ItemStructType.COMPACT_RADIO in entry_item:
                item = RadioItem(title=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

            elif ItemStructType.PLAYLIST in entry_item:
                video_items = self._extract_child_videos(self._get(ds, "videos"))
                videos_num = to_int(self._get(ds, "videoCount"))

                channel_data = self._get(ds, "shortBylineText", "runs", 0, opt=True)
                channel_name = self._get(channel_data, "text")
                channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
                channel_item = ChannelItem(title=channel_name, endpoint=channel_endpoint)

                item = YouTubePlaylistItem(
                    title=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint, video_items=video_items,
                    channel_item=channel_item, videos_num=videos_num
                )

            else:  # ItemStructType.RADIO
                video_items = self._extract_child_videos(self._get(ds, "videos"))
                item = RadioItem(
                    title=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint, video_items=video_items
                )

        elif ItemStructType.REEL_ITEM in entry_item:
            ds = self._get(entry_item, ItemStructType.REEL_ITEM)
            name = self._get(ds, "headline", "simpleText")
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails"))
            endpoint = WatchEndpoint(video_id=self._get(ds, "videoId"))
            item = YouTubeVideoItem(title=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

        elif ItemStructType.WATCH_CARD_COMPACT_VIDEO in entry_item:
            ds = self._get(entry_item, ItemStructType.WATCH_CARD_COMPACT_VIDEO)
            name = self._get(ds, "title", "simpleText")
            length = self._clc_length(self._get(ds, "lengthText", "simpleText"))
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            views = self._clc_int(self._get(ds, "subtitle", "simpleText"))
            tmp = self._get(ds, "subtitle", "simpleText").split(TextDivisorType.BULLET_POINT)
            published_time = tmp[1] if len(tmp) > 1 else None
            channel_data = self._get(ds, "byline", "runs", 0)
            channel_name = self._get(channel_data, "text")
            channel_endpoint = self._extract_endpoint(self._get(channel_data, "navigationEndpoint"))
            channel_item = ChannelItem(title=channel_name, endpoint=channel_endpoint)
            item = YouTubeVideoItem(
                title=name, endpoint=endpoint, length=length, views=views,
                channel_item=channel_item, published_time=published_time
            )

        elif ItemStructType.SEARCH_REFINEMENT_CARD in entry_item:
            ds = self._get(entry_item, ItemStructType.SEARCH_REFINEMENT_CARD)
            name = self._get(ds, "query", "runs", 0, "text")
            thumbnail_urls = self._extract_urls(self._get(ds, "thumbnail", "thumbnails"))
            endpoint = self._extract_endpoint(self._get(ds, "searchEndpoint"))

            item = AlbumItem(title=name, thumbnail_urls=thumbnail_urls, endpoint=endpoint)

        elif ItemStructType.C4_TABBED_HEADER in entry_item:
            ds = self._get(entry_item, ItemStructType.C4_TABBED_HEADER)
            name = self._get(ds, "title")
            videos_num = to_int(self._get(ds, "videosCountText", "runs", 0, "text"))
            endpoint = self._extract_endpoint(self._get(ds, "navigationEndpoint"))
            thumbnail_urls = self._extract_urls(self._get(ds, "avatar", "thumbnails"))
            banner_thumbnail_urls = self._extract_urls(self._get(ds, "banner", "thumbnails"))
            subscribers = self._clc_int(self._get(ds, "subscriberCountText", "simpleText", opt=True), opt=True)
            verified = self._is_verified(ds, opt=True)
            official = self._is_official(ds, opt=True)

            item = ChannelItem(
                title=name, endpoint=endpoint, thumbnail_urls=thumbnail_urls,
                banner_thumbnail_urls=banner_thumbnail_urls, verified=verified, official=official,
                subscribers=subscribers, videos_num=videos_num
            )

        elif ItemStructType.PAGE_HEADER in entry_item:
            ds = self._get(entry_item, ItemStructType.PAGE_HEADER, "content", "pageHeaderViewModel")
            name = self._get(entry_item, ItemStructType.PAGE_HEADER, "pageTitle")
            thumbnail_urls = self._extract_urls(self._get(
                ds, "image", "decoratedAvatarViewModel", "avatar", "avatarViewModel", "image", "sources"
            ))
            banner_thumbnail_urls = self._extract_urls(self._get(
                ds, "banner", "imageBannerViewModel", "image", "sources"
            ))

            videos_num = None
            subscribers = None

            tmp = self._get(ds, "metadata", "contentMetadataViewModel", "metadataRows")
            index = 1 % len(tmp)
            for entry in self._get(tmp, index, "metadataParts"):
                content = self._get(entry, "text", "content")
                _, num_type = content.split()
                if num_type in ("video", "videos"):
                    videos_num = self._clc_int(content)
                elif num_type in "subscribers":
                    subscribers = self._clc_int(content)
                else:
                    raise AccessError(data=content)

            item = ChannelItem(
                title=name, banner_thumbnail_urls=banner_thumbnail_urls, thumbnail_urls=thumbnail_urls,
                subscribers=subscribers, videos_num=videos_num
            )

        elif (
                ItemStructType.AUTOMIX_PREVIEW_VIDEO in entry_item
                or ItemStructType.RELATED_CHIP_CLOUD in entry_item
                or ItemStructType.AD_SLOT in entry_item
                or ItemStructType.CONTINUATION_ITEM in entry_item
                or ItemStructType.MESSAGE in entry_item
                or ItemStructType.SEARCH_HEADER in entry_item
                or ItemStructType.MUSIC_HEADER in entry_item
                or ItemStructType.PLAYLIST_HEADER in entry_item
        ):
            return None

        else:
            raise AccessError(data=entry_item)

        return item

    @return_on_input_none
    @_handle_exception
    def _extract_endpoint(self, data: Dict) -> Optional[Endpoint]:
        if EndpointType.BROWSE in data:
            browse_endpoint_data = self._get(data, "browseEndpoint")
            browse_id = self._get(browse_endpoint_data, "browseId")
            params = self._get(browse_endpoint_data, "params", opt=True)

            canonical_base_url = self._get(browse_endpoint_data, "canonicalBaseUrl", opt=True)
            if canonical_base_url is None:
                endpoint = BrowseEndpoint(browse_id=browse_id, params=params)
            else:
                endpoint = YouTubeBrowseEndpoint(
                    browse_id=browse_id, params=params, canonical_base_url=canonical_base_url
                )

        elif EndpointType.WATCH in data:
            video_id = self._get(data, EndpointType.WATCH, "videoId")
            playlist_id = self._get(data, EndpointType.WATCH, "playlistId", opt=True)
            params = self._get(data, EndpointType.WATCH, "params", opt=True)
            endpoint = WatchEndpoint(video_id=video_id, playlist_id=playlist_id, params=params)

        elif EndpointType.WATCH_PLAYLIST in data:
            playlist_id = self._get(data, EndpointType.WATCH_PLAYLIST, "playlistId")
            endpoint = WatchEndpoint(playlist_id=playlist_id)

        elif EndpointType.REEL_WATCH in data:
            video_id = self._get(data, EndpointType.REEL_WATCH, "videoId")
            playlist_id = self._get(data, EndpointType.REEL_WATCH, "playlistId", opt=True)
            params = self._get(data, EndpointType.REEL_WATCH, "params", opt=True)
            endpoint = WatchEndpoint(video_id=video_id, playlist_id=playlist_id, params=params)

        elif EndpointType.SEARCH in data:
            query = self._get(data, EndpointType.SEARCH, "query")
            params = self._get(data, EndpointType.SEARCH, "params", opt=True)
            endpoint = SearchEndpoint(query=query, params=params)

        elif EndpointType.URL in data:
            url = self._get(data, EndpointType.URL, "url")
            params = self._get(data, EndpointType.URL, "params", opt=True)
            endpoint = UrlEndpoint(url=url, params=params)

        elif EndpointType.CONTINUATION in data:
            continuation = self._get(data, EndpointType.CONTINUATION, "continuationCommand", "token")
            endpoint = ContinuationEndpoint(continuation=continuation)

        elif EndpointType.NEXT_CONTINUATION_DATA in data:
            continuation = self._get(data, EndpointType.NEXT_CONTINUATION_DATA, "continuation")
            endpoint = ContinuationEndpoint(continuation=continuation)

        else:
            raise AccessError(data=data)

        return endpoint

    @return_on_input_none
    @_handle_exception
    def _clc_length(self, string: str) -> Optional[time]:
        return clc_length(string)

    @return_on_input_none
    @_handle_exception
    def _clc_publication_date(self, string: str) -> Optional[date]:
        return clc_publication_date(string)

    @return_on_input_none
    @_handle_exception
    def _clc_int(self, string: str) -> Optional[int]:
        return clc_int(string)

    @return_on_input_none
    @_handle_exception
    def _clc_views(self, string: str) -> Optional[int]:
        return clc_views(string)

    @_handle_exception
    def _get(self, ds: Union[List, Dict], *keys) -> Optional[Any]:
        return get(ds, *keys)

    @return_on_input_none
    @_handle_exception
    def _extract_description(self, ds: Union[List[Dict], Dict]) -> List[Tuple[str, Optional[Endpoint]]]:
        if isinstance(ds, List):
            return [
                (self._get(e, "text"), self._extract_endpoint(self._get(e, "navigationEndpoint", opt=True)))
                for e in ds
            ]
        else:
            content = self._get(ds, "content")
            cmds = self._get(ds, "commandRuns", opt=True)
            if cmds is None:
                return [(content, None)]
            description: List[Tuple[str, Optional[Endpoint]]] = []
            index = 0
            for entry in cmds:
                start = self._get(entry, "startIndex")
                end = start + int(self._get(entry, "length"))
                endpoint = self._extract_endpoint(self._get(entry, "onTap", "innertubeCommand"))
                if len(content[index:start]) > 0:
                    description.append((content[index: start], None))
                description.append((content[start: end], endpoint))
                index = end
            if index < len(content):
                description.append((content[index:], None))
            return description

    @return_on_input_none
    def _extract_urls(self, urls_data: List[Dict]) -> List[Dict]:
        urls = urls_data if self.include_all_urls is True else [self._get(urls_data, -1)]
        for entry in urls:
            if not entry["url"].startswith("https:"):
                entry["url"] = f"https:{entry['url']}"
        return urls

    def _extract_child_videos(self, videos_data: List[Dict]) -> List[YouTubeVideoItem]:
        videos: List[YouTubeVideoItem] = []
        for video_data in videos_data:
            video_data = self._get(video_data, "childVideoRenderer")
            name = self._get(video_data, "title", "simpleText")
            endpoint = self._extract_endpoint(self._get(video_data, "navigationEndpoint"))
            length = self._clc_length(self._get(video_data, "lengthText", "simpleText"))
            videos.append(YouTubeVideoItem(title=name, endpoint=endpoint, length=length))
        return videos

    def _is_explicit(self, data: Dict) -> Optional[bool]:
        label = self._get(data, "badges", opt=True)
        if label is None:
            label = self._get(data, "subtitleBadges", opt=True)

        if label is None:
            return None
        else:
            return self._get(label, 0, "musicInlineBadgeRenderer",
                             "accessibilityData", "accessibilityData", "label"
                             ) == "Explicit"

    @_handle_exception
    def _is_official(self, data: Dict) -> bool:
        return self._get(
            data, "badges", 0, "metadataBadgeRenderer", "accessibilityData", "label", opt=True
        ) == "Official Artist Channel"

    @_handle_exception
    def _is_verified(self, data: Dict) -> Optional[bool]:
        label = self._get(data, "ownerBadges", opt=True)
        if label is None:
            label = self._get(data, "badges", opt=True)
            if label is None:
                return
        return self._get(label, 0, "metadataBadgeRenderer", "accessibilityData", "label") == "Verified"

    @return_on_input_none
    def _extract_subtitle_items(
            self,
            data: List[Dict]
    ) -> Tuple[Optional[List[ArtistItem]], Optional[AlbumItem]]:

        artist_items: List[ArtistItem] = []
        album_item: Optional[AlbumItem] = None
        artist_items_terminated = False

        for entry in data:
            name = self._get(entry, "text")
            if "navigationEndpoint" in entry:
                endpoint = self._extract_endpoint(self._get(entry, "navigationEndpoint"))
                if artist_items_terminated is True:
                    album_item = AlbumItem(title=name, endpoint=endpoint)
                else:
                    artist_items.append(ArtistItem(title=name, endpoint=endpoint))

            elif TextDivisorType.BULLET_POINT in name and len(artist_items) > 0:
                if artist_items_terminated is not True:
                    artist_items_terminated = True
                elif album_item is not None:
                    break
                else:
                    raise RuntimeError("Invalid state")

        return None if len(artist_items) == 0 else artist_items, album_item

    @return_on_input_none
    def _extract_album_item(self, data: List[Dict]) -> Optional[AlbumItem]:
        for entry in data:
            name = self._get(entry, "text")
            if "navigationEndpoint" in entry:
                return AlbumItem(
                    title=name,
                    endpoint=self._extract_endpoint(self._get(entry, "navigationEndpoint"))
                )

    def _extract_artist_items(self, data: List[Dict]) -> Optional[List[ArtistItem]]:
        artist_items: List[ArtistItem] = []
        for entry in data:
            name = self._get(entry, "text")
            if "navigationEndpoint" in entry:
                artist_items.append(
                    ArtistItem(
                        title=name,
                        endpoint=self._extract_endpoint(self._get(entry, "navigationEndpoint"))
                    )
                )
        return artist_items
