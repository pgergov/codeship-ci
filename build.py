import os


def build(*args, **kwargs):
    print('Building:')
    print('Args are:', args)
    print('Kwargs are:', kwargs)
    variables = ['CI', 'CI_BUILD_NUMBER', 'CI_BUILD_URL', 'CI_PULL_REQUEST',
                 'CI_BRANCH', 'CI_COMMIT_ID', 'CI_COMMITTER_NAME',
                 'CI_COMMITTER_EMAIL', 'CI_COMMITTER_USERNAME', 'CI_MESSAGE',
                 'CI_NAME']
    for variable in variables:
        print(variable, os.environ[variable])


if __name__ == '__main__':
    build()
