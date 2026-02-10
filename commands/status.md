| description | Show detailed progress of the active spec |
| disable-model-invocation | true |

# Spec Status

Show detailed progress of the active spec.

1. Read `.specs/active` to find active spec ID
2. Load `.specs/specs/<id>/SPEC.md`
3. Parse all phases and tasks
4. Show detailed breakdown:

```
User Auth System [active, high priority]
Created: 2026-02-10 | Updated: 2026-02-11

Phase 1: Foundation [completed] ✓
  ✓ Set up auth middleware
  ✓ Create user model
  ✓ Implement JWT token generation
  ✓ Add refresh token logic

Phase 2: OAuth Integration [in-progress] →
  ✓ Google OAuth provider
  → GitHub OAuth provider ← current
  ○ Token exchange flow

Phase 3: Testing [pending] ○
  ○ Unit tests for auth middleware
  ○ Integration tests
  ○ Security audit

Progress: 5/10 tasks (50%)
Current: GitHub OAuth provider
```

4. Also show the Resume Context section
5. If there are research notes in `.specs/research/<id>/`, mention them
