from typing import Any, List

from django.core.management.base import BaseCommand
from django_extensions.management.utils import signalcommand as signalcommand

HAS_BOTO: bool

class Command(BaseCommand):
    AWS_ACCESS_KEY_ID: str = ...
    AWS_SECRET_ACCESS_KEY: str = ...
    AWS_BUCKET_NAME: str = ...
    AWS_CLOUDFRONT_DISTRIBUTION: str = ...
    SYNC_S3_RENAME_GZIP_EXT: str = ...
    DIRECTORIES: str = ...
    FILTER_LIST: Any = ...
    GZIP_CONTENT_TYPES: Any = ...
    uploaded_files: List[str] = ...
    upload_count: int = ...
    skip_count: int = ...
    help: str = ...
    args: str = ...
    can_import_settings: bool = ...
    def add_arguments(self, parser: Any) -> None: ...
    verbosity: Any = ...
    prefix: Any = ...
    do_gzip: Any = ...
    rename_gzip: Any = ...
    do_expires: Any = ...
    do_force: Any = ...
    invalidate: Any = ...
    s3host: Any = ...
    default_acl: Any = ...
    media_only: Any = ...
    static_only: Any = ...
    def handle(self, *args: Any, **options: Any) -> None: ...
    def open_cf(self): ...
    def invalidate_objects_cf(self) -> None: ...
    def sync_s3(self) -> None: ...
    def compress_string(self, s: Any): ...
    def get_s3connection_kwargs(self): ...
    def open_s3(self): ...
    def upload_s3(self, arg: Any, dirname: Any, names: Any, dirs: Any) -> None: ...