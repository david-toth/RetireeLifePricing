from __future__ import annotations

from retiree_life_pricer.soa import DEFAULT_SOA_EXPORT_DIR, cache_catalog_exports


def main() -> None:
    paths = cache_catalog_exports()
    print(f"Cached {len(paths)} SOA export files in {DEFAULT_SOA_EXPORT_DIR}")


if __name__ == "__main__":
    main()
