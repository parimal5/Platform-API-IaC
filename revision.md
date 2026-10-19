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
