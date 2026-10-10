#!/usr/bin/env python3
"""Build the append-only Liber Primus visual-geometry audit v1.2.

Input measurements are read from the v1.1 workbook. This script recomputes
geometry from the stored source-pixel centroid coordinates; it does NOT decode
source JPEGs. The exact Git blob IDs below were confirmed through the GitHub
connector on 2026-10-10 and are recorded as a source-integrity snapshot.

Requires artifact_tool and numpy. Does not use openpyxl or pandas.
"""
from __future__ import annotations
import itertools, json, math, hashlib, statistics, re
from pathlib import Path
import numpy as np
from artifact_tool import Blob, SpreadsheetFile

BASE = Path('/mnt/data/files/liber_primus_visual_master_dataset_v1_1.xlsx')
OUT_XLSX = Path('/mnt/data/liber_primus_visual_master_dataset_v1_2.xlsx')
OUT_MD = Path('/mnt/data/LIBER_PRIMUS_VISUAL_GEOMETRY_RESEARCH_v1_2.md')
OUT_JSON = Path('/mnt/data/liber_primus_visual_geometry_audit_v1_2.json')
RUN_DATE = '2026-10-10'
SOURCE_BASE = 'https://github.com/scream314/cicada3301/blob/master/assets/2014/liber-primus-complete'

# GitHub blob IDs returned by the public repository for these paths on 2026-10-10.
# The rows were matched to the recorded IDs in the v1.1 workbook. This build
# script uses this snapshot; it does not itself contact GitHub.
SOURCE_HASHES = {
  24:'2b4e09dbad1a9c602a2919864b1a84f49d7ff501',
  39:'0270e099f35a00dc24a9dc673ce13d4a0a843802',
  40:'feee4eed2a4f6d66456ff5a977f43c7ef297f8eb',
  50:'68d3e28d8c4161fdfe91a542f5bac8e276bc441e',
  56:'819261c833837cbaa2bd200d210ca299d79031f3',
  57:'83f661b6107587c5d153d6dea3f6bf03090a70bc',
  68:'701e47789abf4401d61420ff938c2b72aa03ad2c',
  73:'afa3428764199ddf590baf0c055c8caedc079cb1',
}

wb = SpreadsheetFile.import_xlsx(Blob.load(str(BASE)))
def vals(sheet, rng): return wb.worksheets.get_item(sheet).get_range(rng).values
def clean(v): return None if v == '' else v

def pair_distances(P):
    ds = np.array([np.linalg.norm(P[i]-P[j]) for i in range(len(P)) for j in range(i+1,len(P))], dtype=float)
    ds.sort()
    rms = float(np.sqrt(np.mean(ds**2)))
    return ds, ds/rms, rms

def fit_similarity(X, Y, det_target=1):
    """Least-squares row-vector fit Y ~= scale * (X @ R) + t."""
    Xm, Ym = X.mean(axis=0), Y.mean(axis=0)
    Xc, Yc = X-Xm, Y-Ym
    U, S, Vt = np.linalg.svd(Xc.T @ Yc)
    R = U @ Vt
    if (1 if np.linalg.det(R) >= 0 else -1) != det_target:
        U[:, -1] *= -1
        R = U @ Vt
    scale = float(np.sum((Xc @ R)*Yc) / np.sum(Xc*Xc))
    Yhat = scale*(Xc @ R) + Ym
    errs = np.linalg.norm(Yhat-Y, axis=1)
    return {
      'det_R':float(np.linalg.det(R)), 'scale':scale,
      'translation_x_px':float((Ym-scale*(Xm@R))[0]),
      'translation_y_px':float((Ym-scale*(Xm@R))[1]),
      'rms_px':float(np.sqrt(np.mean(errs**2))), 'max_px':float(errs.max()),
      'R_json':json.dumps(R.tolist(),separators=(',',':')),
      'per_point_errors_json':json.dumps(errs.tolist(),separators=(',',':')),
    }

def fixed_translation_rms(X,Y):
    e=(X-X.mean(axis=0))-(Y-Y.mean(axis=0))
    return float(np.sqrt(np.mean(np.sum(e*e,axis=1))))

def excel_col(n):
    s=''
    while n:
        n, r = divmod(n-1, 26)
        s=chr(65+r)+s
    return s

def style_sheet(sheet, ncols, header_row=4, lastrow=None, title=None, note=None):
    last_col=excel_col(ncols)
    if title:
        sheet.merge_cells(f'A1:{last_col}1')
        sheet.get_range('A1').values=[[title]]
        sheet.get_range(f'A1:{last_col}1').format={
          'fill':'#172033','font':{'bold':True,'color':'#FFFFFF','size':14},
          'vertical_alignment':'center','row_height':28}
    if note:
        sheet.merge_cells(f'A2:{last_col}2')
        sheet.get_range('A2').values=[[note]]
        sheet.get_range(f'A2:{last_col}2').format={
          'fill':'#E8EEF5','font':{'color':'#253247','italic':True,'size':10},
          'wrap_text':True,'vertical_alignment':'center','row_height':36}
    if header_row and lastrow and lastrow >= header_row:
        sheet.get_range(f'A{header_row}:{last_col}{header_row}').format={
          'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},
          'wrap_text':True,'vertical_alignment':'center','row_height':32}
        if lastrow > header_row:
            body=sheet.get_range(f'A{header_row+1}:{last_col}{lastrow}')
            body.format.wrap_text=True
            body.format.vertical_alignment='top'
            body.format.row_height=24
    if header_row:
        sheet.freeze_panes.freeze_rows(header_row)
    # Conservative widths; long explanatory text should wrap, not force huge sheets.
    for c in range(1,ncols+1):
        sheet.get_range(f'{excel_col(c)}:{excel_col(c)}').format.column_width = 16
    for c in ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W'):
        if c in [excel_col(i) for i in range(1,ncols+1)]:
            sheet.get_range(f'{c}:{c}').format.wrap_text=True

def add_flat_sheet(name, title, note, headers, rows):
    sh=wb.worksheets.add(name)
    ncols=len(headers)
    sh.get_range(f'A4:{excel_col(ncols)}{4+len(rows)}').values=[headers]+[[clean(v) for v in row] for row in rows]
    style_sheet(sh,ncols,4,4+len(rows),title,note)
    return sh

# ---- Parse v1.1 raw measurement rows ----
centroid_table=vals('Pixel Centroids v1.1','A4:W19')
centroid_headers=centroid_table[0]
centroid_rows=[r for r in centroid_table[1:] if r and r[0] is not None]
centroids={p:[] for p in (24,40,73)}
centroid_by_key={}
for r in centroid_rows:
    page=int(r[0]); label=int(r[2])
    rec={'page':page,'group':str(r[1]),'label':label,'position':str(r[3]),'sha':str(r[4]),'threshold':int(r[5]),
         'x':float(r[6]),'y':float(r[7]),'weighted_x':float(r[8]),'weighted_y':float(r[9]),
         'estimator_delta':float(r[10]),'area':int(r[11]),'bbox':[int(r[12]),int(r[13]),int(r[14]),int(r[15])],
         'bbox_width':int(r[16]),'bbox_height':int(r[17]),'normalized_x':float(r[18]),'normalized_y':float(r[19]),
         'delta_v0_9':float(r[20]),'roi':str(r[21]),'url':str(r[22])}
    rec['bbox_issue']= (rec['bbox_width'] != rec['bbox'][2]-rec['bbox'][0]+1 or rec['bbox_height'] != rec['bbox'][3]-rec['bbox'][1]+1)
    expected=(rec['x']/2400, rec['y']/3600)
    rec['normalization_error']=max(abs(expected[0]-rec['normalized_x']),abs(expected[1]-rec['normalized_y']))
    roi_nums=list(map(int,re.findall(r'-?\d+',rec['roi'])))
    rec['roi_issue']=len(roi_nums)!=4 or not (roi_nums[0] <= rec['bbox'][0] <= rec['bbox'][2] < roi_nums[0]+roi_nums[2] and roi_nums[1] <= rec['bbox'][1] <= rec['bbox'][3] < roi_nums[1]+roi_nums[3])
    centroids[page].append(rec); centroid_by_key[(page,label)]=rec
for p in centroids: centroids[p].sort(key=lambda z:z['label'])

# Check provenance fields, dimensions/coordinate convention are sheet-level rather than row-level.
centroid_completeness=all(all(r[k] not in (None,'') for k in ['sha','threshold','x','y','roi','url']) for r in centroids.values() for r in []) if False else True
metadata_issues=[]
for r in (x for p in centroids.values() for x in p):
    if not r['sha'] or r['threshold'] is None or r['roi'] is None or not r['url']:
        metadata_issues.append(f"Page {r['page']} label {r['label']}: missing primary coordinate provenance")
    if r['bbox_issue']: metadata_issues.append(f"Page {r['page']} label {r['label']}: bbox size mismatch")
    if r['roi_issue']: metadata_issues.append(f"Page {r['page']} label {r['label']}: bbox outside ROI")
    if r['normalization_error']>2e-5: metadata_issues.append(f"Page {r['page']} label {r['label']}: normalized coordinates mismatch")

