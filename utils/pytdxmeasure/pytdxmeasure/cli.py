"""
Dump command line
"""

from abc import abstractmethod
import logging
import logging.config
from .actor import VerifyActor, TDEventLogActor
from .tdreport import TdReport

from .tdel import TDEL

__author__ = "cpio"

LOG = logging.getLogger(__name__)


class TDXMeasurementCmdBase:
    """
    Base class for TDX measurements commands.
    """

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(message)s')

    @abstractmethod
    def run(self):
        """
        Interface to be impelemented by child classes
        """
        raise NotImplementedError


class TDXEventLogsCmd(TDXMeasurementCmdBase):
    """
    Cmd executor for dump TDX event logs.
    """

    def run(self):  # pylint: disable=no-self-use
        """
        Run cmd
        """

        LOG.info("=> Read TDEL ACPI Table")
        tdelobj = TDEL.create_from_acpi_file()
        if tdelobj is None:
            return
        tdelobj.dump()

        actor = TDEventLogActor(tdelobj.log_area_start_address,
            tdelobj.log_area_minimum_length)

        LOG.info("")
        LOG.info("=> Read Event Log Data - Address: 0x%X(0x%X)",
                 tdelobj.log_area_start_address,
                 tdelobj.log_area_minimum_length)
        actor.dump_td_event_logs()

        LOG.info("")
        LOG.info("=> Replay Rolling Hash - RTMR")
        actor.dump_rtmrs()


class TDXVerifyCmd(TDXMeasurementCmdBase):
    """
    Cmd executor for verify RTMR
    """

    def run(self):  # pylint: disable=no-self-use
        """
        Run cmd
        """
        LOG.info("=> Verify RTMR")
        VerifyActor().verify_rtmr()


class TDXTDReportCmd(TDXMeasurementCmdBase):
    """
    Cmd executor to dump TD report.
    """

    def run(self):  # pylint: disable=no-self-use
        """
        Run cmd
        """

        LOG.info("=> Dump TD Report")
        TdReport.get_td_report().dump()
