"""
Unit tests that don't require real .osu files.
Run with: python test_extractor.py
"""
import math
import unittest

from osu_parser import Beatmap, HitObject, TimingPoint
from feature_extractor import (
    _dist, _angle_between, _direction_change,
    _detect_streams, _slider_features, extract_features,
)


def _circle(x, y, t) -> HitObject:
    return HitObject(x=x, y=y, time=t, type_flags=1,
                     is_slider=False, is_spinner=False)


def _slider(x, y, t, length=100.0, curve_pts=None) -> HitObject:
    ho = HitObject(x=x, y=y, time=t, type_flags=2,
                   is_slider=True, is_spinner=False)
    ho.length = length
    ho.curve_points = curve_pts or [(x+50, y)]
    ho.slides = 1
    ho.slider_velocity = 1.0
    return ho


class TestGeometry(unittest.TestCase):
    def test_dist(self):
        a, b = _circle(0, 0, 0), _circle(3, 4, 100)
        self.assertAlmostEqual(_dist(a, b), 5.0)

    def test_angle_straight(self):
        # a→b→c in a straight line → angle = 180°
        a, b, c = _circle(0, 0, 0), _circle(100, 0, 100), _circle(200, 0, 200)
        self.assertAlmostEqual(_angle_between(a, b, c), 180.0, places=4)

    def test_angle_right(self):
        # a→b→c form a right angle at b
        a, b, c = _circle(0, 100, 0), _circle(0, 0, 100), _circle(100, 0, 200)
        self.assertAlmostEqual(_angle_between(a, b, c), 90.0, places=4)

    def test_direction_change_left(self):
        # osu! uses screen coords (Y increases downward).
        # Moving right (+x) then curving to y+50 (downward on screen) = left turn
        # → cross product positive → positive result.
        a, b, c = _circle(0, 0, 0), _circle(100, 0, 100), _circle(150, 50, 200)
        turn = _direction_change(a, b, c)
        self.assertGreater(turn, 0)

    def test_direction_change_right(self):
        # Moving right (+x) then curving to y-50 (upward on screen) = right turn
        # → cross product negative → negative result.
        a, b, c = _circle(0, 0, 0), _circle(100, 0, 100), _circle(150, -50, 200)
        turn = _direction_change(a, b, c)
        self.assertLess(turn, 0)


class TestStreamDetection(unittest.TestCase):
    def _make_stream(self, start_t, n, gap_ms):
        return [_circle(i * 10, 0, start_t + i * gap_ms) for i in range(n)]

    def test_detects_stream(self):
        # 200 BPM stream → gap = 150ms → within threshold
        objs = self._make_stream(0, 16, 150)
        result = _detect_streams(objs, dom_bpm=200)
        self.assertEqual(result["stream_run_count"], 1)
        self.assertEqual(result["stream_max_run_length"], 16)

    def test_no_stream_slow(self):
        # 120 BPM notes → gap = 500ms → too slow
        objs = self._make_stream(0, 8, 500)
        result = _detect_streams(objs, dom_bpm=120)
        self.assertEqual(result["stream_run_count"], 0)

    def test_partial_stream(self):
        # 8 stream notes, 1000ms pause, then 3 notes (too short to qualify)
        stream = self._make_stream(0, 8, 150)          # t = 0..1050
        short  = self._make_stream(1050 + 1000, 3, 150)  # t = 2050..2350
        result = _detect_streams(stream + short, dom_bpm=200)
        self.assertEqual(result["stream_run_count"], 1)

    def test_stream_ratio(self):
        stream = self._make_stream(0, 8, 150)
        result = _detect_streams(stream, dom_bpm=200)
        self.assertAlmostEqual(result["stream_note_ratio"], 1.0)


class TestSliderFeatures(unittest.TestCase):
    def test_no_sliders(self):
        objs = [_circle(0, 0, 0), _circle(100, 0, 100)]
        feats = _slider_features(objs)
        self.assertEqual(feats["slider_count"], 0)
        self.assertEqual(feats["slider_complex_ratio"], 0.0)

    def test_complex_slider(self):
        s = _slider(0, 0, 0, length=200.0, curve_pts=[(50,0),(100,50),(150,0)])
        feats = _slider_features([s])
        self.assertEqual(feats["slider_count"], 1)
        self.assertAlmostEqual(feats["slider_complex_ratio"], 1.0)
        self.assertAlmostEqual(feats["slider_avg_curve_pts"], 3.0)


class TestFullExtraction(unittest.TestCase):
    def _make_beatmap(self, objects, bpm=200.0) -> Beatmap:
        bm = Beatmap(title="Test", artist="Artist", version="Hard")
        bm.slider_multiplier = 1.4
        beat_ms = 60_000 / bpm
        bm.timing_points = [
            TimingPoint(time=0, beat_length=beat_ms, meter=4, uninherited=True)
        ]
        bm.hit_objects = objects
        return bm

    def test_stream_map(self):
        # 16 circles at 200 BPM spacing
        objs = [_circle(i * 20 % 512, (i * 15) % 384, i * 150) for i in range(16)]
        bm = self._make_beatmap(objs, bpm=200)
        feats = extract_features(bm)
        self.assertIn("stream_run_count", feats)
        self.assertGreater(feats["note_density_per_s"], 0)
        self.assertGreater(feats["dominant_bpm"], 0)
        self.assertIn("slider_count", feats)

    def test_feature_keys_present(self):
        objs = [_circle(i * 30, i * 20, i * 200) for i in range(10)]
        bm = self._make_beatmap(objs, bpm=150)
        feats = extract_features(bm)
        required = [
            "dominant_bpm", "note_density_per_s", "avg_distance", "max_distance",
            "distance_variance", "rhythm_cv", "dir_change_freq",
            "angle_variance_deg", "stream_run_count", "stream_note_ratio",
            "slider_complex_ratio",
        ]
        for key in required:
            self.assertIn(key, feats, f"Missing key: {key}")

    def test_mixed_objects(self):
        objs = [
            _circle(0, 0, 0),
            _slider(100, 100, 300, length=150),
            _circle(200, 200, 600),
            _slider(300, 100, 900, length=80, curve_pts=[(350,50),(380,100)]),
        ]
        bm = self._make_beatmap(objs, bpm=180)
        feats = extract_features(bm)
        self.assertEqual(feats["slider_count"], 2)
        self.assertEqual(feats["circle_count"], 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
