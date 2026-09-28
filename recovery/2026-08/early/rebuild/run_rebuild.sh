#!/usr/bin/env bash
# Re-runs the transcribed August build chain in a temp dir and recalculates with LibreOffice.
# Order mirrors the sessions: f00a0b22 (turns 25,27,37,39,41,45) -> 1d9082f0 (turn 5) -> e2953710 (turns 1,9).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; OUT="${1:-$HERE/..}"
W="$(mktemp -d)"; cp "$HERE"/*.py "$W"/; cd "$W"
sed -i "s#/mnt/user-data/outputs/#$W/#" build_a1_frame.py build_a2.py build_a2_frame.py build_fixture.py
python3 a1_v2_transform.py && sed -i "s#/mnt/user-data/outputs/#$W/#" build_a1_frame_v2.py
python3 build_a1_frame_v2.py && python3 a1_session3_patches.py cph-route-a1-frame.xlsx
python3 build_a2.py && python3 a2_turn39_41_transforms.py && python3 build_a2_frame.py
python3 a2_legend_turn45.py cph-route-a2-frame.xlsx
python3 a2_session2_fix.py cph-route-a2-frame.xlsx a2_s2.xlsx && python3 a2_session3_upd.py a2_s2.xlsx a2_final.xlsx
mv a2_final.xlsx cph-route-a2-frame.xlsx
python3 build_fixture.py
mkdir -p rc && for f in cph-route-a1-frame.xlsx cph-route-a2-frame.xlsx f2-test-fixture-copenhagen.xlsx; do soffice --headless --calc --convert-to xlsx --outdir rc "$f" >/dev/null 2>&1; done
cp rc/*.xlsx "$OUT"/; echo "written to $OUT"
