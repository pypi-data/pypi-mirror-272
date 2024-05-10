import time

from jupyter_client.client import KernelClient
from jupyter_client.manager import KernelManager


class Kernel:
    def __init__(self) -> None:
        self._manager: KernelManager | None = None
        self._client: KernelClient | None = None

    @property
    def manager(self) -> KernelManager:
        if not self._manager:
            self._manager = KernelManager(kernel_name="python3")
            self._manager.start_kernel()
        return self._manager

    @property
    def client(self) -> KernelClient:
        if not self._client:
            self._client = self.manager.client()
            self._client.start_channels()
        return self._client

    def wait_for_ready(self, timeout: int = 5) -> None:
        manager = self.manager
        start_time = time.time()
        while not manager.is_alive():
            if time.time() - start_time > timeout:
                raise Exception("Kernel took too long to start")
            time.sleep(0.05)
        time.sleep(0.5)

    def execute_code(self, code: str, timeout: int = 10) -> str:
        self.wait_for_ready()
        client = self.client
        client.execute(code)
        client.connect_iopub()
        results = []
        start_time = time.time()
        while True:
            try:
                msg = client.iopub_channel.get_msg(timeout=1)
                content = msg["content"]
                if msg["msg_type"] == "stream" and content["name"] == "stdout":
                    results.append(content["text"])
                    break
            except Exception:
                if time.time() - start_time > timeout:
                    raise Exception("Kernel took too long to execute code")
                continue
        return "\n".join(results)

    def close(self) -> None:
        if self._client:
            self._client.stop_channels()
            self._client = None
        if self._manager:
            self._manager.shutdown_kernel()
            self._manager = None
