from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_windows_env_acl_verification_requires_exact_protected_rules() -> None:
    powershell = (ROOT / "scripts/bootstrap.ps1").read_text(encoding="utf-8")

    assert "$effectiveAcl.AreAccessRulesProtected" in powershell
    assert "Environment file ACL still inherits access rules" in powershell
    assert "$requiredSidRights" in powershell
    assert "FileSystemRights]::FullControl" in powershell
    assert "Environment file ACL is missing required FullControl" in powershell
    assert "Environment file ACL grants access to an unexpected identity" in powershell
    assert powershell.index("$effectiveAcl = Get-Acl") < powershell.index("Invoke-Compose config --quiet")
