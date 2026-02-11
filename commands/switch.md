---
description: Switch to a different spec — pause current, activate and resume target
disable-model-invocation: true
---

# Switch Spec

Switch to a different spec. The argument should be a spec ID.

Target: $ARGUMENTS

1. **Pause current spec** — run the full pause workflow (save resume
   context, update checkboxes, set status to paused)
2. **Load target spec** — read `.specs/specs/<target-id>/SPEC.md`
3. **Activate it** — write the target ID to `.specs/active`, set its
   status to `active` in frontmatter
4. **Resume it** — run the full resume workflow (parse progress, find
   current task, read resume context, present summary)
5. **Update registry** — ensure both specs' statuses are current in
   `.specs/registry.md`

If no argument was given, show `.specs/registry.md` and ask the user
which spec to switch to.

This should feel like one seamless operation — context switch in a
single command.
