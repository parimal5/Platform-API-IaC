# LaunchPad --- Agent Context and Working Agreement

> **Purpose of this file:** Give coding agents (Codex, Claude Code,
> ChatGPT, or another assistant) the project context and decisions they
> need so the owner does not have to re-explain the scenario in every
> session.
>
> **Agent instruction:** Read this file before making changes. Treat the
> decisions below as the current source of truth. If the repository
> contains newer explicit decisions or implementation facts, inspect
> them and reconcile carefully rather than blindly overwriting them.

## 1. Project summary

**LaunchPad** is a learning and portfolio project for building a
self-service Internal Developer Platform (IDP) using Kubernetes and
Crossplane.

The platform should let a developer request infrastructure through a
simple, well-designed Kubernetes API. LaunchPad then applies platform
defaults and guardrails and uses Crossplane to provision and reconcile
the underlying cloud resources.

The project has two equally important goals:

1.  **Learn Crossplane progressively**, from fundamentals through
    practical, advanced patterns.
2.  **Build a credible portfolio project** that demonstrates platform
    engineering, API design, infrastructure automation, security,
    GitOps, and operational thinking.

This is not intended to be a production platform on day one. Build a
small working foundation first, then add capabilities deliberately.

## 2. The problem LaunchPad solves

Without a platform, developers may need to understand cloud-provider
details, request infrastructure manually, or maintain one-off Terraform
and cloud configuration.

LaunchPad should hide unnecessary implementation details behind stable,
self-service APIs. A developer expresses **what they need**; the
platform owns **how it is implemented**, including safe defaults,
permissions, policy, and lifecycle management.

Initial example: a developer requests an S3 bucket by creating a
Kubernetes custom resource. Crossplane reconciles the request and
provisions the AWS S3 bucket.

## 3. Current product and API decisions

These decisions are deliberate. Do not casually redesign them.

### Platform name

-   Overall platform/project name: **LaunchPad**.
-   Use a consistent API group rooted at `platform.parimal.io`, with
    resource-specific groups considered where that produces a clearer
    public contract.
-   Begin with `v1alpha1` while the API is evolving.

### Start with a capability API, not a generic environment API

The first public API should be **`S3Bucket`** because it communicates
the developer's intent directly.

Do **not** start with a generic `AppEnvironment` or
`ApplicationEnvironment` that hides the actual requested capability. A
developer who only needs storage should be able to request storage
directly.

Conceptual example only; validate the final API group, schema, scope,
and fields before treating this as deployable:

``` yaml
apiVersion: storage.platform.parimal.io/v1alpha1
kind: S3Bucket
metadata:
  name: invoice-storage
  namespace: team-payments
spec:
  region: ap-south-1
  versioning: true
```

The example communicates intent, not a finalized schema. Choose the
Crossplane XRD kind, plural, group, version, scope (namespaced or
cluster-scoped), and fields deliberately. Explain the trade-offs before
making a public API contract hard to change.

### Future API direction

Grow incrementally toward distinct capabilities, potentially including:

-   `S3Bucket` --- first capability.
-   `ComputeInstance` or another clearly scoped compute API --- later,
    only when there is a learning objective and cost-safe plan.
-   `ApplicationIdentity` or a workload identity capability --- later.
-   `ApplicationEnvironment` --- eventually, a higher-level API that
    composes multiple capabilities for a complete app environment.

These are future possibilities, not a commitment to implement all of
them immediately. An environment API should compose clear capabilities
rather than replace them.

### API design principles

-   Separate the developer-facing API contract from the underlying
    provider-specific implementation.
-   Use meaningful names that communicate intent.
-   Prefer additive changes and backwards-compatible evolution.
-   Do not rename a public Kind, API group, or field casually. If a
    breaking change is necessary, explain why, identify migration
    impact, and update examples and documentation.
-   Keep provider-specific complexity out of the developer-facing API
    where practical.
-   Enforce security-sensitive settings through platform defaults and
    policy, not developer trust. For S3, consider encryption,
    public-access blocking, and other safe defaults as part of the
    design.
-   Never claim a manifest is valid until it has been checked against
    the actual schema and installed provider/version.

## 4. Target architecture

The intended architecture evolves in stages:

``` text
Developer
   |
   | kubectl apply -f s3bucket.yaml
   v
Kubernetes API server
   |
   | validates and stores the custom resource
   v
LaunchPad API (Crossplane XRD)
   |
   v
Crossplane Composition / composition functions
   |
   v
AWS provider managed resources
   |
   | authenticated with least-privilege AWS IAM permissions
   v
AWS resource (initially S3 bucket)
```

Cross-cutting concerns will be added progressively:

-   **Git + GitHub:** source control, review, collaboration,
    documentation.
-   **GitHub Actions:** CI checks for YAML, schema, policy, and project
    changes.
-   **Kyverno:** policy validation and guardrails when the base API
    works.
-   **Argo CD:** GitOps delivery of platform configuration when it is
    useful.
