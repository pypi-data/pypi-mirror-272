from __future__ import annotations

import asyncio.subprocess
import base64
import json
import logging
import os
import re
import shlex
from typing import Any, MutableMapping, MutableSequence, cast

from importlib_resources import files
from streamflow.core import utils
from streamflow.core.deployment import ExecutionLocation
from streamflow.core.exception import WorkflowExecutionException
from streamflow.core.utils import get_option
from streamflow.deployment.connector.queue_manager import (
    QueueManagerConnector,
    QueueManagerService,
)
from streamflow.log_handler import logger


def get_lsf_option(
    name: str,
    value: Any,
):
    option = get_option(name, value)
    return option[1:] if len(name) > 1 else option


def _get_result(job_id, stdout, field_names):
    if ((json_start := stdout.find("{")) != -1) and (
        (json_end := stdout.rfind("}")) != -1
    ):
        try:
            output = json.loads(stdout[json_start : (json_end + 1)])
            if len(output["RECORDS"]) != 1:
                raise WorkflowExecutionException(
                    f"Error while retrieving job {job_id} record: {stdout.strip()}"
                )
            return [output["RECORDS"][0][field_name] for field_name in field_names]
        except json.decoder.JSONDecodeError:
            raise WorkflowExecutionException(
                f"Error while decoding JSON output for job {job_id}: {stdout.strip()}"
            )
    else:
        raise WorkflowExecutionException(
            f"Error while retrieving job {job_id} record: {stdout.strip()}"
        )