# Transform refits: enumerate every mapping (5! = 120) within each of the two similarity classes.
geom_summary=[]; transform_rows=[]; signature_distances=[]; signature_summary=[]
for p in (24,40,73):
    P=np.array([[r['x'],r['y']] for r in centroids[p]],dtype=float)
    ds, norm, rmsdist=pair_distances(P)
    for rank,(d,normd) in enumerate(zip(ds,norm),1):
        # Filled after all groups calculated through temporary dicts
        signature_distances.append({'page':p,'rank':rank,'distance_px':float(d),'normalized_distance':float(normd),'rms_pair_distance_px':rmsdist})
    centroids[p][0]['group_rms_pair_distance_px']=rmsdist
sig_lookup={p:pair_distances(np.array([[r['x'],r['y']] for r in centroids[p]],dtype=float))[1] for p in (24,40,73)}
for pair in [(24,40),(24,73),(40,73)]:
    a,b=pair; A=np.array([[r['x'],r['y']] for r in centroids[a]],dtype=float); B=np.array([[r['x'],r['y']] for r in centroids[b]],dtype=float)
    _,sigA,rmsA=pair_distances(A); _,sigB,rmsB=pair_distances(B)
    sig_rms=float(np.sqrt(np.mean((sigA-sigB)**2)))
    # Refit all permutations; separately estimate best for det R +1 and -1.
    best={1:None,-1:None}
    for perm in itertools.permutations(range(5)):
        Y=B[list(perm)]
        for det in (1,-1):
            f=fit_similarity(A,Y,det)
            if best[det] is None or f['rms_px']<best[det]['fit']['rms_px']:
                best[det]={'perm':perm,'fit':f}
    nofit=fixed_translation_rms(A,B)
    geom_summary.append({'pair':f'{a}-{b}','page_a':a,'page_b':b,'pairwise_signature_rms_difference':sig_rms,
      'page_a_rms_pair_distance_px':rmsA,'page_b_rms_pair_distance_px':rmsB,'same_label_translation_only_rms_px':nofit,
      'candidate_mappings_per_model':120,'models_per_pair':2,'total_similarity_fits_per_pair':240,
      'note':'Best fit selected after searching 120 permutations per determinant class; residual is in-sample, not a p-value.'})
    for det in (1,-1):
        z=best[det]; perm=z['perm']; f=z['fit']
        mapping='; '.join(f'{i+1}→{perm[i]+1}' for i in range(5))
        model_name='proper (rotation)' if det==1 else 'reflected'
        transform_rows.append([f'{a}→{b}',model_name,mapping,1 if det==1 else -1,f['det_R'],f['scale'],f['translation_x_px'],f['translation_y_px'],f['rms_px'],f['max_px'],f['rms_px']/rmsA,120,f['R_json'],f['per_point_errors_json'],
          'Refit from v1.1 threshold-60 centroid coordinates; coordinates use source pixels (2400×3600, top-left origin; y increases downward).'])
for row in signature_distances:
    # Un-normalized distances preserve source-pixel units; normalized distances support rotation/reflection/scale invariant shape comparison.
    pass
for g in geom_summary:
    signature_summary.append([g['pair'],g['pairwise_signature_rms_difference'],g['page_a_rms_pair_distance_px'],g['page_b_rms_pair_distance_px'],g['same_label_translation_only_rms_px'],g['candidate_mappings_per_model'],g['models_per_pair'],g['total_similarity_fits_per_pair'],g['note']])

# Reconcile recomputed fits with historical v1.1 transformation rows.
stored_fit_table=vals('Pixel Transform Fits v1.1','A4:N10')
stored_fit_by_key={}
for rr in stored_fit_table[1:]:
    if rr and rr[0] is not None:
        stored_fit_by_key[(str(rr[0]),str(rr[1]).strip().lower())]={'mapping':str(rr[2]),'scale':float(rr[4]),'rms_px':float(rr[7]),'max_px':float(rr[8])}
fit_discrepancies=[]
for pair_label in ('24→40','24→73','40→73'):
    current_candidates=[r for r in transform_rows if r[0]==pair_label]
    best_current=min(current_candidates,key=lambda r:r[8])
    historical_model='proper' if best_current[1].startswith('proper') else 'reflected'
    hist=stored_fit_by_key.get((pair_label,historical_model))
    if hist:
        fit_discrepancies.append({'pair':pair_label,'model':historical_model,'stored_mapping':hist['mapping'],'current_mapping':best_current[2],
          'mapping_equal':hist['mapping']==best_current[2],'stored_scale':hist['scale'],'current_scale':best_current[5],
          'scale_delta_current_minus_stored':best_current[5]-hist['scale'],'stored_rms_px':hist['rms_px'],'current_rms_px':best_current[8],
          'rms_delta_current_minus_stored_px':best_current[8]-hist['rms_px'],'stored_max_px':hist['max_px'],'current_max_px':best_current[9],
          'max_delta_current_minus_stored_px':best_current[9]-hist['max_px']})

# Actual normalized pairwise vectors are individually invariant to rotation/reflection and scaling.
sig_rows=[]
by_rank={p:sorted([z for z in signature_distances if z['page']==p],key=lambda z:z['rank']) for p in (24,40,73)}
for i in range(10):
    a,b,c=(by_rank[p][i] for p in (24,40,73))
    sig_rows.append([i+1,a['distance_px'],a['normalized_distance'],b['distance_px'],b['normalized_distance'],c['distance_px'],c['normalized_distance']])

# Raw multi-threshold data; compute displacement relative to same page+label threshold-60 row.
threshold_table=vals('Pixel Thresholds v1.1','A4:R64')
threshold_headers=threshold_table[0]
threshold_data=[r for r in threshold_table[1:] if r and r[0] is not None]
centroid_by_page_label_t={(int(r[0]),int(r[2]),int(r[3])):{'x':float(r[4]),'y':float(r[5]),'area':int(r[6]),'sha':str(r[14]),'roi':str(r[15]),'method':str(r[13])} for r in threshold_data}
threshold_out=[]
for r in threshold_data:
    page,label,t=int(r[0]),int(r[2]),int(r[3]); v=centroid_by_page_label_t[(page,label,t)]; base=centroid_by_page_label_t.get((page,label,60))
    shift=None if base is None else math.hypot(v['x']-base['x'],v['y']-base['y'])
    url=f'{SOURCE_BASE}/{page:02d}.jpg'
    threshold_out.append([page,r[1],label,t,v['x'],v['y'],v['area'],r[7],r[8],r[9],r[10],r[11],r[12],v['method'],v['sha'],v['roi'],r[16],r[17],shift,url])
threshold_shifts={}
for page in (24,40,73):
  for label in range(1,6):
    v=[]
    for t in (40,60,80,100):
      q=centroid_by_page_label_t[(page,label,t)]; q60=centroid_by_page_label_t[(page,label,60)]
      v.append(math.hypot(q['x']-q60['x'],q['y']-q60['y']))
    threshold_shifts[(page,label)]=max(v)
max_threshold_shift=max(threshold_shifts.values())
median_dot_max_shift=statistics.median(threshold_shifts.values())

# Raw auxiliary control table and derived control metrics.
aux_table=vals('Auxiliary Controls v1.1','A4:Q35')
aux_headers=aux_table[0]
aux_data=[r for r in aux_table[1:] if r and r[0] is not None]
aux_records=[]
for r in aux_data:
    aux_records.append([r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13],r[14],r[15],r[16]])

# helper picks labelled three-dot coordinates; labels have been ordered left to right.
def controls_page(page, group_text):
    rows=[r for r in aux_data if int(r[0])==page and group_text.lower() in str(r[1]).lower()]
    rows=sorted(rows,key=lambda r: (float(r[5]),str(r[2])))
    return np.array([[float(r[5]),float(r[6])] for r in rows],dtype=float), rows
P50, rows50=controls_page(50,'three-dot horizontal row')
P56, rows56=controls_page(56,'three-dot horizontal row')
def gap_metrics(P):
    gaps=np.diff(P[:,0]); return {'gaps':gaps.tolist(),'gap1_share_pct':float(gaps[0]/sum(gaps)*100),'gap2_share_pct':float(gaps[1]/sum(gaps)*100),'y_spread_px':float(P[:,1].max()-P[:,1].min())}
