from pathlib import Path

REQUIRED = [
    "README.md",
    "AGENTS.md",
    "plans/master-plan.md",
    "plans/implement.md",
    "plans/documentation.md",
    "docs/01-architecture.md",
    "docs/03-evaluation.md",
    "CITATION.cff",
    "codemeta.json",
    "SECURITY.md",
    "CODEOWNERS",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/workflows/ci.yml",
]

def main() -> int:
    root = Path(__file__).resolve().parent.parent
    missing = [p for p in REQUIRED if not (root / p).exists()]
    if missing:
        print("Missing required files:")
        for item in missing:
            print(f" - {item}")
        return 1
    print("Scaffold validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
