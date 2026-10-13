"""Lifecycle checks protect unrelated processes; no platform publishing."""
import importlib.util
import tempfile
import unittest
import socket
import subprocess
import sys
from types import SimpleNamespace
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("control", Path(__file__).with_name("control.py"))
control = importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)


class ControlTests(unittest.TestCase):
    def test_only_loopback_mcp(self):
        for url in ("http://127.0.0.1:18060/mcp", "http://localhost:18060/mcp", "http://[::1]:18060/mcp"):
            control.validate_loopback(url)
        for url in ("http://0.0.0.0:18060/mcp", "https://example.com/mcp", "http://secret@127.0.0.1/mcp"):
            with self.assertRaises(control.ControlError):
                control.validate_loopback(url)

    def test_reused_pid_is_not_owned(self):
        state = {"pid": 456, "start_signature": "original"}
        with patch.object(control, "read_state", return_value=state), patch.object(control, "start_signature", return_value="different"):
            self.assertIsNone(control.owned_process("backend"))

    def test_same_timestamp_foreign_command_is_not_owned(self):
        state = {"pid": 456, "start_signature": "same second", "command_signature": "original command"}
        with patch.object(control, "read_state", return_value=state), patch.object(control, "start_signature", return_value="same second"), patch.object(control, "command_signature", return_value="foreign command"):
            self.assertIsNone(control.owned_process("backend"))

    def test_stop_does_not_signal_foreign_pid(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(control, "RUN", Path(directory)), patch.object(control, "owned_process", return_value=None), patch.object(control.os, "killpg") as kill, patch.object(control, "emit"):
            control.stop_service("backend")
            kill.assert_not_called()

    def test_used_port_rejects_start(self):
        with patch.object(control, "private_dirs"), patch.object(control, "owned_process", return_value=None), patch.object(control, "port_open", return_value=True), patch.object(control.subprocess, "Popen") as popen:
            with self.assertRaises(control.ControlError):
                control.start_service("backend")
            popen.assert_not_called()

    def test_space_paths_remain_single_argument(self):
        with tempfile.TemporaryDirectory(prefix="xhs spaces ") as directory:
            root = Path(directory)
            python = root / ".venv/bin/python"
            python.parent.mkdir(parents=True)
            python.touch()
            with patch.object(control, "ROOT", root), patch.object(control, "PYTHON", python):
                result = control.command("backend")
            self.assertEqual(result[0], str(python))
            self.assertEqual(result[2], "uvicorn")

    def test_shell_text_in_env_is_not_evaluated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".env").write_text("EXAMPLE='$(touch should-never-exist)'\nXHS_MCP_URL=http://127.0.0.1:18060/mcp\n")
            with patch.object(control, "ROOT", root), patch.dict(control.os.environ, {}, clear=True):
                result = control.configuration()
            self.assertEqual(result["EXAMPLE"], "$(touch should-never-exist)")
            self.assertFalse((root / "should-never-exist").exists())

    def test_redaction_also_handles_invalid_mcp_url(self):
        import contextlib
        import io
        output = io.StringIO()
        with patch.dict(control.os.environ, {"MODEL_API_KEY": "example-private-key-value", "XHS_MCP_URL": "https://example.com/mcp"}), contextlib.redirect_stdout(output):
            control.emit({"detail": "example-private-key-value", "token": "cookie-value"})
        self.assertNotIn("example-private-key-value", output.getvalue())
        self.assertNotIn("cookie-value", output.getvalue())

    def test_uninstall_does_not_erase_manual_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "run").mkdir()
            state = root / "run" / "backend.json"
            state.write_text("manual state")
            with patch.object(control.sys, "platform", "darwin"), patch.object(control.Path, "home", return_value=root), patch.object(control, "RUN", root / "run"), patch.object(control, "read_state", return_value={"launcher": "manual"}), patch.object(control, "emit"):
                control.uninstall_services()
            self.assertTrue(state.exists())

    def test_unattested_mcp_binary_is_never_started(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory)
            (runtime / "bin").mkdir()
            (runtime / "bin" / "xiaohongshu-mcp").write_bytes(b"unverified release")
            with patch.object(control, "RUNTIME", runtime):
                with self.assertRaises(control.ControlError):
                    control.command("mcp")

    def test_lifecycle_with_real_child_process(self):
        """Start/stop a disposable local listener, never the actual application."""
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            port = probe.getsockname()[1]
        program = f"import socket,time; s=socket.socket(); s.bind(('127.0.0.1',{port})); s.listen(); time.sleep(60)"
        real_popen = subprocess.Popen
        children = []

        def retain(*args, **kwargs):
            child = real_popen(*args, **kwargs)
            children.append(child)
            return child

        with tempfile.TemporaryDirectory(prefix="xhs lifecycle spaces ") as directory:
            root = Path(directory)
            runtime = root / ".runtime"
            with patch.object(control, "ROOT", root), patch.object(control, "RUNTIME", runtime), patch.object(control, "RUN", runtime / "run"), patch.object(control, "LOGS", runtime / "logs"), patch.object(control, "PORTS", {"backend": port}), patch.object(control, "command", return_value=[sys.executable, "-c", program]), patch.object(control, "cwd_for", return_value=root), patch.object(control, "emit"), patch.object(control.subprocess, "Popen", side_effect=retain):
                try:
                    control.start_service("backend")
                    self.assertTrue(control.port_open(port))
                    self.assertIsNotNone(control.owned_process("backend"))
                    control.stop_service("backend")
                    self.assertFalse(control.port_open(port))
                    self.assertIsNone(control.owned_process("backend"))
                finally:
                    control.stop_service("backend")
                    for child in children:
                        child.wait(timeout=5)

    def test_foreign_real_process_survives_stale_record(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            foreign = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                with patch.object(control, "ROOT", root), patch.object(control, "RUNTIME", root / ".runtime"), patch.object(control, "RUN", root / ".runtime/run"), patch.object(control, "LOGS", root / ".runtime/logs"), patch.object(control, "emit"):
                    control.write_state("backend", {"root": str(root), "service": "backend", "pid": foreign.pid, "start_signature": "stale process timestamp", "launcher": "manual"})
                    control.stop_service("backend")
                    self.assertIsNone(foreign.poll(), "An unrelated live process must survive")
            finally:
                foreign.terminate()
                foreign.wait(timeout=5)

    def test_live_approved_command_enqueues_once_without_typed_authorization(self):
        arguments = SimpleNamespace(command="publish-approved", mode="live", ids=None)
        with patch.object(control, "api", return_value={"count": 2, "enqueued": [], "blocked": []}) as api, patch.object(control, "emit"):
            control.cli(arguments)
        api.assert_called_once_with("POST", "/publishing/enqueue-approved", {})

    def test_live_id_filter_is_forwarded_without_expanding_article_scope(self):
        arguments = SimpleNamespace(command="publish-approved", mode="live", ids=["one-specific-article"])
        with patch.object(control, "api", return_value={"count": 1, "enqueued": [], "blocked": []}) as api, patch.object(control, "emit"):
            control.cli(arguments)
        api.assert_called_once_with("POST", "/publishing/enqueue-approved", {"article_ids": ["one-specific-article"]})

    def test_operator_request_has_long_wait_and_no_automatic_retry(self):
        import urllib.error
        opener = unittest.mock.Mock()
        opener.open.side_effect = urllib.error.URLError("connection closed")
        with patch.object(control.urllib.request, "build_opener", return_value=opener), patch.object(control, "configuration", return_value={"XHS_CLI_HTTP_TIMEOUT_SECONDS": "1"}):
            with self.assertRaises(control.ControlError):
                control.api("POST", "/publishing/enqueue-approved", {})
        self.assertEqual(opener.open.call_count, 1)
        self.assertGreaterEqual(opener.open.call_args.kwargs["timeout"], 900)


if __name__ == "__main__":
    unittest.main()