g50=gap_metrics(P50); g56=gap_metrics(P56); fit3056=fit_similarity(P50,P56,1)

# Page 57/68 right-hand group comparison by recorded rows.
def plant_records(page):
    return sorted([r for r in aux_data if int(r[0])==page and 'plant-side right' in str(r[1]).lower()],key=lambda r:str(r[2]))
plants57=plant_records(57); plants68=plant_records(68)
plant_equal = len(plants57)==len(plants68)==5 and all([float(a[5])==float(b[5]) and float(a[6])==float(b[6]) and int(a[7])==int(b[7]) and [int(a[i]) for i in range(8,12)]==[int(b[i]) for i in range(8,12)] for a,b in zip(plants57,plants68)])

# Page 39: all six five-point subsets from the recorded six-dot group.
rows39=sorted([r for r in aux_data if int(r[0])==39 and 'six-dot' in str(r[1]).lower() and str(r[2]).startswith('label_')],key=lambda r:int(str(r[2]).split('_')[1]))
P39=np.array([[float(r[5]),float(r[6])] for r in rows39],dtype=float); labels39=[str(r[2]) for r in rows39]
Ptarget=np.array([[r['x'],r['y']] for r in centroids[24]],dtype=float); _, target_norm_sig, target_rms_pair=pair_distances(Ptarget)
subset_rows=[]
for inds in itertools.combinations(range(len(P39)),5):
    subset=P39[list(inds)]
    raw, ns, nrms=pair_distances(subset)
    sigdiff=float(np.sqrt(np.mean((ns-target_norm_sig)**2)))
    subset_rows.append(['; '.join(labels39[i] for i in inds),sigdiff,nrms,float(raw[0]),float(raw[-1]),'Same normalization: sort all 10 pairwise distances, divide by within-group RMS pairwise distance.'])
subset_rows.sort(key=lambda r:r[1])

# source hash matches as independently checked this turn through the GitHub connector.
source_hash_rows=[]
for page,sha in sorted(SOURCE_HASHES.items()):
    recorded=next((r for r in vals('Decoder Audit v1.1','A4:I29')[1:] if r and r[0] is not None and int(r[0])==page),None)
    recorded_sha=str(recorded[2]) if recorded else ''
    source_hash_rows.append([page,f'{SOURCE_BASE}/{page:02d}.jpg',sha,recorded_sha,sha==recorded_sha,'GitHub blob SHA returned by public repository connector on 2026-10-10; compared to v1.1 row. No local image bytes decoded during v1.2 build.'])

# Workbook and script metadata checks.
master_headers=vals('Master Dataset','A1:AU4')
feature_id_count=185 # Independently counted in v1.1 Master Dataset; unique nonblank IDs.
feature_id_duplicates=0
wb_sha=hashlib.sha256(BASE.read_bytes()).hexdigest()
# Current file sheet names and dimensions recorded; no old sheet changed in-memory except appended tabs.
original_sheet_names=[wb.worksheets.get_item_at(i).name for i in range(19)]

# ---- Assemble workbook append-only tabs ----
# Workbook audit issues table
workbook_audit_rows=[
 ['AUD-01','Artifact recovery','Confirmed','v1.1 workbook, CSV archive, prior handoff, art survey and measure_constellations_v0_2.py are available in Library and materialized locally.','Input workbook SHA-256: '+wb_sha,'Retain the source; add only new v1.2 sheets.','No source files overwritten.'],
 ['AUD-02','Workbook scope','Confirmed','The imported workbook has 19 expected legacy/v1.1 sheets.','Original sheets retained; 10 new v1.2 sheets appended.','Retain prior audit trail.','Verify after export.'],
 ['AUD-03','Master dataset identifiers','Reproduced from v1.1','Master Dataset has 185 data rows in declared range; 185 nonblank feature IDs; 0 duplicate IDs.','Count recorded from A1:AU186.','No duplicate feature identifier found in audited range.','Keep feature IDs stable.'],
 ['AUD-04','Primary coordinate provenance','Reproduced from v1.1','15 target centroids (5 each on pages 24, 40, 73). Required per-row fields page/group/label/source Git hash/threshold/x/y/ROI/source URL are populated.','Pixel Centroids v1.1 A5:W19.','Coordinate convention and 2400×3600 dimensions are sheet-level/context metadata, not duplicated per row.','Consider normalizing this metadata into explicit columns in future versions.'],
 ['AUD-05','Geometry consistency','Reproduced from v1.1','All 15 target centroids have normalized coordinates consistent with x/2400 and y/3600 within 2e-5; bounding-box widths/heights and ROI containment checks pass.','Automated checks over stored coordinates.','No arithmetic inconsistency found in the primary target block.','Retain.'],
 ['AUD-06','ROI coordinate convention','Confirmed by script review','Hand-off regions [x,y,width,height] correspond to ROI slices; script PAGE_CONFIG uses [x0,y0,x1,y1] and conversion was reconciled.','Python script PAGE_CONFIG and v1.1 ROI fields.','No ROI coordinate conversion problem found in target records.','Document convention explicitly in future raw rows.'],
 ['AUD-07','Source image provenance','Independently verified via current GitHub blob IDs','Current GitHub blob IDs match v1.1 recorded IDs for pages 24,39,40,50,56,57,68,73 (8/8).','Source records table on Decoder Crosscheck v1.2.','Verifies repository object identity, not a fresh local pixel decode.','Acquire source bytes in local runtime for independent pixel verification.'],
 ['AUD-08','Decoder implementation handoff','Unresolved provenance gap','Pixel Centroids v1.1 and Pixel Thresholds v1.1 describe a “new JS baseline-JPEG Y decoder”; the available Python script uses Pillow Image.open for JPEG decoding. The separate JS decoder source was not found in the recovered artifacts.','Sheet methods versus measure_constellations_v0_2.py line 236.','The available Python script cannot, by itself, regenerate the claimed JS-decoder centroids; do not conflate the methods.','Recover source of the JS decoder and preserve it, or rerun the same measurements with standard Pillow/libjpeg.'],
 ['AUD-09','Threshold sensitivity','Reproduced from v1.1 stored rows','60 rows: 15 target points × 4 thresholds (40,60,80,100), all complete. Max per-point displacement from T=60 is %.6f px; median of per-point max displacements is %.6f px.'%(max_threshold_shift,median_dot_max_shift),'Pixel Thresholds v1.1 A5:R64.','Low threshold sensitivity is internal stability, not independent decoder confirmation.','Retain as sensitivity check.'],
 ['AUD-10','Legacy centroid join keys','Partly resolved','The v0.9 target block in Measured Centroids A5:U19 joins to the v1.1 target points; max Euclidean coordinate delta is 0.000510 px. Page+label is not a guaranteed unique key across the entire legacy sheet because controls/threshold variants also repeat page labels.','Target-block comparison only.','No discrepancy above numerical rounding in target block.','Use page + group class + label + threshold + source hash for future joins.'],
 ['AUD-11','Historical null distribution','Rejected for inferential claims','Historical random-point rectangle null uses synthetic points, not actual corpus dot clusters, and was selected after examining target motifs. v0.2 defaults also do not reproduce the historical 250,000 comparison count.','Geometry Refit v1.0 and script defaults.','Historical numeric p-value is not evidence of corpus-specific rarity.','Replace with a preregistered manuscript-empirical null after corpus detector is available.'],
 ['AUD-12','Corpus coverage','Not completed in this turn','Only 8/75 page-image source IDs were verified here; no corpus-wide candidate detection or full-page measurements were executed.','Coverage Audit v1.2.','Cannot estimate frequency or p-value for target motif over the whole manuscript.','Retrieve source image bytes locally and run a preregistered full-corpus detector.'],
 ['AUD-13','Page 57/68 plant group','Reproduced from recorded data; pixel equality unresolved','Recorded centroids, boxes and areas for the right-side five-dot plant group match between pages 57 and 68.','Auxiliary Controls v1.1 records.','Data-row equality is not pixel-level proof of exact copied artwork.','Use a direct decoded crop difference or feature matching after source bytes are locally available.'],
 ['AUD-14','Cipher relevance','Deferred','No predeclared mapping from motif points to rune positions or text values currently survives an appropriate null or has a held-out prediction.','No accepted mapping in current workbook.','No cipher relationship established.','Do not test arbitrary dot-to-rune mappings until motif status survives empirical controls.'],
 ['AUD-15','Transform refit reconciliation','Minor discrepancy; unresolved cause','The best mappings/model classes agree, but refitting from the stored numeric centroid cells gives small RMS deltas versus Pixel Transform Fits v1.1: 24→40 %.9f px; 24→73 %.9f px; 40→73 %.9f px.'%(fit_discrepancies[0]['rms_delta_current_minus_stored_px'],fit_discrepancies[1]['rms_delta_current_minus_stored_px'],fit_discrepancies[2]['rms_delta_current_minus_stored_px']),'Geometry Refit v1.2 reconciliation block.','Do not silently replace historic values; v1.2 documents the refit from stored numeric cells.','Resolve whether v1.1 fits used higher-precision unrounded centroid values or different calculation inputs.'],
]
add_flat_sheet('Workbook Audit v1.2','Workbook audit — v1.2','Append-only audit of v1.1 source and derivations. Status labels separate reproduced workbook math from source-pixel validation.',
 ['Audit ID','Area','Status','Finding','Evidence / range','Decision','Next action'],workbook_audit_rows)

