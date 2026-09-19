# FOLD Experiment Conversation / Handoff Protocol

この文書は、FOLD の実験を ChatGPT / Codex / 別チャットへ継続して引き継ぐための **標準会話フォーマット** を定義する。

対象は主に `C###` 実験系列。個別実験の科学的仕様を置き換えるものではなく、`docs/experiment-ledger-and-handoff.md`、各 `experiment-ledger-addendum-*`、Gate decision、実験コードを人間と次のエージェントへ一貫して伝えるための運用規約である。

## 0. Current response format (v2)

この節が現在の会話フォーマットの authoritative rule。後続の A〜K は詳細チェックリストとして残すが、毎回その全項目を同じ長さで再掲する義務はない。

### 0.1 返答モードを3つに分ける

1. **Formal result mode** — ACCEPTED PASS / ACCEPTED VALID NEGATIVE を正式判定し、同じ返答内で次Cの設計・実装・preregistration・launcherまで準備する。
2. **Execution recovery mode** — precheck / regression / source / artifact / replay / schema / nonfinite等で科学的結果が成立していないとき。同じCだけを修復し、次Cへ進まない。
3. **Operational mode** — 実行中確認、Git認証、log push、短い技術質問。formal statusを変更しない。

### 0.2 Formal result mode の順序

```text
1. Formal verdict
2. Execution validity
3. Deciding metrics
4. Scientific interpretation
5. Confound / non-claim
6. Repository update
7. Next C — one scientific question
8. Changed / held constant
9. Workload / fixed gate / interpretation boundary
10. Registration HEAD
11. Short launcher command
12. Expected progress
13. Stop condition
```

accepted resultでは acceptance commit と next-C preregistration commit を分離する。ただしユーザーにもう一度「続けて」と言わせず、同じ返答内で次C準備まで完了する。

### 0.3 Execution recovery mode の順序

```text
1. C{N} — INVALID EXECUTION / RETRY SAME C{N}
2. Failure phase — どこまで通ったか
3. Root cause — 最小の技術原因
4. Why not scientific evidence
5. Minimal recovery — 科学条件は固定
6. invalid log / recovery HEAD
7. Short retry command
8. Stop — C{N+1}へ進まない
```

INVALID時に新Cの設計・登録をしない。結果を見てthreshold / seed / cohort / comparator / gateを緩めてPASSへ変えない。

### 0.4 実行コマンドはlauncherを標準にする

長いinline PowerShellを毎回貼らず、repo内の `tools/run_c###.ps1` と `tools/invoke_c###.ps1` に詳細を固定する。ユーザー向け標準は原則これだけ:

```powershell
Set-Location -LiteralPath "M:\asobiba\fold"

git pull --ff-only origin feat/sft-target-loss
if ($LASTEXITCODE -ne 0) {
    throw "Repository synchronization failed"
}

.\tools\invoke_c###.ps1 `
    -ExpectedHead "<registered-head>"
