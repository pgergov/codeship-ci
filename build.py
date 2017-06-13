import os
import boto3
import shutil


BRANCH_TO_FOLDER_MAPPING = {
    'master': 'staging',
    'develop': 'dev'
}


def build(*args, **kwargs):
    print('Building:')
    print('Args are: ', args)
    print('Kwargs are: ', kwargs)
    variables = ['CI', 'CI_BUILD_NUMBER', 'CI_BUILD_URL', 'CI_PULL_REQUEST',
                 'CI_BRANCH', 'CI_COMMIT_ID', 'CI_COMMITTER_NAME',
                 'CI_COMMITTER_EMAIL', 'CI_COMMITTER_USERNAME', 'CI_MESSAGE',
                 'CI_NAME']
#    for variable in variables:
#        print(variable, os.environ[variable])

    public_key = os.environ['AWS_ACCESS_KEY_ID']
    private_key = os.environ['AWS_SECRET_ACCESS_KEY']
    bucket = os.environ['AWS_STORAGE_BUCKET_NAME']

    s3 = boto3.client('s3',
                      aws_access_key_id=public_key,
                      aws_secret_access_key=private_key)
    print('Buckets response: ', s3.list_buckets())

    # handle production manually
    branch = os.environ.get('CI_BRANCH')
    s3_container_folder = BRANCH_TO_FOLDER_MAPPING.get(branch, branch)
    s3_build_folder = '1.2.0'

    build_path = 'ui/build'
    build_zip = shutil.make_archive(s3_build_folder, 'zip', build_path)

    with open(build_zip, 'rb') as zip_data:
        # make the file private
        s3.upload_fileobj(zip_data,
                          bucket,
                          "{}/{}".format(s3_container_folder, s3_build_folder))
    os.remove(build_zip)


if __name__ == '__main__':
    build()
