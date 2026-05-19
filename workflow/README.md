# workflow/

Stage-by-stage evidence for one idea. Three subfolders, one shared slug per idea, so an ID like `#0001-realtime-collab-editor` threads from validate → hunt → market.

## Subfolders

| Folder        | What lives here                                                                                                     | Skill that writes it |
| ------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------- |
| `ideas/`      | Problem, user, pain, alternatives, weakest link, riskiest assumption                                                | `validate-idea`      |
| `approach/`   | Demand-evidence hunt: where to find unsolicited complaints, interview scripts, kill criteria                        | `pain-hunt`          |
| `marketing/`  | Pre-launch / first-1000-users plan: single channel, real budget, 30-day actions, success vs kill criteria           | `marketing-plan`     |

## Naming

`#NNNN-<slug>.md`. Each subfolder counts independently — first file is `#0001`, next `#0002`. The slug carries across folders for the same idea. Re-running a skill on the same idea appends a new dated section; the number stays fixed.

## Feeds `business-canvas`

Given an ID, `business-canvas` reads all three files and renders a Lean Canvas PNG into `docs/`. An empty canvas cell points back to the missing source file — empty `Channels` ⇒ run `marketing-plan` for that ID.
