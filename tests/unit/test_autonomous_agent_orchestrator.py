import unittest
from openoperator.agent.autonomous_agent_orchestrator import AutonomousAgentOrchestratorImpl

class TestAutonomousAgentOrchestrator(unittest.TestCase):
    def test_accept_goal(self):
        orchestrator = AutonomousAgentOrchestratorImpl()
        goal = "Test goal"
        orchestrator.accept_goal(goal)
        self.assertEqual(orchestrator.goal_completion_detector.get_goal(), goal)

    def test_check_goal_completion(self):
        orchestrator = AutonomousAgentOrchestratorImpl()
        goal = "Test goal"
        orchestrator.accept_goal(goal)
        self.assertTrue(orchestrator.check_goal_completion())

    def test_execute_multi_step_plan(self):
        orchestrator = AutonomousAgentOrchestratorImpl()
        plan = ["Step 1", "Step 2", "Step 3"]
        self.assertTrue(orchestrator.execute_multi_step_plan(plan))

    def test_trigger_self_correction(self):
        orchestrator = AutonomousAgentOrchestratorImpl()
        orchestrator.trigger_self_correction()
        self.assertTrue(orchestrator.self_correction_loop.is_triggered())

    def test_manage_retries(self):
        orchestrator = AutonomousAgentOrchestratorImpl()
        max_retries = 3
        self.assertEqual(orchestrator.manage_retries(max_retries), "Failed after all retries")

    def test_return_final_status(self):
        orchestrator = AutonomousAgentOrchestratorImpl()
        self.assertEqual(orchestrator.return_final_status(), "Execution completed successfully")