from src.bot import ChatBot


def test_bot_chat(cfg):
    bot = ChatBot(cfg)
    expected_roles = ["assistant", "user", "assistant", "user", "assistant"]
    expected_messages = [
        "Hi, how can I help you today?",
        "foo",
        "This is just a mock reply",
        "bar",
        "This is just a mock reply",
    ]

    # Test initial history
    assert len(bot.history) == 1
    assert bot.history[0]["content"] == expected_messages[0]

    # Test after 1 question
    a1 = bot.chat(expected_messages[1])
    assert len(bot.history) == 3
    assert isinstance(a1, str)
    assert a1 == expected_messages[2]
    for i, msg in enumerate(bot.history):
        assert msg["role"] == expected_roles[i]
        assert msg["content"] == expected_messages[i]

    # Test after 2 questions
    a2 = bot.chat(expected_messages[3])
    assert len(bot.history) == 5
    assert isinstance(a2, str)
    assert a2 == expected_messages[4]
    for i, msg in enumerate(bot.history):
        assert msg["role"] == expected_roles[i]
        assert msg["content"] == expected_messages[i]
