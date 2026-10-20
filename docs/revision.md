# Crossplane Dummed down

#### Crossplane is a tool that help you to expose Platform API which can be consumed bu end user to create resrouces.

Crossplane can be deployed in the Kuberbtes CLsuter using helm it will deploy the CRD's that can help you tom manage the resouces via crossplane.

For simplicicty going forward I am gogin to use AWS as example

The very first thing you need with corssplane to works are [Providers](https://marketplace.upbound.io/providers) and [https://marketplace.upbound.io/providers/upbound/provider-family-aws/v2.9.1?tab=providerConfig](ProviderConfig) :

Provider are basically help you to create relation between crossplane and the AWS resoruces i.e. Managed Resoruces

A Crossplane Managed Resource (MR) is basically a piece of cloud infrastructure—like a database, a storage bucket, or a virtual machine—that you can create and manage using Kubernetes.

EG.

So if we need to create resource like AWS S3 thenwe are gogin to use

1. `provider-aws-s3`
   and under theses provieder you will be able to edit many realted managed resource like Bucket, BucketLifecycleConfiguration, BucketPolicy, BucketVersioning etc.
2. `provider-aws-ec2`
   like ec2, vpc, subnet, eni etc etc

   Now the provider are not just enough so provider just provide you a way to connect to AWS but how does a provider know that how to connect and does it have access to connect that?

   So the answer is you will need creds inorder to connect to AWS using IAM. There are many ways to authnticate yourself like IRSA, webidentity etc etc

   but simpleicyt sake we are going to use simple version where we are gogin to create a secrets from file and then use that secrete to authnticate to AWS.

   Now finally to bring everythig together we will use `ProviderConfig`

   Provider config tells your config on wich kind of creds it should use to authenticate to AWS

   See more (example here)[https://marketplace.upbound.io/providers/upbound/provider-family-aws/v2.9.1/resources/aws.m.upbound.io/ProviderConfig/v1beta1]

### How the crossplane work at runtime

The crossplane has 5 main component

1. XRD - Schema [Terraform Module]
2. Claim - Created by developer to supply input to variables [Terraform tfvars]
3. XR - This is automtically created by crossplane which contain the vaules from claim
4. Managed Resoruce - Theses are crossplane resoruces that actuially create the AWS resoruce like S3, EC2 etc
5. Compositions - now this help pass the vaule we have in XR that we got from Claim to Managed Resource.

So Basic flow is

- Developer create a Claim
- Claim first looks at XRD to create an XR.
- This XR now contain the bluprint what our resoruce looks like from XRD and it get vaules from Claim.
- Now the Compostiion allow us to patch or override the vaules from XR to the Managed Resoruce.

> One small nuance: the XR contains the requested values, but the Composition can also apply defaults, transformations, and other logic. So its output isn't necessarily just a direct copy of the Claim.
