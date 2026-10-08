# AWS Serverless Monitoring Application

A hands-on AWS serverless monitoring application built using **Amazon S3, Amazon CloudFront, Origin Access Control (OAC), AWS Lambda, and Amazon DynamoDB**.

The project demonstrates secure static frontend hosting, CDN-based delivery, serverless backend processing, and a managed NoSQL data layer.

---

## Project Overview

This project implements a serverless web application using AWS managed services.

The frontend application is hosted in **Amazon S3** and delivered to users through **Amazon CloudFront**.

CloudFront uses **Origin Access Control (OAC)** to securely access the S3 origin.

The backend is implemented using **AWS Lambda with Python**, and **Amazon DynamoDB** is used as the serverless data store for the monitoring workflow.

### Main Architecture
                   
                    USER
                     |
                     | HTTPS
                     v
             +----------------+
             |  CloudFront    |
             |   CDN + OAC    |
             +-------+--------+
                     |
                     | Secure Origin Access
                     v
             +----------------+
             |    Amazon S3   |
             | Static Website |
             +-------+--------+
                     |
                     | API Request
                     v
             +----------------+
             |   AWS Lambda   |
             | Python Backend |
             +-------+--------+
                     |
                     | Data Operations
                     v
             +----------------+
             |   DynamoDB     |
             | Monitoring DB  |
             +----------------+
```

---

# AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Stores frontend HTML, CSS and JavaScript files |
| Amazon CloudFront | CDN and frontend content delivery |
| CloudFront OAC | Secure access between CloudFront and S3 |
| AWS Lambda | Serverless backend/API processing |
| Amazon DynamoDB | Stores monitoring/application data |
| IAM | Controls permissions between AWS services |
| CloudWatch | Lambda execution logs and troubleshooting |

---

# Project Architecture

The application is divided into three main layers.

### 1. Presentation Layer

```text
Browser
   |
   v
CloudFront
   |
   v
S3
```

The frontend consists of static files:


index.html
style.css
script.js


These files are stored in Amazon S3.

CloudFront distributes the files to users.

---

### 2. Application Layer

```text
Frontend
    |
    | API Request
    v
AWS Lambda
```

The backend uses a Python Lambda function:

```text
serverless-monitoring-api
```

Lambda executes the backend logic without requiring an EC2 server.

---

### 3. Data Layer

```text
AWS Lambda
     |
     v
DynamoDB
```

DynamoDB provides the serverless NoSQL data layer for the monitoring workflow.

---

# Backend

## AWS Lambda Function

Function name:

```text
serverless-monitoring-api
```

Runtime:

```text
Python
```

Lambda is responsible for:

- Processing API requests
- Executing backend logic
- Accessing monitoring data
- Communicating with DynamoDB
- Returning API responses

---

# Backend Code

Create the following file in the GitHub repository:

```text
lambda/
└── serverless-monitoring-api.py
```

Example structure:

```python
import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")

# Replace with your actual DynamoDB table name
table = dynamodb.Table("YOUR_TABLE_NAME")


def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def lambda_handler(event, context):

    try:

        # Example:
        # response = table.scan()
        # items = response.get("Items", [])

        response = {
            "status": "success",
            "message": "Serverless monitoring API is working"
        }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(response)
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "status": "error",
                "message": str(e)
            })
        }
```

> **Important:** Replace `YOUR_TABLE_NAME` with your actual DynamoDB table name before using this code. Do not upload AWS credentials or secrets to GitHub.

---

# Frontend

Recommended frontend structure:

```text
frontend/
├── index.html
├── style.css
└── script.js
```

### index.html

Contains the application user interface.

### style.css

Contains the frontend styling.

### script.js

Handles frontend JavaScript functionality and API communication.

---

# S3 Configuration

The frontend files are uploaded to an Amazon S3 bucket.

Example:

```text
S3 Bucket
│
├── index.html
├── style.css
└── script.js
```

The bucket acts as the origin for CloudFront.

---

# CloudFront Configuration

CloudFront is configured with the S3 bucket as the origin.

```text
User
 |
 v
CloudFront
 |
 | OAC
 v
S3
```

CloudFront provides:

- HTTPS delivery
- CDN distribution
- Edge caching
- Secure S3 origin access

---

# Origin Access Control

CloudFront Origin Access Control is used to control access to the S3 origin.

Instead of exposing the S3 bucket directly:

```text
User → S3
```

the architecture uses:

```text
User
 |
 v
CloudFront
 |
 v
OAC
 |
 v
S3
```

This provides a more secure architecture for serving private S3 content through CloudFront.

---

# DynamoDB

DynamoDB is used as the serverless database layer.

```text
Lambda
   |
   | Read / Write
   v
DynamoDB
```

Advantages:

- Fully managed
- Serverless
- No database server management
- Automatic scaling capabilities
- Native AWS integration

---

# API Response

The backend returns JSON responses.

### Successful response

```json
{
    "status": "success",
    "message": "Serverless monitoring API is working"
}
```

HTTP status:

```text
200 OK
```

### Error response

```json
{
    "status": "error",
    "message": "Error description"
}
```

HTTP status:

```text
500 Internal Server Error
```

---

# CORS

The backend response includes CORS headers:

```text
Access-Control-Allow-Origin: *
```

This allows the frontend to communicate with the backend from a different origin during development/testing.

For production, CORS should be restricted to the actual application domain instead of allowing all origins.

---

# Request Flow

```text
1. User opens application
            |
            v
