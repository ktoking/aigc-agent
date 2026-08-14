import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ark_video.py"
SPEC = importlib.util.spec_from_file_location("ark_video", MODULE_PATH)
assert SPEC and SPEC.loader
ark_video = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ark_video
SPEC.loader.exec_module(ark_video)


class ArkVideoReferenceMapTest(unittest.TestCase):
    def test_multiple_digital_humans_require_names(self) -> None:
        with self.assertRaisesRegex(ark_video.ArkVideoError, "explicit role binding"):
            ark_video.validate_digital_humans([
                "asset://asset-xu",
                "asset://asset-gu",
            ])

    def test_named_digital_humans_preserve_input_order(self) -> None:
        references = ark_video.validate_digital_humans([
            "许砚=asset://asset-xu",
            "顾承泽=asset://asset-gu",
        ])

        self.assertEqual([reference.name for reference in references], ["许砚", "顾承泽"])
        self.assertEqual(
            [reference.asset_url for reference in references],
            ["asset://asset-xu", "asset://asset-gu"],
        )

    def test_reference_map_matches_actual_payload_order(self) -> None:
        digital_humans = ark_video.validate_digital_humans([
            "许砚=asset://asset-xu",
            "顾承泽=asset://asset-gu",
        ])
        prompt = "\n".join([
            "数字人身份锁：许砚 asset-xu；顾承泽 asset-gu。",
            "参考图1：上一段尾帧，只锁定连续性。",
            "参考图2：别墅控制室，只锁定场景。",
        ])

        reference_map = ark_video.validate_prompt_reference_map(
            prompt,
            digital_humans,
            [Path("last-frame.png"), Path("control-room.png")],
            [],
            ["上一段尾帧", "别墅控制室"],
            [],
        )

        self.assertEqual(
            [(reference["kind"], reference["label"]) for reference in reference_map],
            [
                ("digital_human", "许砚"),
                ("digital_human", "顾承泽"),
                ("local_image", "上一段尾帧"),
                ("local_image", "别墅控制室"),
            ],
        )

    def test_reference_map_rejects_omitted_tail_frame(self) -> None:
        digital_humans = ark_video.validate_digital_humans([
            "许砚=asset://asset-xu",
            "顾承泽=asset://asset-gu",
        ])
        prompt = "\n".join([
            "数字人身份锁：许砚 asset-xu；顾承泽 asset-gu。",
            "参考图1：别墅控制室，只锁定场景。",
        ])

        with self.assertRaisesRegex(ark_video.ArkVideoError, "exact API image order"):
            ark_video.validate_prompt_reference_map(
                prompt,
                digital_humans,
                [Path("last-frame.png"), Path("control-room.png")],
                [],
                ["上一段尾帧", "别墅控制室"],
                [],
            )

    def test_exact_api_numbering_includes_digital_humans(self) -> None:
        digital_humans = ark_video.validate_digital_humans([
            "顾承泽=asset://asset-gu",
            "许砚=asset://asset-xu",
        ])
        prompt = "\n".join([
            "参考图1：顾承泽固定数字人。",
            "参考图2：许砚固定数字人。",
            "参考图3：别墅控制室。",
        ])

        reference_map = ark_video.validate_prompt_reference_map(
            prompt,
            digital_humans,
            [Path("control-room.png")],
            [],
            ["别墅控制室"],
            [],
        )

        self.assertEqual(
            [reference["label"] for reference in reference_map],
            ["顾承泽", "许砚", "别墅控制室"],
        )

    def test_next_segment_requires_preceding_passed_qa(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            episode = Path(temp_dir)
            segment_01 = episode / "segment_01_00-15s"
            segment_02 = episode / "segment_02_15-30s"
            (segment_01 / "output").mkdir(parents=True)
            segment_02.mkdir()

            with self.assertRaisesRegex(ark_video.ArkVideoError, "has not passed visual QA"):
                ark_video.require_previous_segment_qa(segment_02)

            qa_path = segment_01 / "output" / "video-qa.json"
            qa_path.write_text(json.dumps({"status": "rejected"}), encoding="utf-8")
            with self.assertRaisesRegex(ark_video.ArkVideoError, "QA status is rejected"):
                ark_video.require_previous_segment_qa(segment_02)

            qa_path.write_text(json.dumps({"status": "passed"}), encoding="utf-8")
            ark_video.require_previous_segment_qa(segment_02)


if __name__ == "__main__":
    unittest.main()
