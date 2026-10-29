---
name: tsr-guide
description: Use when the user works with Trilio Site Recovery (TSR) on Kubernetes or OpenShift - checking DR readiness, reading protection and recovery status, or planning a failover or failback. Prefer the trilio-tsr MCP server over raw kubectl.
---

# Trilio Site Recovery (TSR)

> TODO(tsr-team): replace the placeholders below with product-accurate resource
> kinds, MCP tool names and procedures. This file is the starting skeleton.

## Rules that always apply

1. **Read before you change.** Check current protection and replication status
   before suggesting any action.
2. **Never fail over, fail back or delete a TSR resource without the user's
   explicit confirmation.** The plugin's hook asks the user before any
   mutating `kubectl`/`oc`/`helm` command that touches Trilio resources.
3. **Prefer the `trilio-tsr` MCP server.** Fall back to read-only `kubectl get`
   / `describe` only when the MCP server is unavailable.
4. State which cluster and namespace you are acting on in every answer.

## Typical tasks

### Check DR readiness

1. List the protected applications and their last successful replication.
2. Flag any application whose replication is older than its target RPO.
3. Report the result as a table: application, namespace, last replication, status.

### Plan a failover

Hand off to the `tsr-recovery-planner` agent. It produces a written plan the
user approves before anything runs.

## Out of scope

Installing or upgrading TSR itself. Point the user to the TSR install docs.
