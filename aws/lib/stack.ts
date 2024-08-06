import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

import { ApiConstruct } from './api';

export class AppStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    new ApiConstruct(this, "ApiConstruct");
  }
}
