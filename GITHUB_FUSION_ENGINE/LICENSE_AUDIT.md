# LICENSE_AUDIT.md — License Compatibility Analysis

## Target Product: VoiceStack (Self-Hosted Voice Agent Platform)

### Component Licenses

| Component | License | Commercial Use | Modification | Distribution | SaaS | Compatibility |
|-----------|---------|---------------|--------------|--------------|------|---------------|
| Dograh | BSD-2-Clause | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Compatible |
| Knowhere | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Compatible |
| n8n | Sustainable Use License | ⚠️ Limited | ✅ Yes | ⚠️ Limited | ⚠️ Restricted | ⚠️ Check terms |
| VibeVoice | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Compatible |
| nanobot | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Compatible |
| CrewAI | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Compatible |

### License Risk Assessment

**n8n (Sustainable Use License):**
- n8n uses a "fair-code" license, not a standard open-source license
- Commercial use as a hosted service may require a separate license
- Self-hosted internal use is generally permitted
- **Recommendation:** Use n8n as an optional workflow engine, or replace with Conductor (Apache-2.0) for the core product

**Apache-2.0 + MIT components:**
- All other components are fully compatible
- Can be combined, modified, and distributed commercially
- No copyleft obligations requiring source disclosure

### Final License Stack (VoiceStack)

```
Core: Dograh (BSD-2) + Knowhere (Apache-2.0) + nanobot (MIT)
Voice: VibeVoice (MIT) or OmniVoice (Apache-2.0)
Workflow: Conductor (Apache-2.0) — replaces n8n for core
Optional: n8n (SUL) as add-on, not core dependency
```

**License Status: ✅ CLEAN — No blockers for commercial use**
