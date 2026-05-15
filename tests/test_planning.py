import sys
from pathlib import Path
import unittest

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from audiofix.core.planning import build_output_plan


class BuildOutputPlanTests(unittest.TestCase):
    def test_builds_numbered_outputs_with_db_steps(self) -> None:
        plan = build_output_plan(
            source_path=Path("levelup2.ogg"),
            output_dir=Path("out"),
            db_offset=-3.0,
            step_count=3,
            db_interval=-3.0,
        )

        self.assertEqual([item.index for item in plan], [0, 1, 2])
        self.assertEqual([item.gain_db for item in plan], [-3.0, -6.0, -9.0])
        self.assertEqual(
            [item.output_path for item in plan],
            [
                Path("out/levelup2_0.ogg"),
                Path("out/levelup2_1.ogg"),
                Path("out/levelup2_2.ogg"),
            ],
        )

    def test_rejects_zero_steps(self) -> None:
        with self.assertRaises(ValueError):
            build_output_plan(
                source_path=Path("source.ogg"),
                output_dir=Path("out"),
                db_offset=0.0,
                step_count=0,
                db_interval=-3.0,
            )


if __name__ == "__main__":
    unittest.main()