```

expected regression count / branch / ExpectedHead /主要workloadは返答本文に出す。詳細hash/pathはrunner/preregistrationへ固定する。

### 0.5 Remote log first

通常はログ添付・clipboard・OSC52を要求しない。正式run後は `publish_experiment_log.ps1` が:

```text
docs/experiment-run-logs/c###/latest.log
docs/experiment-run-logs/c###/latest.json
```

を専用log commitとしてpushする。ユーザーは原則 **「終わった」だけ送ればよい**。assistantはremoteからmetadata/logを取得して判定する。

`latest.json.execution_head` が scientific execution HEAD。remote branch HEADはlog commitのため先へ進んでいてよい。`summary.commit_sha / metadata.execution_head / registered ExpectedHead` を区別して確認する。

log pushだけ失敗した場合は科学実験を再実行しない。既存local log commitのpushを直す。log transport failureをscientific INVALIDと呼ばない。

### 0.6 Active-run branch safety

ユーザーが正式runを実行中は、同じexperiment branchのremote HEADを無関係なdocumentation変更で進めない。log pushがnon-fast-forwardになるため。

作業中に基準文書等を更新する必要がある場合は別 `docs/...` branchへ保存し、formal run/log push完了後にexperiment branchへ取り込む。

### 0.7 Scientific HEAD と log commit

必ず別物として表記する:

```text
scientific execution HEAD = <実験コードを実行したcommit>
published log commit      = <latest.log/latest.jsonだけのcommit>
```

formal verdictのexecution identityは前者。後者は証拠輸送/引き継ぎ用。

### 0.8 数値の見せ方

summary全文をチャットへ再掲しない。gateを決める deciding metrics を先に出し、必要なconfoundだけ追加する。

- candidate error と control errorを分離する。
- raw logit drift と argmax/action flipを分離する。
- execution-validity replay と scientific correctnessを分離する。
- PASSでもGate E completionや一般化を自動的に主張しない。

### 0.9 Experiment authoring quality gate

新しいC番号をユーザーへ渡す前に、実装側で以下を必須チェックする。これを通していないCを「実行可能」と表現しない。

- UTF-8 / NULなし / import可能なsource構造
- manifest self-hash と固定SHAの一致
- new test定義数とexpected regression総数の一致
- runnerのmodule list件数とCLI引数index整合
- **parent artifact contract audit**: childが読むNPZ/JSON/checkpointのschemaを、実際にそれを生成したparent Cのoutput contractと照合する
- parent helper再利用時は「名前が似ている」だけで使わず、そのhelperがどのCのartifact schemaを読む関数か確認する
- child自身にloaderがある場合、run pathが実際にそのloaderを呼んでいることをsource-level testで固定する
- synthetic unit testだけでなく、少なくとも1本は本番run pathのcall ordering / resource accounting / loader dispatchを検証する
- preregistrationに書いた数字（cohort, blocks, expected reads, protected count, artifact count）とcode定数を相互照合する

このquality gateは科学的regressionとは別物で、**実験ハーネスの作者側の品質確認**である。
ここで見つかる問題をユーザー実行時のINVALIDで初めて発見する状態を減らす。

### 0.10 Handoff更新

accepted result: `experiment-ledger-addendum-c{N}-c{N+1}.md` + authoritative handoff。
INVALID: 同じCの execution-recovery addendumへ追記。
handoffは最新accepted evidence / active C / current recovery / claim boundary / next stopを中心にし、古い詳細はaddendumへ退避する。

## 1. 基本原則

- 返答は「前実験の正式判定」から始める。`ACCEPTED PASS`、`ACCEPTED VALID NEGATIVE`、`INVALID EXECUTION / RETRY SAME C NUMBER`、`ACTIVE / NOT YET JUDGED` を曖昧にしない。
- 数値結果と科学的解釈を分ける。PASSでも claim scope を明記し、測っていない一般化を主張しない。
- 次実験は、前実験で残った **1つの主要制約または交絡因子** を外す形で説明する。原則として one scientific question per C number を維持する。
- 「何を変えるか」と同じくらい「何を固定するか」を明示する。比較不能な複数変更を同じC番号へ混ぜない。
- production runtimeを変更したか、diagnostic-onlyかを明記する。
- 長い実験では progress output を事前に示す。ユーザーが実行中に停止・再開・異常判定できるよう seed / phase / case / remaining を出す。
- 実行前後に protected artifact、tracked tree、prerequisite identity 等の guard / postcheck を置く。
- 有効な negative result は失敗扱いで捨てず、正式な科学的結果として ledger に残す。
- accepted resultでは **remote log取得 → 判定 → ledger/handoff更新 → 同じ返答内で次Cを設計・実装・preregister** の順序にする。INVALIDではsame-C recoveryだけを行う。
- チャットが変わっても、この文書と `experiment-ledger-and-handoff.md` を読めば同じ応答形式を再開できる状態を保つ。

## 2. 標準返答フォーマット

新しい実験を提示する返答は、原則として次の順序を使う。

### A. 前実験の正式判定

```text
C{N} — {FORMAL STATUS}
```

含めるもの:

- focused regression件数
- fresh seed数とvalidation件数
- deciding metricの主要値
- protected artifact / fixture / tracked tree の状態
- production runtime変更有無
- Gate候補か否か

例:

```text
C136 — ACCEPTED PASS
84/84 regression
3 fresh seeds × 8 held-out queries
query-address / retrieval-key / provenance / commit-once / ANSWER / evidence = 1.0
protected artifacts preserved
```

### B. 科学的に何が成立したか

実験で実際に成立した経路を、小さなASCII図で示す。

```text
input
→ learned component
→ real runtime component
→ validated evidence/state
→ output
```

その後、**claim** と **non-claim** を文章で分ける。

- claim: この実験が直接支持するもの
- non-claim: 似ているがまだ測っていないもの

「自然言語理解できた」「汎化した」などの広い表現だけで済ませない。

### C. 次実験の名前と目的

```text
## C{N+1} — {short descriptive name}
```

最初に「前実験のどの制約を外すか」を1文で書く。

次に before / after をできるだけ図示する。

```text
C{N}:
query → fixed classes

