# LaunchPad Helm Architecture

## Structure

- **Provider prerequisite:** Install `provider-aws-s3` separately. Crossplane creates its CRDs asynchronously, so wait until `ClusterProviderConfig`'s CRD is available.
- **Platform chart:** `helm/platform-infra-helm/` manages the `ClusterProviderConfig`, Function, S3 XRD and Composition.
- **Developer request:** `XS3Bucket` manifests are separate; the chart does not create buckets by default.

## Why

- Keep provider installation separate because dependent APIs are not available immediately.
- Use Helm to version and deploy LaunchPad's shared S3 capability consistently.
- Keep encryption and public-access blocking enforced by the Composition.

## Deployment

1. Install the AWS S3 provider.
2. Wait for the required CRDs/provider readiness.
3. Deploy the platform chart:

   ```bash
   helm upgrade --install launchpad-platform helm/platform-infra-helm/ --namespace crossplane-system
   ```

4. Apply a separate `XS3Bucket` request and verify the bucket in AWS.

**Later:** automate these steps in a pipeline or GitOps workflow.