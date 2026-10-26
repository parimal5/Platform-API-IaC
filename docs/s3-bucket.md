# S3 Bucket API (V1)

The S3 Bucket API lets application teams request an AWS S3 bucket using a small set of application-facing settings. The platform handles AWS credentials, infrastructure provisioning, and security configuration so teams do not need to manage those details themselves.

## What developers can define

| Setting | Description | Requirements and options |
| --- | --- | --- |
| Bucket name | Name used for the S3 bucket. | Required. Must be lowercase, follow AWS S3 naming rules, and be globally unique. |
| Region | AWS region in which to create the bucket. | Required. For example, `us-east-1` or `ap-south-1`. |
| Versioning status | Whether S3 object versioning is enabled. | Current API values are `Enabled`, `Suspended`, and `Disabled`. |
| Bucket access mode | Object and bucket-list access granted by the generated bucket policy to the platform-designated IAM role. | Required. `ReadOnly` allows listing the bucket and reading objects. `ReadWrite` also allows writing objects. |
| Tags | Application or team metadata for ownership and organization. | Optional map of string keys to string values. |

Each request has a name and a team namespace. Choose a meaningful name and use the namespace provided by the platform.

## What the platform enforces and manages

- **AWS access:** provider configuration and credentials are managed by the platform and are not part of the developer claim.
- **Server-side encryption:** AES256 encryption is configured automatically.
- **Public access protection:** S3 public-access blocking is enabled automatically.
- **Bucket policy:** the platform creates a policy for the platform-designated IAM role. Both access modes allow `s3:ListBucket` and `s3:GetObject`; `ReadWrite` additionally allows `s3:PutObject`. The role identity is platform-managed, not supplied in the claim.
- **Provisioning:** the platform creates and maintains the bucket and its supporting resources.
- **Resource naming and tagging:** the requested bucket name and tags are passed through to the managed bucket, with platform-managed tags added as configured.

Encryption and public-access settings are fixed by the current V1 Composition; developers cannot override them through this API.

## Request example

See the [complete example claim](examples/s3-bucket.yaml). For instructions on submitting a claim with the developer Helm chart, see [Helm chart usage](../helm/Readme.md).

## Related documentation

- [Helm chart usage](../helm/Readme.md)
- [Platform architecture](architecture.md)
- [Repository overview](../README.md)