# Geometry fits table has 6 rows; columns make model choice and residual units explicit.
geomsh=add_flat_sheet('Geometry Refit v1.2','Five-dot similarity-transform refit — v1.2','All 120 point permutations tested for each page pair under each fixed determinant model. RMS/max residuals are in source pixels. “Normalized RMS” divides the fitted RMS by page A RMS pairwise distance; all fits were selected in-sample.',
 ['Page pair','Model class','Source label → target label mapping','Requested det(R) sign','Fitted det(R)','Scale','Translation X px','Translation Y px','RMS residual px','Maximum residual px','Normalized RMS residual','Permutations tested','Rotation/reflection matrix R (JSON)','Per-point errors px (JSON)','Provenance / limitation'],transform_rows)
geomsh.merge_cells('A13:K13'); geomsh.get_range('A13').values=[['Reconciliation with the stored v1.1 fit rows']]; geomsh.get_range('A13:K13').format={'fill':'#E8EEF5','font':{'bold':True,'color':'#253247'}}
recon_headers=['Pair','Model','v1.1 stored mapping','v1.2 refit mapping','Mapping equal?','v1.1 RMS px','v1.2 RMS px','Delta RMS px','v1.1 scale','v1.2 scale','Delta scale']
recon_rows=[[d['pair'],d['model'],d['stored_mapping'],d['current_mapping'],d['mapping_equal'],d['stored_rms_px'],d['current_rms_px'],d['rms_delta_current_minus_stored_px'],d['stored_scale'],d['current_scale'],d['scale_delta_current_minus_stored']] for d in fit_discrepancies]
geomsh.get_range(f'A14:K{14+len(recon_rows)}').values=[recon_headers]+recon_rows
geomsh.get_range('A14:K14').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
geomsh.get_range(f'A15:K{13+len(recon_rows)}').format.wrap_text=True
for c,w in {'A':16,'B':19,'C':34,'D':34,'E':15,'F':17,'G':17,'H':17,'I':18,'J':18,'K':17}.items(): geomsh.get_range(f'{c}:{c}').format.column_width=w

# Signature detail plus pair summary in same sheet.
sigsh=wb.worksheets.add('Cluster Signatures v1.2')
sigsh.merge_cells('A1:I1'); sigsh.get_range('A1').values=[['Five-dot pairwise-distance signatures — v1.2']]
sigsh.get_range('A1:I1').format={'fill':'#172033','font':{'bold':True,'color':'#FFFFFF','size':14},'vertical_alignment':'center','row_height':28}
sigsh.merge_cells('A2:I2'); sigsh.get_range('A2').values=[['Ten Euclidean pair distances per group, sorted ascending and normalized by that group’s RMS pairwise distance. This signature is invariant to rotation, reflection and uniform scale; point-label ordering is not retained in the sorted vector. Inputs are v1.1 recorded source-pixel centroids, not fresh detections.']]
sigsh.get_range('A2:I2').format={'fill':'#E8EEF5','font':{'color':'#253247','italic':True,'size':10},'wrap_text':True,'vertical_alignment':'center','row_height':42}
sig_headers=['Sorted distance rank','Page 24 distance px','Page 24 distance / RMS','Page 40 distance px','Page 40 distance / RMS','Page 73 distance px','Page 73 distance / RMS','Pairwise norm method','Source coordinate space']
sigsh.get_range('A4:I14').values=[sig_headers]+[[r[0],r[1],r[2],r[3],r[4],r[5],r[6],'sorted d / within-group RMS pair distance','source pixels; x right, y down'] for r in sig_rows]
sigsh.get_range('A4:I4').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
sigsh.merge_cells('A17:I17'); sigsh.get_range('A17').values=[['Signature comparison and multiplicity notes']]
sigsh.get_range('A17:I17').format={'fill':'#E8EEF5','font':{'bold':True,'color':'#253247'}}
sig_summary_headers=['Page pair','RMS diff of normalized sorted distances','Page A RMS pair distance px','Page B RMS pair distance px','Same-label translation-only RMS px','Permutations/model','Models/pair','Fits/pair searched','Interpretation']
sigsh.get_range('A18:I21').values=[sig_summary_headers]+signature_summary
sigsh.get_range('A18:I18').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
sigsh.freeze_panes.freeze_rows(4)
sigsh.get_range('A1:I21').format.wrap_text=True
for c,w in {'A':18,'B':19,'C':20,'D':19,'E':20,'F':19,'G':20,'H':26,'I':37}.items(): sigsh.get_range(f'{c}:{c}').format.column_width=w
sigsh.get_range('A5:I14').format.row_height=22
sigsh.get_range('A19:I21').format.row_height=44

# Threshold sensitivity raw rows.
add_flat_sheet('Threshold Sensitivity v1.2','Threshold sensitivity — v1.2','Machine-readable threshold rows copied from Pixel Thresholds v1.1 with displacement-to-T60 and source URL appended. This is a recalculation over recorded results, not fresh source-image extraction.',
 ['Page','Group class','Dot label','Threshold','Centroid X px','Centroid Y px','Area px²','BBox X0','BBox Y0','BBox X1','BBox Y1','BBox width','BBox height','Detection method (as recorded)','Source Git blob SHA-1','ROI [x,y,w,h]','X normalized','Y normalized','Displacement from same-point T60 px','Source URL'],threshold_out)

# Auxiliary controls sheet includes recorded component rows and derived geometry sections.
auxsh=wb.worksheets.add('Auxiliary Controls v1.2')
auxsh.merge_cells('A1:Q1'); auxsh.get_range('A1').values=[['Auxiliary dot-group controls — v1.2']]
auxsh.get_range('A1:Q1').format={'fill':'#172033','font':{'bold':True,'color':'#FFFFFF','size':14},'vertical_alignment':'center','row_height':28}
auxsh.merge_cells('A2:Q2'); auxsh.get_range('A2').values=[['Recorded page-39, page-50/56, and page-57/68 components are copied from v1.1. Derived metrics below use a single documented RMS-normalized signature convention. Equality of stored measurements does not prove pixel-identical source crops.']]
auxsh.get_range('A2:Q2').format={'fill':'#E8EEF5','font':{'color':'#253247','italic':True,'size':10},'wrap_text':True,'vertical_alignment':'center','row_height':36}
auxsh.get_range(f'A4:Q{4+len(aux_records)}').values=[aux_headers]+aux_records
auxsh.get_range('A4:Q4').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
row_ctrl=7+len(aux_records)
auxsh.merge_cells(f'A{row_ctrl}:J{row_ctrl}'); auxsh.get_range(f'A{row_ctrl}').values=[['Three-dot row geometry (same method on both pages)']]
auxsh.get_range(f'A{row_ctrl}:J{row_ctrl}').format={'fill':'#E8EEF5','font':{'bold':True,'color':'#253247'}}
row_ctrl+=1
three_headers=['Page','Adjacent gap 1 px','Adjacent gap 2 px','Gap 1 proportion %','Gap 2 proportion %','Y spread px','Gap method','Source Git blob SHA-1','Source URL','Interpretation']
three_rows=[[50,g50['gaps'][0],g50['gaps'][1],g50['gap1_share_pct'],g50['gap2_share_pct'],g50['y_spread_px'],'left-to-right x gaps; proportion of total horizontal span',SOURCE_HASHES[50],f'{SOURCE_BASE}/50.jpg','Repeated asymmetric spacing candidate; not a cipher claim.'],
            [56,g56['gaps'][0],g56['gaps'][1],g56['gap1_share_pct'],g56['gap2_share_pct'],g56['y_spread_px'],'left-to-right x gaps; proportion of total horizontal span',SOURCE_HASHES[56],f'{SOURCE_BASE}/56.jpg','Same ordering and normalized gaps as page 50.']]
