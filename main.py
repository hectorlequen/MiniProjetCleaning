import argparse
import logging
from pathlib import Path

import pandas as pd

from utils.cleaning import add_valid_mail_column, clean_data
from utils.enrichment import add_country_column

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean and validate a customer CSV file."
    )

    parser.add_argument(
        "--input",
        default="data/input.csv",
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--output",
        default="output/cleaned_data.csv",
        help="Path where the cleaned CSV file will be saved.",
    )

    parser.add_argument(
        "--invalid-output",
        default="output/invalid_emails.csv",
        help="Path where invalid email rows will be saved.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    invalid_output_path = Path(args.invalid_output)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    invalid_output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    cleaned_df = clean_data(df)
    cleaned_df = add_country_column(cleaned_df)
    cleaned_df, invalid_emails_df = add_valid_mail_column(cleaned_df)

    cleaned_df.to_csv(output_path, index=False)
    invalid_emails_df.to_csv(invalid_output_path, index=False)

    print(f"Cleaned data saved to: {output_path}")
    print(f"Invalid emails saved to: {invalid_output_path}")


if __name__ == "__main__":
    main()
