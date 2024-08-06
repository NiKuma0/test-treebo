import * as cdk from 'aws-cdk-lib';
import * as python from '@aws-cdk/aws-lambda-python-alpha';
import { Construct } from 'constructs';
import { Runtime } from 'aws-cdk-lib/aws-lambda';
import * as sm from 'aws-cdk-lib/aws-secretsmanager';
import * as gateway from 'aws-cdk-lib/aws-apigateway';

export class ApiConstruct extends Construct {
  constructor(scope: Construct, id: string){
    super(scope, id)
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
          BOT_TOKEN: secrets.secretValueFromJson('BOT_TOKEN').toString(),
        },
      }
    )
    const authHandler = new python.PythonFunction( this, "AuthHandler", {
        entry: './src/lambdas',  // Now it will not install deps from requirements.txt
        index: 'auth.py',
        handler: 'handler',
        timeout: cdk.Duration.seconds(20),
        memorySize: 256,
        runtime: Runtime.PYTHON_3_12,
        environment: {
          SECRET_TOKEN: secrets.secretValueFromJson('SECRET_TOKEN').toString(),
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