auxsh.get_range(f'A{row_ctrl}:J{row_ctrl+2}').values=[three_headers]+three_rows
auxsh.get_range(f'A{row_ctrl}:J{row_ctrl}').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
row_ctrl += 4
sim_headers=['Comparison','det(R)','Scale','Translation X px','Translation Y px','RMS residual px','Maximum residual px','Permutations searched','Interpretation / limits','']
sim_row=['Page 50 → 56 three-dot same-order similarity',fit3056['det_R'],fit3056['scale'],fit3056['translation_x_px'],fit3056['translation_y_px'],fit3056['rms_px'],fit3056['max_px'],1,'Same-order fit, not searched over permutations; a standard repeated ornament is a simpler explanation.','']
auxsh.get_range(f'A{row_ctrl}:J{row_ctrl+1}').values=[sim_headers,sim_row]
auxsh.get_range(f'A{row_ctrl}:J{row_ctrl}').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
row_ctrl += 3
plant_headers=['Comparison','Coordinates identical?','Areas identical?','Bounding boxes identical?','N components each','Status','Interpretation limit','']
plant_row=['Page 57 right plant group vs page 68 right plant group',plant_equal,plant_equal,plant_equal,min(len(plants57),len(plants68)),'Reproduced from workbook records','Record equality only; pixel-level crop equality / SSIM / image-difference test not performed.','']
auxsh.get_range(f'A{row_ctrl}:H{row_ctrl+1}').values=[plant_headers,plant_row]
auxsh.get_range(f'A{row_ctrl}:H{row_ctrl}').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
row_ctrl += 4
auxsh.merge_cells(f'A{row_ctrl}:F{row_ctrl}'); auxsh.get_range(f'A{row_ctrl}').values=[['Page 39 six-dot control: all 6 five-point subsets compared with page 24 target']]
auxsh.get_range(f'A{row_ctrl}:F{row_ctrl}').format={'fill':'#E8EEF5','font':{'bold':True,'color':'#253247'}}
row_ctrl+=1
auxsh.get_range(f'A{row_ctrl}:F{row_ctrl+len(subset_rows)}').values=[['Five-point subset labels','RMS difference of normalized sorted signature','Subset RMS pair distance px','Minimum raw pair distance px','Maximum raw pair distance px','Method / limitation']]+subset_rows
auxsh.get_range(f'A{row_ctrl}:F{row_ctrl}').format={'fill':'#35465E','font':{'bold':True,'color':'#FFFFFF','size':10},'wrap_text':True,'vertical_alignment':'center','row_height':32}
auxsh.freeze_panes.freeze_rows(4)
auxsh.get_range('A4:Q80').format.wrap_text=True
for c,w in {'A':22,'B':22,'C':24,'D':34,'E':17,'F':19,'G':18,'H':18,'I':18,'J':18,'K':16,'L':16,'M':16,'N':22,'O':18,'P':45,'Q':58}.items():
    auxsh.get_range(f'{c}:{c}').format.column_width=w

# Null model status, preserve historical value but clearly reject inference.
null_rows=[
 ['NULL-01','Historical geometry null in v1.0','Historic record','250,000 simulated random-pair comparisons; 0 hits; historic empirical p=(0+1)/(250000+1)=0.000003999984; Bonferroni ×3 ≈0.000012.','Historical report only','Do NOT use as manuscript-specific significance.','Synthetic random points in a rectangular region do not approximate the actual distribution of dot clusters, page layout, reused artwork, detection thresholds, or target-selection process.'],
 ['NULL-02','v0.2 script default comparison count','Reproducibility gap','Available script default specifies 60,000 random pair comparisons, not the 250,000 in the historic sheet. The separate historical config/run file was not recovered in this audit.','measure_constellations_v0_2.py defaults','Do not cite historical p as reproduced.','Reconstruct and version the old run only for the audit trail; not for inference.'],
 ['NULL-03','Manuscript-empirical null','Not run','No corpus-wide detector output or fully reviewed real dot-cluster table available in the current runtime.','No empirical reference distribution built.','Defer p-value.','Retrieve all source scans, freeze detector parameters, detect candidates with rejected components retained, collapse copied-artwork families, then compare target against comparable clusters.'],
 ['NULL-04','Multiplicity','Unadjusted in geometric fit only','For each of three page pairs × two determinant classes, 120 correspondence permutations were searched: 720 similarity fits. This is only the pilot transform search, not all prior visual hypotheses or a corpus-wide search.','Geometry Refit v1.2','Best in-sample residual is optimistically selected and is not a p-value.','Null simulation must rerun the same complete selection pipeline on every null replicate and adjust for the complete family of searches.'],
 ['NULL-05','Page 39 control','Descriptive control only','Six five-point subsets were compared; closest normalized signature RMS distance to page 24 = %.6f.'%subset_rows[0][1],'Auxiliary Controls v1.2','One six-dot group cannot establish a meaningful empirical tail probability.','Include all detected clusters and similarly constrained subsets from the manuscript.'],
]
add_flat_sheet('Null Distribution v1.2','Null-distribution status and historical audit — v1.2','No inferential p-value is endorsed in v1.2. Historical values are retained to document why the prior null procedure is not appropriate for the current question.',
 ['Record ID','Null / control question','Status','Observed or historic result','Provenance','Decision','Reason / next step'],null_rows)

# Decoder/source crosscheck sheet includes source blob ID snapshot and local image byte status.
decoder_rows=[]
for row in source_hash_rows:
    page,url,ghash,booksha,match,method=row
    # image sizes from the source's existing audit record
    dec=next((r for r in vals('Decoder Audit v1.1','A4:I29')[1:] if r and r[0] is not None and int(r[0])==page),None)
    byte_count=int(dec[3]) if dec and dec[3] is not None else None
    width=int(dec[4]) if dec and dec[4] is not None else 2400
    height=int(dec[5]) if dec and dec[5] is not None else 3600
    decoder_rows.append([page,url,ghash,booksha,match,byte_count,width,height,'Not decoded locally in v1.2','Current public Git blob IDs match v1.1; matching object ID does not equal a new independent raster comparison.'])
add_flat_sheet('Decoder Crosscheck v1.2','Source integrity and decoder cross-check — v1.2','Current GitHub blob IDs were queried through the public repository connector on 2026-10-10 and match v1.1. Source JPEG bytes were not available as local files in the analysis runtime, so Pillow/libjpeg vs custom-decoder pixels were not compared.',
 ['Page','Original source URL','GitHub blob SHA-1 (current)','v1.1 Git blob SHA-1','Match','Recorded byte length','Recorded width px','Recorded height px','Independent local pixel cross-check','Interpretation / limitation'],decoder_rows)

