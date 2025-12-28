"""Tests for mixer module."""

import pytest
from chatbot.mixer import (
    MixStrategy,
    SentimentSource,
    MixedSentiment,
    SentimentMixer,
    AverageMixer,
    WeightedMixer,
    MaxMixer,
    MinMixer,
    SentimentCombiner,
    mix_sentiments,
)


class TestMixers:
    """Tests for individual mixers."""

    def test_average_mixer(self):
        """Test average mixer."""
        mixer = AverageMixer()
        sources = [
            SentimentSource("a", 0.5),
            SentimentSource("b", 0.7),
        ]
        result = mixer.mix(sources)
        assert result == pytest.approx(0.6)

    def test_weighted_mixer(self):
        """Test weighted mixer."""
        mixer = WeightedMixer()
        sources = [
            SentimentSource("a", 0.5, weight=1.0),
            SentimentSource("b", 1.0, weight=3.0),
        ]
        result = mixer.mix(sources)
        assert result == pytest.approx(0.875)

    def test_max_mixer(self):
        """Test max mixer."""
        mixer = MaxMixer()
        sources = [
            SentimentSource("a", 0.3),
            SentimentSource("b", 0.8),
        ]
        result = mixer.mix(sources)
        assert result == 0.8

    def test_min_mixer(self):
        """Test min mixer."""
        mixer = MinMixer()
        sources = [
            SentimentSource("a", 0.3),
            SentimentSource("b", 0.8),
        ]
        result = mixer.mix(sources)
        assert result == 0.3

    def test_empty_sources(self):
        """Test with empty sources."""
        mixer = AverageMixer()
        result = mixer.mix([])
        assert result == 0.0


class TestSentimentCombiner:
    """Tests for SentimentCombiner."""

    def test_combine_average(self):
        """Test combining with average."""
        combiner = SentimentCombiner(MixStrategy.AVERAGE)
        sources = [
            SentimentSource("a", 0.4),
            SentimentSource("b", 0.6),
        ]
        result = combiner.combine(sources)
        
        assert result.final_score == pytest.approx(0.5)
        assert result.strategy == MixStrategy.AVERAGE

    def test_combine_first(self):
        """Test first strategy."""
        combiner = SentimentCombiner()
        sources = [
            SentimentSource("a", 0.1),
            SentimentSource("b", 0.9),
        ]
        result = combiner.combine(sources, MixStrategy.FIRST)
        
        assert result.final_score == 0.1

    def test_combine_last(self):
        """Test last strategy."""
        combiner = SentimentCombiner()
        sources = [
            SentimentSource("a", 0.1),
            SentimentSource("b", 0.9),
        ]
        result = combiner.combine(sources, MixStrategy.LAST)
        
        assert result.final_score == 0.9

    def test_set_strategy(self):
        """Test setting strategy."""
        combiner = SentimentCombiner()
        combiner.set_strategy(MixStrategy.MAX)
        
        sources = [SentimentSource("a", 0.3), SentimentSource("b", 0.7)]
        result = combiner.combine(sources)
        
        assert result.final_score == 0.7


class TestMixSentiments:
    """Tests for mix_sentiments function."""

    def test_mix(self):
        """Test mixing sentiments."""
        scores = {"vader": 0.5, "custom": 0.7}
        result = mix_sentiments(scores)
        
        assert result == pytest.approx(0.6)

    def test_mix_with_strategy(self):
        """Test mixing with strategy."""
        scores = {"a": 0.3, "b": 0.9}
        result = mix_sentiments(scores, MixStrategy.MAX)
        
        assert result == 0.9
