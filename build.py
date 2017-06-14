import os
import boto3
import shutil

from datetime import datetime, timezone


CURRENT_ZIP = 'current.zip'
BRANCH_TO_FOLDER_MAPPING = {
    'master': 'staging',
    'develop': 'dev'
}


def build(*args, **kwargs):
    print('Copying to UI bucket.')
    public_key = os.environ['AWS_ACCESS_KEY_ID']
    private_key = os.environ['AWS_SECRET_ACCESS_KEY']
    bucket = os.environ['AWS_STORAGE_BUCKET_NAME']
    branch = os.environ.get('CI_BRANCH')

    s3 = boto3.client('s3',
                      aws_access_key_id=public_key,
                      aws_secret_access_key=private_key)

    # TODO: handle production push?
    s3_container_folder = BRANCH_TO_FOLDER_MAPPING.get(branch, branch)
    # TODO: get version correctly
    ui_version = '1.2.0'
    # Do we want this human readable - count files, increment result + 1?
    timestamp = int(datetime.now(timezone.utc).timestamp())
    zipped_ui = '{}.{}.{}'.format(ui_version, timestamp, 'zip')
    zipped_ui_key = '{}/{}'.format(s3_container_folder, zipped_ui)

    build_path = 'ui/build'
    builded_ui_zip = shutil.make_archive(zipped_ui, 'zip', build_path)

    with open(builded_ui_zip, 'rb') as data:
        s3.put_object(Body=data,
                      Bucket=bucket,
                      ACL='private',
                      Key=zipped_ui_key)
    os.remove(builded_ui_zip)

    # simulate 'symlink' by copying desired build in `current.zip`
    s3.copy_object(Bucket=bucket,
                   ACL='public-read',
                   CopySource={
                       'Bucket': bucket,
                       'Key': zipped_ui_key
                   },
                   Key='{}/{}'.format(s3_container_folder, CURRENT_ZIP))
    # TODO: handle possible errors?


if __name__ == '__main__':
    build()