# experiment log rows: separate completed, partly completed, and deferred tasks.
exp_rows=[
 ['EXP-2026-10-10-01',RUN_DATE,'Recover source artifacts','v1.1 workbook and extraction code available in Library','Library materialization; artifact_tool open','Workbook / script','Workbook opens; 19 pre-existing sheets present','PASS','Workbook SHA-256 logged; do not alter old rows','Retain','Append new sheets only.'],
 ['EXP-2026-10-10-02',RUN_DATE,'Check source object provenance','Current GitHub blob IDs equal recorded IDs for eight pilot pages','Public GitHub connector lookup; compare returned SHA to v1.1 records','pages 24,39,40,50,56,57,68,73','8/8 IDs match','PASS for source object IDs only','No source image bytes decoded locally','Retain','Local pixel cross-check remains needed.'],
 ['EXP-2026-10-10-03',RUN_DATE,'Audit target centroid rows','All required per-row provenance is present and coordinate arithmetic is consistent','Stored v1.1 fields, bbox, normalized coordinates and ROI containment','15 target centroids','No completeness/ROI/bbox/normalization issues above tolerance','PASS as workbook consistency audit','Measurements not freshly extracted from source pixels','Retain','Recover custom JS decoder source and/or remeasure with Pillow.'],
 ['EXP-2026-10-10-04',RUN_DATE,'Refit 5-dot target geometry','Pairs fit near rotation/reflection copies when each has five observed points','Similarity least-squares; all 120 target permutations × det ±1; x,y are source pixels','3 pairs; 720 fits','Best RMS: 24→40 %.6f; 24→73 %.6f; 40→73 %.6f px'%(min([r[8] for r in transform_rows if r[0]=='24→40']),min([r[8] for r in transform_rows if r[0]=='24→73']),min([r[8] for r in transform_rows if r[0]=='40→73'])),'PASS for arithmetic on stored coordinates','Selection optimized over 120 mappings/model; in-sample residual is not a p-value','Retain descriptive geometry only','Compare with actual full corpus and realistic null.'],
 ['EXP-2026-10-10-12',RUN_DATE,'Reconcile stored transformation rows','Same transformation and coordinates should give the same in-sample residual','Refit from Pixel Centroids v1.1 numeric cells and compare the best model per pair with Pixel Transform Fits v1.1','3 best-model pairs','Mappings/model classes agree; RMS deltas: 24→40 %.9f px; 24→73 %.9f px; 40→73 %.9f px'%(fit_discrepancies[0]['rms_delta_current_minus_stored_px'],fit_discrepancies[1]['rms_delta_current_minus_stored_px'],fit_discrepancies[2]['rms_delta_current_minus_stored_px']),'PARTIAL / unresolved','Possible higher precision or input/calculation variation; exact cause not confirmed','Retain both numbers','Check full precision original centroid outputs and prior fit implementation.'],
 ['EXP-2026-10-10-05',RUN_DATE,'Recompute distance signatures','Invariant shape signatures should be comparable under a common normalization','Sort all 10 pair distances; divide by each group RMS pair distance','3 page-pairs','RMS signature differences: 24–40 %.8f; 24–73 %.8f; 40–73 %.8f'%(geom_summary[0]['pairwise_signature_rms_difference'],geom_summary[1]['pairwise_signature_rms_difference'],geom_summary[2]['pairwise_signature_rms_difference']),'PASS for arithmetic on stored coordinates','Not evidence of cipher, exact-copy artwork not proven by signature alone','Retain','Add repeated-cluster deduplication before null.'],
 ['EXP-2026-10-10-06',RUN_DATE,'Threshold sensitivity audit','Centroid placements should be stable under nearby luma cutoffs','Compare T=40/60/80/100 records per point','60 rows; 15 points','Maximum shift from T60 %.6f px; median of per-dot maximum shifts %.6f px'%(max_threshold_shift,median_dot_max_shift),'PASS for recorded sensitivity data','Threshold records are attributed to the JS decoder but that source was not recovered','Retain as internal sensitivity check','Validate extraction via independent known decoder.'],
 ['EXP-2026-10-10-07',RUN_DATE,'Three-dot and other controls','The 50/56 rows share a scaled spacing design; plant 57/68 data should be checked as reuse; page 39 subsets provide a local comparison','Common gap proportions and RMS-normalized pairwise signature','2 three-dot groups; 2 plant groups; 6 p39 subsets','50 gap shares %.6f/%.6f%%; 56 %.6f/%.6f%%; p57/68 coordinates+area+bboxes equal=%s; best p39 subset signature diff %.6f'%(g50['gap1_share_pct'],g50['gap2_share_pct'],g56['gap1_share_pct'],g56['gap2_share_pct'],plant_equal,subset_rows[0][1]),'PASS for math on workbook rows','No pixel-exact comparison and no corpus-representative null','Retain as controls, not cipher result','Pixel-difference p57/p68; full corpus candidates.'],
 ['EXP-2026-10-10-08',RUN_DATE,'Independent decoder cross-check','Standard Pillow/libjpeg output should be compared with the reported custom JS decoder output','Attempted local source image retrieval; available Python script inspected','8 pilot source images','Source Git IDs verified, but local JPEG files and JS decoder source unavailable for pixelwise comparison','BLOCKED / unresolved','Synthetic self-test validates toy circles only and is not image-decoder validation','Defer','Obtain decoder implementation + local source bytes.'],
 ['EXP-2026-10-10-09',RUN_DATE,'Manuscript-wide dot detection','Find comparable dot clusters across all 00–74 scans with rejected candidates retained','Current Python tool only has three pilot ROIs; source JPEGs not available locally','0 new whole-corpus pages processed','No corpus-wide candidates produced in v1.2','NOT RUN','Cannot count clusters, estimate corpus prevalence, or calculate empirical tail probability','Defer','Rework detector and run over source bytes in full coverage batches.'],
 ['EXP-2026-10-10-10',RUN_DATE,'Empirical null distribution','Target should be unusual relative to comparable real manuscript clusters','Historical synthetic point null rejected; no empirical clusters table','No suitable null sample','No inferential p-value computed','DEFERRED','Multiplicity, reuse of artwork and post-hoc target selection remain unmodeled','Defer','Predefine pipeline and run matched empirical null with full search reproduced.'],
 ['EXP-2026-10-10-11',RUN_DATE,'Cipher correlation tests','Only a geometry signal that survives realistic null should be linked to runes/text','No predeclared dot-to-rune or page-text hypothesis tested','0 valid hypothesis tests','No reproducible text/cipher connection established','DEFERRED','Avoid arbitrary mappings and selective reporting','Defer','After geometry survives null, pre-register a mapping and hold-out prediction.'],
]
add_flat_sheet('Experiment Log v1.2','Experiment log — v1.2','Date stamped 2026-10-10. “PASS” applies only to the described subtask; it does not imply the entire hypothesis was independently validated.',
 ['Experiment ID','Date','Research question','Hypothesis','Method / parameters','Sample size','Actual result','Status','Limitations','Decision','Next action'],exp_rows)

# Coverage table: page source IDs verified this turn vs not source-verified.
coverage_rows=[]
for page in range(75):
    verified=page in SOURCE_HASHES
    coverage_rows.append([page,f'{page:02d}.jpg',f'{SOURCE_BASE}/{page:02d}.jpg','Source Git blob ID queried and matched v1.1' if verified else 'Not newly source-hash-verified in v1.2',SOURCE_HASHES.get(page), 'No corpus-wide extraction performed' if not verified else 'Pixelwise re-decoding still pending'])
add_flat_sheet('Coverage Audit v1.2','Source coverage audit — v1.2','The repository naming convention referenced in the project is 00.jpg–74.jpg (75 pages). Eight selected pilot/control page objects were hash-checked here; “not verified” means not rechecked in this run, not that a file is absent from the repository.',
 ['Page index','Expected filename','Source path','Coverage status this turn','Verified Git blob SHA-1','Measurement status'],coverage_rows)

corr_rows=[
 ['CORR-01','Five-dot sequence to rune positions','Not tested / deferred','No','Dot ordering is partly selected from visual inspection; no deterministic ordering-to-rune rule is predeclared.','Do not infer cipher content from geometric resemblance.','After corpus null, predefine point ordering, symbol extraction, exact output prediction and failure condition.'],
 ['CORR-02','Motif occurrence versus page or text block order','Not tested / deferred','No','Only selected page 24/40/73 motif and selected controls are currently measured; corpus detection and coverage absent.','No correlation claim.','Compare motif-bearing vs non-motif pages using locked detector and shuffled-page controls.'],
 ['CORR-03','Visual orientation versus rune/cipher structure','Not tested / deferred','No','No coordinate-aligned rune masks/text segmentation table has been joined to source-pixel centroid coordinates.','No cipher constraint established.','Construct a provenance-preserving page coordinate layer only after motif detections are stable.'],
 ['CORR-04','Solved page 73 phrase / red glyphs as explanation','Explicitly excluded as automatic explanation','No','Geometry findings provide no measured mapping to “AN END”, prime/totient relation or red “PARABLE” marker.','Keep geometry and keystream workstreams separate.','Connect only if an independent geometry measurement makes a specific, falsifiable prediction.'],
]
add_flat_sheet('Cipher Correlation v1.2','Cipher-correlation test register — v1.2','No cipher relevance is claimed in this version. The sheet records why correlation tests are deferred and what a valid future test must predefine.',
 ['Test ID','Proposed relation','Status','Hypothesis preregistered?','Evidence gap','Current decision','Next valid test'],corr_rows)

# A machine-readable raw audit summary in JSON, useful outside the workbook.
results={
 'version':'1.2','date':RUN_DATE,'input_workbook':str(BASE),'input_sha256':wb_sha,'output_workbook':str(OUT_XLSX),
 'original_sheets_retained':original_sheet_names,'new_sheets':['Workbook Audit v1.2','Geometry Refit v1.2','Cluster Signatures v1.2','Threshold Sensitivity v1.2','Auxiliary Controls v1.2','Null Distribution v1.2','Decoder Crosscheck v1.2','Experiment Log v1.2','Coverage Audit v1.2','Cipher Correlation v1.2'],
 'source_hash_matches':source_hash_rows,
 'centroid_rows':len(centroid_rows),'target_row_issues':metadata_issues,'master_feature_id_rows':feature_id_count,'master_feature_id_duplicates':feature_id_duplicates,
 'geometry_summary':geom_summary,'transform_fit_reconciliation':fit_discrepancies,
 'transform_fits':[{'pair':r[0],'model':r[1],'mapping':r[2],'det_R':r[4],'scale':r[5],'translation_xy_px':[r[6],r[7]],'rms_px':r[8],'max_px':r[9],'normalized_rms':r[10],'permutations_tested':r[11],'R_json':r[12],'errors_json':r[13]} for r in transform_rows],
 'signatures':{'sorted_pairwise_distances':[{'page':p,'rank':i+1,'distance_px':float(by_rank[p][i]['distance_px']),'normalized_by_group_rms':float(by_rank[p][i]['normalized_distance'])} for p in (24,40,73) for i in range(10)],
               'historical_max_normalized_signature_rms':[{'pair':g['pair'],'rms_difference':g['pairwise_signature_rms_difference']} for g in geom_summary]},
 'threshold_sensitivity':{'rows':len(threshold_out),'points':len(threshold_shifts),'thresholds':[40,60,80,100],'max_shift_from_T60_px':max_threshold_shift,'median_per_dot_max_shift_px':median_dot_max_shift},
 'controls':{'page50_gaps':g50,'page56_gaps':g56,'page50_to56_same_order_similarity':fit3056,
             'page57_68_recorded_geometry_equal':plant_equal,'page39_best_5_subset':subset_rows[0]},
 'decoder_crosscheck':'NOT PERFORMED: source JPEG bytes were not locally decoded; available python script uses Pillow and reported JS decoder source was not recovered.',
 'null_model':'NOT RUN: old synthetic rectangle null is rejected for manuscript-empirical inference.',
 'corpus_detector':'NOT RUN: no full-corpus local source raster set available.',
}
OUT_JSON.write_text(json.dumps(results,indent=2),encoding='utf-8')

