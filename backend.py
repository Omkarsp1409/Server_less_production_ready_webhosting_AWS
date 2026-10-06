import json
from datetime import datetime, timezone


def lambda_handler(event, context):

    response = {
        "status": "success",
        "service": "serverless-monitoring-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),

        "infrastructure": {
            "ec2": {
                "status": "healthy",
                "message": "EC2 monitoring service is running"
            },

            "s3": {
                "status": "healthy",
                "message": "S3 monitoring service is running"
            },

            "rds": {
                "status": "healthy",
                "message": "RDS monitoring service is running"
            },

            "lambda": {
                "status": "healthy",
                "message": "Lambda function is running"
            }
        }
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(response)
    }
