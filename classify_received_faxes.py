"""
Classify received faxes by document type.

Usage:
    python classify_received_faxes.py [--discover] [--dir received_faxes]

Modes:
    --discover   Analyze all PDFs and print a type distribution summary.
                 Shows text samples for Unknown documents so you can refine
                 the keyword rules in modules/fax_classifier.py.
                 No output file is written.

    (default)    Classify all PDFs and write received_fax_types.tsv.

In both modes, extracted text is cached back to the .txt files.
"""

import argparse
import json
import os
from collections import defaultdict

from alive_progress import alive_bar

from modules.fax_classifier import classify_pdf, OCR_AVAILABLE
from modules.gemini_classifier import classify_pdf_with_gemini
from modules.healthie import Healthie

FAX_DIR = "received_faxes"
OUTPUT_TSV = "received_fax_types.tsv"


def load_json_meta(fax_dir: str, fax_id: str) -> dict:
    json_path = os.path.join(fax_dir, f"{fax_id}.json")
    if os.path.exists(json_path):
        with open(json_path) as f:
            return json.load(f)
    return {}


def cache_text(fax_dir: str, fax_id: str, text: str) -> None:
    txt_path = os.path.join(fax_dir, f"{fax_id}.txt")
    # Only write if we got something meaningful
    if text and text.strip():
        with open(txt_path, "w") as f:
            f.write(text)


def get_pdf_ids(fax_dir: str) -> list[str]:
    entries = os.listdir(fax_dir)
    return sorted(entry[:-4] for entry in entries if entry.endswith(".pdf"))


def run_discover(fax_dir: str) -> None:
    if not OCR_AVAILABLE:
        print("WARNING: pytesseract / pdf2image not installed. OCR fallback disabled.")
        print("         Install with: pip install pytesseract pdf2image")
        print("         Also requires: brew install tesseract\n")

    fax_ids = get_pdf_ids(fax_dir)
    print(f"Found {len(fax_ids)} PDFs in {fax_dir}/\n")

    type_counts: dict[str, int] = defaultdict(int)
    unknowns: list[tuple[str, str]] = []  # (fax_id, text_snippet)

    with alive_bar(len(fax_ids), title="Analyzing") as bar:
        for fax_id in fax_ids:
            pdf_path = os.path.join(fax_dir, f"{fax_id}.pdf")
            result = classify_pdf(pdf_path)
            cache_text(fax_dir, fax_id, result["text"])
            type_counts[result["document_type"]] += 1
            if result["document_type"] == "Unknown":
                unknowns.append((fax_id, result["text_snippet"]))
            bar()

    print("\n--- Document Type Distribution ---")
    total = sum(type_counts.values())
    for doc_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        print(f"  {doc_type:<20} {count:>4}  ({pct:.1f}%)")
    print(f"  {'TOTAL':<20} {total:>4}")

    if unknowns:
        print(f"\n--- Unknown Documents ({len(unknowns)}) ---")
        print("Add keyword rules to modules/fax_classifier.py to classify these.\n")
        for fax_id, snippet in unknowns[:20]:
            print(f"  [{fax_id}]")
            if snippet:
                print(f"    {snippet[:300]!r}")
            else:
                print("    (no text extracted — PDF may be unreadable)")
            print()
        if len(unknowns) > 20:
            print(f"  ... and {len(unknowns) - 20} more.")


MANUAL_CLASSIFICATIONS_PATH = "manual_classifications.json"


def load_manual_classifications() -> dict[str, str]:
    if os.path.exists(MANUAL_CLASSIFICATIONS_PATH):
        with open(MANUAL_CLASSIFICATIONS_PATH) as f:
            return json.load(f)
    return {}


def run_classify(fax_dir: str, output_tsv: str) -> None:
    if not OCR_AVAILABLE:
        print("WARNING: pytesseract / pdf2image not installed. OCR fallback disabled.")
        print("         Install with: pip install pytesseract pdf2image")
        print("         Also requires: brew install tesseract\n")

    healthie = Healthie("PROD")
    manual = load_manual_classifications()

    fax_ids = get_pdf_ids(fax_dir)
    print(f"Found {len(fax_ids)} PDFs in {fax_dir}/\n")

    rows: list[dict] = []

    with alive_bar(len(fax_ids), title="Classifying") as bar:
        for fax_id in fax_ids:
            pdf_path = os.path.join(fax_dir, f"{fax_id}.pdf")
            result = classify_pdf(pdf_path)
            cache_text(fax_dir, fax_id, result["text"])

            meta = load_json_meta(fax_dir, fax_id)
            healthie_id = healthie.find_user_by_name_and_dob(
                result["patient_name"], result["patient_dob"]
            )
            gemini = classify_pdf_with_gemini(pdf_path)
            rows.append(
                {
                    "fax_id": fax_id,
                    "document_type": result["document_type"],
                    "confidence": result["confidence"],
                    "manual_category": manual.get(fax_id, ""),
                    "gemini_category": gemini["gemini_category"],
                    "from_number": meta.get("from_number", ""),
                    "created_at": meta.get("created_at", ""),
                    "patient_name": result["patient_name"],
                    "gemini_patient_name": gemini["gemini_patient_name"],
                    "patient_dob": result["patient_dob"],
                    "gemini_patient_dob": gemini["gemini_patient_dob"],
                    "healthie_id": healthie_id or "n/a",
                }
            )
            bar()

    with open(output_tsv, "w") as f:
        f.write(
            "fax_id\tdocument_type\tconfidence\tmanual_category\tgemini_category\t"
            "from_number\tcreated_at\t"
            "patient_name\tgemini_patient_name\tpatient_dob\tgemini_patient_dob\thealthie_id\n"
        )
        for row in rows:
            f.write(
                f"{row['fax_id']}\t{row['document_type']}\t{row['confidence']}\t"
                f"{row['manual_category']}\t{row['gemini_category']}\t"
                f"{row['from_number']}\t{row['created_at']}\t"
                f"{row['patient_name']}\t{row['gemini_patient_name']}\t"
                f"{row['patient_dob']}\t{row['gemini_patient_dob']}\t{row['healthie_id']}\n"
            )

    type_counts: dict[str, int] = defaultdict(int)
    for row in rows:
        type_counts[row["document_type"]] += 1

    print(f"\nWrote {output_tsv}\n")
    print("--- Summary ---")
    for doc_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {doc_type:<20} {count:>4}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Classify received faxes by document type."
    )
    parser.add_argument(
        "--discover",
        action="store_true",
        help="Print type distribution and Unknown samples; do not write output file.",
    )
    parser.add_argument(
        "--dir",
        default=FAX_DIR,
        help=f"Directory containing fax PDFs (default: {FAX_DIR})",
    )
    args = parser.parse_args()

    if args.discover:
        run_discover(args.dir)
    else:
        run_classify(args.dir, OUTPUT_TSV)


if __name__ == "__main__":
    main()
