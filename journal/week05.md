Week 05 — DynamoDB (NoSQL) Integration
Overview

In Week 05, I added DynamoDB as a NoSQL datastore to the Cruddur project. The focus of this week was learning how to model and interact with DynamoDB locally using DynamoDB Local, Python (boto3), and supporting scripts. This work introduces NoSQL concepts and prepares the backend for scalable message storage patterns that do not rely on relational joins.

Why DynamoDB (NoSQL) vs Postgres (Relational)

Postgres remains part of the Cruddur project for relational data that benefits from structured schemas and joins, such as core application data. DynamoDB is introduced for access patterns where fast lookups, scalability, and simple key-based access are more important than relational queries.

DynamoDB is well-suited for message timelines and activity feeds because these patterns can be efficiently modeled using partition keys and sort keys without requiring joins. This week focused on understanding and practicing that design approach.

DynamoDB Local Setup

To develop and test locally, I ran DynamoDB using DynamoDB Local via Docker Compose. This allowed me to work without needing AWS credentials or cloud resources while still using the same DynamoDB APIs.

I verified that DynamoDB Local was running by checking container status and confirming the service responded on port 8000.

Screenshot:
journal/assets/week05/week05-01-dynamodb-local-running.png

Table Schema Creation

I created the DynamoDB table cruddur-messages using a Python script (schema-load) built with boto3. The table uses a composite primary key:

Partition Key (pk)

Sort Key (sk)

This design supports multiple access patterns within a single table, which is a common DynamoDB best practice.

Once the table was created, DynamoDB reported the table status as ACTIVE.

Screenshot:
journal/assets/week05/week05-02-create-table.png

Seeding the Table with Data

After creating the table, I populated it with sample message data using a custom seed script. The seed process inserted multiple message records and group records to simulate a real conversation thread between users.

This step confirmed that the schema worked correctly and that DynamoDB could store and retrieve application-style data.

Screenshot:
journal/assets/week05/week05-03-seed-data.png

Verifying Data with Scan

To verify the seeded data, I created a simple Python script (bin/ddb/scan) that performs a DynamoDB scan operation using boto3. Running this script returned all items in the cruddur-messages table, confirming that records were written successfully.

This also demonstrated how DynamoDB items differ from relational rows and how multiple entity types can exist within a single table.

Screenshot:
journal/assets/week05/week05-04-scan-table.png

Verifying Table Access with boto3

I additionally verified table access by listing DynamoDB tables using boto3. This confirmed that the local AWS SDK configuration was correct and that DynamoDB Local was responding as expected.

Screenshot:
journal/assets/week05/week05-05-boto3-list-tables.png

DynamoDB Admin UI

To visually inspect the table and its contents, I used DynamoDB Admin, a web-based UI connected to DynamoDB Local. This provided a convenient way to confirm table structure and item data without relying only on CLI or scripts.

Screenshot:
journal/assets/week05/week05-06-dynamodb-admin-ui.png

Summary and Learning Outcome

By the end of Week 05, I successfully:

Ran DynamoDB Local using Docker

Created a DynamoDB table with a composite key schema

Seeded the table with realistic message data

Verified data access using boto3 scripts

Compared NoSQL design concepts with relational databases like Postgres

This week strengthened my understanding of when NoSQL databases like DynamoDB are appropriate and how to design data models around access patterns rather than joins.

Notes for Review

Postgres remains part of the Cruddur project and is not removed

DynamoDB is used where NoSQL access patterns make more sense

All work was completed locally using DynamoDB Local and Python