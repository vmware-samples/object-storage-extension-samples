import os
import shutil


class TestEnvMgmt:
    """
    #
    #
    """
    def __init__(self):
        self.src_folder = os.path.join(os.getcwd(), 'framework', 'libs', 's3api', 'models')
        self.dest_folder = os.path.join(os.path.expanduser('~'), '.aws', 'models')

    def env_init(self):
        # copy custom boto model files to ~/.aws/models

        # src_folder = os.path.join(os.getcwd(), 'framework', 'libs', 's3api', 'models')
        # dest_folder = os.path.join(os.path.expanduser('~'), '.aws', 'models')
        shutil.rmtree(self.dest_folder, ignore_errors=True)
        shutil.copytree(self.src_folder, self.dest_folder)

    def env_teardown(self):
        shutil.rmtree(self.dest_folder, ignore_errors=True)


if __name__ == '__main__':
    pass
