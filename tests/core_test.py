import contextlib
import io
import os
import shutil
import subprocess
import unittest
from unittest.mock import patch

from simple_slurm_command import SlurmCommand


class Testing(unittest.TestCase):

    script = r'''#!/bin/sh

#SBATCH --array               3-11
#SBATCH --cpus-per-task       15
#SBATCH --dependency          after:65541,afterok:34987
#SBATCH --job-name            name
#SBATCH --output              %A_%a.out
'''

    def test_01_args_short(self):
        slurm = SlurmCommand(
            '-a', '3-11',
            '-c', '15',
            '-J', 'name',
            '-d', 'after:65541,afterok:34987',
            '-o', r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_02_args_long(self):
        slurm = SlurmCommand(
            '--array', '3-11',
            '--cpus_per_task', '15',
            '--job_name', 'name',
            '--dependency', 'after:65541,afterok:34987',
            '--output', r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_03_args_simple(self):
        slurm = SlurmCommand(
            'array', '3-11',
            'cpus_per_task', '15',
            'job_name', 'name',
            'dependency', 'after:65541,afterok:34987',
            'output', r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_04_kwargs(self):
        slurm = SlurmCommand(
            array='3-11',
            cpus_per_task='15',
            job_name='name',
            dependency='after:65541,afterok:34987',
            output=r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_05_add_arguments_single(self):
        slurm = SlurmCommand()
        slurm.add_arguments(
            array='3-11',
            cpus_per_task='15',
            job_name='name',
            dependency='after:65541,afterok:34987',
            output=r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_06_add_arguments_multiple(self):
        slurm = SlurmCommand()
        slurm.add_arguments(array='3-11')
        slurm.add_arguments(cpus_per_task='15')
        slurm.add_arguments(job_name='name')
        slurm.add_arguments(dependency='after:65541,afterok:34987')
        slurm.add_arguments(output=r'%A_%a.out')
        self.assertEqual(self.script, str(slurm))

    def test_07_setter_methods(self):
        slurm = SlurmCommand()
        slurm.set_array('3-11')
        slurm.set_cpus_per_task('15')
        slurm.set_job_name('name')
        slurm.set_dependency('after:65541,afterok:34987')
        slurm.set_output(r'%A_%a.out')
        self.assertEqual(self.script, str(slurm))

    def test_08_parse_range(self):
        slurm = SlurmCommand(
            array=range(3, 12),
            cpus_per_task='15',
            job_name='name',
            dependency='after:65541,afterok:34987',
            output=r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_09_parse_int(self):
        slurm = SlurmCommand(
            array=range(3, 12),
            cpus_per_task=15,
            job_name='name',
            dependency='after:65541,afterok:34987',
            output=r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_10_parse_dict(self):
        slurm = SlurmCommand(
            array=range(3, 12),
            cpus_per_task=15,
            job_name='name',
            dependency=dict(after=65541, afterok=34987),
            output=r'%A_%a.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_11_filename_patterns(self):
        slurm = SlurmCommand(
            array=range(3, 12),
            cpus_per_task=15,
            job_name='name',
            dependency=dict(after=65541, afterok=34987),
            output=f'{SlurmCommand.JOB_ARRAY_MASTER_ID}_{SlurmCommand.JOB_ARRAY_ID}.out',
        )
        self.assertEqual(self.script, str(slurm))

    def test_12_output_env_vars_object(self):
        slurm = SlurmCommand()
        self.assertEqual(slurm.SLURM_ARRAY_TASK_ID, r'$SLURM_ARRAY_TASK_ID')

    def test_13_output_env_vars(self):
        self.assertEqual(SlurmCommand.SLURM_ARRAY_TASK_ID, r'$SLURM_ARRAY_TASK_ID')

    # def test_14_srun_returncode(self):
    #     slurm = SlurmCommand()
    #     if shutil.which('srun') is not None:
    #         code = slurm.srun('echo Hello!')
    #     else:
    #         with patch('subprocess.run', subprocess_srun):
    #             code = slurm.srun('echo Hello!')
    #     self.assertEqual(code, 0)

    # def test_15_sbatch_execution(self):
    #     with io.StringIO() as buffer:
    #         with contextlib.redirect_stdout(buffer):
    #             slurm = SlurmCommand()
    #             if shutil.which('sbatch') is not None:
    #                 job_id = slurm.sbatch('echo Hello!')
    #             else:
    #                 with patch('subprocess.run', subprocess_sbatch):
    #                     job_id = slurm.sbatch('echo Hello!')
    #             stdout = buffer.getvalue()

    #     out_file = f'slurm-{job_id}.out'
    #     while True:  # wait for job to finalize
    #         if os.path.isfile(out_file):
    #             break
    #     with open(out_file, 'r') as fid:
    #         contents = fid.read()
    #     os.remove(out_file)

    #     self.assertIsInstance(job_id, int)
    #     self.assertIn('Hello!', contents)
    #     self.assertIn(f'Submitted batch job {job_id}', stdout)


def subprocess_srun(*args, **kwargs):
    print('Hello!!!')
    return subprocess.CompletedProcess(*args, returncode=0)


def subprocess_sbatch(*args, **kwargs):
    job_id = 1234
    out_file = f'slurm-{job_id}.out'
    with open(out_file, 'w') as fid:
        fid.write('Hello!!!\n')
    stdout = f'Submitted batch job {job_id}'
    return subprocess.CompletedProcess(*args, returncode=1,
                                       stdout=stdout.encode('utf-8'))


if __name__ == '__main__':
    unittest.main()