class LSFService(QueueManagerService):
    def __init__(
        self,
        file: str | None = None,
        applicationProfile: str | None = None,
        autoResizable: bool | None = None,
        checkpoint: str | None = None,
        clusters: str | None = None,
        coreLimit: int | None = None,
        cpuTimeLimit: str | None = None,
        data: str | None = None,
        dataLimit: int | None = None,
        datagrp: str | None = None,
        dynamicInputFile: str | None = None,
        eligiblePendingTimeLimit: str | None = None,
        enableSpool: bool | None = None,
        env: str | None = None,
        errorFileAppend: str | None = None,
        errorFileOverwrite: str | None = None,
        estimatedRunningTime: int | None = None,
        exclusive: bool | None = None,
        externalSchedulerOptions: str | None = None,
        fileSizeLimit: int | None = None,
        freq: int | None = None,
        hostfile: str | None = None,
        inputFile: str | None = None,
        jobDescription: str | None = None,
        jobGroup: str | None = None,
        jobName: str | None = None,
        jsdlFile: str | None = None,
        jsdlStrict: str | None = None,
        licenseProject: str | None = None,
        localFile: str | None = None,
        locationRequired: str | None = None,
        mailUser: str | None = None,
        memAndSwapLimit: bool | None = None,
        memoryLimit: int | None = None,
        migrationThreshold: int | None = None,
        noRerunnable: bool | None = None,
        numOfTasks: str | None = None,
        pendingTimeLimit: str | None = None,
        postExecCommand: str | None = None,
        preExecCommand: str | None = None,
        priority: int | None = None,
        processLimit: str | None = None,
        projectName: str | None = None,
        queueName: str | None = None,
        requeueExitValue: str | None = None,
        rerunOnHostFailure: bool | None = None,
        reservation: str | None = None,
        resizeNotificationCmd: str | None = None,
        resourceRequirements: str | None = None,
        runLimit: int | None = None,
        sendMail: bool | None = None,
        serviceClassName: str | None = None,
        signal: str | None = None,
        stackSizeLimit: int | None = None,
        startTime: str | None = None,
        terminationDeadline: str | None = None,
        threadLimit: int | None = None,
        userGroup: str | None = None,
        virtualMemLimit: int | None = None,
        warningAction: str | None = None,
        warningTimeAction: str | None = None,
    ):
        super().__init__(file)
        self.application_profile: str | None = applicationProfile
        self.auto_resizable: bool | None = autoResizable
        self.checkpoint: str | None = checkpoint
        self.clusters: str | None = clusters
        self.core_limit: int | None = coreLimit
        self.cpu_time_limit: str | None = cpuTimeLimit
        self.data: str | None = data
        self.data_limit: int | None = dataLimit
        self.datagrp: str | None = datagrp
        self.dynamic_input_file: str | None = dynamicInputFile
        self.eligible_pending_time_limit: str | None = eligiblePendingTimeLimit
        self.enable_spool: bool | None = enableSpool
        self.env: str | None = env
        self.error_file_append: str | None = errorFileAppend
        self.error_file_overwrite: str | None = errorFileOverwrite
        self.estimated_running_time: int | None = estimatedRunningTime
        self.exclusive: bool | None = exclusive
        self.external_scheduler_options: str | None = externalSchedulerOptions
        self.file_size_limit: int | None = fileSizeLimit
        self.freq: int | None = freq
        self.hostfile: str | None = hostfile
        self.location_required: str | None = locationRequired
        self.input_file: str | None = inputFile
        self.job_description: str | None = jobDescription
        self.job_group: str | None = jobGroup
        self.job_name: str | None = jobName
        self.jsdl_file: str | None = jsdlFile
        self.jsdl_strict: str | None = jsdlStrict
        self.license_project: str | None = licenseProject
        self.local_file: str | None = localFile
        self.mail_user: str | None = mailUser
        self.mem_and_swap_imit: bool | None = memAndSwapLimit
        self.memory_limit: int | None = memoryLimit
        self.migration_threshold: int | None = migrationThreshold
        self.no_rerunnable: str | None = noRerunnable
        self.num_of_tasks: str | None = numOfTasks
        self.pending_time_limit: str | None = pendingTimeLimit
        self.post_exec_command: str | None = postExecCommand
        self.pre_exec_command: str | None = preExecCommand
        self.priority: int | None = priority
        self.process_limit: int | None = processLimit
        self.project_name: str | None = projectName
        self.queue_name: str | None = queueName
        self.requeue_exit_value: str | None = requeueExitValue
        self.rerun_on_host_failure: bool | None = rerunOnHostFailure
        self.reservation: str | None = reservation
        self.resize_notification_cmd: str | None = resizeNotificationCmd
        self.resource_requirements: str | None = resourceRequirements
        self.run_limit: int | None = runLimit
        self.send_mail: bool | None = sendMail
        self.service_class_name: str | None = serviceClassName
        self.signal: str | None = signal
        self.stack_size_limit: int | None = stackSizeLimit
        self.start_time: str | None = startTime
        self.termination_deadline: str | None = terminationDeadline
        self.thread_limit: int | None = threadLimit
        self.user_group: str | None = userGroup
        self.virtual_mem_limit: int | None = virtualMemLimit
        self.warning_action: str | None = warningAction
        self.warning_time_action: str | None = warningTimeAction


