import os
import psycopg2

from config.settings import DB_CONFIG


class DatabaseService:

    @staticmethod
    def get_transaction(transaction_id):

        conn = psycopg2.connect(**DB_CONFIG)

        cursor = conn.cursor()

        cursor.execute("""
        SELECT *
        FROM cirrus.cirrus_operations
        WHERE "transactionId" = %s
        ORDER BY create_dt_ts DESC
        LIMIT 1
        """, (transaction_id,))

        row = cursor.fetchone()

        columns = [col[0] for col in cursor.description]

        conn.close()

        return columns, row

    @staticmethod
    def save_transaction_output(
            transaction_id,
            output_folder,
            transaction_name):

        columns, row = DatabaseService.get_transaction(
            transaction_id
        )

        if not row:
            raise Exception(
                f"No DB record found for "
                f"{transaction_id}"
            )

        db_file = os.path.join(
            output_folder,
            f"{transaction_name}_DB_Output.txt"
        )

        with open(
                db_file,
                "w",
                encoding="utf-8") as f:

            f.write("DATABASE OUTPUT\n")
            f.write("=" * 80 + "\n\n")

            for col, value in zip(
                    columns,
                    row):

                f.write(
                    f"{col}: {value}\n"
                )

        print(
            f"DB Output saved: {db_file}"
        )

        return db_file