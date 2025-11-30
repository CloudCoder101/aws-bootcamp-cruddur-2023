# Week 0 — Foundations, Setup, and Verification

This week focused on preparing my AWS account, establishing security best practices,
configuring the AWS CLI, and documenting proof of each step.

---

## 1. AWS Account Setup & Billing Protections

### Role Access to Billing
I verified that IAM User access to billing is enabled so I can view budgets and cost reports.

![Billing Access](assets\week0-role-access-to-billing-information.png)

### Monthly Cost Budget
Created a monthly cost budget with email alerting configured.

![Cost Budget](assets/week0-crc-monthly-cost-budget.png)

---

## 2. AWS CLI Installation & Identity Verification

Installed AWS CLI, configured credentials with MFA enforced, and verified identity
using STS.

**Command:**
```bash
aws sts get-caller-identity
```

**Proof:**

![STS Identity](assets/week0-sts-get-caller-identity.png)

---

## 3. CloudWatch Alarm & SNS Notifications

### CloudWatch Alarm
Created a CloudWatch alarm for budget notifications and verified alarm details.

![Describe Alarm](assets/week0-cloudwatch-describe-alarm.png)

### SNS Email Subscription
Configured an SNS topic and confirmed the subscription via email.

![SNS Notification](assets/week0-aws-sns-subscription-email-notification.png)

---

## 4. Architecture Diagrams (Conceptual → Logical → Infrastructure)

### Conceptual Diagram
High-level overview of the Crudder application and its major components.

![Conceptual Diagram](assets/week0-crudder-conceptual-napkin-diagram.png)

### Logical Architecture
Shows hop-by-hop communication between services and how requests flow through the stack.

![Logical Architecture](assets/week0-logical-architecture-diagram.png)

### Infrastructure Diagram
Full AWS infrastructure view of how Crudder is deployed in my account.

![Infrastructure Diagram](assets/week0-infrastructure-diagram.png)

---

## 5. Week 0 Reflections

- Turned on MFA and cleaned up the AWS account to be “bootcamp ready.”
- Added billing protections (budget + alarm + SNS) so I don’t get surprised by charges.
- Installed and verified the AWS CLI using `aws sts get-caller-identity`.
- Rebuilt my Week 0 diagrams and captured them as assets stored under `journal/assets/`.

I also created a `journal/backfill/` folder and a `markdown_playground.md` file to
practice Markdown so that my future journal entries are clearer and easier to grade.
