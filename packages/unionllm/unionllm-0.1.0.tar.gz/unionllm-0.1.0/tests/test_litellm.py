import sys
import os
import unittest
import json
import litellm

# 将项目根目录添加到sys.path中
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from unionllm.providers.base_provider import BaseProvider

class TestLiteLLMProvider(unittest.TestCase):
    def setUp(self):
        self.provider = BaseProvider(api_key="sk-45ad8752a48d47ffaf86f5b000eff589")

    def test_completion(self):
        model = "qwen-turbo"
        messages = [{"content": "你好，今天天气怎么样？", "role": "user"}]
        response = self.provider.completion(model=model, messages=messages)
        print("response: ", response)
        self.assertIsNotNone(response)

if __name__ == "__main__":
    unittest.main()
