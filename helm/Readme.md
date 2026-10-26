# S3 Bucket Claim Helm Chart

This chart renders an `XS3Bucket` developer claim from [`s3-bucket-claim/values.yaml`](s3-bucket-claim/values.yaml). It packages the request only; it does not install Crossplane, the platform API, the AWS provider, or the Composition.

The Crossplane API and supporting platform resources must already be available in the target cluster before you submit a claim. See the [platform architecture](../docs/architecture.md) for component responsibilities and the [S3 Bucket API guide](../docs/s3-bucket.md) for the full request contract and platform-managed behavior.

## Configure a claim

Copy the chart's `values.yaml` and set values for your application:

| Value | Purpose |
| --- | --- |
| `metadata.name` | Name of the Kubernetes claim. |
| `metadata.namespace` | Namespace assigned to your team. |
| `spec.bucketName` | Lowercase, globally unique S3 bucket name. |
| `spec.region` | AWS region for the bucket. |
| `spec.versioning.enable` | `true` renders versioning status `Enabled`; `false` renders `Suspended`. |
| `spec.bucketPolicy.accessMode` | Select an access mode supported by the [S3 Bucket API](../docs/s3-bucket.md). |
| `spec.tags` | Optional string-valued tags. |

The platform API supports `Disabled` versioning, but this chart's boolean setting does not expose that option.

## Render and submit

Render the claim locally to review it:

```powershell
helm template my-bucket .\helm\s3-bucket-claim --values .\my-bucket-values.yaml
```

Submit the chart to the current Kubernetes context after reviewing the rendered claim and confirming the platform API is available:

```powershell
helm upgrade --install my-bucket .\helm\s3-bucket-claim --values .\my-bucket-values.yaml
```

Helm tracks the generated claim as a release resource. Follow your team's namespace and deployment workflow.
