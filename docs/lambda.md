# Lambda API

The Lambda API lets application teams request an AWS Lambda function using an `XLambda` resource. Crossplane provisions the function and its execution role. The platform manages AWS credentials and provider configuration; teams provide the function settings and a deployment package already uploaded to S3.

## What developers can define

| Setting | Description | Requirements and options |
| --- | --- | --- |
| Region | AWS region for the function. | Required. Currently supported: `us-east-1`, `us-west-1`, and `ap-south-1`. |
| Runtime | Lambda language runtime. | Required. Currently supported: `python3.12` and `nodejs22.x`. |
| Handler | Function entry point, such as `app.handler`. | Required and non-empty. |
| Code S3 bucket | Bucket containing the deployment ZIP. | Required. Upload the package before requesting the function. |
| Code S3 key | Object key of the deployment ZIP in that bucket. | Required. |
| S3 object version | Specific S3 object version to deploy. | Optional; useful for selecting an immutable package version. |
| Memory size | Function memory allocation in MB. | Optional; defaults to `256`, minimum `128`, maximum `1024`. |
| Timeout | Maximum execution time in seconds. | Optional; defaults to `30`, minimum `1`, maximum `60`. |
| Environment | Non-secret environment variables. | Optional map of string keys to string values. Do not put secrets here. |
| Tags | Application or team metadata. | Optional map of string keys to string values. |

## S3 deployment package

The function code is not uploaded by the `XLambda` request. Build and upload a Lambda-compatible ZIP package to an S3 bucket that the Crossplane AWS identity can access, then provide its bucket name and object key under `spec.code`.

The example uses the existing bucket `parimal-s3-bucket-5320` and object key `lambda-package-crossplane/lambda-package.zip`. Ensure that object exists and that the AWS identity used by Crossplane has the required access to read it.

## What the platform manages

- **Execution role:** Crossplane creates an IAM role trusted by `lambda.amazonaws.com` and attaches the AWS-managed `AWSLambdaBasicExecutionRole` policy.
- **Function:** Crossplane creates and reconciles the Lambda function using the selected runtime, handler, S3 package, environment, memory, timeout, and tags.
- **AWS credentials:** credentials and provider configuration are platform-managed and are not supplied in the `XLambda` request.

The Lambda function depends on its execution role becoming ready. AWS permissions must allow the Crossplane identity to manage the role and function, pass the role to Lambda, and access the S3 deployment object.

## Request example

See the [complete example claim](examples/lambda.yaml), which references the existing bucket `parimal-s3-bucket-5320`. For the fields and schema, see the [Lambda XRD](../crossplane/xrd/lamda-xrd.yaml) and [Lambda Composition](../crossplane/compositions/lambda-compositions.yaml).

## Related documentation

- [Platform architecture](architecture.md)
- [S3 Bucket API guide](s3-bucket.md)
- [Repository overview](../README.md)