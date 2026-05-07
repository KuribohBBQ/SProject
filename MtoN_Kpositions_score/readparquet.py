from collections import defaultdict
import duckdb as db


def fetch_sorted_results(parquet_file: str):
    con = db.connect()

    result = con.execute("""
        SELECT *
        FROM read_parquet(?)
        ORDER BY professorName ASC, stabilityScore DESC
    """, [parquet_file]).fetchall()

    con.close()
    return result

def load_preferences(parquet_file):
    con = db.connect()
    rows = con.execute("""
        SELECT *
        FROM read_parquet(?)
        ORDER BY professorName ASC, stabilityScore DESC
    """, [parquet_file]).fetchall()
    con.close()

    prefs = defaultdict(list)
    for student, emplID, professor, score in rows:
        prefs[professor].append((student, emplID, score))

    return prefs


def pretty_print_results(results):
    grouped = defaultdict(list)

    # group rows by professor
    for student, emplID, professor, score in results:
        grouped[professor].append((student, emplID, score))

    # print nicely
    for professor in sorted(grouped.keys()):
        print(f"\n=== {professor} ===")
        for i, (student, emplID, score) in enumerate(grouped[professor], start=1):
            print(f"{i:2d}. {student:<4} (ID: {emplID}) -> {score:.3f}")


def print_table(results):
    print(f"{'Student':<8} {'ID':<6} {'Professor':<10} {'Score':<6}")
    print("-" * 40)

    for student, emplID, professor, score in results:
        print(f"{student:<8} {emplID:<6} {professor:<10} {score:.3f}")


if __name__ == "__main__":
    parquet_file = "matches.parquet"

    results = fetch_sorted_results(parquet_file)

    print("\n===== GROUPED VIEW =====")
    pretty_print_results(results)

    print("\n\n===== TABLE VIEW =====")
    print_table(results)