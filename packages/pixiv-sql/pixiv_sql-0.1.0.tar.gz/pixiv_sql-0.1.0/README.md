# pixiv-sql

[![PyPI version](https://badge.fury.io/py/pixiv-sql.svg)](https://badge.fury.io/py/pixiv-sql)
![build](https://github.com/ryohidaka/pixiv-sql/workflows/Build/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Python library to backup pixiv user data to SQLite DB.

## Installation

You can install this library using PyPI:

```shell
pip install pixiv-sql
```

## Usage

initialize the PixivSQL class with your Pixiv user ID, refresh token, and database:

```python
user_id = "your_user_id"
refresh_token = "your_refresh_token"
database = "your_database_path_from_root_dir"

app = PixivSQL(user_id, refresh_token, database)
```

You can then fetch your bookmarks and insert them into the database:

```python
app.bookmark()
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
