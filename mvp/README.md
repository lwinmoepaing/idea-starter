# mvp/

Prototype code for **one product**, built phase-by-phase from `plans/`. Grows across IDs as feature drops ship — `#0001` lays the scaffold, `#0002+` extend it.

## Stack (default — picked by `mvp-plan`)
- Vite + React + TypeScript
- React Router for navigation
- Zustand as in-memory fake DB (seed on load, mutate freely, no persistence)
- CSS / CSS-modules per the design-system phase's aesthetic call

Optional, only when a demo needs it: `react-hook-form`, `motion` (Framer Motion v11+).

## Scope

Pitch-demo only. Happy path. No real auth/backend/tests/CI. Out-of-scope items live in each phase's "MVP shortcuts (deliberate)" section — don't "fix" stubs that were intentional.

## Bootstrap (`#0001`)

First `mvp-plan` run with an empty `mvp/` writes a `design-system + scaffold` phase. Execute it to land `package.json`, `src/`, tokens, base components. Then build feature phases on top.

## Subsequent feature drops (`#0002+`)

Don't redo the scaffold. `mvp-plan` reads `plans/done/*.md` from prior IDs and plans new phases that **extend** the app — adding routes, store slices, pages, or refining what's already there. Different product entirely? Clone the scaffolding into a new folder; don't shoehorn it as `#0002`.

## Detection

The `scaffold-inspector` sub-agent reads `mvp/package.json` + `mvp/src/**` and reports stack, conventions, and gaps. `mvp-plan` uses that to decide between a full scaffold phase, a slim tokens-only phase, or skipping scaffold work.

## Run

```bash
cd mvp
npm install
npm run dev
```
