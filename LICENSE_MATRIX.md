# LICENSE MATRIX

## Core Dependencies for UDCL

| Project | License | Commercial Use | Modification | Redistribution | Notice Required | Restrictions |
|---------|---------|---------------|-------------|---------------|----------------|-------------|
| spaCy | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | None |
| KGGen | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | None |
| Yjs | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | None |
| txtai | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Patent grant |
| mail-parser | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Patent grant |
| changedetection.io | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Patent grant |
| local-semantic-search | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Patent grant |
| Automerge | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | None |
| ElectricSQL | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Patent grant |
| DeepKE | MIT | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | None |
| Crawlee | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Patent grant |
| Reader (Jina) | Apache-2.0 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | Patent grant |
| keeper.sh | AGPL-3.0 | ⚠️ Network | ✅ Yes | ⚠️ Copyleft | ✅ Yes | Must release source if modified & served |
| PM4Py | GPL-3.0 | ⚠️ Network | ✅ Yes | ⚠️ Copyleft | ✅ Yes | Must release source if modified & served |
| Opensemanticsearch | GPL-3.0 | ⚠️ Network | ✅ Yes | ⚠️ Copyleft | ✅ Yes | Must release source if modified & served |

## License Strategy

### For Core System (AGPL-compatible)
- Use MIT/Apache-2.0 libraries as primary building blocks
- For GPL/AGPL dependencies: use as separate microservices or avoid
- The UDCL core itself: **Apache-2.0** (maximizes adoption)

### For Connectors
- Each connector is independent — can use different licenses
- Email connector: MIT (based on mail-parser)
- Document connector: Apache-2.0 (based on doc tools)
- Calendar connector: Avoid AGPL deps, implement fresh or use MIT alternatives
- Web connector: Apache-2.0 (based on Crawlee/Reader)

### Avoid These Dependencies
| Project | License | Why Avoid |
|---------|---------|-----------|
| PM4Py | GPL-3.0 | Contamination risk for core |
| keeper.sh | AGPL-3.0 | Network copyleft obligation |
| Apromore | Community Ed | Unclear commercial terms |

### Safe Alternative Approaches
| Instead of | Use | License |
|-----------|-----|---------|
| PM4Py | Custom process mining with PM4Py algorithms reimplemented | Apache-2.0 |
| keeper.sh | Custom calendar sync using iCal libraries | MIT |
| Apromore | Custom visualization with D3.js | ISC |

## Compliance Checklist

- [ ] All MIT/Apache-2.0 deps: Include NOTICE file
- [ ] All GPL/AGPL deps: Only in separate processes, not linked
- [ ] Core system: Apache-2.0 license header in all files
- [ ] Network deployment: No copyleft contamination
- [ ] Attribution: All third-party licenses preserved
- [ ] Patent: Apache-2.0 patent grant covers all Apache deps
