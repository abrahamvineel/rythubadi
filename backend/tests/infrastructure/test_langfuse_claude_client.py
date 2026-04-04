from tests.fakes.fake_llm_client import FakeLLMClient
from tests.fakes.fake_langfuse_client import FakeLangFuseClient
import hashlib
from infrastructure.llm.langfuse_claude_client import LangFuseClaudeClient

class TestLangfuseClaudeClient:

    def test_input_to_langfuse_is_sha256(self):
        fake_llm = FakeLLMClient("water now")
        fake_langfuse = FakeLangFuseClient()

        client = LangFuseClaudeClient(llm_client=fake_llm, langfuse=fake_langfuse, agent_name="crop advisor")
        messages = [{"role": "user", "content":"when should i water?"},
                           {"role": "system", "content":"water now"}]
        result = client.generate(messages)
        assert fake_langfuse.recorded_input == hashlib.sha256(str(messages).encode()).hexdigest()
        assert "water now" in result
