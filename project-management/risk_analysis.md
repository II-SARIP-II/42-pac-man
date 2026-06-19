# Risk Analysis

## Purpose
This document tracks things that could go wrong during the project, before they
actually happen. The goal is not to predict the future perfectly — it's to show
we thought ahead and had a plan, instead of being caught off guard.

## How to fill this out
Add a new row whenever you identify a risk (technical, organizational, or time-related).
Update the "Status" column if the risk actually occurs or is resolved.

- **Risk**: one sentence describing what could go wrong.
- **Likelihood**: Low / Medium / High — your gut estimate of how likely this is.
- **Impact**: Low / Medium / High — how bad it would be if it happened.
- **Mitigation**: what we will do to prevent it, or what we'll do if it happens anyway.
- **Status**: Open / Happened / Avoided / Resolved.

## Example
| Risk | Likelihood | Impact | Mitigation | Status |
|---|---|---|---|---|
| Mac Intel incompatibility with required PyTorch version | Medium | High | Test build on Linux VM in week 1 as backup | Open |
| Underestimating evaluation tuning time | High | Medium | Reserve 2 extra days before deadline as buffer | Open |

## Notes
- Add risks as soon as you think of them — don't wait for a "review meeting."
- If a risk actually happens, update its row and briefly note what you did about it
  (this becomes good evidence for the "blocking points" part of project management).
