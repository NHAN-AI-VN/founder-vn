# One line from the body GitHub returns for a failed REST call (what `gh api` prints on stdout
# when the status is not 2xx): the message, then each error's message, or its resource, field
# and code when it carries no message, joined by "; ". D24b: a failed adoption names its reason.
[ .message ] + [ .errors[]? | .message // ([ .resource, .field, .code ] | map(select(. != null)) | join(" ")) ]
| map(select(. != null and . != "")) | join("; ")
