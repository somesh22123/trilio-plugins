import importlib.util
import unittest
from pathlib import Path

HOOK_PATH = Path(__file__).resolve().parent.parent / "plugins/tsr/hooks/guard_trilio_changes.py"
spec = importlib.util.spec_from_file_location("guard", HOOK_PATH)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def bash(command):
    return {"tool_name": "Bash", "tool_input": {"command": command}}


class GuardHookTest(unittest.TestCase):
    def test_asks_before_mutating_trilio_resources(self):
        for cmd in (
            "kubectl delete ns trilio-system",
            "oc -n trilio patch deploy x -p '{}'",
            "helm uninstall trilio-operator",
            "kubectl apply -f trilio-config.yaml",
        ):
            with self.subTest(cmd=cmd):
                result = guard.decide(bash(cmd))
                self.assertEqual(result["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_allows_reads_and_unrelated_commands(self):
        for cmd in (
            "kubectl get pods -n trilio-system",
            "kubectl describe ns trilio",
            "kubectl delete pod nginx",
            "kubectl get pods -n trilio | grep apply",
            "ls",
        ):
            with self.subTest(cmd=cmd):
                self.assertIsNone(guard.decide(bash(cmd)))

    def test_ignores_other_tools(self):
        self.assertIsNone(guard.decide({"tool_name": "Read", "tool_input": {"file_path": "trilio delete"}}))


if __name__ == "__main__":
    unittest.main()