2. CloudFront receives request
            |
            v
3. CloudFront accesses S3 using OAC
            |
            v
4. Frontend files are delivered
            |
            v
5. JavaScript sends API request
            |
            v
6. AWS Lambda receives request
            |
            v
7. Lambda executes Python code
            |
            v
8. Lambda accesses DynamoDB
            |
            v
9. Lambda generates JSON response
            |
            v
10. Frontend displays result
```

---

# Security

The project follows these security practices:

### S3

- Use CloudFront OAC
- Avoid unnecessary public bucket access
- Use appropriate bucket policies

### Lambda

- Use IAM execution roles
- Follow least-privilege permissions
- Do not hard-code credentials

### DynamoDB

- Give Lambda only the required table permissions
- Avoid unnecessary broad IAM policies

### GitHub

Never upload:

```text
AWS Access Key
AWS Secret Access Key
Passwords
API Keys
Tokens
.env files
Private credentials
```

---

# Troubleshooting

## 1. CloudFront 403 AccessDenied

Check:

```text
CloudFront
    |
    +-- Origin
    |
    +-- OAC
    |
    +-- S3 Bucket Policy
    |
    +-- Object Path
```

Verify:

- Correct S3 origin
- Correct OAC
- Correct bucket policy
- Object exists
- CloudFront deployment completed

---

## 2. Lambda 500 Error

Check:

```text
Lambda
   |
   v
CloudWatch Logs
   |
   v
Error Message
```

Verify:

- Lambda code
- IAM permissions
- Request payload
- Environment variables
- DynamoDB permissions
- DynamoDB data types

---

## 3. DynamoDB Decimal Error

When using DynamoDB with Python, floating-point values can cause errors such as:

```text
Float types are not supported.
Use Decimal types instead.
```

Use Python's `Decimal` when storing numeric values that require DynamoDB-compatible number handling.

Example:

```python
from decimal import Decimal

value = Decimal("10.50")
```

---

# Testing

## S3 Testing

Verify:

```text
✓ Bucket exists
✓ Frontend files uploaded
✓ Correct object names
```

## CloudFront Testing

Verify:

```text
✓ Distribution deployed
✓ CloudFront URL accessible
✓ Frontend loads
✓ S3 origin accessible through OAC
```

## Lambda Testing

Verify:

```text
✓ Function executes
✓ HTTP response returned
✓ JSON response generated
✓ No execution errors
```

## DynamoDB Testing

Verify:

```text
✓ Table exists
✓ Lambda has permission
✓ Data can be read/written
✓ Data types are supported
```

---

# Repository Structure

```text
aws-serverless-monitoring/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── lambda/
│   └── serverless-monitoring-api.py
│
├── architecture/
│   └── aws-serverless-architecture.png
│
├── docs/
│   ├── screenshots/
│   │   ├── 01-s3-service.png
│   │   ├── 02-s3-bucket.png
│   │   ├── 03-s3-settings.png
│   │   ├── 04-s3-objects.png
│   │   ├── 05-cloudfront.png
│   │   ├── 06-cloudfront-origin.png
│   │   ├── 07-oac.png
│   │   ├── 08-cloudfront-status.png
│   │   ├── 09-lambda.png
│   │   ├── 10-lambda-code.png
│   │   └── 11-lambda-test.png
│   │
│   ├── AWS_Serverless_Project_Screenshot_Documentation.pdf
│   └── AWS_Serverless_Project_Full_Documentation_With_Screenshots.docx
│
├── README.md
└── .gitignore
```

---

# Architecture Diagram

Add the generated architecture diagram to:

```text
architecture/aws-serverless-architecture.png
```

Then display it in GitHub using:

```markdown
![AWS Serverless Architecture](architecture/aws-serverless-architecture.png)
```

---

# Screenshots

Add your AWS console screenshots under:

```text
docs/screenshots/
```

Recommended order:

1. S3 service
2. S3 bucket creation
3. S3 security settings
4. S3 uploaded objects
5. CloudFront distribution
6. CloudFront origin
7. Origin Access Control
8. CloudFront distribution status
9. Lambda function
10. Lambda code
11. Lambda test result

---

# Future Improvements

The project can be extended with:

- [ ] Amazon API Gateway
- [ ] CloudWatch Dashboard
- [ ] CloudWatch Alarms
- [ ] Amazon SNS notifications
- [ ] Authentication
- [ ] IAM fine-grained permissions
- [ ] Terraform Infrastructure as Code
- [ ] AWS CloudFormation
- [ ] GitHub Actions CI/CD
- [ ] Automated testing
- [ ] Centralized logging
- [ ] DynamoDB backup
- [ ] Multi-Region Disaster Recovery
- [ ] Route 53 DNS failover

---

# Skills Demonstrated

```text
AWS
├── Amazon S3
├── Amazon CloudFront
├── Origin Access Control
├── AWS Lambda
├── Amazon DynamoDB
├── IAM
└── CloudWatch

Cloud Concepts
├── Serverless Architecture
├── CDN
├── API
├── Cloud Security
├── NoSQL
└── Cloud Troubleshooting
```

---

# Project Documentation

Detailed implementation documentation containing the project screenshots and explanations is available in:

```text
docs/AWS_Serverless_Project_Screenshot_Documentation.pdf
```

and

```text
docs/AWS_Serverless_Project_Full_Documentation_With_Screenshots.docx
```

---

