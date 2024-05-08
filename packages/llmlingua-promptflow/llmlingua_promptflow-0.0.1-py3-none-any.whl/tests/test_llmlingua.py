import pytest
import unittest

from promptflow.connections import CustomConnection
from llmlingua_promptflow.tools.llmlingua import prompt_compress


@pytest.fixture
def my_custom_connection() -> CustomConnection:
    my_custom_connection = CustomConnection(
        {
            "api-key" : "my-api-key",
            "api-secret" : "my-api-secret",
            "api-url" : "my-api-url"
        }
    )
    return my_custom_connection


class TestTool:
    def test_prompt_compress(self, my_custom_connection):
        result = prompt_compress(my_custom_connection, input_text="Microsoft")
        assert result == "Hello Microsoft"


# Run the unit tests
if __name__ == "__main__":
    unittest.main()