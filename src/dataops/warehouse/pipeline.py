from dataops.warehouse.manager import WarehouseManager


def main():

    print("=" * 60)
    print("DATAOPS WAREHOUSE PIPELINE")
    print("=" * 60)

    warehouse = WarehouseManager()

    warehouse.initialize()

    warehouse.load_all_bronze()

    print("\nBronze Layer Completed.")


if __name__ == "__main__":
    main()
