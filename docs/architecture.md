# Platform Architecture

## Purpose

This repository is the foundation of an internal developer platform (IDP) for self-service cloud infrastructure. It provides a Kubernetes-native interface where application teams describe the infrastructure they need, while the platform team retains control over how that infrastructure is provisioned and secured.

The current implementation is the first increment: an AWS S3 bucket API backed by Crossplane.

## Architecture at a glance

```text
Application team
       |
       | S3Bucket claim: name, region, versioning, tags
       v
Kubernetes API
       |
       | Validates the request against the platform API schema
       v
Crossplane composite resource (XS3Bucket)
       |
       | Composition + patch-and-transform function
       | Applies platform defaults and creates supporting resources
       v
Crossplane AWS provider
       |
       | Uses platform-managed AWS credentials
       v
AWS
  ├── S3 bucket
  ├── Bucket encryption configuration
  ├── Public access block
  └── Bucket versioning
```

## Design and responsibilities

### Developer interface

Developers submit a declarative `XS3Bucket` resource using the `platform.parimal.com/v1alpha1` API. The request captures the application-level choices: bucket name, AWS region, versioning state, and optional string-valued tags. The interface intentionally avoids exposing AWS credentials or the details of individual provider resources.

### Platform API and orchestration

The Crossplane CompositeResourceDefinition (XRD) defines the API contract and schema. A Composition translates each request into AWS managed resources. The patch-and-transform function passes user-selected values to the appropriate resources and applies platform-owned configuration.

### Cloud integration

The Upbound AWS S3 provider reconciles managed-resource specifications with AWS. A platform-managed ProviderConfig supplies credentials; credentials are not part of a developer request. Crossplane continuously reconciles desired state, rather than treating a request as a one-time provisioning script.

## V1 capability and policy boundary

| Area | Developer input | Platform responsibility |
| --- | --- | --- |
| Bucket identity | S3 bucket name | Map the requested name to the AWS bucket; AWS enforces global name availability and service naming rules. |
| Location | AWS region | Propagate the selected region to the bucket and supporting resources. |
| Object versioning | `Enabled`, `Suspended`, or `Disabled` | Create and configure the corresponding bucket versioning resource. |
| Metadata | Optional string key/value tags | Apply requested tags and platform-managed tags. |
| Security | No per-request security override | Configure AES256 server-side encryption and block public access. |
| Cloud access | No credentials in the request | Maintain provider configuration and AWS credentials. |

The security settings are platform defaults in the current Composition, not developer-selectable options. Changes to those controls are therefore platform changes rather than per-application choices.

## Reconciliation and ownership

The claim represents desired state. Crossplane observes it, creates the composite resource and its composed AWS managed resources, and reconciles them through the provider. The platform API is the supported abstraction; the provider-specific managed resources are implementation details owned by the platform.

The API and Composition are versioned separately from individual application requests. This allows the platform team to evolve implementation details while keeping the developer-facing contract deliberate and stable.

## Current scope

The repository currently defines one AWS capability: S3 bucket provisioning with region selection, tags, versioning, AES256 encryption, and public-access blocking. It does not yet define a broader service catalog, tenant onboarding workflow, approval workflow, automated delivery interface, or operational SLOs. These are future platform design areas, not implied capabilities of the current implementation.

## Key architecture decisions

- **Kubernetes-native contract:** infrastructure requests are declarative resources that can fit into existing Kubernetes and GitOps workflows.
- **Abstraction over provider details:** application teams request platform capabilities; Crossplane compositions and provider resources implement them.
- **Centralized cloud identity:** the platform owns cloud credentials and provider configuration instead of distributing AWS credentials to application teams.
- **Secure defaults:** encryption and public-access controls are applied consistently by the Composition.
- **Reconciliation-based lifecycle:** desired state is continuously reconciled, making drift correction part of the control plane.

## Related documentation

- [S3 Bucket API guide](s3-bucket.md) — developer-facing fields and platform-managed behavior.
- [S3 bucket example](examples/s3-bucket.yaml) — example API request.
- [Repository overview](../README.md) — platform purpose and current V1 summary.
