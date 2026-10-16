# FOLD Reflex Path — System-One-Inspired Fast Decision Hypothesis Report

作成日: 2026-09-19  
状態: **研究仮説 / 文献検証 / FOLD適合性分析 / 実験計画。実装済み機能・性能実証済み機能・現行v0.5正規仕様の変更ではない。**

関連文書:

- `AGENTS.md`
- `docs/architecture-v0.5.md`
- `docs/theory-v0.5.md`
- `docs/development-roadmap-v0.5.md`
- `docs/information-acquisition.md`
- `docs/shared-basis-auto-module-partition-report.md`

本書は既存の `C###` 実験系列とは別の研究トラックとして扱う。  
既存C系列のformal status / Gate statusを変更しない。

---

## 1. 目的

TypeSafe AIのJevが示している、

> unstructured state -> typed probabilistic decision

という「文字列生成ではなく、限定された判断を高速に直接返す」考え方から着想し、FOLD内部に **Reflex Path** を持たせる価値を検証する。

ここでいうReflex Pathは、

- 自由文生成を伴わない
- 出力候補が事前に型・集合として限定される
- probability / uncertaintyを明示的に持つ
- 十分に簡単な判断では深い計算を省略できる
- 不確実・高リスク・分布外では通常推論へdeferする

高速判断経路を指す。

目的はJevを模倣することではない。Jevの内部アーキテクチャやRLCDの詳細は公開情報だけでは再現できないため、FOLDでは既知研究と現行v0.5設計から独立に検証可能な形へ落とす。

---

## 2. 先に結論

### 2.1 結論

**Reflex PathはFOLDの研究候補として強く支持できる。**

ただし支持されるのは、

> confidenceが高ければ即行動する単純なearly-exit

ではない。

第一候補は、

> **bounded typed decision + calibrated selective risk + defer/slow-path + consequence-aware execution gate**

である。

概念図:

```text
Input / Evidence
      |
      v
Shared Core / Working State
      |
      +-------------------------------+
      |                               |
      v                               v
Reflex Probe                     Normal FOLD Path
typed bounded decision           compute / acquire / reason
probability / defer                    |
      |                               |
      +-- safe + accepted ------------+
      |
      +-- uncertain / OOD / risky ---> Slow Path
```

さらにruntime側で、

```text
new evidence revision
      |
      v
Reflex interrupt probe
      |
      +-- stale state detected -> cancel / re-evaluate
      +-- no material change   -> continue
```

というinterrupt用途も研究価値がある。

### 2.2 現時点で正規仕様へ入れない

まだ以下は実証されていない。

- FOLDの中間stateに浅い段階で十分なdecision informationが存在するか
- Reflex用auxiliary lossが主LM品質を傷つけないか
- FOLDの共有コア・反復構造で本当にwall-clockが短くなるか
- calibrationがOOD / domain shiftでも十分維持されるか
- interrupt判定がstale actionを減らすか
- Shared Basis圧縮後もdecision flipが許容範囲か

したがって、**まずRP系列で潰す**。

---

## 3. 外部一次・既存研究から確認できること

## 3.1 TypeSafe AI / Jev

TypeSafe AIは2026-09-14公開のJev紹介で、System One Modelを、

- unstructured stateを入力
- type-safe structured valuesを出力
- probability / confidenceを付与
- string generationを行わない
- outputsをparallelに生成
- workflow内のclassify / route / score / branch向け

として説明している。

同社workflow evalでは主に、

- yes/no型
- Choice型
- Score型

の狭い判断をworkflow中に配置している。

また、TypeSafeはJevの速度・価格・workflow性能について大きな改善値を報告しているが、これらは**ベンダー自身の評価**であり、FOLD設計の性能根拠としてそのまま採用しない。

重要なのはベンチマーク数値ではなく、

> **自由文生成を捨てることで、software-facing decisionを直接最適化する**

という問題設定である。

### 注意: "zero hallucinations" の解釈

TypeSafeはJevについて型安全性と「hallucinationしない」という表現を使っている。

FOLDではこの表現をそのまま使わない。

候補集合をschema / enum / maskで物理的に限定すれば、

- 不正なtype
- 存在しないaction ID
- schema外の文字列

は構造上防げる。

しかし、

```text
有効な型の中から
間違った選択肢を高確率で選ぶ
```

ことは依然あり得る。

