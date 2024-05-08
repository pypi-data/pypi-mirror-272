import os

import boto3

from burlap import Satchel
from burlap.constants import *
from burlap.decorators import task


class EC2MonitorSatchel(Satchel):
    """
    Wraps the EC2 monitor script provided by Amazon:

        http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/mon-scripts.html

    Note, the script has package dependencies described at:

        http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mon-scripts.html#mon-scripts-perl_prereq
    """

    name = 'ec2monitor'

    @property
    def packager_system_packages(self):
        return {
            UBUNTU: ['unzip', 'libwww-perl', 'libdatetime-perl'],
        }

    def set_defaults(self):
        self.env.installed = True
        self.env.cron_path = ''
        self.env.install_path = '/home/{user}/aws-scripts-mon'
        self.env.awscreds = 'roles/{role}/aws-{role}.creds'
        self.env.awscreds_install_path = '{install_path}/aws-{role}.creds'
        self.env.options = [
            '--mem-util',
            '--disk-path=/',
            '--disk-space-util',
            '--swap-util',
            # --verify --verbose
        ]
        self.env.access_key_id = None
        self.env.secret_access_key = None
        # Run every 5 minutes by default.
        # Increase to every minute ('* * * * *') if Detailed Monitoring is enabled on the EC2 instance(s).
        self.env.schedule = '*/5 * * * *'

        self.define_cron_job(
            template='etc_crond_ec2monitor',
            script_path='/etc/cron.d/ec2monitor',
            name='default',
        )

    def _get_renderer(self, verify=False):
        r = self.local_renderer

        r.env.install_path = r.env.install_path.format(**{'user': self.genv.user})

        kwargs = {
            'role': self.genv.ROLE,
            'install_path': r.env.install_path,
        }
        r.env.awscreds = r.env.awscreds.format(**kwargs)
        r.env.awscreds_install_path = r.env.awscreds_install_path.format(**kwargs)

        options = self.env.options
        if verify:
            options.extend(['--verify --verbose'])

        r.env.command_options = ' '.join(options)
        return r

    def _get_check_command(self):
        return (
            'cd {install_path} '
            '&& export AWS_CREDENTIAL_FILE={awscreds_install_path} '
            '&& ./mon-put-instance-data.pl {command_options} '
        )

    @task
    def clear_host_data_cache(self):
        """
        Remove cached instance attribute data that may cause instance_id conflicts when an EBS volume is cloned.
        """
        r = self.local_renderer
        host_data_cache_path = '/var/tmp/aws-mon/'  # Set in CloudWatchClient::$meta_data_loc
        self.vprint(f'Removing temporary host data cache at {host_data_cache_path}.')
        r.sudo(f'rm -rf {host_data_cache_path}')

    @task
    def verify(self):
        r = self._get_renderer(verify=True)
        r.run(self._get_check_command())

    @task
    def check(self):
        r = self._get_renderer(verify=False)
        r.run(self._get_check_command())

    @task
    def install(self):
        r = self._get_renderer()

        local_path = self.env.awscreds.format(role=self.genv.ROLE)
        assert os.path.isfile(local_path), 'Missing cred file: %s' % local_path

        r.install_packages()
        r.run('cd ~; curl http://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.1.zip -O')
        r.run('cd ~; unzip -o CloudWatchMonitoringScripts-1.2.1.zip')
        r.run('cd ~; rm CloudWatchMonitoringScripts-1.2.1.zip')
        r.put(local_path=local_path, remote_path=r.env.awscreds_install_path)

        self.clear_host_data_cache()
        self.install_cron_job(
            name='default',
            extra={'command': self._get_check_command().format(**r.env), 'schedule': self.env.schedule}
        )

    @task
    def uninstall(self):
        self.vprint('EC2MonitorSatchel.uninstall is not yet supported.')

    @task(precursors=['packager', 'user'])
    def configure(self):
        """
        Executed when your settings have changed since the last deployment.
        Run commands to apply changes here.
        """
        self.install()


ec2monitor = EC2MonitorSatchel()


class RDSSatchel(Satchel):

    name = 'rds'

    def set_defaults(self):
        pass

    @task
    def list_instances(self):
        rds = boto3.client(
            'rds',
            aws_access_key_id=self.genv.vm_ec2_aws_access_key_id,
            aws_secret_access_key=self.genv.vm_ec2_aws_secret_access_key,
            region_name=self.genv.vm_ec2_region
        )
        for instance in rds.describe_db_instances()['DBInstances']:
            print(instance['DBInstanceIdentifier'], instance['Engine'], instance['EngineVersion'])

    @task(precursors=['packager', 'user'])
    def configure(self):
        pass


rds = RDSSatchel()
