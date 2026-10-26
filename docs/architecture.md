# Platform Architecture

This page describes how the developer claim chart, Crossplane platform API, and AWS provider fit together. For request fields and bucket behavior, see the [S3 Bucket API guide](s3-bucket.md).

## Architecture at a glance

```text
Application team
       |
       | Developer values
       v
Helm chart (developer claim)
       |
       | Renders and submits an XS3Bucket claim
       v
Kubernetes API
       |
       | Validates the request against the Crossplane platform API
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
  ├── Bucket versioning
  └── Bucket policy (read-only or read/write access)
```

## Component responsibilities

- **Developer claim chart (`helm/s3-bucket-claim/`):** packages the application team's bucket request as an `XS3Bucket` resource. It does not install platform components. See [Helm chart usage](../helm/Readme.md).
- **Crossplane platform API (`crossplane/`):** the XRD defines the request contract, and the Composition maps accepted claims to provider resources and applies platform-owned configuration.
- **Cloud integration:** the Upbound AWS provider reconciles those resources with AWS using platform-managed credentials. Credentials and provider-specific resources are not part of the developer request.

The Crossplane API and supporting platform resources must already be available in the cluster before a chart-generated claim can be accepted. Application teams manage claim desired state; the platform team owns the API, Composition, provider configuration, and cloud identity.

## Reconciliation

Crossplane observes each claim, creates the corresponding composite resource and composed AWS resources, and continually reconciles them through the provider. This makes the claim the desired state rather than a one-time provisioning instruction.

For the request schema, supported access modes, and bucket security behavior, see the [S3 Bucket API guide](s3-bucket.md).

## Related documentation

- [Helm chart usage](../helm/Readme.md) — submitting developer claims.
- [Repository overview](../README.md) — documentation entry point.