-   **Prometheus/Grafana and improved operational visibility:** later.
-   **Backstage:** optional later developer portal; not required for the
    first milestone.

Crossplane and Argo CD have different roles: Crossplane reconciles
infrastructure; Argo CD reconciles Git-managed Kubernetes configuration.
They may be used together, but Argo CD is not a prerequisite for the
first local Crossplane exercise.

## 5. Tooling and prerequisites

### Initial local development stack

Start with only the tools needed for the first working capability:

-   Git and a GitHub repository.
-   A code editor (for example, VS Code).
-   Docker Desktop (on Windows, WSL 2 backend is a practical choice).
-   `kubectl`.
-   `kind` for a local Kubernetes cluster.
-   Helm to install Crossplane.
-   Crossplane and the AWS provider required for the S3 resource.
-   An AWS account and AWS CLI only when ready to create real AWS
    resources.

The initial local Kubernetes cluster should be `kind`, not EKS. Do not
create paid cloud infrastructure just to learn the Crossplane API
mechanics.

### Add later, when justified

-   GitHub Actions for CI.
-   Kyverno for policy and guardrails.
-   Argo CD for GitOps.
-   Prometheus/Grafana for metrics and dashboards.
-   Backstage for a developer portal.
-   Additional Crossplane providers or composition functions when
    required by an explicit milestone.

Do not install every tool at the start. Introduce each tool when it
solves a concrete problem in the current milestone.

## 6. Learning and implementation roadmap

Work through the roadmap in order. Keep the implementation small enough
that the owner can understand every important component.

### Milestone 0 --- Inspect and establish the baseline

-   Inspect the repository and its existing files before changing
    anything.
-   Document the local setup and prerequisites.
-   Establish a clean `kind` cluster and verify `kubectl` access.
-   Record tool versions and commands used.
-   Do not assume the existing repository is empty or that earlier setup
    is still present; inspect first.

### Milestone 1 --- Understand Crossplane reconciliation

-   Install Crossplane into the local cluster with Helm.
-   Understand Providers, ProviderRevisions, ProviderConfigs, managed
    resources, and reconciliation status.
-   Configure AWS access safely only when needed.
-   Provision one basic S3 bucket through a Crossplane AWS managed
    resource.
-   Learn how to inspect conditions, events, provider logs, and
    failures.
-   Clean up the resource and confirm that deletion behavior is
    understood.

### Milestone 2 --- Create the public `S3Bucket` API

-   Define an XRD for `S3Bucket`.
-   Define a Composition that maps the public API to the appropriate AWS
    managed resources.
-   Create a sample claim/resource and verify the complete provisioning
    path.
-   Add minimal validation and sensible defaults.
-   Explain the relationship among XRD, Composite Resource, Composition,
    managed resource, and claim before introducing unnecessary
    abstractions.
-   Test both valid and invalid requests.
-   Keep the public API simple; do not expose every AWS provider field.

### Milestone 3 --- Security and quality

-   Add least-privilege AWS IAM permissions.
-   Keep credentials out of Git, manifests, logs, and documentation.
-   Decide how namespaces, RBAC, and ownership should work.
-   Add platform-controlled S3 safety defaults, including encryption and
    public-access protections where supported by the chosen provider
    API.
-   Introduce Kyverno only after the underlying resource flow is
    understood.
-   Add automated validation and tests in GitHub Actions.

### Milestone 4 --- GitOps

-   Decide which resources are platform-owned configuration and which
    are developer requests.
-   Add Argo CD to sync reviewed platform definitions from Git.
-   Understand drift correction, sync failures, pruning, and deletion
    consequences.
-   Do not force all developer requests through GitOps without
    explaining the trade-offs.

### Milestone 5 --- Add another capability

-   Add a second capability only after `S3Bucket` is documented, tested,
    and understood.
-   Possible candidates: compute or workload identity.
-   Make cloud-cost and cleanup implications explicit before introducing
    resources that can incur significant charges.

### Milestone 6 --- Compose higher-level APIs

-   Design `ApplicationEnvironment` only after the individual
    capabilities are stable.
-   Show how the higher-level API composes reusable capabilities.
-   Explain dependency ordering, readiness, status propagation, and
    failure handling.

### Milestone 7 --- Portfolio and operational polish

-   Add architecture diagrams, clear setup instructions,
    troubleshooting, examples, tests, and cleanup.
-   Add monitoring and dashboards only when there are meaningful signals
    to observe.
-   Consider Backstage as an optional user interface, not as a
    prerequisite for the platform.

## 7. Cost and safety constraints

Cost control is a first-class requirement.

-   Prefer `kind` for learning and local integration testing.
-   Start with a single S3 bucket; do not provision EC2, EKS, NAT
    gateways, load balancers, or other costly resources unless a
    milestone explicitly needs them.
-   Before any cloud operation, state which resources may be created,
    likely cost drivers, and cleanup steps.
-   Do not claim that AWS resources are free merely because the control
    plane is local.
