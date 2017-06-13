import os
import boto3


def build(*args, **kwargs):
    print('Building:')
    print('Args are:', args)
    print('Kwargs are:', kwargs)
    variables = ['CI', 'CI_BUILD_NUMBER', 'CI_BUILD_URL', 'CI_PULL_REQUEST',
                 'CI_BRANCH', 'CI_COMMIT_ID', 'CI_COMMITTER_NAME',
                 'CI_COMMITTER_EMAIL', 'CI_COMMITTER_USERNAME', 'CI_MESSAGE',
                 'CI_NAME']
#    for variable in variables:
#        print(variable, os.environ[variable])

    public_key = os.environ['AWS_ACCESS_KEY_ID']
    private_key = os.environ['AWS_SECRET_ACCESS_KEY']
    print(public_key)
    print(private_key)
    s3 = boto3.client('s3',
                      aws_access_key_id=public_key,
                      aws_secret_access_key=private_key)
    response = s3.list_buckets()
    print(response)


if __name__ == '__main__':
    build()