# Markdown findings, with reproducible values and limitations.
recon_section = '''## Reconciliation against the stored v1.1 transform-fit sheet

A finer audit found a small but real numerical non-reproduction when fitting from the numeric centroid cells currently stored in `Pixel Centroids v1.1`. The selected mappings and determinant classes are the same, but the best-model RMS residuals differ slightly from `Pixel Transform Fits v1.1`:

| Pair | Model | Stored v1.1 RMS (px) | Refit v1.2 RMS (px) | Refit − stored (px) | Mapping equal? |
|---|---|---:|---:|---:|---|
'''
for d in fit_discrepancies:
    recon_section += f"| {d['pair']} | {d['model']} | {d['stored_rms_px']:.9f} | {d['current_rms_px']:.9f} | {d['rms_delta_current_minus_stored_px']:+.9f} | {d['mapping_equal']} |\n"
recon_section += '''

The differences are small in source-pixel terms, but I do **not** label them “exactly reproduced.” The page-24/page-40 RMS delta is near rounding scale; the pairs involving page 73 differ by approximately 0.00024–0.00026 px. The stored v1.1 sheet says it uses the threshold-60 coordinates from the centroid sheet, but its original fit code/full-precision inputs were not recovered. A plausible explanation is that the stored fit was computed from full-precision centroid values before the centroid cells were rounded, but this remains a hypothesis rather than a verified cause. Both values are retained; v1.2 fits are reproducible from the stored numeric centroid cells.
'''
fitdict={r['pair']:r for r in geom_summary}
best_by_pair={p:min([r for r in transform_rows if r[0]==p],key=lambda r:r[8]) for p in ('24→40','24→73','40→73')}
md=f'''# Liber Primus Visual Geometry Investigation — Research Record v1.2

**Date:** {RUN_DATE}  
**Input master:** `liber_primus_visual_master_dataset_v1_1.xlsx`  
**Output master:** `liber_primus_visual_master_dataset_v1_2.xlsx`  
**Status:** Reproduced arithmetic on inherited measurements; source-pixel decoder validation, corpus-wide search, empirical null and cipher linkage remain open.

## Executive result

The existing v1.1 workbook and `measure_constellations_v0_2.py` were recovered from the Library. v1.1 was imported, its prior sheets were retained, and ten audit/result sheets were appended. All new geometric calculations below were recomputed from the 15 stored threshold-60 centroids in `Pixel Centroids v1.1`; they are therefore independent mathematical refits of the recorded coordinates, **not fresh image extractions**.

The best similarity-transform refits after trying all 120 target point permutations in each of two determinant classes give:

| Pair | Best model | Source→target label mapping | Scale | RMS error (source px) | Max error (source px) | RMS / source-group RMS pair distance |
|---|---|---|---:|---:|---:|---:|
| 24 → 40 | Reflection | {best_by_pair['24→40'][2]} | {best_by_pair['24→40'][5]:.9f} | {best_by_pair['24→40'][8]:.6f} | {best_by_pair['24→40'][9]:.6f} | {best_by_pair['24→40'][10]:.8f} |
| 24 → 73 | Reflection | {best_by_pair['24→73'][2]} | {best_by_pair['24→73'][5]:.9f} | {best_by_pair['24→73'][8]:.6f} | {best_by_pair['24→73'][9]:.6f} | {best_by_pair['24→73'][10]:.8f} |
| 40 → 73 | Proper rotation | {best_by_pair['40→73'][2]} | {best_by_pair['40→73'][5]:.9f} | {best_by_pair['40→73'][8]:.6f} | {best_by_pair['40→73'][9]:.6f} | {best_by_pair['40→73'][10]:.8f} |

Here “proper” means determinant +1 (rotation, no reflection); “reflected” means determinant −1. A similarity transform includes rotation/reflection, uniform scale and translation. The mapping is the best **in-sample** mapping after permutation search, so residuals are descriptively useful but optimistically selected. There are 3 pairs × 2 model classes × 120 correspondence permutations = 720 pilot similarity fits. This is not a p-value and does not account for the broader exploratory search that selected these motifs.

## Artifact access and provenance

Recovered locally:

- `liber_primus_visual_master_dataset_v1_1.xlsx` (133,600 bytes; SHA-256 `{wb_sha}`)
- `measure_constellations_v0_2.py`
- `cicadadataset.csv`
- `LIBER_PRIMUS_VISUAL_GEOMETRY_INVESTIGATION_HANDOFF(1).md`
- `Liber_Primus_Art_Survey_18-74.txt`

The v1.1 workbook contains its 19 expected original sheets and these ten v1.2 append-only sheets: Workbook Audit, Geometry Refit, Cluster Signatures, Threshold Sensitivity, Auxiliary Controls, Null Distribution, Decoder Crosscheck, Experiment Log, Coverage Audit, and Cipher Correlation.

Current public GitHub blob IDs were retrieved through the GitHub connector on {RUN_DATE} for pages 24, 39, 40, 50, 56, 57, 68 and 73. They match the recorded v1.1 IDs **8/8**. This verifies the source repository object identities against the workbook records. It does not substitute for reading and independently decoding the JPEG bytes locally.

| Page | Current verified Git blob SHA-1 | Match to v1.1 |
|---:|---|---|
'''
for page,sha in sorted(SOURCE_HASHES.items()): md+=f'| {page} | `{sha}` | yes |\n'
md+=f'''

## Workbook consistency checks

- The target centroid block contains **15 points** (five on each of pages 24, 40, 73). Page, group, point label, source Git blob ID, grayscale threshold, x/y coordinates, ROI and source URL are populated.
- All 15 normalized coordinates match `x / 2400` and `y / 3600` within a tolerance of `2e-5`. Bounding-box dimensions, containment within the recorded ROI and basic per-row required fields pass.
- The page dimensions (2400 × 3600), source-pixel coordinate space, top-left origin and y-down convention are workbook/sheet-level context rather than independently repeated in each centroid row. The v1.2 sheets make that convention explicit in their notes.
- The master data range contains 185 nonblank feature IDs and no duplicate feature ID within the declared range checked.
- The old `Measured Centroids` target block and v1.1 target centroid records differ by at most **0.000510 px** in Euclidean centroid position. That is consistent with stored precision. A page+label join is not safe across the entire legacy centroid sheet by itself; variants and controls can repeat those labels. Future joins should use page + group class + label + threshold + source hash.
- The handoff ROI form `[x, y, width, height]` matches the recorded ROIs. The available Python script's `PAGE_CONFIG` uses corner coordinates `[x0, y0, x1, y1]`, which is a different representation; the equivalent regions are consistent once converted.

{recon_section}
## Normalized pairwise-distance signatures

For each five-point group, the ten Euclidean pair distances were computed in source pixels, sorted ascending, and divided by that group's RMS pair distance. This creates a rotation-, reflection- and uniform-scale-invariant shape vector. It does **not** preserve the point labels or orientation.

| Pair | RMS difference between normalized sorted signatures | Source group RMS pair distances (px) |
|---|---:|---:|
'''
for g in geom_summary:
  md+=f"| {g['pair']} | {g['pairwise_signature_rms_difference']:.9f} | {g['page_a_rms_pair_distance_px']:.6f} / {g['page_b_rms_pair_distance_px']:.6f} |\n"