-   Include a cleanup path and verify deletion where practical.
-   Never run destructive commands or delete real resources without
    explaining the impact and obtaining explicit approval when the
    action is consequential.
-   Never put access keys, secret values, tokens, or kubeconfig
    credentials into source control.
-   Prefer temporary or dedicated least-privilege credentials. Avoid
    broad administrator access.
-   Do not ask the user to paste secret credentials into chat.

## 8. Repository and implementation approach

Preserve the repository's current structure unless there is a concrete
reason to change it. This is a learning project; avoid unnecessary
abstraction and scaffolding.

A possible structure, if the repository needs one, is:

``` text
launchpad/
├── README.md
├── docs/
│   ├── architecture.md
│   ├── decisions/
│   └── troubleshooting.md
├── bootstrap/
│   └── kind/
├── platform/
│   ├── crossplane/
│   │   ├── providers/
│   │   ├── xrd/
│   │   └── compositions/
│   └── policies/
├── examples/
│   └── s3bucket/
└── tests/
```

This is a suggestion, not a mandate. Inspect the existing repository and
follow established conventions before moving files or introducing
directories.

## 9. Agent working agreement

When working on this repository, follow these rules:

1.  **Read first.** Read this file and inspect relevant repository files
    before proposing edits.
2.  **Work incrementally.** Implement the current milestone, not the
    entire roadmap.
3.  **Teach as you build.** Explain what each important resource does,
    why it exists, and how the pieces connect. The owner wants to learn
    the concepts, not just receive generated YAML.
4.  **Do not skip foundations.** Introduce advanced patterns only after
    the current behavior is clear and working.
5.  **Do not over-engineer.** Avoid unnecessary frameworks,
    abstractions, extra providers, or tools that do not solve a current
    problem.
6.  **Validate changes.** Run available syntax checks, tests, schema
    checks, and relevant Kubernetes validation. If a command cannot be
    run, say so and provide the exact command the owner can run.
7.  **Be honest about validation.** Distinguish between files authored,
    checks actually run, resources applied, and cloud resources
    confirmed created.
8.  **Inspect versions.** Verify installed Crossplane/provider versions
    and their API schemas before using fields or examples. Do not assume
    a field from another version is supported.
9.  **Explain API changes.** Before changing a public Kind, group,
    scope, version, or field, explain compatibility and migration
    consequences.
10. **Keep secrets safe.** Never print, commit, or request secret
    values.
11. **Respect cost controls.** Do not create paid cloud resources or run
    destructive cleanup without clearly explaining the impact.
12. **Update documentation.** When behavior, setup, commands, API
    contracts, or architecture changes, update the relevant docs and
    examples.
13. **Summarize each task.** At the end, report what changed, why, what
    was validated, what remains, and the next recommended step.
14. **Ask only necessary questions.** If the repository and this
    document answer the question, proceed. Ask the owner only when a
    decision materially affects API design, security, cost, or
    architecture and cannot safely be inferred.

## 10. Expected response format for agent tasks

For substantial implementation tasks, structure the response as:

1.  **Goal:** what the current step is intended to teach or deliver.
2.  **Design:** the chosen approach and key trade-offs.
3.  **Changes:** files created or edited and why.
4.  **Validation:** exact checks run and their outcomes.
5.  **Cost/security impact:** any AWS resources, permissions, or
    destructive operations involved.
6.  **Next step:** one logical next step, not a long list of unrelated
    improvements.

## 11. Current project status and next action

Treat the following as the intended direction, not proof that any
resources currently exist:

-   Project name: LaunchPad.
-   Goal: self-service developer platform and Crossplane
    learning/portfolio project.
-   First public capability: `S3Bucket`.
-   Local lab: `kind`.
-   Cloud: AWS only when required, with cost controls.
-   Later stack candidates: GitHub Actions, Kyverno, Argo CD,
    observability, optional Backstage.
-   API strategy: capability APIs first; `ApplicationEnvironment` later.
-   Learning style: step-by-step, foundational concepts first, then
    advanced topics.

**Next action:** inspect the actual repository and current cluster
state, report what is already present, then propose or execute only the
next small step toward a working Crossplane-managed S3 bucket. Do not
assume the setup is complete, and do not provision cloud resources
without making the cost and cleanup implications clear.

------------------------------------------------------------------------

## 12. Quick context prompt for a new agent session

If an agent needs a short instruction, use this:

> Read `AGENTS.md` (or this file if named `README_AGENTS.md`) before
> doing anything. We are building LaunchPad, a step-by-step
> Crossplane-based self-service IDP and portfolio project. Start with a
> clear `S3Bucket` capability API, not a generic `AppEnvironment`; later
> add other capabilities and compose them into `ApplicationEnvironment`.
> Use local `kind` first, use AWS only when needed, control cost and
> secrets, inspect the existing repository and tool versions, implement
> only the current milestone, validate changes, explain concepts, and
> update documentation. Do not casually change public API contracts or
> install extra tools before they are needed.
