import yaml
import csv
import sys

SECTIONS = ["Functionality", "Wheat", "Chaff"]


def process(assignment, submissions):
    names, student_results = {}, {}
    for submission in submissions.values():
        assert submission[":status"] == "processed", "autograder finished"
        results = process_results(submission[":results"]["tests"], names)
        for student in submission[":submitters"]:
            email = student[":email"]
            assert email not in student_results, "student in multiple submissions"
            student_results[email] = results

    col_names = {
        section: ["student"] + list(section_cols)
        for section, section_cols in names.items()
    }
    files = {
        section: open(f'{assignment}_{section.lower()}_autograder.csv',
                      'w',
                      newline='')
        for section in SECTIONS
    }
    writers = {
        section: csv.DictWriter(f, fieldnames=col_names[section])
        for section, f in files.items()
    }
    for writer in writers.values():
        writer.writeheader()

    for student, results in student_results.items():
        for section_results in results.values():
            section_results["student"] = student
        for section, writer in writers.items():
            writer.writerow(results[section])


def process_results(results, names):
    results = list(
        filter(lambda r: r["extra_data"]["type"] == "Detailed", results))
    processed = {}
    for section in SECTIONS:
        successes = result_successes(filter(is_section(section), results))
        names[section] = names.get(section, set()) | successes.keys()
        processed[section] = successes
    return processed


def is_section(section):
    return lambda result: result["extra_data"]["section"] == section


def successful(result):
    return result["score"] == result["max_score"]


def result_successes(results):
    return {result["name"]: successful(result) for result in results}


if __name__ == "__main__":
    with open(sys.argv[2]) as metadata_file:
        submission_metadata = yaml.safe_load(metadata_file)
    process(sys.argv[1], submission_metadata)
