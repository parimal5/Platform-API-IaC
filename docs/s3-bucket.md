# S3 Bucket API (V1)

The S3 Bucket API lets application teams request an AWS S3 bucket using a small set of application-facing settings. The platform handles AWS credentials, infrastructure provisioning, and security configuration so teams do not need to manage those details themselves.

## What developers can define

| Setting | Description | Requirements and options |
| --- | --- | --- |
| Bucket name | Name used for the S3 bucket. | Required. Must be lowercase, follow AWS S3 naming rules, and be globally unique. |
| Region | AWS region in which to create the bucket. | Required. For example, `us-east-1` or `ap-south-1`. |
| Versioning status | Whether S3 object versioning is enabled. | Current API values are `Enabled`, `Suspended`, and `Disabled`. |
| Tags | Application or team metadata for ownership and organization. | Optional map of string keys to string values. |

Each request has a name and a team namespace. Choose a meaningful name and use the namespace provided by the platform.

## What the platform enforces and manages

- **AWS access:** provider configuration and credentials are managed by the platform and are not part of the developer claim.
- **Server-side encryption:** AES256 encryption is configured automatically.
- **Public access protection:** S3 public-access blocking is enabled automatically.
- **Provisioning:** the platform creates and maintains the bucket and its supporting resources.
- **Resource naming and tagging:** the requested bucket name and tags are passed through to the managed bucket, with platform-managed tags added as configured.

Encryption and public-access settings are fixed by the current V1 Composition; developers cannot override them through this API.

## Bucket versioning

Choose `Enabled`, `Suspended`, or `Disabled` for the bucket's versioning status. The platform applies the requested status to the S3 bucket.

## Example claim

See the complete [S3 bucket example](examples/s3-bucket.yaml). The main fields are:

```yaml
apiVersion: platform.parimal.com/v1alpha1
kind: XS3Bucket
metadata:
  name: demo-app-storage
  namespace: crossplane-system
spec:
  bucketName: launchpad-demo-unique-name
  region: ap-south-1
  versioningConfiguration:
    status: Enabled
  tags:
    team: platform
    application: demo-app
```

Use a unique lowercase bucket name and the namespace assigned to your team. The example namespace reflects the current development environment; use the namespace specified by your platform team.

## Related documentation

- [Repository overview](../README.md)
- [Platform architecture](architecture.md)
