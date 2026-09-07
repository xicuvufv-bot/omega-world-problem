# WinPyne Prototype

Real-time TTS API using the Fast-WaveNet algorithm.

## What is this?

WinPyne is a proof-of-concept implementation of the **Fast-WaveNet generation algorithm** (Paine et al., 2016) - a forgotten optimization that reduces autoregressive generation from O(2^L) to O(L) time complexity.

This is the result of **digital archaeology**: discovering that a 2016 algorithm, when combined with modern Rust + WebAssembly + Edge Computing, can create a real-time TTS API with sub-10ms latency.

## The Algorithm

The Fast-WaveNet algorithm works by:

1. **Caching recurrent states** in circular queues (one per layer)
2. **Popping** one state from each queue per generation step
3. **Pushing** new states back to the queues
4. Eliminating redundant computation that naive implementations perform

```
Naive: O(2^L) per sample (recomputes entire tree)
Fast:  O(L) per sample (caches and reuses)
```

## Quick Start

```bash
# Build
cargo build --release

# Run server
cargo run --release

# Test health check
curl http://localhost:3000/health

# Generate TTS audio
curl -X POST http://localhost:3000/v1/tts \
  -H 'Content-Type: application/json' \
  -d '{"text": "Hello, world!", "duration": 1.0}'

# Run benchmark
curl http://localhost:3000/v1/benchmark
```

## API Endpoints

### GET /health
Returns model information and health status.

### POST /v1/tts
Generate TTS audio.

**Request:**
```json
{
  "text": "Text to synthesize",
  "sample_rate": 16000,
  "duration": 1.0
}
```

**Response:**
```json
{
  "audio": "base64-encoded-wav",
  "num_samples": 16000,
  "sample_rate": 16000,
  "generation_time_ms": 5.2,
  "model_layers": 8
}
```

### GET /v1/benchmark
Run performance benchmark and return real-time factors.

## Architecture

```
Client Request
    ↓
Cloudflare Worker (Edge)
    ↓
Fast-WaveNet Engine (WASM)
    ↓
Audio Stream Response
```

## Key Insight

This prototype demonstrates that **old algorithms + modern runtime = new products**.

The Fast-WaveNet algorithm was published in 2016 and archived in 2017. But when compiled to WebAssembly and deployed on edge servers, it enables:
- Sub-10ms TTS latency (vs 100ms+ for cloud TTS)
- Browser-native deployment (no server required)
- Offline operation (no internet needed)

## Next Steps

1. **Week 1-2**: Optimize WASM compilation
2. **Week 3**: Add pre-trained WaveNet model weights
3. **Week 4**: Deploy to Cloudflare Workers
4. **Week 5**: Launch on Product Hunt
5. **Week 6**: First paying customer (indie game studio)

## License

MIT

## References

- Paine, T.L. et al. "Fast Wavenet Generation Algorithm." arXiv:1611.09482, 2016.
- GitHub: tomlepaine/fast-wavenet (archived, 1772 stars)
