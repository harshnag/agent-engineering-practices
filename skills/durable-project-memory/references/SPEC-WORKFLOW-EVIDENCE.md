# Spec workflows: public evidence and limits

**Read on 2026-09-17 UTC.** This is a first-party documentation review, not an
installation, benchmark, or recommendation to adopt a particular product.
The observations describe the live pages on that date, not pinned releases.

## Separate the useful mechanism from the package

[OpenSpec's concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)
distinguish maintained behavior specifications from proposed changes.
Requirements describe observable behavior; scenarios make the intended outcome
checkable. Change artifacts carry intent, design, tasks, and explicit added,
modified, or removed requirements. The documented sync/archive workflow
reconciles those changes into the maintained specifications and retains history.

That supplies a useful ownership distinction, not proof that an implementation
satisfies the requirements. The
[command reference](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)
describes agent-assisted implementation verification as well as specification
sync. Neither a generated verdict nor synchronized prose replaces the adopting
project's executable checks, real-environment evidence, or review.

Borrowing the distinction does not require adopting the directory layout,
installing OpenSpec, or enabling automatic reconciliation. Whether a packaged
workflow reduces maintenance depends on what the project already does.

## Spec Kit is customizable, not universally rigid

[Spec Kit's README](https://github.com/github/spec-kit) documents a default
specification/planning/tasks/implementation/convergence workflow. It also
documents extensions, presets, workflows, bundles, and project-local overrides,
plus independent entry points for bug fixing and idea assessment.

The [existing-project guide](https://github.github.io/spec-kit/guides/existing-projects.html)
recommends starting with a bounded change rather than reconstructing every
existing feature as a spec. It asks teams to choose whether completed artifacts
are immutable history, maintained contracts, or reconciled artifacts.

Calling every Spec Kit workflow rigid would discard those documented choices.
Whether its default review artifacts are useful or duplicative is a local fit
decision, not a measured cost comparison.

## Kiro is not documented as IDE-only or Claude-only

[Kiro's documentation home](https://kiro.dev/docs/) describes IDE, CLI, Web, and
Mobile surfaces sharing project configuration.
Its [model documentation](https://kiro.dev/docs/models/) lists more than one
provider, including Anthropic and OpenAI, with availability qualifications.
These sources contradict the blanket IDE-only and Claude-only restrictions;
they do not establish arbitrary provider support or identical availability.

The [spec documentation](https://kiro.dev/docs/specs/) describes requirements or
bug analysis, design, and tasks, with a capability table that varies by surface.
In particular, its correctness/property-based testing integration is listed for
the IDE, not every surface. Shared configuration does not imply feature parity.

## What was not established

No framework was installed or exercised for this review. Generated files,
integration with an agent runtime, resource use, productivity, defect rates,
and task-completion quality were not measured. Vendor claims about speed are
not local observations. No universal vendor ranking follows from these sources.

An adopting project can evaluate one bounded change against comparable work,
recording retrieval and clarification effort, missed acceptance cases, rework,
and artifact maintenance. That is an evaluation recommendation, not a result.

The portable workflow belongs in the existing `durable-project-memory` skill:
assign ownership, route current behavior separately from proposals and history,
and preserve the project's evidence and safety controls. This note supports
that design choice; it does not establish a new enforced control.
