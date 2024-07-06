from src.bot import ChatBot


def test_bot_chat(cfg):
    bot = ChatBot(cfg)
    bot.cfg["model"] = "mock-model"
    expected_roles = ["user", "assistant", "user", "assistant"]
    expected_messages = ["foo", "This is just a mock reply", "bar", "This is just a mock reply"]

    # Test empty history
    assert len(bot.chat_history) == 0

    # Test after 1 question
    a1 = bot.chat(expected_messages[0])
    assert len(bot.chat_history) == 2
    assert isinstance(a1, str)
    assert a1 == expected_messages[1]
    for i, msg in enumerate(bot.chat_history):
        assert msg["role"] == expected_roles[i]
        assert msg["content"] == expected_messages[i]

    # Test after 2 questions
    a2 = bot.chat(expected_messages[2])
    assert len(bot.chat_history) == 4
    assert isinstance(a2, str)
    assert a2 == expected_messages[3]
    for i, msg in enumerate(bot.chat_history):
        assert msg["role"] == expected_roles[i]
        assert msg["content"] == expected_messages[i]