C{N+1}:
query → shared/content-addressed mechanism → live candidate set
```

### D. 変数分離

最低限、以下を明記する。

```text
Scientific question:
Changed variable:
Held constant:
Training split:
Evaluation split:
Fresh seeds:
Production code change:
Prerequisite:
```

交絡因子診断では特に、変更変数を1つに限定する。

### E. 実験の具体構造

必要に応じて以下を短いコードブロックで示す。

```text
training candidates = {n}
evaluation candidates = {m}
unseen cases = {k}
queries/entity = {q}
validation cases/seed = {v}
total validation cases = {t}
```

未知entity / held-out combination / OOD条件などは、何が unseen なのかを明示する。

### F. 制限事項 / interpretation boundary

実行前に、そのC番号だけでは主張できないことを明示する。

PASS / FAIL の双方について、次の意味を事前に固定する。

```text
PASS -> ...
FAIL -> ...
INVALID -> same C number retry
```

閾値や解釈を結果を見た後で有利に変更しない。

### G. 現在HEADと期待HEAD

```text
Current/expected branch: feat/sft-target-loss
Expected HEAD: <full or short SHA>
```

リポジトリ同期を伴う場合、ユーザーのローカルHEADと remote HEAD の関係が分かるようにする。

### H. 実行コマンド

現在の標準は **repo内launcherを短く呼ぶ** こと。runner/launcherが未整備な古いCだけ、下記の長いinline blockをfallbackとして使う。

標準構造:

```powershell
Set-Location M:\asobiba\fold

$log = "M:\asobiba\fold\runs\chatgpt-last.log"
$protected = "..."
$fixture = "..."

