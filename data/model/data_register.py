"""Validate the tourism CSV and register its metadata locally."""

import csv
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[2]
    dataset = root / "tourism_project/data/tourism.csv"
    if not dataset.is_file():
        raise FileNotFoundError(f"Dataset not found: {dataset}")

    with dataset.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.reader(source, strict=True)
        columns = next(reader, None)
        if not columns or any(not column.strip() for column in columns):
            raise ValueError("Dataset must contain a non-empty CSV header")
        if len(set(columns)) != len(columns):
            raise ValueError("Dataset contains duplicate column names")
        row_count = 0
        for line_number, row in enumerate(reader, start=2):
            if not row:
                continue
            if len(row) != len(columns):
                raise ValueError(f"CSV row {line_number} has an unexpected column count")
            row_count += 1
    if not row_count:
        raise ValueError("Dataset contains no data rows")

    metadata = {
        "path": dataset.relative_to(root).as_posix(),
        "columns": columns,
        "row_count": row_count,
        "sha256": hashlib.sha256(dataset.read_bytes()).hexdigest(),
    }
    manifest = dataset.with_suffix(".metadata.json")
    manifest.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {row_count} rows from {metadata['path']}")
    print(f"Local manifest: {manifest.relative_to(root)}")


if __name__ == "__main__":
    main()
