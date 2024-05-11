"""
Confidential VM class manages following items:

1. Confidential device node like /dev/tdx-guest or /dev/sev-guest
2. Event log table from memory
3. IMR (integrated measurement register)

"""
import base64
import hashlib
import os
import logging
import struct
import fcntl
import socket
import tempfile
from abc import abstractmethod
from cctrusted_base.api import CCTrustedApi
from cctrusted_base.imr import TcgIMR
from cctrusted_base.ccreport import CcReport
from cctrusted_base.tcg import TcgAlgorithmRegistry
from cctrusted_base.tdx.common import TDX_VERSION_1_0, TDX_VERSION_1_5
from cctrusted_base.tdx.rtmr import TdxRTMR
from cctrusted_base.tdx.quote import TdxQuoteReq10, TdxQuoteReq15, TdxQuote, TdxQuoteReq
from cctrusted_base.tdx.report import TdxReportReq10, TdxReportReq15

LOG = logging.getLogger(__name__)

class ConfidentialVM:

    _inst = None
    # Configfs-tsm directory prefix
    tsm_prefix = "/sys/kernel/config/tsm/report"

    def __init__(self, cctype):
        self._cc_type:int = cctype
        self._is_init:bool = False
        self._imrs:dict[int, TcgIMR] = {}
        self._boot_time_event_log:bytes = None
        self._runtime_event_log = None

    @property
    def cc_type(self) -> int:
        """CC type like TYPE_CC_TDX, TYPE_CC_SEV etc."""
        return self._cc_type

    @property
    @abstractmethod
    def default_algo_id(self):
        """Default algorithms ID supported by this Confidential VM."""
        raise NotImplementedError("Should be implemented by inherited class")

    @property
    @abstractmethod
    def version(self):
        """Version of CC VM."""
        raise NotImplementedError("Should be implemented by inherited class")

    @property
    def imrs(self) -> list[TcgIMR]:
        """The array of integrated measurement registers (IMR)."""
        return self._imrs

    @property
    def cc_type_str(self):
        """the CC type string."""
        return CCTrustedApi.cc_type_str[self.cc_type]

    @property
    def boot_time_event_log(self):
        """boot time event log data blob."""
        return self._boot_time_event_log

    @property
    def runtime_event_log(self):
        """runtime event log data blob"""
        return self._runtime_event_log

    def init(self) -> bool:
        """Initialize the CC stub and environment.

        Returns:
            Success or not
        """
        if self._is_init:
            return True

        if not self.process_cc_report():
            return False

        if not self.process_eventlog():
            return False

        self._is_init = True
        return True

    @staticmethod
    def detect_cc_type():
        """Detect the type of current confidential VM"""
        # TODO: refine the justification
        for devpath in TdxVM.DEVICE_NODE_PATH.values():
            if os.path.exists(devpath):
                return CCTrustedApi.TYPE_CC_TDX
        return CCTrustedApi.TYPE_CC_NONE

    @abstractmethod
    def process_cc_report(self, report_data=None) -> bool:
        """Process the confidential computing REPORT.

        Returns:
            Success or not.
        """
        raise NotImplementedError("Should be implemented by inherited class")

    @abstractmethod
    def process_eventlog(self) -> bool:
        """Process the event log.

        Returns:
            Success or not.
        """
        raise NotImplementedError("Should be implemented by inherited class")

    @abstractmethod
    # pylint: disable-next=R0911
    def get_cc_report(self, nonce: bytearray, data: bytearray, extraArgs) -> CcReport:
        """Get the CcReport (i.e. quote) for given nonce and data.

        The CcReport is signing of attestation data (IMR values or hashes of IMR
        values), made by a trusted foundation (TPM) using a key trusted by the
        verifier.

        Different trusted foundation may use different quote format.

        Args:
            nonce (bytearray): against replay attacks.
            data (bytearray): user data
            extraArgs: for TPM, it will be given list of IMR/PCRs
                       for configfs-tsm, it will be privilege level

        Returns:
            The ``CcReport`` object.
        """
        if not os.path.exists(self.tsm_prefix):
            return None

        # Process input data
        input_data = None
        privilege = None

        LOG.info("Calculate report data by nonce and user data")
        hash_algo = hashlib.sha512()
        if nonce is not None:
            hash_algo.update(bytes(nonce))
        if data is not None:
            hash_algo.update(bytes(data))
        input_data = hash_algo.digest()
        if extraArgs is not None and isinstance(extraArgs, dict) and \
            "privilege" in extraArgs.keys():
            privilege = extraArgs["privilege"]

        td_report = None
        provider = None
        generation = None
        aux_blob = None
        # Create a temporary directory to request TEE attestation report
        with tempfile.TemporaryDirectory(prefix="report_", dir=self.tsm_prefix) as tempdir:
            LOG.info("Creating tempdir %s to request cc report", tempdir)
            # Check if configfs-tsm interface has been generated
            if not os.path.exists(os.path.join(tempdir, "inblob")):
                LOG.debug("Inblob file not found under directory %s.", tempdir)
                os.rmdir(tempdir)
                return None

            if privilege is not None and isinstance(privilege, int):
                with open(os.path.join(tempdir, "privlevel"), 'w', encoding='utf-8') \
                    as privilege_file:
                    privilege_file.write(privilege)

            # Insert input data
            with open(os.path.join(tempdir, "inblob"), 'wb') as inblob_file:
                inblob_file.write(input_data)

            # Read the output of report and prevent case of resource busy
            try:
                with open(os.path.join(tempdir, "outblob"), 'rb') as outblob_file:
                    td_report = outblob_file.read()
            except OSError:
                LOG.error("Read outblob failed with OSError")
                return None
            except:
                LOG.error("Error in opening outblob file.")
                return None

            # Read provider info
            with open(os.path.join(tempdir, "provider"), 'r', encoding='utf-8') as provider_file:
                provider = provider_file.read()

            # Read generation info
            with open(os.path.join(tempdir, "generation"), 'r', encoding='utf-8') \
                as generation_file:
                generation = generation_file.read()
            # Check if the outblob has been corrupted during file open
            if int(generation) > 1:
                LOG.error("Found corrupted generation. Skipping attestation report fetching...")
                return None

            if os.path.exists(os.path.join(tempdir, "auxblob")):
                with open(os.path.join(tempdir, "auxblob"), 'rb') as auxblob_file:
                    aux_blob = auxblob_file.read()

            os.rmdir(tempdir)

        if td_report is not None:
            LOG.info("Fetched cc report using Configfs TSM with type %s", provider)
            # pylint: disable-next=E1121
            return CcReport(td_report, self._cc_type, aux_blob, generation, provider)

        return None

    def dump(self):
        """Dump confidential VM information."""
        LOG.info("======================================")
        LOG.info("CVM type = %s", self.cc_type_str)
        LOG.info("CVM version = %s", self.version)
        LOG.info("======================================")

    @staticmethod
    def inst():
        """Singleton interface for the instance of CcLinuxStub"""
        if ConfidentialVM._inst is None:
            obj = None
            cc_type = ConfidentialVM.detect_cc_type()
            if cc_type is CCTrustedApi.TYPE_CC_TDX:
                obj = TdxVM()
            else:
                LOG.error("Unsupported confidential environment.")
                return None

            if obj is not None and obj.init():
                ConfidentialVM._inst = obj
            else:
                LOG.error("Fail to initialize the confidential VM.")
        return ConfidentialVM._inst