したがってFOLDでは、

```text
type validity != semantic correctness
```

を明示する。

---

## 3.2 Early Exitは既に成立した研究領域

Reflex Pathの「簡単な入力では浅い段階で終了する」という部分自体は新規ではない。

代表例:

- BranchyNet: early branch classifierで簡単な例を早期終了
- DeeBERT: BERTの中間層からdynamic early exit
- FastBERT: self-distillation + adaptive inference
- CALM: autoregressive language modelで入力・generation timestepごとに計算量を適応
- LayerSkip: 中間層early exitと後段によるverification / correction
- PonderNet: 問題難度に応じて計算step数を学習
- Mixture-of-Depths: token / layerごとにcompute allocationを動的化

これらから、

> **すべての入力に最大計算量を使う必要はない**

という中心前提は十分妥当である。

一方、既存研究の多くはTransformer / classifier / token generation上の結果であり、FOLDの共有state-update coreへ自動的に一般化できるわけではない。

---

## 3.3 Confidenceはそのまま信用できない

Guo et al.のcalibration研究を含め、modern neural networkのsoftmax confidenceが実際のcorrectness probabilityと一致しないことは既知である。

よって、

```text
p_max > 0.98
=> reflex execute
```

という固定ルールだけでは不十分。

FOLDでは最低でも、

- held-out calibration
- class/action別calibration
- selective risk
- OOD / shift slice
- consequence別threshold
- defer coverage

を評価する。

---

## 4. FOLD v0.5との適合性

現行v0.5はすでに、

```text
Shared state-update core
+
Selected compressed modules
+
Controller
  -> ANSWER
  -> COMPUTE
  -> ACQUIRE
+
bounded internal steps
```

を第一候補としている。

V5-Dでは、

```text
ANSWER / COMPUTE(module, steps)
```

の動的routingを研究する。

V5-Eでは、

```text
PARTIAL_ANSWER
READ_MEMORY
RETRIEVE
OBSERVE
ASK_USER
STOP_UNRESOLVED
```

を追加する。

したがってReflex Pathは別システムとして横付けするより、

> **Controller decisionを浅いstateから直接予測できるか**

という形で接続するのが最も自然である。

### 第一候補

```text
evidence
   |
   v
core step 0
   |
   +--> Reflex Head 0
   |       |
   |       +--> accepted -> typed decision
   |       +--> defer
   |
core step 1
   |
   +--> Reflex Head 1
   |
...
   |
normal controller / decoder
```

これはv0.5の、

- adaptive compute
- bounded steps
- routing
- acquire
- uncertainty

と整合する。

---

## 5. 提案名称

研究上の仮称:

> **FOLD Reflex Path (FRP)**

実験系列:

> **RP-0, RP-1, ...**

`C###`、PC-ALMの`PA-`、Auto-Partitionの`AP-`とは分離する。

---

## 6. 出力契約

Reflex Pathに自由文生成をさせない。

最小候補:

```text
ReflexDecision {
    kind:
      ANSWER
      COMPUTE
      ACQUIRE
      INTERRUPT
      NO_OP
      DEFER

    target_id:
      bounded enum / registered module / registered acquisition

    probs:
      probability over valid bounded choices

    evidence_revision:
      revision used for decision
}
```

重要:

- arbitrary tool nameを生成しない
- arbitrary path / shell / codeを生成しない
- authorityを持たない
- Reflex Headはproposalを返すだけでもよい
- execution runtimeがpermission / consequence / revisionを検査する

---

## 7. 数理的な判断基準

state depth / internal step `k` のworking representationを、

```text
z_k
```

とする。

Reflex Head:

```text
q_k(a | z_k)
```

ここで `a` は有限action set。

単純なconfidence thresholdではなく、Reflexを採用した集合に対するriskを見る。

```text
Coverage(tau)
  = P(accept)

SelectiveRisk(tau)
  = E[loss(a, y) | accept]
```

最終的に必要なのは、

```text
Reflex execution cost
vs
Slow-path additional compute cost
vs
Wrong early decision cost
```

の比較である。

概念上:

```text
J_fast
  = expected_task_loss_fast
  + consequence_cost
  + compute_cost_fast

J_continue
  = expected_task_loss_slow
  + compute_cost_slow
```

Reflexを使う価値があるのは、

```text
J_fast < J_continue
```

が十分再現する領域だけ。

