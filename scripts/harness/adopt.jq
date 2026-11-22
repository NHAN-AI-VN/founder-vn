# Lane adoption (D24): which in-flight lanes have finished on their branch without a pull request,
# so the dispatcher opens the pull request itself instead of waiting for a recall.
#
# Input:
#   { now: iso8601,
#     lanes: [ { number, branch, pushedAt: iso8601|null, headSha: string|null, ahead: int,
#                openPr: int|null, evidence: { path, text } | null } ] }
# Output:
#   [ { number, branch, adopt: bool, reasons: [string] } ]  # reasons say why NOT, or "ready"
#
# A lane is adopted only when every line holds: no open pull request for the branch, the branch
# exists and is ahead of the base, it has not moved for quiet_after seconds (the session may be
# a step away from opening the pull request itself: #222 opened its own 2 minutes after the
# evidence commit), and the evidence file on the branch records the segmented gate's verdict
# (`gate-segment.sh verify` prints "GREEN on <sha>", D28). Three lanes in a row (#221, #223,
# #224, 2026-09-10) died between that commit and the open-PR command; the operator opened the
# pull request by hand each time from the same evidence. The gate and both review turns keep
# their authority: adoption only moves the lane to where they can see it.
def quiet_after: 600;

def seconds: sub("\\.[0-9]+"; "") | fromdateiso8601;

def green: test("GREEN on [0-9a-f]{7,40}");

.now as $now
| [ .lanes[]
    | . as $l
    | ( [ (if .openPr != null then "pull request #\(.openPr) is already open" else empty end),
          (if .pushedAt == null then "no branch \(.branch) yet" else empty end),
          (if .pushedAt != null and (.ahead // 0) == 0 then "branch \(.branch) has no commit beyond the base" else empty end),
          (if .pushedAt != null and (($now | seconds) - (.pushedAt | seconds)) < quiet_after
             then "branch moved \((($now | seconds) - (.pushedAt | seconds)) | tostring) s ago; wait \(quiet_after) s of quiet" else empty end),
          (if .evidence == null then "no evidence file docs/evidence/issue-\(.number)-*.md on the branch" else empty end),
          (if .evidence != null and ((.evidence.text // "") | green | not)
             then "evidence \(.evidence.path) does not record `gate-segment.sh verify` GREEN" else empty end) ] ) as $why
    | { number, branch, adopt: ($why | length == 0), reasons: (if ($why | length) == 0 then ["ready"] else $why end) } ]