class LSFConnector(QueueManagerConnector):
    async def _get_output(self, job_id: str, location: ExecutionLocation) -> str:
        command = ["bjobs", "-a", "-json", "-o", "'EXEC_CWD OUTPUT_FILE'", job_id]
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Running command `{' '.join(command)}`")
        stdout, _ = await self.connector.run(
            location=location, command=command, capture_output=True
        )
        results = _get_result(job_id, stdout, ["EXEC_CWD", "OUTPUT_FILE"])
        if output_path := str(os.path.join(*results)):
            stdout, _ = await super().run(
                location=location, command=["cat", output_path], capture_output=True
            )
            return stdout.strip()
        else:
            return ""

    async def _get_returncode(self, job_id: str, location: ExecutionLocation) -> int:
        command = ["bjobs", "-a", "-json", "-o", "EXIT_CODE", job_id]
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Running command `{' '.join(command)}`")
        stdout, _ = await super().run(
            location=location,
            command=command,
            capture_output=True,
        )
        result = _get_result(job_id, stdout, ["EXIT_CODE"])[0]
        try:
            return int(result) if result else 0
        except ValueError:
            raise WorkflowExecutionException(
                f"Error while retrieving return code for job {job_id}: {result}"
            )

    async def _get_running_jobs(
        self, location: ExecutionLocation
    ) -> MutableSequence[str]:
        # bjobs -noheader -o jobid [JOBIDS] # missing a state filter parameter
        command = [
            "bjobs",
            "-a",
            "-json",
            "-o",
            "'JOBID STAT'",
            " ".join(self._scheduled_jobs.keys()),
        ]
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Running command `{' '.join(command)}`")
        stdout, _ = await super().run(
            location=location,
            command=command,
            capture_output=True,
        )
        if ((json_start := stdout.find("{")) != -1) and (
            (json_end := stdout.rfind("}")) != -1
        ):
            try:
                stdout = json.loads(stdout[json_start : (json_end + 1)])
            except json.decoder.JSONDecodeError:
                raise WorkflowExecutionException(
                    f"Error parsing running jobs: {stdout.strip()}"
                )
            return [
                record["JOBID"]
                for record in stdout["RECORDS"]
                if record["STAT"] in ("PEND", "RUN")
            ]
        else:
            raise WorkflowExecutionException(
                f"Error retrieving running jobs: {stdout.strip()}"
            )

    @property
    def _service_class(self) -> type[QueueManagerService]:
        return LSFService

    async def _remove_jobs(
        self, location: ExecutionLocation, jobs: MutableSequence[str]
    ) -> None:
        await super().run(
            location=location,
            command=["bkill", " ".join(jobs)],
        )

    async def _run_batch_command(
        self,
        command: str,
        environment: MutableMapping[str, str] | None,
        job_name: str,
        location: ExecutionLocation,
        workdir: str | None = None,
        stdin: int | str | None = None,
        stdout: int | str = asyncio.subprocess.STDOUT,
        stderr: int | str = asyncio.subprocess.STDOUT,
        timeout: int | None = None,
    ) -> str:
        batch_command = [
            "echo",
            base64.b64encode(command.encode("utf-8")).decode("utf-8"),
            "|",
            "base64",
            "-d",
            "|",
        ]
        if environment:
            batch_command.extend([f"{k}={v}" for k, v in environment.items()])
        batch_command.append("bsub")
        if stdin is not None and stdin != asyncio.subprocess.DEVNULL:
            batch_command.append(get_lsf_option("i", shlex.quote(stdin)))
        if stderr != asyncio.subprocess.STDOUT and stderr != stdout:
            batch_command.append(get_lsf_option("e", self._format_stream(stderr)))
        if stdout != asyncio.subprocess.STDOUT:
            batch_command.append(get_lsf_option("o", self._format_stream(stdout)))
        if timeout:
            batch_command.append(
                get_lsf_option("W", utils.format_seconds_to_hhmmss(timeout))
            )
        if service := cast(LSFService, self.services.get(location.service)):
            batch_command.append(get_lsf_option("app", service.application_profile))
            batch_command.append(get_lsf_option("ar", service.auto_resizable))
            batch_command.append(get_lsf_option("k", service.checkpoint))
            batch_command.append(get_lsf_option("clusters", service.clusters))
            batch_command.append(get_lsf_option("C", service.core_limit))
            batch_command.append(get_lsf_option("c", service.cpu_time_limit))
            batch_command.append(get_lsf_option("data", service.data))
            batch_command.append(get_lsf_option("D", service.data_limit))
            batch_command.append(get_lsf_option("datagrp", service.datagrp))
            batch_command.append(get_lsf_option("is", service.dynamic_input_file))
            batch_command.append(
                get_lsf_option("eptl", service.eligible_pending_time_limit)
            )
            batch_command.append(get_lsf_option("Zs", service.enable_spool))
            batch_command.append(get_lsf_option("env", service.env))
            batch_command.append(get_lsf_option("e", service.error_file_append))
            batch_command.append(get_lsf_option("eo", service.error_file_overwrite))
            batch_command.append(get_lsf_option("We", service.estimated_running_time))
            batch_command.append(get_lsf_option("x", service.exclusive))
            batch_command.append(
                get_lsf_option("ext", service.external_scheduler_options)
            )
            batch_command.append(get_lsf_option("F", service.file_size_limit))
            batch_command.append(get_lsf_option("freq", service.freq))
            batch_command.append(get_lsf_option("hostfile", service.hostfile))
            batch_command.append(get_lsf_option("m", service.location_required))
            batch_command.append(get_lsf_option("i", service.input_file))
            batch_command.append(get_lsf_option("Jd", service.job_description))
            batch_command.append(get_lsf_option("g", service.job_group))
            batch_command.append(get_lsf_option("J", service.job_name))
            batch_command.append(get_lsf_option("jsdl", service.jsdl_file))
            batch_command.append(get_lsf_option("jsdl_strict", service.jsdl_strict))
            batch_command.append(get_lsf_option("Lp", service.license_project))
            batch_command.append(get_lsf_option("f", service.local_file))
            batch_command.append(get_lsf_option("u", service.mail_user))
            batch_command.append(get_lsf_option("hl", service.mem_and_swap_imit))
            batch_command.append(get_lsf_option("M", service.memory_limit))
            batch_command.append(get_lsf_option("mig", service.migration_threshold))
            batch_command.append(get_lsf_option("rn", service.no_rerunnable))
            batch_command.append(get_lsf_option("n", service.num_of_tasks))
            batch_command.append(get_lsf_option("ptl", service.pending_time_limit))
            batch_command.append(get_lsf_option("Ep", service.post_exec_command))
            batch_command.append(get_lsf_option("E", service.pre_exec_command))
            batch_command.append(get_lsf_option("sp", service.priority))
            batch_command.append(get_lsf_option("p", service.process_limit))
            batch_command.append(get_lsf_option("P", service.project_name))
            batch_command.append(get_lsf_option("q", service.queue_name))
            batch_command.append(get_lsf_option("Q", service.requeue_exit_value))
            batch_command.append(get_lsf_option("r", service.rerun_on_host_failure))
            batch_command.append(get_lsf_option("U", service.reservation))
            batch_command.append(get_lsf_option("rnc", service.resize_notification_cmd))
            batch_command.append(get_lsf_option("R", service.resource_requirements))
            batch_command.append(get_lsf_option("B", service.send_mail))
            batch_command.append(get_lsf_option("sla", service.service_class_name))
            batch_command.append(get_lsf_option("s", service.signal))
            batch_command.append(get_lsf_option("S", service.stack_size_limit))
            batch_command.append(get_lsf_option("b", service.start_time))
            batch_command.append(get_lsf_option("t", service.termination_deadline))
            batch_command.append(get_lsf_option("T", service.thread_limit))
            batch_command.append(get_lsf_option("G", service.user_group))
            batch_command.append(get_lsf_option("v", service.virtual_mem_limit))
            batch_command.append(get_lsf_option("wa", service.warning_action))
            batch_command.append(get_lsf_option("wt", service.warning_time_action))
            if not timeout:
                batch_command.append(get_lsf_option("W", service.run_limit))
        batch_command.extend(
            [
                get_lsf_option("cwd", workdir),
                get_lsf_option("outdir", workdir),
                get_lsf_option("N", True),
            ]
        )
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Running command {' '.join(batch_command)}")
        stdout, returncode = await super().run(
            location=location, command=batch_command, capture_output=True
        )
        if returncode == 0:
            return re.search("Job <(.*)> is submitted", stdout.strip())[1]
        else:
            raise WorkflowExecutionException(
                f"Error submitting job {job_name} to LSF: {stdout.strip()}"
            )

    @classmethod
    def get_schema(cls) -> str:
        return (
            files(__package__)
            .joinpath("schemas")
            .joinpath("lsf.json")
            .read_text("utf-8")
        )
