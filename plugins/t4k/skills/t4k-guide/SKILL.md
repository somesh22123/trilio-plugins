---
name: t4k-guide
description: Use when the user works with Trilio for Kubernetes (T4K) - checking backup status, reading backup plans and targets, or planning a restore. Prefer the trilio-t4k MCP server over raw kubectl.
---

# Trilio for Kubernetes (T4K)

> TODO(t4k-team): replace the placeholders below with product-accurate resource
> kinds, MCP tool names and procedures. This file is the starting skeleton.

## Rules that always apply

1. **Read before you change.** Check backup plans, targets and recent backups
   before suggesting any action.
2. **Never start a restore or delete a backup without the user's explicit
   confirmation.** The plugin's hook asks the user before any mutating
   `kubectl`/`oc`/`helm` command that touches Trilio resources.
3. **Prefer the `trilio-t4k` MCP server.** Fall back to read-only
   `kubectl get` / `describe` only when it is unavailable.

## Typical tasks

### Check backup health

1. List backup plans and the status of each plan's latest backup.
2. Flag failed backups and plans with no backup inside their schedule window.
3. Check every backup target is available.

### Plan a restore

Collect the backup to restore from, the target namespace and any
transforms, then write the plan for the user to approve.