ただし実際には`J_continue`を事前に正確に知れないため、RP系列ではoracle / replay / shadow resultからvalue-of-compute推定を作る。

---

## 8. 中心仮説

## H1 — Intermediate stateには一部の判断に十分な情報が早く現れる

仮説:

> 簡単なrouting / binary / bounded choiceでは、最終decoderまで進まなくても中間working stateから高品質に判断できる。

既存early-exit研究はこの可能性を強く支持する。

### 反証条件

浅いstateにprobeを付けても、

- final stateとの差が大きい
- confidenceを上げてもselective riskが下がらない
- deferするとcoverageがほぼゼロ

なら、Reflex Pathは価値が低い。

---

## H2 — Typed bounded decisionは自由文生成よりsoftware-facing controlに向く

仮説:

> routing / branch / scoreのような有限判断では、decoderにJSONや文字列を生成させるより、有限logit headから直接選択する方が低遅延で、schema violationを構造上排除できる。

これは構造的には成立する。

ただしsemantic correctnessまで保証しない。

### 比較

```text
A. decoder -> structured text -> parse
B. final-state bounded decision head
C. early-state bounded decision head
```

比較項目:

- task correctness
- invalid output rate
- latency
- bytes generated
- peak memory
- calibration

---

## H3 — Confidence単独ではなくSelective Predictionが必要

仮説:

> Reflex Pathを安全に使うには、全サンプルaccuracyではなく「受理したサンプルだけのrisk」とcoverageのtrade-offを直接最適化する必要がある。

主要指標:

- risk-coverage curve
- AURC
- NLL
- Brier score
- ECE / classwise calibration
- false-high-confidence rate
- defer rate

特にOOD sliceを別計測する。

---

## H4 — Action consequenceでacceptance policyを変えるべき

同じ0.95 confidenceでも、

```text
UI highlight
file read
movement
file delete
external side effect
```

では誤りのコストが異なる。

仮説:

> Reflex decisionのacceptanceはprobabilityだけでなく、action consequence classを入力したpolicyで決めるべき。

初期RP系列では高副作用actionを**Reflex direct execution対象にしない**。

Reflexはproposalまで。

---

## H5 — Slow Path fallbackがあることでReflexを攻められる

仮説:

> Reflexを万能にしようとせず、難しい例をDEFERする設計の方がquality-compute Paretoを改善できる。

```text
easy
 -> reflex accept

hard / ambiguous / OOD
 -> DEFER
 -> COMPUTE / ACQUIRE / normal reasoning
```

これはPonderNet / early-exit / selective predictionの方向と整合する。

---

## H6 — Verification付きReflexは裸のEarly Exitより頑健になり得る

LayerSkip型の考え方から、

```text
fast proposal
-> deeper verification
-> accept / correct
```

も候補。

ただしFOLDでは毎回verifyすると速度利点が消える。

第一候補は:

```text
low consequence + calibrated accept
  -> no verify

medium consequence / marginal confidence
  -> lightweight verify

high consequence
  -> slow path / external policy
```

---

## H7 — Reflex InterruptはFOLDエージェント用途に強い価値がある可能性

長い内部計算中にevidence revisionが変わった場合、

```text
old evidence
 -> long reasoning
new observation arrives
 -> old reasoning continues
 -> stale action
```

を避けたい。

仮説:

> 新観測を小さなReflex Headで評価し、現在のworking stateをinvalidateすべきかを高速判定すれば、stale-action率を下げられる。

出力候補:

```text
CONTINUE
RECHECK
INTERRUPT
URGENT_INTERRUPT
```

ただしinterrupt authorityはruntime側。

evidence revision / provenance一致を必須にする。

---

## H8 — Shared representationからHeadだけ追加できるなら容量効率が高い

第一候補:

```text
Shared Core State z_k
      |
      +--> normal path
      |
      +--> tiny Reflex Head
```

仮説:

> separate reflex modelを持つより、小さいheadをshared stateへ付ける方が保存量とstate reuseで有利。

### 反証候補

shared stateがlanguage generation向けで、decision separabilityが悪い場合、

```text
tiny side encoder
+
reflex head
```

の方が良い可能性がある。

したがってRP-0で、

- linear head
- small MLP head
- tiny side encoder

を比較する。

---

## H9 — Auxiliary Reflex Lossが主能力を壊す可能性がある