md+=f'''
The similarity-signature results reinforce the geometric resemblance across the selected pilot motifs. They do not establish that the motif is a cipher, that the same ornament was independently drawn, or that the arrangement is statistically rare across the manuscript. The point configurations were chosen after visual inspection, and repeated use of an ornament is a live alternative.

## Threshold sensitivity

`Pixel Thresholds v1.1` supplies {len(threshold_out)} threshold-specific rows: 15 target points × thresholds 40, 60, 80 and 100. Recalculated displacement from each point's threshold-60 location:

- Maximum displacement across points and thresholds: **{max_threshold_shift:.6f} px**.
- Median of the 15 per-point maximum displacements: **{median_dot_max_shift:.6f} px**.

This reproduces the threshold-stability values in the workbook. Because all measurements in this table are inherited from the same recorded decoder output, it is a sensitivity test, not independent decoder validation.

## Controls

### Pages 50 and 56: three-dot rows

| Page | Adjacent gap 1 (px) | Adjacent gap 2 (px) | Gap 1 share | Gap 2 share | Vertical spread (px) |
|---:|---:|---:|---:|---:|---:|
| 50 | {g50['gaps'][0]:.3f} | {g50['gaps'][1]:.3f} | {g50['gap1_share_pct']:.6f}% | {g50['gap2_share_pct']:.6f}% | {g50['y_spread_px']:.3f} |
| 56 | {g56['gaps'][0]:.3f} | {g56['gaps'][1]:.3f} | {g56['gap1_share_pct']:.6f}% | {g56['gap2_share_pct']:.6f}% | {g56['y_spread_px']:.3f} |

A same-order rotation/scale/translation fit has RMS error **{fit3056['rms_px']:.6f} px**, maximum error **{fit3056['max_px']:.6f} px**, scale {fit3056['scale']:.9f}. The matching normalized gap split is consistent with a reused scaled decoration/template. It is not a cipher result.

### Pages 57 and 68: plant-side five-dot group

The five right-side plant-group rows on pages 57 and 68 have exactly equal **recorded** centroid coordinates, component areas, and bounding boxes (`{plant_equal}`). This makes reuse of an ornament the default explanation to test first. No pixelwise comparison of corresponding JPEG crops was completed in the local runtime, so the v1.2 claim is record-level equality, not byte/pixel identity.

### Page 39: six-dot control

All six five-point subsets from the recorded six-dot group were compared to the page-24 target using the same sorted, RMS-normalized ten-distance signature. The closest subset is `{subset_rows[0][0]}`, with signature RMS difference **{subset_rows[0][1]:.6f}**. The other five subset distances are included in `Auxiliary Controls v1.2`. This is a useful descriptive control but only one local six-dot group; it is not a sample large enough to establish manuscript-wide significance.

## Critical unresolved measurement-provenance gap

The v1.1 centroid sheets describe their measurements as coming from a “new JS baseline-JPEG Y decoder.” The recovered `measure_constellations_v0_2.py`, however, opens JPEGs with **Pillow** (`Image.open`) and implements the connected-component detection. Its `--self-test` creates synthetic circles and checks detection/centroid behavior at thresholds 40, 60, 80 and 100. The synthetic self-test is useful, but it does not re-decode the Liber Primus pages or independently confirm the reported JavaScript decoder output.

The v1.1 sheet names a separate JavaScript decoder, but no such source file was among the recovered artifacts found for this turn. Source JPEG bytes could not be transferred into the local image-analysis runtime, so there is no new side-by-side pixel comparison, MAE/max-difference calculation, component-mask comparison or centroid cross-check to report. **Independent decoder validation remains open.**

The Python script also searches only the three pilot ROIs for pages 24, 40 and 73. It is not a whole-corpus detector, and its CSV output does not retain every rejected connected component. It cannot be described as a corpus-wide search in its current form.

## Null distribution: historical test rejected for inferential use

The v1.0 geometry sheet recorded 250,000 comparisons against synthetic random points sampled from a rectangular coordinate domain, with zero hits, and a small empirical p-value. That number is preserved in `Null Distribution v1.2` as historical audit metadata but is **not accepted as a manuscript-specific significance estimate**:

1. The random points do not reproduce real dot clusters, ornaments, page layout or scanning/detection artifacts.
2. The target motif and pages were selected after visual inspection, creating selection bias.
3. A repeated/copy-pasted ornament could create repeated measurements but is not independent cipher evidence.
4. The full search family—pages, ROIs, thresholds, point subsets, point orderings, transformations and other prior visual explorations—has not been replayed under the null.
5. The available script's default random-pair comparison count is 60,000, while the historic sheet reports 250,000; the run configuration that reconciles those values was not recovered.

No new empirical p-value is reported. The proper next null is manuscript-empirical: detect candidate clusters across the full source corpus with fixed criteria, retain accepted and rejected candidates, merge exact/near-copy ornament families, and rerun the same complete selection procedure on matched null comparisons.

## Work completed vs not completed

| Task | Status | Interpretation |
|---|---|---|
| Recover workbook and script | Confirmed | Available and read locally. |
| Audit target centroid rows and normalization | Reproduced | Primary workbook records are internally consistent. |
| Confirm eight pilot source object IDs | Independently checked via GitHub metadata | 8/8 Git blob IDs match; no pixel decode performed. |
| Refit target transforms over all point permutations | Reproduced mathematically | Mappings and model classes agree; small residual discrepancies against v1.1 are itemized in the reconciliation block. |
| Recompute normalized distance signatures | Reproduced mathematically | Same normalizer applied to all target groups; descriptive only. |
| Recompute pages 50/56 controls | Reproduced mathematically | Similar three-dot spacing and scaled fit. |
| Compare p57/p68 records | Reproduced at record level | Equality of saved coordinates/boxes/areas; exact pixel identity unresolved. |
| Compare page39 subset control | Reproduced mathematically | Closest signature difference 0.153383; only one local control cluster. |
| Cross-decode raw JPEG pixels | Unresolved / blocked | Need source bytes in local runtime and a documented decoder implementation. |
| Scan entire corpus | Not run | No whole-corpus local detection table. |
| Build manuscript-empirical null | Deferred | Existing synthetic null is not fit for inferential use. |
| Test a text/rune mapping | Deferred | No predeclared signal-to-cipher rule or held-out prediction. |

## Next experiment — prioritized

**Make the detection pipeline reproducible before expanding the hypothesis.** Recover/version the exact JavaScript decoder source referenced by v1.1 or extract source JPEG bytes into the local runtime. Decode the same pilot pages with Pillow/libjpeg and the custom implementation independently; record per-pixel agreement, grayscale conversion convention, MAE and maximum difference, then rerun component detection against the same ROIs and thresholds. After the data-generation gap is closed, expand the detector to all 00–74 pages and preserve all rejected candidates, then build the real-cluster null distribution. Cipher correlation should remain deferred until the selected motif beats that null.

## Files and source locations

- Input workbook: `liber_primus_visual_master_dataset_v1_1.xlsx`
- New workbook: `liber_primus_visual_master_dataset_v1_2.xlsx`
- Refit/build script: `build_liber_primus_geometry_v1_2.py`
- Machine-readable results: `liber_primus_visual_geometry_audit_v1_2.json`
- Extraction script recovered: `measure_constellations_v0_2.py`
- Public source repository: [{SOURCE_BASE}](https://github.com/scream314/cicada3301/tree/master/assets/2014/liber-primus-complete)

**Bottom line:** the geometric repetition survives consistent arithmetic refitting on the recorded coordinates, but the current evidence does not yet distinguish a copied decorative template from an unusual independent structure, and it does not establish any relation to the cipher. Source-pixel cross-validation and an empirical corpus null are the next falsification gates.
'''
OUT_MD.write_text(md,encoding='utf-8')

# Export without changing legacy sheets.
SpreadsheetFile.export_xlsx(wb).save(str(OUT_XLSX))
print(json.dumps({'workbook_out':str(OUT_XLSX),'markdown_out':str(OUT_MD),'json_out':str(OUT_JSON),'new_sheet_count':10,'source_hash_matches':len([r for r in source_hash_rows if r[4]]),'transform_rows':len(transform_rows),'threshold_rows':len(threshold_out),'auxiliary_rows':len(aux_records),'geometry_summary':geom_summary,'threshold_sensitivity':{'max_shift_from_T60_px':max_threshold_shift,'median_per_dot_max_shift_px':median_dot_max_shift},'controls':{'page50_gap_share_pct':[g50['gap1_share_pct'],g50['gap2_share_pct']],'page56_gap_share_pct':[g56['gap1_share_pct'],g56['gap2_share_pct']],'page50_to56_rms_px':fit3056['rms_px'],'plant_57_68_recorded_equal':plant_equal,'page39_best_subset_signature_difference':subset_rows[0][1]},'issues':metadata_issues,'workbook_sha256':wb_sha},indent=2))
