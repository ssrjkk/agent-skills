---
name: aws-lambda
description: "Builds and deploys serverless functions with AWS Lambda, API Gateway, and SAM/CDK. Use for event-driven architectures."
category: devops
tags: [aws, lambda, serverless, api-gateway, sam]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# AWS Lambda

> Serverless functions with AWS Lambda, API Gateway, and event triggers.

## Quick Start
```typescript
import { Handler, APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';

export const handler: Handler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
  return {
    statusCode: 200,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: 'Hello from Lambda!',
      path: event.path,
      method: event.httpMethod,
    }),
  };
};
```

```yaml
# template.yaml (SAM)
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: index.handler
      Runtime: nodejs20.x
      Events:
        Api:
          Type: Api
          Properties:
            Path: /hello
            Method: GET
```

## When to Use
- Event-driven serverless APIs
- Background processing (resize images, send emails)
- Not for long-running processes (>15 min)

## Best Practices
- Keep handlers small and idempotent for retries.
- Set memory/timeout to match the workload and cost.
- Use environment variables for config, not secrets in code.
- Use Lambda Powertools for logging, tracing, and metrics.
- Keep cold starts low: minimal deps and a lean runtime.
- Handle errors and dead-letter queues for async invocations.

## Step-by-Step Instructions
1. Install AWS SAM CLI
2. Create SAM template with Lambda functions
3. Write handler code
4. Deploy: `sam deploy --guided`
5. Add observability and alerts

## Dependencies
```bash
# Install AWS SAM CLI
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html
npm install aws-lambda @types/aws-lambda
```

## Examples
Input: GET /hello → Output: `{ "message": "Hello from Lambda!" }`

```typescript
// Idempotent handler with error handling
import { APIGatewayProxyEvent, APIGatewayProxyResult } from "aws-lambda";

export async function handler(event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> {
  try {
    const id = event.pathParameters?.id;
    const data = await getItem(id);
    return { statusCode: 200, body: JSON.stringify(data) };
  } catch (err) {
    console.error(err);
    return { statusCode: 500, body: JSON.stringify({ error: "internal" }) };
  }
}
```
```yaml
# SAM template with env config
Resources:
  ApiFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: index.handler
      Runtime: nodejs20.x
      Environment:
        Variables:
          TABLE_NAME: !Ref ItemsTable
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref ItemsTable
```

## Resources
- [AWS Lambda Docs](https://docs.aws.amazon.com/lambda/)
- [Examples](./examples/)

## Troubleshooting
- **Cold start spikes** — keep dependencies lean, enable provisioned
  concurrency for hot paths, and prefer lighter runtimes (Node/Go).
- **Timeouts at 6s in VPC** — the default Lambda timeout is too low.
  Raise the timeout and check NAT gateway routes to private subnets.
- **Permission denied on SDK calls** — the execution role lacks policy.
  Attach the least-privilege IAM policy and re-test with `--no-sign-request`.
- **`/tmp` fills up** — the 512MB scratch space is shared between invokes.
  Clean it in a finally block or use `/tmp` only for small artifacts.

## Validation
1. Function deploys successfully
2. API Gateway endpoint responds
3. CloudWatch logs show execution
