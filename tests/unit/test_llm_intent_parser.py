"""
Tests for LLMIntentParser.
Verifies LLM parsing capabilities and fallback mechanism to Regex parsing.
"""

import pytest
from unittest.mock import patch, MagicMock
from openoperator.agent.intent_parser import LLMIntentParser
from openoperator.agent.vision_models import VisionActionType

@pytest.fixture
def parser():
    return LLMIntentParser(endpoint="http://fake-endpoint/v1/chat/completions")

def test_llm_parse_success(parser):
    """Test that the parser correctly translates LLM JSON output into a VisionTaskPlan."""
    
    # Simulating a multi-lingual instruction response
    mock_response = b'{"choices": [{"message": {"content": "[{\\"action_type\\": \\"FOCUS_WINDOW\\", \\"target_element\\": \\"Notepad\\"}, {\\"action_type\\": \\"TYPE_TEXT\\", \\"input_data\\": \\"hello\\"}]"}}]}'
    
    mock_urlopen = MagicMock()
    mock_urlopen.__enter__.return_value.read.return_value = mock_response
    
    with patch("urllib.request.urlopen", return_value=mock_urlopen):
        # Even with informal Hinglish prompt, the mocked LLM output works
        plan = parser.parse("notepad khol do aur hello type karo")
        
        assert plan.is_executable is True
        assert len(plan.steps) == 2
        assert plan.steps[0].action_type == VisionActionType.FOCUS_WINDOW
        assert plan.steps[0].target_element == "Notepad"
        assert plan.steps[1].action_type == VisionActionType.TYPE_TEXT
        assert plan.steps[1].input_data == "hello"

def test_llm_fallback_to_regex_on_failure(parser):
    """Test that parser gracefully falls back to Regex if LLM API is unavailable."""
    
    with patch("urllib.request.urlopen", side_effect=Exception("Network error")):
        # The prompt is standard English, so Regex fallback will succeed
        plan = parser.parse("open Notepad and type fallback")
        
        assert plan.is_executable is True
        assert len(plan.steps) == 2
        assert plan.steps[0].action_type == VisionActionType.FOCUS_WINDOW
        assert plan.steps[1].action_type == VisionActionType.TYPE_TEXT