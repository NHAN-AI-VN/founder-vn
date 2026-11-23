# The turns posted on one review issue, read from its comments (review-web.sh). Pure: the
# comments in (`[ { login, created_at, body } ]`, oldest first as the API lists them), the turns
# out, oldest first; scripts/harness/witness.sh replays it over a fixture.
#
# A turn is a comment carrying the harness marker. Its `refused` flag reads Kiro's first reply to
# it (the first later comment by kiro-agent[bot], before the next turn): Kiro Web answers a `/kiro`
# it will not serve within seconds, with its session limit ("You've reached your session limit.
# Please wait for an existing session to finish, then mention /kiro again.", lane #9 on
# 2026-11-23, FV-M-9; the documented ceiling is 10 parallel cloud sessions) or with its error
# reply ("Something went wrong while processing your request. Please try again.", nhan D38).
# Either way no session exists, so review-web.jq treats a refused turn as nothing pending and
# posts it again (FV-D17). A reply by anyone else never counts, whatever it says; no reply yet
# reads as not refused (the session may be starting).
def marker: capture("<!-- harness:turn axis=(?<axis>[a-z]+) code=(?<code>[0-9a-f]+) head=(?<head>[0-9a-f]+) round=(?<round>[0-9]+) at=(?<at>[0-9TZ:-]+) -->");
def is_kiro: .login == "kiro-agent[bot]";
def error_reply: test("Something went wrong|session limit"; "i");

. as $comments
| [ range(length) as $i
    | $comments[$i]
    | select(.body | test("<!-- harness:turn "))
    | (.body | marker) as $turn
    # Comments after this one, up to (not including) the next turn.
    | ([ $comments[$i + 1:][] ] | (map(.body | test("<!-- harness:turn ")) | index(true)) as $next
       | if $next == null then . else .[:$next] end) as $after
    | ([ $after[] | select(is_kiro) ] | first) as $reply
    | $turn + { refused: (($reply != null) and ($reply.body | error_reply)) } ]
| sort_by(.at)
