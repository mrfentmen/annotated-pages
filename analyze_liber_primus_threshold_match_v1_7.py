#!/usr/bin/env python3
"""Reproduce v1.7 fixed-transform threshold robustness checks.

Reads inherited threshold records from the v1.6 workbook using artifact_tool.
This script does NOT download images or process source JPEG pixels.
"""
from __future__ import annotations
import argparse, json, math, statistics
from pathlib import Path
from artifact_tool import Blob, SpreadsheetFile

PAIRS = {
    "24->40": {"src":24, "tgt":40, "mapping":{1:1,2:2,3:5,4:4,5:3},
               "model":"vertical reflection + translation", "xmode":"add", "ymode":"reflect"},
    "24->73": {"src":24, "tgt":73, "mapping":{1:4,2:5,3:3,4:2,5:1},
               "model":"horizontal reflection + translation", "xmode":"reflect", "ymode":"add"},
    "40->73": {"src":40, "tgt":73, "mapping":{1:4,2:5,3:1,4:2,5:3},
               "model":"180-degree rotation + translation", "xmode":"reflect", "ymode":"reflect"},
}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--workbook", default="liber_primus_visual_master_dataset_v1_6.xlsx")
    parser.add_argument("--output", default="liber_primus_threshold_match_reproduction_v1_7.json")
    args=parser.parse_args()
    wb=SpreadsheetFile.import_xlsx(Blob.load(args.workbook))
    l=json.loads(wb.inspect({"kind":"table","range":"Pixel Thresholds v1.1!A5:G64",
                            "include":"values","table_max_rows":70,"table_max_cols":8}).ndjson)["values"]
    r=json.loads(wb.inspect({"kind":"table","range":"Pixel Thresholds v1.1!I5:M64",
                            "include":"values","table_max_rows":70,"table_max_cols":6}).ndjson)["values"]
    records=[]
    for left,right in zip(l,r):
        page,group,label,threshold,x,y,area=left
        y0,x1,y1,width,height=right
        records.append({"page":page,"label":label,"threshold":threshold,"x":x,"y":y,"area":area,
                        "bbox_w":width,"bbox_h":height})
    summary=[]
    points=[]
    for pair,spec in PAIRS.items():
        for threshold in [40,60,80,100]:
            src={z["label"]:z for z in records if z["page"]==spec["src"] and z["threshold"]==threshold}
            tgt={z["label"]:z for z in records if z["page"]==spec["tgt"] and z["threshold"]==threshold}
            joined=[(la,lb,src[la],tgt[lb]) for la,lb in spec["mapping"].items()]
            xcomp=[(b["x"]-a["x"]) if spec["xmode"]=="add" else (a["x"]+b["x"]) for la,lb,a,b in joined]
            ycomp=[(a["y"]+b["y"]) if spec["ymode"]=="reflect" else (b["y"]-a["y"]) for la,lb,a,b in joined]
            px=statistics.mean(xcomp); py=statistics.mean(ycomp)
            residuals=[]; area_equal=0; bbox_equal=0; abs_area_delta=[]
            for la,lb,a,b in joined:
                predicted_x=(a["x"]+px) if spec["xmode"]=="add" else (px-a["x"])
                predicted_y=(py-a["y"]) if spec["ymode"]=="reflect" else (a["y"]+py)
                residual=math.hypot(b["x"]-predicted_x,b["y"]-predicted_y)
                residuals.append(residual)
                area_equal += int(a["area"]==b["area"])
                bbox_equal += int((a["bbox_w"],a["bbox_h"])==(b["bbox_w"],b["bbox_h"]))
                abs_area_delta.append(abs(b["area"]-a["area"]))
                points.append({"pair":pair,"threshold":threshold,"source_label":la,"target_label":lb,
                    "source_xy_px":[a["x"],a["y"]],"target_xy_px":[b["x"],b["y"]],
                    "source_area_px2":a["area"],"target_area_px2":b["area"],
                    "source_bbox_wh_px":[a["bbox_w"],a["bbox_h"]],
                    "target_bbox_wh_px":[b["bbox_w"],b["bbox_h"]],
                    "residual_px":residual,"area_equal":a["area"]==b["area"],
                    "bbox_dimensions_equal":(a["bbox_w"],a["bbox_h"])==(b["bbox_w"],b["bbox_h"])})
            summary.append({"pair":pair,"threshold":threshold,"model":spec["model"],
                "mapping":"; ".join(f"{a}->{b}" for a,b in spec["mapping"].items()),
                "parameter_x":px,"parameter_y":py,
                "rms_residual_px":math.sqrt(sum(x*x for x in residuals)/len(residuals)),
                "max_residual_px":max(residuals),"equal_component_areas_count":area_equal,
                "equal_bbox_dimensions_count":bbox_equal,"mean_absolute_area_delta_px2":statistics.mean(abs_area_delta)})
    result={"version":"1.7","input_workbook":args.workbook,
            "source_sheet":"Pixel Thresholds v1.1",
            "source_pixel_processing":False,
            "note":"Descriptive refit of inherited detector records only; no inferential p-value or cipher claim.",
            "pair_threshold_summaries":summary,"point_level_records":points}
    Path(args.output).write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(f"Wrote {args.output}: {len(summary)} pair-threshold summaries, {len(points)} point records.")
    for s in summary:
        print(s["pair"],s["threshold"],f"RMS={s['rms_residual_px']:.6f}",
              f"max={s['max_residual_px']:.6f}",f"area_equal={s['equal_component_areas_count']}/5",
              f"bbox_equal={s['equal_bbox_dimensions_count']}/5")

if __name__=="__main__":
    main()
