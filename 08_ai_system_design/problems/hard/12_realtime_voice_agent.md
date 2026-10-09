# 🔴 12. Real-Time Voice Agent (AI phone support / voice assistant)

📖 Concepts: [Serving](../../concepts/04_llm_serving_inference.md) · [Agents](../../concepts/03_agents_tool_use.md) · Related: [Communication protocols](../../../02_high_level_design/08_communication_protocols/)
⏱️ Try it yourself first: 45 minutes.

## 1. Requirements
**Functional:** the user speaks over the phone or in an app; the AI responds by voice, can be interrupted mid-sentence ("barge-in"), calls tools (booking, account lookup), and transfers to a human.
**Non-functional:** **voice-to-voice latency < ~800 ms** (people notice longer pauses), natural turn-taking, 10K concurrent calls, high audio quality, call recording with consent.

## 2. Two architectures
| Cascaded pipeline | Speech-to-speech model |
|---|---|
| STT → LLM → TTS, each streaming | One model takes audio in and produces audio out (e.g., Nova Sonic, GPT realtime models) |
| Modular: pick the best component for each step, easy to inspect text, use any LLM and tools | Lowest latency, keeps tone and emotion |
| More hops add latency | Less control and visibility, harder to apply text guardrails |

## 3. High-level design (cascaded)
```
Phone (PSTN/SIP) or app (WebRTC) → Media gateway (codec, jitter buffer, echo cancellation)
   → audio stream (20 ms frames) over WebSocket/gRPC → Voice session service (stateful, one per call)
        VAD (voice activity detection) + turn detection (end-of-utterance model)
        STREAMING STT → partial transcripts → final transcript
        LLM (streaming, small fast model; tools via function calling; conversation state)
        → sentence chunker → STREAMING TTS → audio frames back to caller
        barge-in: if VAD detects user speech while TTS is playing → stop TTS, cancel LLM, listen
   Tools: booking/CRM APIs; Human transfer via SIP REFER with conversation summary
   Recording + transcripts → storage (consent, PII redaction) → QA/evals
```

## 4. Deep dives
- **Latency budget** (example): VAD end-of-turn detection 200 ms + STT finalization 100 ms + LLM time to first token 250 ms + TTS first audio 150 ms + network 100 ms ≈ **800 ms**.
  - Tricks: stream every stage; start the LLM on a stable partial transcript; send TTS the first sentence immediately; filler phrases ("Let me check that…") while a tool runs; colocate the components in one region close to the telephony provider.
- **Turn-taking:** VAD silence thresholds plus a semantic end-of-turn model to avoid cutting the user off.
- **Barge-in:** full-duplex audio, echo cancellation so the bot doesn't hear itself, and instant cancellation of TTS and LLM generation.
- **Scaling:** sessions are stateful and long-lived, so use sticky routing and capacity planning by concurrent calls. GPUs serve STT/TTS/LLM in pools shared across sessions.
- **Reliability:** if a component fails, fall back ("Sorry, could you repeat that?") or transfer to a human.
- **Evaluation:** task completion, transfer rate, latency percentiles, interruption handling, word error rate (STT), and listener ratings for TTS naturalness.
- **Compliance:** call recording consent, PII redaction in transcripts, and an AI disclosure.

## ✅ Takeaways
**Streaming everything**, an explicit latency budget, VAD + turn detection, barge-in handling, and stateful sessions with sticky routing. Compare the cascaded and speech-to-speech approaches.

## 🧠 Test yourself: 5 interview questions

Answer each one out loud first, then click it to check.

<details>
<summary><b>Q1. Break down an 800 ms voice-to-voice latency budget.</b></summary>

For example: end-of-turn detection ~200 ms + STT finalization ~100 ms + LLM time to first token ~250 ms + TTS first audio ~150 ms + network ~100 ms. Everything must **stream**, and the stages overlap rather than run one after another.

</details>

<details>
<summary><b>Q2. How do you handle the user interrupting the bot (barge-in)?</b></summary>

Full-duplex audio with **echo cancellation** (so the bot doesn't hear itself), **VAD** detecting user speech while TTS plays, then **immediately stop the TTS and cancel the LLM generation**, keep what the user heard in the conversation history, and listen to the new utterance.

</details>

<details>
<summary><b>Q3. Cascaded STT→LLM→TTS vs a speech-to-speech model?</b></summary>

**Cascaded:** modular (best component for each stage), easy to inspect and log text, use any LLM and tools, and text guardrails apply. Each hop adds latency. **Speech-to-speech:** lowest latency and natural prosody and emotion, but less control and transparency. Text guardrails and tooling are harder to apply.

</details>

<details>
<summary><b>Q4. How do you avoid awkward silence while a tool call runs?</b></summary>

Speak a short **filler** immediately ("Let me check that for you…"), stream the partial answer as soon as possible, run tool calls in parallel where you can, and set timeouts with graceful fallback phrases.

</details>

<details>
<summary><b>Q5. How do you scale to 10,000 concurrent calls?</b></summary>

Each call is a **stateful, long-lived session**, so use sticky routing to session servers and plan capacity by concurrent calls. STT, LLM, and TTS run in shared, autoscaled GPU pools. Use regional deployment near the telephony provider, plus graceful degradation and human transfer when overloaded.

</details>
