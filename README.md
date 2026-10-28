# Internal Developer Platform

This repository provides a self-service AWS S3 bucket capability through a Crossplane API. Application teams can request buckets without managing AWS credentials or provider-specific resources.

## Request a bucket

Use the [developer Helm chart](helm/Readme.md) to submit a bucket claim. For the supported request fields, access modes, and platform-managed behavior, see the [S3 Bucket API guide](docs/s3-bucket.md).

## How it works

The [platform architecture](docs/architecture.md) explains the responsibilities of the claim chart, Crossplane API, and cloud provider.

## Documentation

- [Helm chart usage](helm/Readme.md) — configure and submit a developer bucket claim.
- [S3 Bucket API](docs/s3-bucket.md) — API fields, constraints, access modes, and managed behavior.
- [Platform architecture](docs/architecture.md) — component boundaries and reconciliation flow.
- [Example claim](docs/examples/s3-bucket.yaml) — a complete Crossplane claim.
.