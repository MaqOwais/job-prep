# 8-Week Study Plan

**Daily time:** about 3–4 hours on weekdays and 5–6 hours on weekends.
**Daily routine:**

| Block | Time | What |
|---|---|---|
| 🧩 Coding | 90 min | 2–3 problems from the week's pattern (Easy first, then Medium) |
| 🏗️ System design | 60 min | 1 concept module, or 1 design problem from week 4 on |
| 🧠 Fundamentals / LLD | 30 min | 1 section from [04_cs_fundamentals](../04_cs_fundamentals/) or [03_low_level_design](../03_low_level_design/) |
| 🗣️ Behavioral | 15 min | Write or rehearse 1 STAR story out loud |
| 🔁 Review | 15 min | Redo 1 problem you failed 3 or 7 days ago |

> **If your interview is sooner**, skip to the [2-week crash plan](#-2-week-crash-plan) at the bottom.

---

## Phase 1: Foundations (Weeks 1–2), Easy level

### Week 1
| Day | Coding | System design | Fundamentals / Behavioral |
|---|---|---|---|
| 1 | [Python toolkit](../01_coding/00_python_toolkit.md) + [How to solve](../01_coding/README.md) 🧱 [Step-by-step HLD fundamentals](../02_high_level_design/00_step_by_step_fundamentals/README.md): steps 1–7 (single server → CDN) | Write "Tell me about yourself" |
| 2 | [Arrays & Hashing](../01_coding/01_arrays_hashing/): all Easy 🧱 [Step-by-step HLD](../02_high_level_design/00_step_by_step_fundamentals/README.md): steps 8–13 + the [10-minute drill](../02_high_level_design/00_step_by_step_fundamentals/13_putting_it_together.md) | [OOP](../04_cs_fundamentals/05_oop.md) |
| 3 | Arrays & Hashing: 3 Medium | [Fundamentals module](../02_high_level_design/01_fundamentals/): scalability, latency, CAP, consistency, availability | Story #1 |
| 4 | [Two Pointers](../01_coding/02_two_pointers/): Easy + 2 Medium | [Estimation](../02_high_level_design/10_estimation/) | [Networking](../04_cs_fundamentals/02_networking.md), part 1 |
| 5 | [Sliding Window](../01_coding/03_sliding_window/): Easy + 2 Medium | [DNS & CDN](../02_high_level_design/02_dns_cdn/) | Story #2 |
| 6 | [Stack](../01_coding/04_stack/): Easy + 3 Medium | [Load balancing & reverse proxy](../02_high_level_design/03_load_balancing_reverse_proxy/) | Networking, part 2 |
| 7 | 🔁 Redo every failed problem from the week + 1 timed mock (2 problems in 45 min) | [Interview framework](../02_high_level_design/11_interview_framework/) + [HLD cheat sheet](../02_high_level_design/00_hld_cheatsheet.md); redo the 10-minute drill | Story #3 |

### Week 2
| Day | Coding | System design | Fundamentals / Behavioral |
|---|---|---|---|
| 8 | [Binary Search](../01_coding/05_binary_search/): Easy + 2 Medium | [Application layer & microservices](../02_high_level_design/04_application_layer_microservices/) | [Operating systems](../04_cs_fundamentals/01_operating_systems.md), part 1 |
| 9 | [Linked List](../01_coding/06_linked_list/): Easy + 2 Medium | [Databases](../02_high_level_design/05_databases/): SQL, replication | OS, part 2 |
| 10 | [Trees](../01_coding/07_trees/): all Easy | Databases: sharding, federation, NoSQL | Story #4 |
| 11 | Trees: 4 Medium | [Caching](../02_high_level_design/06_caching/) | [Databases & SQL](../04_cs_fundamentals/03_databases_sql.md) |
| 12 | [Heap](../01_coding/09_heap_priority_queue/): Easy + 2 Medium | [Asynchronism & queues](../02_high_level_design/07_asynchronism_queues/) | Story #5 |
| 13 | [Tries](../01_coding/08_tries/): Medium | [Communication protocols](../02_high_level_design/08_communication_protocols/) + [Security](../02_high_level_design/09_security/) | [Concurrency](../04_cs_fundamentals/04_concurrency.md) |
| 14 | 🔁 Redo failed problems + timed mock | 📝 Do the primer's [Anki flashcards](https://github.com/donnemartin/system-design-primer#anki-flashcards) | Story #6 |

---

## Phase 2: Core (Weeks 3–5), Medium level

### Week 3
| Day | Coding | System design | LLD / Behavioral |
|---|---|---|---|
| 15 | [Backtracking](../01_coding/10_backtracking/): 3 Medium | 🟢 [URL shortener / Pastebin](../02_high_level_design/12_problems/easy/01_url_shortener_pastebin.md) | [LLD approach](../03_low_level_design/README.md) |
| 16 | Backtracking: 3 Medium | 🟢 [Rate limiter](../02_high_level_design/12_problems/easy/02_rate_limiter.md) | LLD: [LRU cache](../03_low_level_design/problems/lru_cache.py) |
| 17 | [Graphs](../01_coding/11_graphs/): Easy + 3 Medium (DFS/BFS) | 🟢 [Key-value cache](../02_high_level_design/12_problems/easy/03_key_value_cache.md) | Story #7 |
| 18 | Graphs: 3 Medium (topological sort, union-find) | 🟢 [Scale to millions on AWS](../02_high_level_design/12_problems/easy/04_scale_to_millions_aws.md) | LLD: [Parking lot](../03_low_level_design/problems/parking_lot.py) |
| 19 | Graphs: 2 Medium | 🟢 [Unique ID generator](../02_high_level_design/12_problems/easy/05_unique_id_generator.md) | [Design patterns](../03_low_level_design/design_patterns.md) |
| 20 | Mixed: 3 random Medium (from patterns done so far) | Re-draw 2 easy designs from memory (35 min each) | Story #8 |
| 21 | 🔁 Redo failed + **mock interview #1** (with a friend or Pramp) | 🔁 | 🔁 |

### Week 4
| Day | Coding | System design | LLD / Behavioral |
|---|---|---|---|
| 22 | [1-D DP](../01_coding/13_dp_1d/): Easy + 2 Medium | 🟡 [Twitter / news feed](../02_high_level_design/12_problems/medium/06_twitter_news_feed.md) | LLD: [Deck of cards](../03_low_level_design/problems/deck_of_cards.py) |
| 23 | 1-D DP: 3 Medium | 🟡 [Web crawler](../02_high_level_design/12_problems/medium/07_web_crawler.md) | Story #9 |
| 24 | 1-D DP: 2 Medium | 🟡 [Chat system](../02_high_level_design/12_problems/medium/08_chat_system.md) | LLD: [Online chat](../03_low_level_design/problems/online_chat.py) |
| 25 | [2-D DP](../01_coding/14_dp_2d/): 3 Medium | 🟡 [Notification system](../02_high_level_design/12_problems/medium/09_notification_system.md) | Story #10 |
| 26 | 2-D DP: 2 Medium | 🟡 [Typeahead / autocomplete](../02_high_level_design/12_problems/medium/10_typeahead_autocomplete.md) | LLD: [Call center](../03_low_level_design/problems/call_center.py) |
| 27 | Mixed: 3 Medium | 🔁 Re-draw Twitter + Chat from memory | Story #11 |
| 28 | 🔁 + **mock #2** | 🔁 | 🔁 |

### Week 5
| Day | Coding | System design | LLD / Behavioral |
|---|---|---|---|
| 29 | [Greedy](../01_coding/15_greedy/): Easy + 3 Medium | 🟡 [Social graph](../02_high_level_design/12_problems/medium/11_social_graph.md) | LLD: [Hash map](../03_low_level_design/problems/hash_map.py) |
| 30 | [Intervals](../01_coding/16_intervals/): all Medium | 🟡 [Sales rank](../02_high_level_design/12_problems/medium/12_sales_rank.md) | Story #12 |
| 31 | [Advanced graphs](../01_coding/12_advanced_graphs/): Dijkstra, MST | 🟡 [Personal finance (Mint)](../02_high_level_design/12_problems/medium/13_mint_personal_finance.md) | LLD: [Elevator](../03_low_level_design/problems/elevator.py) |
| 32 | [Math & bits](../01_coding/17_math_bits/): Easy + 2 Medium | 🟡 [Search engine / inverted index](../02_high_level_design/12_problems/medium/14_search_engine.md) | Story #13 |
| 33 | Mixed: 4 Medium, timed (25 min each) | 🟢 [Leaderboard](../02_high_level_design/12_problems/easy/20_leaderboard.md) + 🟡 [Instagram](../02_high_level_design/12_problems/medium/21_instagram.md) | Fundamentals review: [quiz](../04_cs_fundamentals/README.md#-rapid-fire-quiz) |
| 34 | Mixed | 🟡 [Dropbox](../02_high_level_design/12_problems/medium/22_dropbox_file_sync.md) + 🟡 [Ticketmaster](../02_high_level_design/12_problems/medium/23_ticketmaster.md) | Story #14 |
| 35 | 🔁 + **mock #3** | 🔁 | 🔁 |

---

## Phase 3: Advanced & mocks (Weeks 6–8), Hard level

### Week 6
| Day | Coding | System design |
|---|---|---|
| 36 | Hard: Trapping Rain Water, Minimum Window Substring | 🔴 [YouTube / video streaming](../02_high_level_design/12_problems/hard/15_youtube_video_streaming.md) |
| 37 | Hard: Largest Rectangle in Histogram, Sliding Window Maximum | 🔴 [Uber / ride sharing](../02_high_level_design/12_problems/hard/16_uber_ride_sharing.md) |
| 38 | Hard: Merge k Sorted Lists, Median from Data Stream | 🔴 [Distributed key-value store](../02_high_level_design/12_problems/hard/17_distributed_kv_store.md) |
| 39 | Hard: Word Ladder, Word Search II | 🔴 [Google Docs / collaborative editing](../02_high_level_design/12_problems/hard/18_google_docs.md) |
| 40 | Hard: Edit Distance (Medium), Longest Increasing Path | 🔴 [Payment system](../02_high_level_design/12_problems/hard/19_payment_system.md) |
| 41 | Hard: Binary Tree Max Path Sum, Serialize/Deserialize Tree | 🤖 [Enterprise RAG platform](../08_ai_system_design/problems/medium/05_enterprise_rag_platform.md) |
| 42 | 🔁 + **full mock loop** (coding + SD + behavioral back to back) | |

### Week 7: 🤖 AI system design track + weak spots
Do this week if you're targeting AI companies, ML roles, or AWS (Bedrock / Startups SA). Otherwise, spend it on weak spots.

| Day | AI system design ([08_ai_system_design](../08_ai_system_design/)) | Coding |
|---|---|---|
| 43 | Concepts: [LLM fundamentals](../08_ai_system_design/concepts/01_llm_fundamentals.md) + [RAG](../08_ai_system_design/concepts/02_rag_retrieval.md) · 🟢 [Customer support chatbot](../08_ai_system_design/problems/easy/01_customer_support_chatbot.md) | 2 Medium (weakest pattern) |
| 44 | Concepts: [Agents](../08_ai_system_design/concepts/03_agents_tool_use.md) · 🟢 [Semantic search](../08_ai_system_design/problems/easy/02_semantic_search.md) + [Content moderation](../08_ai_system_design/problems/easy/03_content_moderation.md) | 2 Medium |
| 45 | Concepts: [Serving](../08_ai_system_design/concepts/04_llm_serving_inference.md) · 🟡 [LLM gateway](../08_ai_system_design/problems/medium/04_llm_gateway.md) | 2 Medium |
| 46 | Concepts: [Evaluation](../08_ai_system_design/concepts/05_evaluation_observability.md) + [Safety](../08_ai_system_design/concepts/06_safety_security.md) · 🟡 [Multi-agent research assistant](../08_ai_system_design/problems/medium/08_multi_agent_research_assistant.md) (tell it as your research story) | 2 Medium |
| 47 | Concepts: [Classic ML](../08_ai_system_design/concepts/07_classic_ml_system_design.md) · 🟡 [Recommendation system](../08_ai_system_design/problems/medium/07_recommendation_system.md) + [AI coding assistant](../08_ai_system_design/problems/medium/06_ai_coding_assistant.md) | 1 Hard |
| 48 | Concepts: [AWS GenAI stack](../08_ai_system_design/concepts/08_aws_genai_stack.md) · 🔴 [AI agent platform](../08_ai_system_design/problems/hard/11_agent_platform.md) | 1 Hard |
| 49 | 🔴 [LLM inference platform](../08_ai_system_design/problems/hard/09_llm_inference_platform.md) · mock: one AI design question, 45 min | 🔁 |

Leftover hard problems ([fine-tuning platform](../08_ai_system_design/problems/hard/10_fine_tuning_platform.md), [voice agent](../08_ai_system_design/problems/hard/12_realtime_voice_agent.md)) go in Week 8 if time allows.

**Weak spots (also this week):**
- Open the [progress tracker](progress_tracker.md). Whichever pattern has the lowest ✅ count gets 2 more days.
- 2 timed coding mocks + 2 SD mocks this week.
- Finish all 16 behavioral stories in the [story bank](../05_behavioral/story_bank.md).

### Week 8: Polish
- **HLD extras, picked by target company** (see the [cheat sheet table](../02_high_level_design/00_hld_cheatsheet.md#8-most-asked-hld-questions-by-company-as-commonly-reported-use-these-to-prioritize)): [E-commerce checkout](../02_high_level_design/12_problems/medium/24_ecommerce_checkout.md) (Amazon!), [Yelp](../02_high_level_design/12_problems/medium/25_proximity_service_yelp.md), [Job scheduler](../02_high_level_design/12_problems/hard/26_distributed_job_scheduler.md), [Metrics](../02_high_level_design/12_problems/hard/27_metrics_monitoring.md), [Kafka](../02_high_level_design/12_problems/hard/28_distributed_message_queue.md), [Stock exchange](../02_high_level_design/12_problems/hard/29_stock_exchange.md).
- Company-specific prep (e.g., [AWS SA plan](../06_company_specific/aws_startup_sa/AWS_Associate_Startup_SA_Prep_Plan.md)).
- Redo the **"must-know 40"** listed in [01_coding/README.md](../01_coding/README.md#-must-know-40-redo-these-before-every-interview).
- Day before: light review only, then use the [interview-day checklist](interview_day_checklist.md).

---

## ⚡ 2-week crash plan
| Day | Coding (3–4 problems) | System design |
|---|---|---|
| 1 | Arrays & Hashing, Two Pointers | [Step-by-step HLD fundamentals](../02_high_level_design/00_step_by_step_fundamentals/README.md) (all 13 steps) + Estimation |
| 2 | Sliding Window, Stack | DNS/CDN, Load balancing, Caching |
| 3 | Binary Search, Linked List | Databases (all) |
| 4 | Trees | Async/queues, Communication, Security |
| 5 | Heap, Tries | URL shortener + Rate limiter |
| 6 | Graphs (BFS/DFS) | Key-value cache + Scale on AWS |
| 7 | Graphs (topo sort, union-find) | Mock #1 |
| 8 | Backtracking | Twitter + Chat |
| 9 | 1-D DP | Notification + Typeahead |
| 10 | 2-D DP | Web crawler + YouTube |
| 11 | Greedy + Intervals | Uber + Distributed KV |
| 12 | Must-know 40 redo, part 1 | Mock #2 |
| 13 | Must-know 40 redo, part 2 | Re-draw 3 favorites |
| 14 | Rest + checklist | Rest |
