#!/usr/bin/env python3
"""Reproduce Liber Primus shape-control comparisons from workbook coordinates.

This script intentionally does not download or process source JPEGs. It recomputes
order-independent pair-distance signatures from inherited threshold-60 centroid
records in the master workbook. The results are descriptive, not inferential.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Sequence

from artifact_tool import Blob, SpreadsheetFile


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pair_distances(points: Sequence[tuple[float, float]]) -> list[float]:
    return sorted(
        math.dist(a, b)
        for a, b in itertools.combinations(points, 2)
    )


def normalized_signature(
    points: Sequence[tuple[float, float]], normalization: str
) -> list[float]:
    distances = pair_distances(points)
    if not distances or max(distances) == 0:
        raise ValueError("Point group is degenerate.")
    if normalization == "rms":
        scale = math.sqrt(sum(d * d for d in distances) / len(distances))
    elif normalization == "max":
        scale = max(distances)
    else:
        raise ValueError(f"Unknown normalization: {normalization}")
    return [d / scale for d in distances]


def signature_difference(
    points_a: Sequence[tuple[float, float]],
    points_b: Sequence[tuple[float, float]],
    normalization: str,
) -> float:
    a = normalized_signature(points_a, normalization)
    b = normalized_signature(points_b, normalization)
    if len(a) != len(b):
        raise ValueError("Signature lengths differ; compare groups with equal point counts.")
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))


def get_values(workbook, sheet_name: str, address: str):
    return workbook.worksheets.get_item(sheet_name).get_range(address).values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workbook",
        type=Path,
        default=Path("liber_primus_visual_master_dataset_v1_7.xlsx"),
        help="Input master workbook (default: v1.7 source workbook).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("liber_primus_shape_controls_audit_v1_8.reproduced.json"),
        help="Output JSON file.",
    )
    args = parser.parse_args()

    if not args.workbook.exists():
        raise FileNotFoundError(
            f"Input workbook not found: {args.workbook}. Run from the folder containing it "
            "or pass --workbook /path/to/workbook.xlsx."
        )

    workbook = SpreadsheetFile.import_xlsx(Blob.load(str(args.workbook)))

    centroid_rows = get_values(workbook, "Pixel Centroids v1.1", "A5:W19")
    groups: dict[int, list[tuple[float, float]]] = {24: [], 40: [], 73: []}
    for row in centroid_rows:
        page = int(row[0])
        if page in groups:
            groups[page].append((float(row[6]), float(row[7])))
    for page, pts in groups.items():
        if len(pts) != 5:
            raise ValueError(f"Expected five points for page {page}, got {len(pts)}.")

    p68_rows = get_values(workbook, "Contextual Controls", "A6:D10")
    page68 = [(float(row[1]), float(row[2])) for row in p68_rows]
    p68_areas = [float(row[3]) for row in p68_rows]

    p39_rows = get_values(workbook, "Contextual Controls", "A21:C26")
    page39 = [(float(row[1]), float(row[2])) for row in p39_rows]
    if len(page39) != 6:
        raise ValueError(f"Expected six page-39 control points, got {len(page39)}.")

    aux57 = get_values(workbook, "Auxiliary Controls v1.2", "A11:Q15")
    aux68 = get_values(workbook, "Auxiliary Controls v1.2", "A19:Q23")
    page57_plant = [(float(row[5]), float(row[6])) for row in aux57]
    page68_plant = [(float(row[5]), float(row[6])) for row in aux68]
    plant_record_equality = []
    for a, b in zip(aux57, aux68):
        plant_record_equality.append({
            "centroid_xy_equal": (a[5], a[6]) == (b[5], b[6]),
            "area_equal": a[7] == b[7],
            "bbox_equal": a[8:14] == b[8:14],
        })

    main_pairs = []
    for a, b in itertools.combinations((24, 40, 73), 2):
        main_pairs.append({
            "comparison": f"{a}-{b}",
            "rms_normalized_signature_rms_diff": signature_difference(groups[a], groups[b], "rms"),
            "max_normalized_signature_rms_diff": signature_difference(groups[a], groups[b], "max"),
        })
    max_main_rms = max(x["rms_normalized_signature_rms_diff"] for x in main_pairs)
    max_main_max = max(x["max_normalized_signature_rms_diff"] for x in main_pairs)

    control_comparisons = []
    for page in (24, 40, 73):
        rms_candidates = []
        max_candidates = []
        for subset in itertools.combinations(range(6), 5):
            points = [page39[i] for i in subset]
            rms_candidates.append((signature_difference(groups[page], points, "rms"), subset))
            max_candidates.append((signature_difference(groups[page], points, "max"), subset))
        best_rms = min(rms_candidates, key=lambda item: item[0])
        best_max = min(max_candidates, key=lambda item: item[0])
        rms_p68 = signature_difference(groups[page], page68, "rms")
        max_p68 = signature_difference(groups[page], page68, "max")
        control_comparisons.append({
            "target_page": page,
            "page68_control": {
                "rms_normalized_signature_rms_diff": rms_p68,
                "max_normalized_signature_rms_diff": max_p68,
                "ratio_to_largest_target_target_difference_rms": rms_p68 / max_main_rms,
                "ratio_to_largest_target_target_difference_max": max_p68 / max_main_max,
            },
            "page39_best_five_of_six_control": {
                "rms_normalized_signature_rms_diff": best_rms[0],
                "rms_best_subset_labels_1based": [i + 1 for i in best_rms[1]],
                "max_normalized_signature_rms_diff": best_max[0],
                "max_best_subset_labels_1based": [i + 1 for i in best_max[1]],
                "ratio_to_largest_target_target_difference_rms": best_rms[0] / max_main_rms,
                "ratio_to_largest_target_target_difference_max": best_max[0] / max_main_max,
                "subsets_searched_per_norm": 6,
            },
        })

    p50_rows = get_values(workbook, "Contextual Controls", "A45:D47")
    p56_rows = get_values(workbook, "Contextual Controls", "A48:D50")
    page50 = [(float(row[2]), float(row[3])) for row in p50_rows]
    page56 = [(float(row[2]), float(row[3])) for row in p56_rows]
    if len(page50) != 3 or len(page56) != 3:
        raise ValueError("Expected three points for both page 50 and page 56.")
    span50 = page50[-1][0] - page50[0][0]
    span56 = page56[-1][0] - page56[0][0]
    gaps50 = [
        (page50[1][0] - page50[0][0]) / span50,
        (page50[2][0] - page50[1][0]) / span50,
    ]
    gaps56 = [
        (page56[1][0] - page56[0][0]) / span56,
        (page56[2][0] - page56[1][0]) / span56,
    ]

    result = {
        "version": "1.8-reproduced",
        "input_workbook": str(args.workbook),
        "input_workbook_sha256": sha256_file(args.workbook),
        "data_provenance": (
            "Inherited threshold-60 centroid/component records; this script does not decode "
            "or validate source JPEGs."
        ),
        "normalization": {
            "rms": "Sorted pair distances divided by each group's RMS pair distance.",
            "max": "Sorted pair distances divided by each group's maximum pair distance.",
            "signature_difference": "RMS difference between normalized sorted signatures.",
        },
        "main_target_pairs": main_pairs,
        "largest_target_target_signature_difference": {
            "rms_normalized": max_main_rms,
            "max_normalized": max_main_max,
        },
        "controls_vs_targets": control_comparisons,
        "page57_vs_page68_plant_control": {
            "stored_centroid_area_bbox_records_match_5_of_5": all(
                r["centroid_xy_equal"] and r["area_equal"] and r["bbox_equal"]
                for r in plant_record_equality
            ),
            "pointwise_record_checks": plant_record_equality,
            "shape_signature_diff_rms_normalized": signature_difference(page57_plant, page68_plant, "rms"),
            "shape_signature_diff_max_normalized": signature_difference(page57_plant, page68_plant, "max"),
        },
        "page50_vs_page56_three_dot_row": {
            "page50_centroids_xy": page50,
            "page56_centroids_xy": page56,
            "page50_span_px": span50,
            "page56_span_px": span56,
            "page50_to_page56_span_ratio": span50 / span56,
            "scale_page50_to_page56": span56 / span50,
            "page50_gap_fractions": gaps50,
            "page56_gap_fractions": gaps56,
            "gap_fraction_absolute_differences": [abs(a - b) for a, b in zip(gaps50, gaps56)],
            "signature_diff_rms_normalized": signature_difference(page50, page56, "rms"),
            "signature_diff_max_normalized": signature_difference(page50, page56, "max"),
        },
        "inference_status": (
            "Descriptive only. The target groups were selected in earlier exploratory work; "
            "the page-39 control searches six subsets. These calculations are not p-values."
        ),
        "source_pixel_validation": (
            "Not performed. Local raw JPEG acquisition failed separately; browser-rendered "
            "images support qualitative visual notes only."
        ),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(args.output),
        "main_target_pairs": result["main_target_pairs"],
        "largest_target_target_signature_difference": result["largest_target_target_signature_difference"],
        "page57_vs_page68_plant_control": result["page57_vs_page68_plant_control"]["stored_centroid_area_bbox_records_match_5_of_5"],
        "page50_to_page56_span_ratio": result["page50_vs_page56_three_dot_row"]["page50_to_page56_span_ratio"],
    }, indent=2))


if __name__ == "__main__":
    main()
