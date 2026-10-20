# Internal Developer Platform

## The Problem

Developers often need infrastructure to build and run their applications. Getting it usually involves raising requests, waiting for approvals, and depending on other teams to set things up.

This slows down development, creates repetitive work, and makes it harder to maintain consistent standards across teams.

## What Are We Trying to Solve?

Our goal is to make infrastructure self-service.

Developers should be able to request the resources they need through a simple, well-defined interface, without having to understand all the complexity behind the scenes.

At the same time, the platform should ensure that resources are created consistently, securely, and according to predefined rules.

## How Does Crossplane Help?

Crossplane helps us turn infrastructure into something developers can request rather than something they need to build and manage themselves.

We define what developers can ask for and how those requests should be fulfilled. Crossplane takes care of creating the required resources and keeping them aligned with the desired configuration.

## Our Goal

Build a platform that makes infrastructure **easy to request, safe to use, and simple to manage** so developers can focus more on building applications and less on waiting for infrastructure.

## S3 Bucket API (V1)

The S3 Bucket API gives application teams a simple way to request an AWS S3 bucket. Developers choose the bucket name, AWS region, versioning state, and tags. The platform manages AWS access and applies the platform-defined encryption and public-access settings.

### What developers can request

- A bucket with a lowercase, globally unique S3 name.
- An AWS region.
- A versioning state: `Enabled`, `Suspended`, or `Disabled`.
- Optional string-valued tags.

### What the platform manages

- AWS credentials and provider configuration.
- AES256 server-side encryption.
- S3 public-access blocking.
- Provisioning and ongoing reconciliation of the bucket and its supporting resources.

The requested versioning state is applied to the bucket. See the [S3 API guide](docs/s3-bucket.md) for the available options and platform-managed settings.

### Getting started

Review the [S3 bucket example](docs/examples/s3-bucket.yaml), provide values for your application, and follow your team's platform workflow to request the bucket. The platform team will provide the approved request and namespace process; platform setup and cluster operations are intentionally not part of this developer overview.

### Documentation

- [S3 Bucket API guide](docs/s3-bucket.md) — developer-configurable fields, platform-managed settings, constraints, and current capability status.
- [S3 bucket YAML example](docs/examples/s3-bucket.yaml) — example request to use as a reference.
- [Platform architecture](docs/architecture.md) — platform goals and high-level design.
