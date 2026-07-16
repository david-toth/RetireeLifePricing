from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from retiree_life_pricer.soa import load_soa_csv, parse_improvement_export, parse_mortality_export


def test_parse_soa_mortality_export():
    text = """Table Name:,Example
Row\\Column,1
65,0.01
66,0.02
"""
    parsed = parse_mortality_export(text, "M")

    assert list(parsed.columns) == ["sex", "age", "qx"]
    assert parsed.loc[0, "sex"] == "M"
    assert parsed.loc[1, "qx"] == 0.02


def test_parse_soa_improvement_export():
    text = """Table Name:,Example
Row\\Column,2026,2027
65,0.01,0.02
66,0.03,0.04
"""
    parsed = parse_improvement_export(text, "F")

    assert set(parsed.columns) == {"sex", "age", "year", "improvement"}
    assert len(parsed) == 4
    assert parsed.loc[0, "year"] == 2026


def test_load_soa_csv_prefers_local_cache():
    with TemporaryDirectory() as temp_dir:
        cache_dir = Path(temp_dir)
        cache_file = cache_dir / "soa_table_1234.csv"
        cache_file.write_text("cached table", encoding="utf-8")

        with patch("retiree_life_pricer.soa.download_soa_csv") as download:
            assert load_soa_csv(1234, cache_dir=cache_dir) == "cached table"
            download.assert_not_called()
