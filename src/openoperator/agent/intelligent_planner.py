"""
Intelligent Task Planner for OpenOperator.

Combines VisionIntentParser and VisionPlanCompiler
into a single high-level planning interface.
"""

import logging
from typing import Optional

from openoperator.agent.intent_parser import VisionIntentParser
from openoperator.agent.plan_compiler import VisionPlanCompiler
from openoperator.agent.vision_models import VisionTaskPlan

logger = logging.getLogger(__name__)


class IntelligentTaskPlanner:
    """
    High-level planner that converts natural language
    into executable VisionTaskPlans.
    """

    def __init__(
        self,
        parser: Optional[VisionIntentParser] = None,
        compiler: Optional[VisionPlanCompiler] = None,
    ) -> None:

        self.parser = parser or VisionIntentParser()
        self.compiler = compiler or VisionPlanCompiler()

    def create_plan(
        self,
        prompt: str,
    ) -> VisionTaskPlan:

        logger.info(
            f"Creating intelligent plan for prompt: '{prompt}'"
        )

        parsed_plan = self.parser.parse(prompt)

        compiled_plan = self.compiler.compile(
            parsed_plan
        )

        return compiled_plan