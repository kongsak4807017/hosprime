from backend.app.engineering_loop.contracts import LoopStage
from backend.app.engineering_loop.run_store import LoopRunStore


def test_loop_run_package_and_next_stage(tmp_path):
    store = LoopRunStore(tmp_path)
    run_dir = store.create_run(
        task="Improve memory graph",
        objective="Use stored notes instead of mock data",
        owner="product-team",
    )

    assert store.load(run_dir).stage == LoopStage.CAPTURED
    assert (run_dir / "manifest.json").exists()
    assert (run_dir / "11-learning.md").exists()
    assert store.advance(run_dir, LoopStage.BASELINED).stage == LoopStage.BASELINED


def test_loop_cannot_skip_required_stage(tmp_path):
    store = LoopRunStore(tmp_path)
    run_dir = store.create_run(
        task="Validate stage order",
        objective="Keep evidence in sequence",
        owner="qa-team",
    )

    try:
        store.advance(run_dir, LoopStage.TESTING)
    except ValueError as exc:
        assert "invalid loop transition" in str(exc)
    else:
        raise AssertionError("stage order was not enforced")
