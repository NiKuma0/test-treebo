import typing as t
import os

import logging

if t.TYPE_CHECKING:
    from aws_lambda_typing import context, events, responses


logger = logging.getLogger(__name__)
SECRET_TOKEN: t.Final[str] = os.getenv('SECRET_TOKEN', '')


def handler(event: 'events.APIGatewayTokenAuthorizerEvent', context: 'context.Context') -> 'responses.api_gateway_authorizer.APIGatewayAuthorizerResponse':
    logger.info(event)
    return gen_policy(
        'User', event.get('authorizationToken') == SECRET_TOKEN, resource=event['methodArn'],
    )


def gen_policy(principal_id: str, allow: bool, resource: str) -> 'responses.api_gateway_authorizer.APIGatewayAuthorizerResponse':
    return {
        'principalId': principal_id,
        'policyDocument': {
            'Version': '2012-10-17',
            'Statement': {
                'Action': 'execute-api:Invoke',
                'Effect': "Allow" if allow else "Deny",
                'Resource': resource
            }
        }
    }
