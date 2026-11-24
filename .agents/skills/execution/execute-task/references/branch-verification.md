# Branch verification

What `SKILL.md`'s **Completion** applies when it verifies the requested behavior on the change's
branch, within the authorized scope and including reachable dependency branches.

When a requested flow failed, repair and push the fix, exercise that branch through the applicable
route, and repeat the complete failed flow until its requested outcome is verified. A narrower health check or passing component
test cannot replace that flow. When a deployment entrypoint consumes configuration, its verification
also proves that entrypoint receives the required settings and reads values in the deployed
representation; a local fixture using different settings or a different representation does not
establish the deployed route.

Trace the verification route to the code it actually loads before treating its result as proof or
proposing a merge: record the exact pull-request head, changed entrypoint and relevant event-specific
paths. Selecting an application's branch does not prove that the workflow, publisher or other
changed command ran from that branch. Use the authorized selected-branch route and verify that its
workflow identity and executed code agree; never assume a trusted workflow must execute default-
branch code. Where an actual security contract prevents live branch execution, first exercise an
equivalent native isolated branch route preserving authentication, permissions and input contracts,
and state precisely which live behavior remains unverified. Do not add a temporary workflow bypass.