Deep supervisionはearly representationをdecision-friendlyにできる一方、主LM objectiveとgradient conflictを起こし得る。

仮説:

> Reflex lossの重み・接続位置を制限すれば、主task qualityを保ったまま早期decision separabilityを改善できる領域がある。

必ず測る:

- primary NLL / task score
- reflex score
- gradient cosine / conflict
- final representation drift
- early representation gain

Reflex accuracyだけ改善して主モデルを悪化させる方式は不採用。

---

## H10 — FLOPs削減がwall-clock高速化を保証しない

Early exitは、

- GPU branch divergence
- host synchronization
- small-kernel overhead
- batch内でexit depthがばらつく
- head evaluation overhead

で速度利点を失う可能性がある。

よって成功条件はFLOPsではなく、

- end-to-end latency
- p50 / p95
- throughput
- kernel count
- synchronization
- active bytes
- peak VRAM

で判定する。

---

## 9. 強い反対仮説 / 失敗モード

### F1 — 早いstateが何も知らない

Reflex Headを付けても最終層近くまでdecision qualityが上がらない。

### F2 — 高confidence誤答

in-distributionではcalibratedでもOODで誤って高confidence。

### F3 — Auxiliary loss interference

Reflex Headを早く賢くするためのlossがlanguage / reasoning表現を狭める。

### F4 — Defer collapse

安全側に寄せた結果、ほぼ全部DEFERになり計算量が減らない。

### F5 — Reckless accept collapse

compute penaltyを強くしすぎて、品質を落として早期終了する。

### F6 — Batch efficiency loss

sampleごとのexit差でGPU利用率が落ち、平均FLOPs削減より遅くなる。

### F7 — Consequence misclassification

低リスクと判定したactionが実際には高副作用。

したがってconsequence classはモデルだけに決めさせず、runtime / tool metadataをauthoritative sourceにする。

### F8 — Stale interrupt false positive

無関係な観測変化で頻繁にreasoningをcancelし、進まなくなる。

### F9 — Shared Basis compression flips routing

小さいlogit差が圧縮誤差でaction flipを起こす。

v0.5 roadmapのrouting head圧縮評価と一致する重要リスク。

### F10 — "System 1"の誤解

人間心理学的System 1を再現したと主張しない。

本研究のSystem-One-inspiredは単に、

> low-latency bounded decision path

というengineering shorthand。

---

## 10. RP実験系列

## RP-0 — Frozen-State Separability Probe

### 問い

> FOLD中間stateに、Reflexに必要なdecision informationがそもそも存在するか。

### 変更

production runtimeを変更しない。

既存state snapshotを取得し、各depth / internal stepにread-only probeを付ける。

比較:

```text
linear probe
small MLP
tiny side encoder + head
final-state head
```

task候補:

- binary routing
- bounded 4-way choice
- ANSWER vs COMPUTE
- COMPUTE vs ACQUIRE
- stale revision detect

### 必須指標

- accuracy / balanced accuracy
- NLL / Brier
- risk-coverage
- AURC
- probe parameter bytes
- probe inference cost
- depth / step別curve

### Gate

早いstateで有用なrisk-coverage領域が無ければ、architecture integrationへ進まない。

---

## RP-1 — Shadow Early Exit

### 問い

> Reflexが判断しても実行せず、final pathと比較したとき、どのcoverageまで安全に一致できるか。

Reflexはshadow-only。

```text
reflex predicts
normal path always runs
compare afterward
```

これで危険なく、

- acceptance
- disagreement
- regret
- missed compute saving

を測れる。

---

## RP-2 — Calibration / Shift / Defer

### 問い

> confidenceを実際のselective-risk制御へ使えるか。

split:

- calibration
- IID held-out
- lexical paraphrase
- difficulty shift
- OOD / unseen task family

比較:

- raw softmax
- temperature scaling
- alternative simple post-hoc calibration
- learned defer head

thresholdはevaluationを見て後付けしない。calibration splitで固定する。

---

## RP-3 — Typed Decision vs Decoder Output

### 問い

> finite decisionではdecoderを通さない価値があるか。

比較:

```text
A. text decoder + JSON/schema parser
B. final-state bounded head
C. early Reflex Head
```

同じdecision task / data / allowed answer setを使う。

主要評価:

- semantic accuracy
- structural validity
- latency
- generated bytes
- total compute
- calibration

