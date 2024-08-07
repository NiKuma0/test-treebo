import { Construct } from 'constructs';
import * as python from '@aws-cdk/aws-lambda-python-alpha';
import * as cdk from 'aws-cdk-lib';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import { ParamsAndSecretsOptions } from 'aws-cdk-lib/aws-lambda/lib/params-and-secrets-layers';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as sm from 'aws-cdk-lib/aws-secretsmanager';
import * as gateway from 'aws-cdk-lib/aws-apigateway';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as iam from 'aws-cdk-lib/aws-iam';


export class ApiConstruct extends Construct {
  constructor(scope: Construct, id: string){
    super(scope, id)
    // Create a VPC
    const vpc = new ec2.Vpc(this, 'MyVpc', {
      maxAzs: 2,
    });

    // Create a security group for the Lambda function
    const lambdaSecurityGroup = new ec2.SecurityGroup(this, 'LambdaSecurityGroup', {
      vpc,
      allowAllOutbound: true,
    });

    const rdsInstance = rds.DatabaseInstance.fromDatabaseInstanceAttributes(this, 'PosgresqlDatabase', {
      instanceEndpointAddress: 'database-1.cjuge2okwrw2.eu-north-1.rds.amazonaws.com',
      port: 5432,
      instanceIdentifier: 'database-1',
      instanceResourceId: 'db-G2QMTJQVR23WS4GBLOF4G7F5UA',
      securityGroups: [ lambdaSecurityGroup, ]
    })

    const secrets = sm.Secret.fromSecretNameV2(this, 'Secrets', 'prod/NoteBot');
  
    const webhook = new python.PythonFunction( this, "TgWebhook", {
        entry: './src',
        index: 'lambdas/webhook.py',
        handler: 'handler',
        timeout: cdk.Duration.seconds(20),
        memorySize: 256,
        runtime: Runtime.PYTHON_3_12,
        environment: {
          DEBUG: 'false',
          BOT_TOKEN: secrets.secretValueFromJson('BOT_TOKEN').unsafeUnwrap(),
          DB_DSN: `aiopg+postgres://${rdsInstance.dbInstanceEndpointAddress}:${rdsInstance.dbInstanceEndpointPort}`,
        },
      }
    )
    rdsInstance.grantConnect(webhook, 'postgres');
    webhook.addToRolePolicy(new iam.PolicyStatement({
      actions: ['rds-db:connect'],
      resources: [rdsInstance.instanceArn],
    }));
    const authHandler = new python.PythonFunction( this, "AuthHandler", {
        entry: './src/lambdas',  // Now it will *not* install deps from ./src/requirements.txt
        index: 'auth.py',
        handler: 'handler',
        timeout: cdk.Duration.seconds(20),
        memorySize: 256,
        runtime: Runtime.PYTHON_3_12,
        environment: {
          SECRET_TOKEN: secrets.secretValueFromJson('SECRET_TOKEN').unsafeUnwrap(),
        },
      }
    )
    const authorizer = new gateway.TokenAuthorizer(this, 'TgToken', {
      handler: authHandler,
      identitySource: 'method.request.header.X-Telegram-Bot-Api-Secret-Token',
    });
    const api = new gateway.LambdaRestApi(this, 'Api', {
      handler: webhook,
      proxy: false,
      defaultMethodOptions: {authorizer: authorizer, authorizationType: gateway.AuthorizationType.CUSTOM}
    });
    api.root.addMethod('POST');
  }
}
