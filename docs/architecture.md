# Platform Architecture

This page describes how the developer claim chart, Crossplane platform API, and AWS provider fit together. For request fields and bucket behavior, see the [S3 Bucket API guide](s3-bucket.md) and [Lambda API guide](lambda.md).

## Architecture at a glance

```text
Application team
       |
       | Developer values
       v
Helm chart or Kubernetes manifest (developer claim)
       |
       | Submits an XS3Bucket or XLambda claim
       v
Kubernetes API
       |
       | Validates the request against the Crossplane platform API
       v
Crossplane composite resource (XS3Bucket or XLambda)
       |
       | Composition + pipeline functions
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
  ├── Bucket policy (read-only or read/write access)
  ├── Lambda execution role
  └── Lambda function (code package loaded from S3)
```

## Component responsibilities

- **Developer claim chart (`helm/s3-bucket-claim/`):** packages the application team's bucket request as an `XS3Bucket` resource. It does not install platform components. See [Helm chart usage](../helm/Readme.md).
- **Crossplane platform API (`crossplane/`):** XRDs define the S3 bucket and Lambda request contracts, and their Compositions map accepted claims to provider resources and apply platform-owned configuration.
- **Cloud integration:** the Upbound AWS provider reconciles those resources with AWS using platform-managed credentials. Credentials and provider-specific resources are not part of the developer request.
- **Lambda package:** the application team uploads its deployment ZIP to S3 and supplies the bucket and object key in the `XLambda` request.

The Crossplane API and supporting platform resources must already be available in the cluster before a chart-generated claim can be accepted. Application teams manage claim desired state; the platform team owns the API, Composition, provider configuration, and cloud identity.

## Reconciliation

Crossplane observes each claim, creates the corresponding composite resource and composed AWS resources, and continually reconciles them through the provider. This makes the claim the desired state rather than a one-time provisioning instruction.

For the request schema, supported access modes, and bucket security behavior, see the [S3 Bucket API guide](s3-bucket.md). For Lambda configuration and its S3 package requirements, see the [Lambda API guide](lambda.md).

## Related documentation

- [Helm chart usage](../helm/Readme.md) — submitting developer claims.
- [Lambda API guide](lambda.md) — requesting an AWS Lambda function.
- [S3 Bucket API guide](s3-bucket.md) — requesting an S3 bucket.
- [Repository overview](../README.md) — documentation entry point.
