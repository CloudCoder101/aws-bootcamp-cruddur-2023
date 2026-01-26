# Week 8 — Serverless Image Processing

Week 08 – Serverless Image Processing
Overview

In Week 8, I implemented a serverless image processing workflow using AWS Lambda and Amazon S3. The goal was to automatically process uploaded images and store optimized versions in a separate S3 bucket.

What Was Built

A Lambda function triggered by S3 upload events

Image processing using the Sharp library

Separate S3 buckets for source and processed images

IAM permissions configured using least privilege

Architecture
Image Upload
   ↓
S3 Source Bucket
   ↓
S3 Event Trigger
   ↓
Lambda Function (Sharp)
   ↓
S3 Processed Bucket

AWS Services Used

Amazon S3 (source and processed buckets)

AWS Lambda (Node.js runtime)

AWS IAM

AWS CDK

Implementation Notes

Lambda function processes images using Sharp

S3 event notifications trigger Lambda execution

IAM role allows read access to source bucket and write access to processed bucket

CDK was used to define and deploy infrastructure

Logging enabled for debugging via CloudWatch

Challenges & Fixes

Resolved Sharp compatibility issues with Lambda runtime

Matched Lambda architecture and Node.js version correctly

Ensured S3 source and destination buckets were separated to avoid recursive triggers

Verification

Uploaded images to the source S3 bucket

Confirmed Lambda execution via logs

Verified processed images appeared in the destination bucket

Screenshots are included to demonstrate successful execution.

Commands Used

cdk deploy

aws s3 ls

docker build

docker push

Key Takeaways

Event-driven serverless architectures scale efficiently

Lambda layers and runtimes must match exactly

Proper IAM permissions are critical for cross-service workflows

Image optimization improves performance and reduces cost

Status

Week 8 implementation completed and verified.