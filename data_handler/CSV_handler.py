import csv
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Union


class CSVHandler:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._cache: Dict[str, List[Dict[str, Any]]] = {}

    # ---------------------------------------------------------------------- #
    # Internal helpers
    # ---------------------------------------------------------------------- #

    def _resolve_path(self, file_path: Union[str, Path]) -> Path:
        """Normalise the file path and append .csv if missing."""

        if isinstance(file_path, str):
            if not file_path.endswith(".csv"):
                file_path = f"{file_path}.csv"

        return Path(file_path)

    # ---------------------------------------------------------------------- #
    # Core loading
    # ---------------------------------------------------------------------- #

    def load_csv_data(
        self,
        file_path: Union[str, Path],
        use_cache: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Read a CSV file and return a list of row-dictionaries.

        Args:
            file_path: Path to the CSV file (with or without .csv extension).
            use_cache: Return cached data when available (default True).

        Returns:
            List of dicts where each dict represents one CSV row.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """

        path = self._resolve_path(file_path)
        cache_key = str(path.resolve())

        if use_cache and cache_key in self._cache:
            self.logger.debug(
                "Returning cached data for: %s",
                cache_key
            )
            return self._cache[cache_key]

        if not path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {path}"
            )

        rows: List[Dict[str, Any]] = []

        with open(path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                rows.append(dict(row))

        self.logger.info(
            "Loaded %d rows from: %s",
            len(rows),
            path
        )

        self._cache[cache_key] = rows

        return rows

    def load_data_from_csv(
        self,
        file_path: Union[str, Path],
        delimiter: str = ",",
        encoding: str = "utf-8",
    ) -> List[Dict[str, Any]]:
        """
        Load CSV data with configurable delimiter and encoding.

        Args:
            file_path: Path to the CSV file.
            delimiter: Column separator character (default ',').
            encoding: File encoding (default 'utf-8').

        Returns:
            List of row-dictionaries.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
        """

        path = self._resolve_path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"CSV file not found: {path}"
            )

        rows: List[Dict[str, Any]] = []

        with open(
            path,
            newline="",
            encoding=encoding
        ) as csv_file:

            reader = csv.DictReader(
                csv_file,
                delimiter=delimiter
            )

            for row in reader:
                rows.append(dict(row))

        self.logger.info(
            "Loaded %d rows from: %s",
            len(rows),
            path
        )

        return rows

    # ---------------------------------------------------------------------- #
    # Row / column access
    # ---------------------------------------------------------------------- #

    def get_data_row(
        self,
        file_path: Union[str, Path],
        row_index: int,
        use_cache: bool = True,
    ) -> Dict[str, Any]:
        """
        Return a single row by zero-based index.

        Args:
            file_path: Path to the CSV file.
            row_index: Zero-based row index.
            use_cache: Use cached data if available.

        Returns:
            Dict representing the requested row.

        Raises:
            IndexError: If the row index is out of range.
        """

        rows = self.load_csv_data(
            file_path,
            use_cache=use_cache
        )

        if row_index < 0 or row_index >= len(rows):
            raise IndexError(
                f"Row index {row_index} is out of range. "
                f"CSV has {len(rows)} row(s)."
            )

        self.logger.debug(
            "Fetched row[%d] from: %s",
            row_index,
            file_path
        )

        return rows[row_index]

    def get_column_value(
        self,
        file_path: Union[str, Path],
        column_name: str,
        row_index: Optional[int] = None,
        use_cache: bool = True,
    ) -> Union[Any, List[Any]]:
        """
        Return value(s) from a specific column.

        Args:
            file_path: Path to the CSV file.
            column_name: Header name of the target column.
            row_index: If provided, return only that row's value;
                       otherwise return all values in the column.
            use_cache: Use cached data if available.

        Returns:
            A single value when row_index is given, otherwise a list.

        Raises:
            KeyError: If the column does not exist in the CSV.
            IndexError: If row_index is out of range.
        """

        rows = self.load_csv_data(
            file_path,
            use_cache=use_cache
        )

        if rows and column_name not in rows[0]:
            raise KeyError(
                f"Column '{column_name}' not found. "
                f"Available columns: {list(rows[0].keys())}"
            )

        if row_index is not None:

            if row_index < 0 or row_index >= len(rows):
                raise IndexError(
                    f"Row index {row_index} is out of range. "
                    f"CSV has {len(rows)} row(s)."
                )

            return rows[row_index][column_name]

        return [row[column_name] for row in rows]

    # ---------------------------------------------------------------------- #
    # Filtering
    # ---------------------------------------------------------------------- #

    def filter_data(
        self,
        file_path: Union[str, Path],
        filters: Dict[str, Any],
        use_cache: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Filter rows where all key-value pairs in *filters* match.

        Args:
            file_path: Path to the CSV file.
            filters: Dict of ``{column_name: expected_value}`` pairs.
                     All conditions must be satisfied (AND logic).
            use_cache: Use cached data if available.

        Returns:
            List of matching row-dicts (empty list if none match).

        Example:
            handler.filter_data(
                "users.csv",
                {"role": "admin", "active": "true"}
            )
        """

        rows = self.load_csv_data(
            file_path,
            use_cache=use_cache
        )

        filtered = [
            row
            for row in rows
            if all(
                str(row.get(key, "")) == str(value)
                for key, value in filters.items()
            )
        ]

        self.logger.info(
            "filter_data: %d/%d rows matched filters %s",
            len(filtered),
            len(rows),
            filters,
        )

        return filtered

    # ---------------------------------------------------------------------- #
    # Cache management
    # ---------------------------------------------------------------------- #

    def clear_cache(
        self,
        file_path: Optional[Union[str, Path]] = None
    ) -> None:
        """
        Clear the in-memory CSV cache.

        Args:
            file_path: If provided, evict only that file's cache entry;
                       otherwise clear the entire cache.
        """

        if file_path is None:
            self._cache.clear()
            self.logger.info("Entire CSV cache cleared.")

        else:
            cache_key = str(
                self._resolve_path(file_path).resolve()
            )

            removed = self._cache.pop(
                cache_key,
                None
            )

            if removed is not None:
                self.logger.info(
                    "Cache cleared for: %s",
                    cache_key
                )

            else:
                self.logger.debug(
                    "No cache entry found for: %s",
                    cache_key
                )

    # ---------------------------------------------------------------------- #
    # pytest integration
    # ---------------------------------------------------------------------- #

    def load_csv_for_pytest(
        self,
        file_path: Union[str, Path],
        use_cache: bool = True,
    ) -> List[tuple]:
        """
        Load CSV data formatted for ``@pytest.mark.parametrize``.

        Each CSV row is converted to a tuple of its values, maintaining
        the column order defined in the header row.

        Args:
            file_path: Path to the CSV file.
            use_cache: Use cached data if available.

        Returns:
            List of tuples ready to be passed to
            ``pytest.mark.parametrize``.

        Example:

            # conftest.py
            from data_handler.CSV_handler import CSVHandler

            handler = CSVHandler()

            TEST_DATA = handler.load_csv_for_pytest(
                "tests/data/users.csv"
            )

            @pytest.mark.parametrize("row", TEST_DATA)
            def test_user(row):
                username, password, role = row
                ...
        """

        rows = self.load_csv_data(
            file_path,
            use_cache=use_cache
        )

        if not rows:
            self.logger.warning(
                "load_csv_for_pytest: no rows found in %s",
                file_path
            )
            return []

        headers = list(rows[0].keys())

        self.logger.debug(
            "load_csv_for_pytest: columns=%s, rows=%d",
            headers,
            len(rows)
        )

        return [
            tuple(row[h] for h in headers)
            for row in rows
        ]