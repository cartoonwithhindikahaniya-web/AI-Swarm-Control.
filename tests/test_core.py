import pytest
import os
from unittest.mock import MagicMock, patch
from src.tools.crypto_tools import get_crypto_price
from src.tools.research_tools import web_search
from src.agents.researcher import ResearchAgent

def test_get_crypto_price_mock():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"bitcoin": {"usd": 50000}}

        result = get_crypto_price("btc")
        assert result["price"] == 50000
        assert result["symbol"] == "btc"

def test_web_search_mock():
    with patch('requests.request') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "organic": [{"title": "Test", "link": "http://test.com", "snippet": "test snippet"}]
        }

        with patch.dict('os.environ', {'SERPER_API_KEY': 'fake_key'}):
            result = web_search("test query")
            assert len(result) == 1
            assert result[0]["title"] == "Test"

def test_researcher_agent_init_openai():
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'fake_openai_key', 'LLM_PROVIDER': 'openai'}):
        agent = ResearchAgent(name="TestResearcher")
        assert agent.name == "TestResearcher"
        assert agent.provider == "openai"
        assert agent.model == "gpt-4o"
        assert agent.api_key == "fake_openai_key"

def test_researcher_agent_init_deepseek():
    with patch.dict('os.environ', {'DEEPSEEK_API_KEY': 'fake_deepseek_key', 'LLM_PROVIDER': 'deepseek'}):
        agent = ResearchAgent(name="TestDeepSeeker")
        assert agent.name == "TestDeepSeeker"
        assert agent.provider == "deepseek"
        assert agent.model == "deepseek-reasoner"
        assert agent.api_key == "fake_deepseek_key"
        assert str(agent.client.base_url).rstrip('/') == "https://api.deepseek.com"
