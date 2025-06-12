import json

INPUT_FILE = 'case_occurence.json'
OUTPUT_FILE = 'court_cases_only.json'

def is_court_case(record):
    return (
        record.get("is_the_case_proceeding_to_court") == "yes" or
        record.get("case_still_in_court") == "yes" or
        record.get("date_of_court_followup") not in [None, "", "null"] or
        record.get("stage_of_case_in_court") not in [None, "", "null"]
    )

def main():
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

        court_cases = [entry for entry in data if is_court_case(entry)]

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
            json.dump(court_cases, outfile, indent=4)

        print(f"✅ Extracted {len(court_cases)} court-related cases to {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ Failed to process file: {e}")

if __name__ == '__main__':
    main()
