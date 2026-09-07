# Nexus - Self-Healing Integration Engine

> Detect schema drift. Generate transforms. Self-heal integrations.

## What is Nexus?

Nexus is an open-source self-healing integration layer that:

1. **Detects** schema drift between API versions
2. **Classifies** changes (breaking, type change, rename, added, removed)
3. **Matches** semantically similar fields across different naming conventions
4. **Generates** Python transform functions automatically
5. **Creates** contract tests for every transform
6. **Learns** from every incident in a known-fixes database
7. **Monitors** integration health across all your systems

## Why Nexus?

- **70% of automation projects fail** due to tool fragmentation
- **Workers waste 25%** of their workweek on manual repetitive tasks
- **Schema drift** silently breaks integrations without triggering errors
- **Existing tools** (Zapier, Make, MuleSoft) don't self-heal

Nexus is the **Integration Immune System** - it detects problems and fixes them automatically.

## Quick Start

```bash
# No dependencies needed - pure Python
python main.py detect tests/schema_v1.json tests/schema_v2.json
python main.py heal tests/schema_v1.json tests/schema_v2.json -o output/
python main.py score tests/schema_v1.json tests/schema_v2.json
```

## How It Works

```
API Schema v1 ──┐
                ├──→ DETECT ──→ HEAL ──→ transforms.py
API Schema v2 ──┘                              test_transforms.py
                                               heal_plan.json
```

## Example Output

```python
# Auto-generated transform
def transform_amount(record: dict) -> dict:
    """Rename: amount -> total"""
    if "amount" in record:
        record["total"] = record.pop("amount")
    return record

# Auto-generated test
def test_amount_renamed_to_total():
    old_record = {"amount": 100}
    new_record = transform_amount(old_record)
    assert "total" in new_record
    assert new_record["total"] == 100
    assert "amount" not in new_record
```

## Supported Formats

- OpenAPI 2/3
- JSON Schema
- GraphQL SDL
- Sample JSON objects

## Architecture

```
core/
├── schema.py          # Data structures
├── loader.py          # Schema parsers
├── known_fixes.py     # Known fixes database
└── monitor.py         # Health monitor
detectors/
└── drift.py           # Drift detection
healers/
└── self_healer.py     # Transform generation
```

## License

MIT
