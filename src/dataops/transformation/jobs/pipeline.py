from dataops.transformation.jobs.process_dataset import DatasetProcessor
from dataops.transformation.config.datasets import DATASETS


class TransformationPipeline:
    """
    Execute all Spark transformation jobs.
    """

    def __init__(self):
        self.processor = DatasetProcessor()

    def run(self):

        print("=" * 70)
        print("STARTING TRANSFORMATION PIPELINE")
        print("=" * 70)

        total = len(DATASETS)

        for index, dataset in enumerate(DATASETS, start=1):

            print(f"\n[{index}/{total}] Processing {dataset['name']}")

            self.processor.process(
                input_path=dataset["input"],
                output_path=dataset["output"]
            )

        print("\n" + "=" * 70)
        print("ALL DATASETS PROCESSED SUCCESSFULLY")
        print("=" * 70)


if __name__ == "__main__":
    pipeline = TransformationPipeline()
    pipeline.run()