---

## RP-4 — Consequence-Aware Gate

### 問い

> action riskを考慮したacceptanceで、compute savingを維持しつつ重大誤実行を抑えられるか。

実機副作用はまだ使わない。

offline / simulator上でaction classを、

```text
LOW
MEDIUM
HIGH
FORBIDDEN_REFLEX
```

に分ける。

HIGH以上はdirect execution不可。

比較:

- one global threshold
- per-consequence threshold
- learned risk gate + hard veto

---

## RP-5 — Interrupt / Re-observation

### 問い

> evidence revision変更を高速検出してstale reasoningを減らせるか。

sequence途中で、

- relevant observation change
- irrelevant change
- contradiction
- correction
- delayed update

を注入。

計測:

- stale action rate
- true interrupt recall
- false interrupt rate
- interrupt latency
- wasted compute before cancel
- progress starvation rate

---

## RP-6 — Real Runtime Benchmark

### 問い

> Reflexが本当にGPU実時間を短縮するか。

必須batch:

```text
1
small interactive batch
medium batch
```

exit pattern:

- homogeneous easy
- homogeneous hard
- mixed difficulty

計測:

- p50 / p95 task latency
- throughput
- kernel launch count
- GPU utilization
- synchronization count
- bytes moved
- peak VRAM
- average internal steps
- quality / selective risk

---

## RP-7 — Compression / Shared Basis Compatibility

RP-0〜RP-6通過後のみ。

比較:

- high precision Reflex Head
- compressed head
- shared-basis head candidate

必須:

- logit drift
- probability drift
- decision flip
- defer flip
- risk-coverage shift
- calibration shift
- latency / bytes

routing / interruptの小さいmarginを圧縮が破壊する場合、Reflex Headだけ高精度維持を許す。

---

## RP-8 — V5-D / V5-E Integration Candidate

ここで初めて、

```text
ANSWER
COMPUTE
ACQUIRE
INTERRUPT
DEFER
```

をv0.5 controller candidateとして比較する。

RP系列の成功だけでV5-D / V5-EをPASSにしない。

各Gateの本来の条件はそのまま維持する。

---

## 11. 学習方法の第一候補

### Phase A — probe only

backbone frozen。

目的:

- information presenceの確認
- architecture intervention前の上限把握

### Phase B — auxiliary head training

```text
L
 = L_primary
 + beta * L_reflex
```

ただし `beta` はsweepし、primary qualityを必ず併記。

Reflex probabilityにはproper scoring ruleを使う。

候補:

- cross entropy / log loss
- Brier score補助

JevのRLCDは公開情報だけで再現できないため、名称や効果を模倣しない。

### Phase C — compute-aware training

RP-1 / RP-2でcalibrationを確認した後だけ、

```text
task quality
+
compute penalty
```

を導入。

最初からcompute penaltyを強くするとreckless early exitへ崩れるため避ける。

---

## 12. 評価指標

### Decision Quality

- accuracy / balanced accuracy
- class-wise accuracy
- NLL
- Brier
- error severity

### Calibration

- ECE
- classwise ECE
- reliability curve
- OOD false-high-confidence
- calibration drift

### Selective Prediction

- coverage
- selective risk
- risk-coverage curve
- AURC
- defer rate
- accepted error severity

### Compute

- average internal steps
- active modules
- FLOPs補助値
- end-to-end wall-clock
- p50 / p95 latency
- throughput
- kernel launches
- synchronization
- peak VRAM

### Main-model Regression

- next-unit NLL
- task score
- generation quality
- routing quality
- acquisition quality
- memory semantics
- correction behavior

### Interrupt

- stale action rate
- false interrupt
- missed interrupt
- cancel latency
- wasted compute

---

## 13. 成功条件

Reflex Pathはaccuracy単独では採用しない。

最低でも次のどれかのPareto改善が必要。

### Case A

```text
same quality / risk
+
lower task wall-clock
```

### Case B

```text
same wall-clock
+
lower harmful decision risk
```

### Case C

```text
same quality
+
lower average internal steps
+
no p95 regression
```

### Case D

```text
agent / dynamic environment
stale-action rate significantly lower
+
interrupt overhead acceptable
```

逆に、

```text
latency改善なし
+
main quality悪化
+
calibration不良
+
DEFER過多
```

なら不採用。

---

## 14. 重要な設計境界