class TdxVM(ConfidentialVM):

    DEVICE_NODE_PATH = {
        TDX_VERSION_1_0: "/dev/tdx-guest",
        TDX_VERSION_1_5: "/dev/tdx_guest"
    }

    IOCTL_GET_REPORT = {
        TDX_VERSION_1_0: int.from_bytes(struct.pack('Hcb', 0x08c0, b'T', 1), 'big'),
        TDX_VERSION_1_5: int.from_bytes(struct.pack('Hcb', 0x40c4, b'T', 1),'big')
    }
    """
    TDX v1.0 reference: arch/x86/include/uapi/asm/tdx.h in kernel source
    TDX ioctl command layout (bits):
    command               dir(2)  size(14)                    type(8) nr(8)
    TDX_CMD_GET_REPORT    11      00,0000,0000,1000 (0xc008)  b'T'    0000,0001 (1)
    Convert the higher 16 bits from little-endian to big-endian:
    0xc008 -> 0x08c0

    TDX v1.5 reference: include/uapi/linux/tdx-guest.h in kernel source
    TDX ioctl command layout (bits):
    command               dir(2)  size(14bit)                 type(8bit)  nr(8bit)
    TDX_CMD_GET_REPORT0   11      00,0100,0100,0000 (0xc440)  b'T'        0000,0001 (1)
    Convert the higher 16 bits from little-endian to big-endian:
    0xc440 -> 0x40c4
    """

    IOCTL_GET_QUOTE = {
        TDX_VERSION_1_0: int.from_bytes(struct.pack('Hcb', 0x0880, b'T', 2), 'big'),
        TDX_VERSION_1_5: int.from_bytes(struct.pack('Hcb', 0x1080, b'T', 4),'big')
    }
    """
    TDX v1.0 reference: arch/x86/include/uapi/asm/tdx.h in kernel source
    TDX ioctl command layout (bits):
    command               dir(2)  size(14)                    type(8) nr(8)
    TDX_CMD_GET_QUOTE     10      00,0000,0000,1000 (0x8008)  b'T'    0000,0010 (2)
    Convert the higher 16 bits from little-endian to big-endian:
    0x8008 -> 0x0880

    TDX v1.5 Reference: include/uapi/linux/tdx-guest.h in kernel source
    TDX ioctl command layout (bits):
    command               dir(2)  size(14bit)                 type(8bit)  nr(8bit)
    TDX_CMD_GET_QUOTE     10      00,0000,0001,0000 (0x8010)  b'T'        0000,0100 (4)
    Convert the higher 16 bits from little-endian to big-endian
    0x8010 -> 0x1080
    """

    # The length of the tdquote 4 pages
    TDX_QUOTE_LEN = 4 * 4096

    # ACPI table containing the event logs
    ACPI_TABLE_FILE = "/sys/firmware/acpi/tables/CCEL"
    ACPI_TABLE_DATA_FILE = "/sys/firmware/acpi/tables/data/CCEL"
    IMA_DATA_FILE = "/sys/kernel/security/integrity/ima/ascii_runtime_measurements"
    CFG_FILE_PATH = "/etc/tdx-attest.conf"

    def __init__(self):
        ConfidentialVM.__init__(self, CCTrustedApi.TYPE_CC_TDX)
        self._version:str = None
        self._tdreport = None
        self._config:dict = self._load_config()

    @property
    def version(self):
        if self._version is None:
            for key, value in TdxVM.DEVICE_NODE_PATH.items():
                if os.path.exists(value):
                    self._version = key
        return self._version

    @property
    def default_algo_id(self):
        return TcgAlgorithmRegistry.TPM_ALG_SHA384

    @property
    def tdreport(self):
        """TDREPORT structure"""
        return self._tdreport

    def _load_config(self):
        """Process TDX attest config file and fetch params within the config."""
        tdx_config_dict = {}
        if os.path.exists(TdxVM.CFG_FILE_PATH):
            LOG.debug("Found TDX Config file at %s", TdxVM.CFG_FILE_PATH)
            try:
                with open(TdxVM.CFG_FILE_PATH, 'rb') as cfg_file:
                    cfg_info = [line.rstrip() for line in cfg_file]
                    for line in cfg_info:
                        # remove spaces in each line
                        # save all configs into tdx_config_dict
                        line = line.decode("utf-8").replace(" ", "")
                        param = line.partition("=")
                        tdx_config_dict[param[0]] = param[2]
            except(PermissionError, OSError):
                LOG.error("Need root permission to open file %s for params.",
                          TdxVM.CFG_FILE_PATH)
                return None

            # convert port param into integer and check its validity
            if "port" in tdx_config_dict:
                tdx_config_dict["port"] = int(tdx_config_dict["port"])
                if tdx_config_dict["port"] < 0 or tdx_config_dict["port"] > 65535:
                    LOG.debug("Invalid vsock port specified in the config.")
                    del tdx_config_dict["port"]

        return tdx_config_dict

    def process_cc_report(self, report_data=None) -> bool:
        """Process the confidential computing REPORT."""
        dev_path = self.DEVICE_NODE_PATH[self.version]
        try:
            tdx_dev = os.open(dev_path, os.O_RDWR)
        except (PermissionError, IOError, OSError):
            LOG.error("Fail to open device node %s", dev_path)
            return False

        LOG.debug("Successful open device node %s", dev_path)

        if self.version is TDX_VERSION_1_0:
            tdreport_req = TdxReportReq10()
        elif self.version is TDX_VERSION_1_5:
            tdreport_req = TdxReportReq15()

        # pylint: disable=E1111
        reqbuf = tdreport_req.prepare_reqbuf(report_data)
        try:
            fcntl.ioctl(tdx_dev, self.IOCTL_GET_REPORT[self.version], reqbuf)
        except OSError:
            LOG.error("Fail to execute ioctl for file %s", dev_path)
            os.close(tdx_dev)
            return False

        LOG.debug("Successful read TDREPORT from %s.", dev_path)
        os.close(tdx_dev)

        # pylint: disable=E1111
        tdreport = tdreport_req.process_output(reqbuf)
        if tdreport is not None:
            LOG.debug("Successful parse TDREPORT.")

        # process IMR
        self._tdreport = tdreport
        self._imrs[0] = TdxRTMR(0, tdreport.td_info.rtmr_0)
        self._imrs[1] = TdxRTMR(1, tdreport.td_info.rtmr_1)
        self._imrs[2] = TdxRTMR(2, tdreport.td_info.rtmr_2)
        self._imrs[3] = TdxRTMR(3, tdreport.td_info.rtmr_3)

        return True

    def process_eventlog(self) -> bool:
        """Process the event log

        Fetch boot time event logs from CCEL table and CCEL data file
        Save contents into TdxVM attributes

        Args:
            None

        Returns:
            A boolean indicating the status of process_eventlog
            True means the function runs successfully
            False means error occurred in event log processing

        Raises:
            PermissionError: An error occurred when accessing CCEL files
        """

        # verify if CCEL files existed
        if (not os.path.exists(TdxVM.ACPI_TABLE_FILE) or
            not os.path.exists(TdxVM.ACPI_TABLE_DATA_FILE)):
            LOG.error("Failed to find TDX CCEL table at %s or CCEL data file at %s",
                      TdxVM.ACPI_TABLE_FILE, TdxVM.ACPI_TABLE_DATA_FILE)
            return False

        try:
            with open(TdxVM.ACPI_TABLE_FILE, "rb") as f:
                ccel_data = f.read()
                assert len(ccel_data) > 0 and ccel_data[0:4] == b'CCEL', \
                    "Invalid CCEL table"
        except (PermissionError, OSError):
            LOG.error("Need root permission to open file %s", TdxVM.ACPI_TABLE_FILE)
            return False

        try:
            with open(TdxVM.ACPI_TABLE_DATA_FILE, "rb") as f:
                self._boot_time_event_log = f.read()
                assert len(self._boot_time_event_log) > 0
        except (PermissionError, OSError):
            LOG.error("Need root permission to open file %s", TdxVM.ACPI_TABLE_DATA_FILE)
            return False

        # Check if the identifier 'ima_hash=sha384' exists on kernel cmdline
        # If yes, suppose IMA over RTMR enabled in kernel (IMA over RTMR patch included in
        # https://github.com/intel/tdx-tools/blob/tdx-1.5/build/common/patches-tdx-kernel-MVP-KERNEL-6.2.16-v5.0.tar.gz)
        # If not, suppose IMA over RTMR not enabled in kernel
        with open("/proc/cmdline", encoding="utf-8") as cmdfile:
            cmdline = cmdfile.read().splitlines()
            if "ima_hash=sha384" not in cmdline[0].split(" "):
                return True

        if not os.path.exists(TdxVM.IMA_DATA_FILE):
            LOG.error("Failed to find IMA binary measurements at %s", TdxVM.IMA_DATA_FILE)
            return True

        try:
            with open(TdxVM.IMA_DATA_FILE, "rb") as f:
                self._runtime_event_log = f.read()
                if len(self._runtime_event_log) == 0:
                    LOG.info("Empty IMA measurement found at %s", TdxVM.IMA_DATA_FILE)
        except (PermissionError, OSError):
            LOG.error("Need root permission to open file %s", TdxVM.IMA_DATA_FILE)

        return True


    def get_cc_report(self, nonce: bytearray, data: bytearray, extraArgs) -> CcReport:
        """Get CcReport (i.e. TD Quote in the context of TDX).

        This depends on Quote Generation Service. Please reference "Whitepaper:
        Linux* Stacks for Intel® Trust Domain Extensions (4.3 Attestation)" for
        settings:
        https://www.intel.com/content/www/us/en/content-details/790888/whitepaper-linux-stacks-for-intel-trust-domain-extensions-1-5.html

        1. Set up the host: follow 4.3.1 ~ 4.3.4.
        2. Set up the guest: follow "Approach 2: Get quote via TDG.VP.VMCALL.GETQUOTE"
        in "4.3.5.1 Launch TD with Quote Generation Support".

        Args:
        nonce (bytearray): against replay attacks.
        data (bytearray): user data
        extraArgs: for TPM, it will be given list of IMR/PCRs

        Returns:
            The ``CcReport`` object. Return None if it fails.

        Raises:
            binascii.Error when the parameter "nonce" or "data" is not base64 encoded.
        """

        td_report = None

        # Prepare user defined data which could include nonce
        if nonce is not None:
            nonce = base64.b64decode(nonce, validate=True)
        if data is not None:
            data = base64.b64decode(data, validate=True)

        # Check if configfs-tsm has been enabled in kernel
        # if yes, call the super function
        if os.path.exists(ConfidentialVM.tsm_prefix):
            td_report = super().get_cc_report(nonce, data, extraArgs)

        if td_report is not None:
            return TdxQuote(td_report.data)

        report_bytes = None
        input_data = None

        LOG.info("Calculate report data by nonce and user data")
        hash_algo = hashlib.sha512()
        if nonce is not None:
            hash_algo.update(bytes(nonce))
        if data is not None:
            hash_algo.update(bytes(data))
        input_data = hash_algo.digest()

        # Check if appropriate qgs vsock port specified in TDX attest config
        # If specified, use vsock to get quote and return TdxQuote object
        self.process_cc_report(input_data)
        report_bytes = self.tdreport.data

        if self.version is TDX_VERSION_1_0:
            quote_req = TdxQuoteReq10()
        elif self.version is TDX_VERSION_1_5:
            quote_req = TdxQuoteReq15()

        if self._config and "port" in self._config:
            LOG.info("Use vsock for TDX quote fetching.")
            td_report = self._invoke_quote_fetching_on_vsock(
                report_bytes, quote_req, self._config["port"])

        # Check if quote fetching by vsock has been done successfully
        # If yes, return result and skip following steps
        if td_report:
            return td_report

        # Fetch quote through tdvmcall
        LOG.info("Use tdvmcall for TDX quote fetching.")
        # pylint: disable=E1111
        req_buf = quote_req.prepare_reqbuf(report_bytes)

        # Open TDX guest device node
        dev_path = self.DEVICE_NODE_PATH[self.version]
        try:
            tdx_dev = os.open(dev_path, os.O_RDWR)
        except (PermissionError, IOError, OSError) as e:
            LOG.error("Fail to open device node %s: %s", dev_path, str(e))
            return None
        LOG.debug("Successful open device node %s", dev_path)

        # Run ioctl command to get TD Quote
        try:
            fcntl.ioctl(tdx_dev, self.IOCTL_GET_QUOTE[self.version], req_buf)
        except OSError as e:
            LOG.error("Fail to execute ioctl for file %s: %s", dev_path, str(e))
            os.close(tdx_dev)
            return None
        LOG.debug("Successful get Quote from %s.", dev_path)
        os.close(tdx_dev)

        # Get TD Quote from ioctl command output
        return quote_req.process_output(req_buf)

    def _invoke_quote_fetching_on_vsock(
        self,
        report_bytes:bytes,
        quote_req:TdxQuoteReq,
        port:int=None
        ) -> TdxQuote:
        """Invoke TDX quote fetching through vsock.

        Args:
          report_bytes(bytes): report data included in quote request
          quote_req(TdxQuoteReq): the TDX quote request instance to call QGS
          port(integer): the port number of QGS vsock

        Returns:
          A TdxQuote object fetched through vsock
        """
        # Setup socket to connect qgs socket on host
        try:
            with socket.socket(socket.AF_VSOCK, socket.SOCK_STREAM, 0) as sock:
                sock.settimeout(30)
                sock.connect((socket.VMADDR_CID_HOST, port))

                header_size = 4
                # Generate p_blob_payload buffer
                qgs_msg = quote_req.qgs_msg_quote_req(report_bytes)
                msg_size = len(qgs_msg)
                p_blob_payload = bytearray(msg_size.to_bytes(header_size, "big"))
                p_blob_payload[header_size:] = qgs_msg[:msg_size]

                # Send quote request
                nsent = sock.send(p_blob_payload)
                LOG.debug("Sent %d bytes for Quote request.", nsent)

                # Receive quote response
                header = sock.recv(header_size)
                in_msg_size = 0
                for i in range(header_size):
                    in_msg_size = (in_msg_size << 8) + (header[i] & 0xFF)
                qgs_resp = sock.recv(in_msg_size)
                LOG.debug("Received %d bytes as Quote response", in_msg_size)

                sock.close()
        except socket.error as msg:
            LOG.error("Socket Error: %s", msg)
            return None
        tdquote = quote_req.qgs_msg_quote_resp(qgs_resp)
        return TdxQuote(tdquote)
