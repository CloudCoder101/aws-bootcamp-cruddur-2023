# Week 0 – Billing & Architecture Journal

This document contains all Week 0 deliverables for the Cloud Resume Challenge (CRUDDR project).  
The goal of Week 0 is to establish the AWS foundation for the project:

- Configure AWS CLI with a non-root IAM user  
- Enable billing access  
- Verify identity via STS  
- Produce architecture diagrams  
- Create an SNS topic and confirm an email subscription  
- Create a CloudWatch billing alarm  
- Create an AWS Budget  
- Confirm the end-to-end billing notification chain  

All required Week 0 assets are included and documented below.

---

## 0. Week 0 Directory Structure

The following screenshot shows the `/journal/week0` directory containing the Week 0 journal file and all proof artifacts:

![Week 0 Directory Structure](./week0/week0-directory-structure.png)

---

## 1. AWS CLI Setup

The AWS CLI was installed and configured using a dedicated IAM user (not the root account).  
This satisfies the Week 0 requirement to verify proper CLI setup, authentication, and permissions.

### 1.1 STS Caller Identity (CLI Verification)

This command confirms:

- The CLI is authenticated  
- The IAM user is correct  
- The AWS Account ID matches  
- Root is **not** being used  

**Command used:**  
`aws sts get-caller-identity`

![STS Get Caller Identity](./week0/week0-sts-get-caller-identity.png)

---

## 2. IAM Billing Access Enabled

CloudWatch billing alarms only function if IAM users are allowed to access billing information.  
This screenshot verifies that IAM billing access is active for the account and the appropriate role/user.

![IAM Billing Access](./week0/week0-role-access-to-billing-information.png)

---

## 3. Architecture Diagrams (Required in Week 0)

Week 0 requires producing three architectural diagrams that represent different layers of understanding for the CRUDDR project.

### 3.1 Conceptual “Napkin” Diagram

High-level conceptual view showing:

- User  
- Front end  
- API / backend  
- Database  
- Supporting cloud services  

![CRUDDR Napkin Diagram](./week0/week0-cruddr-conceptual-napkin-diagram.png)

---

### 3.2 Logical Architecture Diagram

Logical view of the system components and how they interact (frontend, backend, networking, database, and AWS services).

![Logical Architecture](./week0/week0-logical-architecture-diagram.png)

---

### 3.3 Infrastructure / Physical Architecture Diagram

Infrastructure-level diagram showing the actual AWS resources and how they are deployed and connected.

![Infrastructure Diagram](./week0/week0-infrastructure-diagram.png)

---

## 4. SNS Topic & Email Subscription

The SNS topic **crc-billing-alerts** is required to receive billing notifications from the CloudWatch billing alarm.  
An email subscription was created and successfully confirmed.

This proves that the SNS topic exists and that the email endpoint has confirmed the subscription, completing the SNS portion of the notification chain.

![SNS Subscription Email Notification](./week0/week0-aws-sns-subscription-email-notification.png)

---

## 5. CloudWatch Billing Alarm (CLI)

A CloudWatch billing alarm was created using the **AWS/Billing** namespace to monitor estimated charges in USD.  
This alarm triggers when estimated charges exceed the configured threshold and publishes to the **crc-billing-alerts** SNS topic.

![CloudWatch Describe Alarm](./week0/week0-cloudwatch-describe-alarm.png)

---

### 5.1 Command Used to Create the Billing Alarm

*(Formatted as text instead of a code block to avoid markdown formatting issues.)*

aws cloudwatch put-metric-alarm  
--alarm-name "CRC-Billing-Alarm-10USD"  
--alarm-description "Billing alarm for AWS account"  
--metric-name "EstimatedCharges"  
--namespace "AWS/Billing"  
--statistic Maximum  
--period 21600  
--threshold 10  
--comparison-operator GreaterThanThreshold  
--dimensions Name=Currency,Value=USD  
--evaluation-periods 1  
--alarm-actions "arn:aws:sns:us-east-1:563770762158:crc-billing-alerts"  
--region us-east-1

---

### 5.2 CloudWatch Alarm Verification (CLI Output)

The following screenshot is the CLI proof that the alarm was created and is active:

**Command used:**  
`aws cloudwatch describe-alarms --alarm-names "CRC-Billing-Alarm-10USD"`

This screenshot shows:

- Alarm name  
- Alarm ARN  
- AWS/Billing namespace  
- EstimatedCharges metric  
- USD currency dimension  
- Threshold = 10  
- SNS action → `crc-billing-alerts`  
- Alarm state and configuration  

![CloudWatch Describe Alarm](./week0/week0-cloudwatch-describe-alarm.png)

---

## 6. AWS Monthly Cost Budget

Week 0 requires both:

- A CloudWatch Billing Alarm  
- An AWS Monthly Cost Budget  

The budget monitors overall monthly spending and sends alerts when thresholds are exceeded, providing a second layer of cost protection.

### 6.1 CRC Monthly Cost Budget Screenshot

![CRC Monthly Cost Budget](./week0/week0-crc-monthly-cost-budget.png)

---

## 7. Week 0 Completion Summary

All Week 0 requirements have been successfully completed:

- ✅ AWS CLI installed and configured using IAM credentials  
- ✅ IAM billing access enabled and validated  
- ✅ STS identity verification performed (`aws sts get-caller-identity`)  
- ✅ Conceptual “napkin” diagram created  
- ✅ Logical architecture diagram created  
- ✅ Infrastructure / physical diagram created  
- ✅ SNS topic (`crc-billing-alerts`) created  
- ✅ SNS subscription confirmed via email  
- ✅ CloudWatch billing alarm created, wired to SNS, and verified via CLI output  
- ✅ AWS Monthly Cost Budget created and documented  
- ✅ All proof artifacts (screenshots + diagrams) stored in `/journal/week0`  