& {
    Write-Output "=== FOLD C{N} ... ==="
    Write-Output "=== syncing repository ==="

    git pull --rebase origin feat/sft-target-loss

    $branch = git branch --show-current
    $commit = git rev-parse HEAD

    Write-Output "branch = $branch"
    Write-Output "commit = $commit"
    Write-Output "stage = ..."
    Write-Output "fresh_seeds = ..."

    if ($branch -ne "feat/sft-target-loss") {
        throw "Unexpected branch: $branch"
    }

    $dirtyBefore = git status --porcelain --untracked-files=no
    if ($dirtyBefore) {
        throw "Tracked working tree is not clean before C{N}"
    }

    # protected hashes / prerequisite guards

    Write-Output "=== focused regression ==="
    # exact unittest list

    Write-Output "=== C{N} benchmark ==="
    # exact benchmark module

    # protected hashes / tracked-tree postcheck

    Write-Output "=== C{N} POSTCHECK ==="
    Write-Output "..."
    Write-Output "=== script error, if any ==="

} *>&1 | Tee-Object -FilePath $log
```

ルール:

- Python環境名は現在の authoritative environment を使う。推測で `.venv` と `.venv-py31315` を入れ替えない。
- focused regression は「想定件数」も併記する。
- benchmarkは `-u` 等、進捗が即時表示される形を優先する。
- production runtime modified の表示は実際の変更有無と一致させる。
- protected hash は handoff の authoritative value を使用する。

### I. 期待される進捗表示

長いbenchmarkでは例を出す。

```text
C{N} prerequisite_summary = ...
[C{N}] seed 1/3 ... start
[C{N}] seed 1/3 ... done
[C{N}] seed 1/3 case 1/12 ... remaining=11
...
```

これは厳密な全文一致ではなく、実行中に正常進行を判断するための目印。

### J. ログ公開 / 回収

標準運用は **ログをチャットへ貼らない**。正式C実験のouter PowerShellが完了したら、
`tools/publish_experiment_log.ps1` で `runs/chatgpt-last.log` を
`docs/experiment-run-logs/c{N}/latest.log` と `latest.json` へミラーし、
専用の `logs(fold): publish C{N} execution log` commitとして同じ実験branchへpushする。

対象はconsole text logと小さいmetadataだけ。dataset / NPZ / checkpoint / source fixture /
generated runtime directoryなどは従来どおりlocal-onlyで、ログ公開commitへ含めない。

outer blockは、科学実験がPASS/FAIL/INVALIDのどれで終了しても `finally` でlog publishを試みる。
publisherはbranch/origin、publish直前HEAD、tracked/staged state、source log path/size/UTF-8、
staged pathをguardしてからpushする。

ユーザーは実験終了後、原則として **「終わった」だけ送ればよい**。
assistantはGitHub上の `docs/experiment-run-logs/c{N}/latest.json` と `latest.log`
を取得し、metadataのexecution_head / SHA256 / bytesを照合して正式判定する。

pushが失敗した場合だけ従来のファイル添付またはclipboardをfallbackとして使う。
OSC 52は標準経路ではない。

### K. 停止条件

返答末尾で、その実験が終わるまで次へ進まないことを明記する。

```text
C{N}の結果を判定するまではC{N+1}へ進まない。
実行とlog pushが終わったらユーザーは「終わった」と送る。
assistantはremoteのpublished logを取得し、formal status / scientific interpretation /
ledger update / next experiment の順で続ける。
```

## 3. 結果ログを受け取ったときの標準返答

ユーザーが実験ログを貼った場合、または「終わった」と通知してremote published logを取得した場合は次の順序にする。

1. **Formal verdict** — PASS / VALID NEGATIVE / INVALID を最初に明示。
2. **Execution validity** — regression、seed、artifact hashes、tree cleanliness、prerequisite、runtime modificationを確認。
3. **Metric summary** — deciding metricsだけを表または短い箇条書きで整理。
4. **Scientific interpretation** — 何が支持され、何が否定・未確定か。
5. **Confound audit** — 異常なerror patternやfront-end/runtime confoundがないか確認。
6. **Repository update** — ledger addendum と authoritative handoff を更新。
7. **Next C design** — one scientific questionとして次実験を提示。
8. **Execution block** — 上記標準フォーマットH〜Jを付ける。
9. **Stop condition** — 次結果待ちで止める。

有効なFAILでは、すぐにモデル容量・hidden width・学習時間を増やさない。まず表現、データsplit、collision、OOV、leakage、metric、runtime path等の交絡を切り分ける。

## 4. Handoff更新ルール

各C番号の判定後:

- 詳細履歴は `docs/experiment-ledger-addendum-c{N}-c{N+1}.md` 等へ残す。
- `docs/experiment-ledger-and-handoff.md` は長大な履歴ではなく、**最新のaccepted evidence、現在のactive experiment、次のinterpretation boundary** を保持する。
- handoffには branch、environment、protected hashes、Gate status、active architecture/path を残す。
- 古いC番号の詳細がhandoffを圧迫したらaddendumへ退避するが、accepted chainを追える参照は維持する。
- 新しいチャットはまず `AGENTS.md`、このprotocol、`experiment-ledger-and-handoff.md` を読み、active C番号から再開する。

## 5. 会話上の省略ルール

標準フォーマットは一貫性を優先するが、毎回同じ説明を冗長に繰り返さない。

- 単純な途中質問への回答ではフルテンプレート不要。
- **新C番号を提示するとき**、**実験結果を正式判定するとき**、**別チャットへ引き継ぐとき**はフルまたは準フル形式を使う。
- 既知の環境情報は再質問しない。
- 実験コードに既に埋め込まれている値でも、ユーザーが実行時に確認すべき seed / candidate count / expected regression count / branch / protected hashes は返答に出す。
- 実際のrepository stateと食い違うサンプルコマンドを出さない。必要なら先にremote branchを確認する。

このprotocolの目的は、個々の実験説明をきれいに見せることではなく、**どのチャット・どのエージェントからでも、科学的claim scopeと実行再現性を失わずに次の1実験へ継続できること**である。
