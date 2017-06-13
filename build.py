import os
import boto3
import shutil


BRANCH_TO_FOLDER_MAPPING = {
    'master': 'staging',
    'develop': 'dev'
}


def build(*args, **kwargs):
    print('Building:')

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
    # get ui version from?
    # count files in folder. Generate the last (build) numb correctly.
    s3_build_folder = '1.2.0'

    build_path = 'ui/build'
    build_zip = shutil.make_archive(s3_build_folder, 'zip', build_path)

    with open(build_zip, 'rb') as zip_data:
        # make the file private
        s3.upload_fileobj(zip_data,
                          bucket,
                          "{}/{}".format(s3_container_folder, s3_build_folder))
    os.remove(build_zip)
    # Make current simpling to last build


if __name__ == '__main__':
    build()
