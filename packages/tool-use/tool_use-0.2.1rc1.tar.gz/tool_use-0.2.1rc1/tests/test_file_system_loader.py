import os
import unittest

import pytest
import pytest_asyncio
from promptflow.connections import OpenAIConnection

from tool_use.tools.anthropic_tool_use import AnthropicConnection, anthropic_tool_use
from tool_use.tools.openai_tool_use import openai_tool_use


@pytest_asyncio.fixture
def load_env():
    from dotenv import load_dotenv

    load_dotenv()


@pytest_asyncio.fixture
def anthropic_connection(load_env) -> OpenAIConnection:
    return AnthropicConnection(
        secrets=dict(
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            api_type="anthropic",
            api_base="https://api.anthropic.com",
            client_key=None,
        ),
    )


@pytest_asyncio.fixture
def openai_connection(load_env) -> OpenAIConnection:
    return OpenAIConnection(
        api_key=os.environ.get("OPENAI_API_KEY"),
        organization=os.environ.get("OPENAI_ORG_ID"),
    )


@pytest_asyncio.fixture
def prompt() -> str:
    path = os.path.join(os.path.dirname(__file__), "file_system_loader_includer.jinja2")
    prompt = ""

    with open(path) as f:
        prompt = f.read()

    return prompt


@pytest.mark.asyncio
async def test_file_system_loader_anthropic_tool_use(prompt, anthropic_connection):
    result = await anthropic_tool_use(
        use_template_loader=True,
        connection=anthropic_connection,
        prompt=prompt,
        model="claude-3-haiku-20240307",
        max_tokens=2000,
    )
    assert result is not None
    print(result)


@pytest.mark.asyncio
async def test_file_system_loader_openai_tool_use(prompt, openai_connection):
    result = await openai_tool_use(
        use_template_loader=True,
        connection=openai_connection,
        prompt=prompt,
        model="gpt-4-0125-preview",
    )
    assert result is not None
    print(result)


# Run the unit tests
if __name__ == "__main__":
    unittest.main()
