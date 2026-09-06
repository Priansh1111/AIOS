import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from schemas import Candidate, UnderstandingResult
from response_filter import filter_and_select


def make_understanding(goals=None) -> UnderstandingResult:
    return UnderstandingResult(
        emotion="frustrated",
        intent="seeking_advice",
        working_memory=["I keep messing up binary tree traversal"],
        current_goals=goals or ["clear placements by Dec"],
        search_terms=["tree traversal"],
    )


def test_prefers_no_risk_candidate_over_risky_one():
    candidates = [
        Candidate(
            reply_text="That sounds frustrating.",
            predicted_reaction="may feel dismissive",
            risk_flag="too generic / may feel dismissive",
        ),
        Candidate(
            reply_text="Want to try a quick 3-question refresher first?",
            predicted_reaction="likely receptive, prefers practical steps",
            risk_flag=None,
        ),
    ]
    result = filter_and_select(candidates, make_understanding())
    assert result.reply_text == "Want to try a quick 3-question refresher first?"


def test_avoids_topic_already_mentioned_today():
    candidates = [
        Candidate(
            reply_text="Want another tree traversal quiz?",
            predicted_reaction="neutral",
            risk_flag=None,
        ),
        Candidate(
            reply_text="Want to look at something else instead?",
            predicted_reaction="neutral",
            risk_flag=None,
        ),
    ]
    result = filter_and_select(
        candidates,
        make_understanding(),
        already_mentioned_today=["tree traversal"],
    )
    assert result.reply_text == "Want to look at something else instead?"


def test_prefers_goal_aligned_candidate_when_otherwise_tied():
    candidates = [
        Candidate(
            reply_text="Sure, sounds good.",
            predicted_reaction="neutral",
            risk_flag=None,
        ),
        Candidate(
            reply_text="Let's keep pushing toward placements this month.",
            predicted_reaction="neutral",
            risk_flag=None,
        ),
    ]
    result = filter_and_select(candidates, make_understanding(goals=["placements"]))
    assert "placements" in result.reply_text.lower()


def test_returns_final_response_shape():
    candidates = [
        Candidate(reply_text="Got it.", predicted_reaction="neutral", risk_flag=None)
    ]
    result = filter_and_select(candidates, make_understanding())
    assert result.reply_text == "Got it."
    assert result.speak is True
    assert result.popup is None
    assert result.action is None
    assert result.pending_permission is None


def test_raises_on_empty_candidates():
    try:
        filter_and_select([], make_understanding())
        assert False, "should have raised ValueError on zero candidates"
    except ValueError:
        pass


def test_all_risky_still_picks_the_least_bad():
    # when every candidate has a risk flag, filtering should still return
    # something rather than crashing - just picks the highest remaining score
    candidates = [
        Candidate(reply_text="Option A", predicted_reaction="risky", risk_flag="risk A"),
        Candidate(reply_text="Option B", predicted_reaction="risky", risk_flag="risk B"),
    ]
    result = filter_and_select(candidates, make_understanding())
    assert result.reply_text in ("Option A", "Option B")