### 14.1 Reflexはauthorityではない

```text
model proposal
!=
runtime permission
```

既存information-acquisition設計と同じ。

### 14.2 高副作用actionを最初から即実行しない

最初はshadow / simulator / proposal-only。

### 14.3 confidenceをcorrectness証明にしない

高confidenceでも別sliceでriskを測る。

### 14.4 evidence revisionを持つ

古い観測で出したReflexDecisionを新しいworld stateへ適用しない。

### 14.5 unrestricted textをReflexに入れない

Reflex Pathの利点を維持するため、finite / typed / bounded outputに限定する。

---

## 15. v0.5ロードマップとの位置関係

Reflex Pathは特に、

```text
V5-D Adaptive Compute / Routing
V5-E Information Acquisition
```

に接続する。

研究順としては、

```text
current C-series work
  remains authoritative

RP-0 / RP-1
  can be independent research

then
RP-2..RP-7

finally
V5-D/E candidate integration
```

とする。

既存Gateを飛ばさない。

---

## 16. Jevから採るもの / 採らないもの

### 採る

- decisions, not strings
- typed bounded outputs
- probability / uncertainty as first-class output
- workflow / routing / scoring用途
- fast pathとnormal reasoningの役割分離

### 採らない / 未確定

- Jev内部architectureの推測
- RLCDの未公開詳細の推測
- vendor benchmark倍率のFOLDへの外挿
- "zero hallucination"をsemantic correctness保証として使用
- System 1心理モデルそのものの再現主張

---

## 17. 現時点の判断

### 研究採用: YES

Reflex Pathは、

- FOLD v0.5のadaptive compute
- routing
- information acquisition
- bounded runtime
- agent re-observation

と高い整合性がある。

### 正規architecture採用: NOT YET

まずRP-0で、

> **浅いFOLD stateに本当にdecision informationがあるか**

を確認する。

これがnegativeなら、Reflex Pathを無理に載せない。

### 最重要ポイント

本仮説の価値は単なるearly exitではない。

FOLDで狙うべき組合せは、

```text
Shared representation
+
Typed bounded decision
+
Selective risk / calibrated defer
+
Consequence-aware gate
+
Slow-path fallback
+
Evidence-revision interrupt
```

である。

これが成立すればFOLDは、

> **簡単な判断は反射的に低コストで処理し、難しい・危険・情報不足な判断だけを深く考えるモデル**

へ発展できる可能性がある。

ただし、この文は現時点では仮説である。

第一実験はRP-0のfrozen-state separability probeとする。

---

## 参考資料

### TypeSafe AI / Jev

1. TypeSafe AI, **Introducing System One Models and Jev**, 2026-09-14.  
   https://typesafe.ai/blog/introducing-system-one-models-and-jev

2. TypeSafe AI, **System One Models / Jev**.  
   https://typesafe.ai/

3. TypeSafe AI, **Workflow evals**.  
   https://evals.typesafe.ai/

### Adaptive computation / Early Exit

4. Teerapittayanon, McDanel, Kung, **BranchyNet: Fast Inference via Early Exiting from Deep Neural Networks**, 2017.  
   https://arxiv.org/abs/1709.01686

5. Xin et al., **DeeBERT: Dynamic Early Exiting for Accelerating BERT Inference**, 2020.  
   https://arxiv.org/abs/2004.12993

6. Liu et al., **FastBERT: a Self-distilling BERT with Adaptive Inference Time**, 2020.  
   https://arxiv.org/abs/2004.02178

7. Banino, Balaguer, Blundell, **PonderNet: Learning to Ponder**, 2021.  
   https://arxiv.org/abs/2107.05407

8. Schuster et al., **Confident Adaptive Language Modeling**, 2022.  
   https://arxiv.org/abs/2207.07061

9. Elhoushi et al., **LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding**, 2024.  
   https://arxiv.org/abs/2404.16710

10. Raposo et al., **Mixture-of-Depths: Dynamically allocating compute in transformer-based language models**, 2024.  
    https://arxiv.org/abs/2404.02258

11. Bajpai, Hanawal, **A Survey of Early Exit Deep Neural Networks in NLP**, 2025.  
    https://arxiv.org/abs/2501.07670

### Calibration

12. Guo et al., **On Calibration of Modern Neural Networks**, 2017.  
    https://arxiv.org/abs/1706.04599
