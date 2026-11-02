from sheettruth.prompt import SYSTEM_PROMPT, build_messages, normalise_messages, parse_reply


def test_normalise_strips_leading_reasoning_line():
    msgs = [{"role": "system", "content": "Reasoning strength: low\n" + SYSTEM_PROMPT}, {"role": "user", "content": "x"}]
    out = normalise_messages(msgs)
    assert out[0]["content"] == SYSTEM_PROMPT
    assert out[1] == msgs[1]


def test_build_messages_has_no_reasoning_line():
    msgs = build_messages("TARGET|Sheet1!A1|=SUM(A2:A3)")
    assert msgs[0]["role"] == "system" and "Reasoning strength" not in msgs[0]["content"]
    assert msgs[1]["role"] == "user"


def test_parse_reply_reads_json_after_message_marker():
    raw = ' to=user<|message|>{"verdict": "error", "type": "skipped_rows", "expected": "=SUM(A1:A5)", "reason": "r"}<|eot|>'
    p = parse_reply(raw)
    assert p == {"verdict": "error", "type": "skipped_rows", "expected": "=SUM(A1:A5)", "reason": "r", "parsed": True}


def test_parse_reply_drops_type_on_ok_and_handles_garbage():
    assert parse_reply('{"verdict": "ok", "type": "wrong_sign", "expected": "=A1", "reason": ""}')["type"] is None
    bad = parse_reply("no json here")
    assert bad["verdict"] == "unsupported" and bad["parsed"] is False
