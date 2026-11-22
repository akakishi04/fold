# main統合と進行状況 — 2026-11-22

この文書は運用上の統合記録。正式な実験状態は
[experiment-ledger-and-handoff.md](experiment-ledger-and-handoff.md)を参照する。
C344-R1の結果受理と、独立レビュー済みC345の登録をmainへ統合した。

## 現在の進行

| 対象 | 正式状態 | 到達点 |
|---|---|---|
| C342 | ACCEPTED VALID NEGATIVE | mixed45候補のfull gateは2/5 seed。 |
| C343 | ACCEPTED PASS (DIAGNOSTIC INTEGRITY) | 保存結果の整合性と誤答の所在を確認。 |
| C344 | ACCEPTED VALID NEGATIVE | R1実行は成立。pair-max候補は2/5 seed、事前条件は未達。 |
| C345 | ACTIVE / NOT YET JUDGED | 保存済み損失・予測の診断。実装・作成者テスト・独立remote reviewが完了し、正式実行待ち。 |

Gate A/BはPASSED、C/Dは測定範囲内でPASSED、EはPASSED、FはNOT PASSED。
production採用はない。C344初回失敗はattempt-01として保持する。

C344-R1は6件のnative cleanup確認、6514 tests / 239 modules、242 subprocessの
終了コード0、930 source pins / 8183 protected inputs、全8183件の最終再読、
10モデル学習・評価・replay、fresh verifierを完了し、run_execution_valid=true。
科学実行HEADは8d1e1170cd614503deab1e09474fe82de4bba561、ログ公開は
9d163289775373aaf62028a7b8aeacbfb41593a6で、両者を区別する。

interior4正答はTRAIN2864->2728/2880、HOLDOUT1430->1331/1440。
original6には集計上の改善があるが、固定gate全体は不合格。
詳細と解釈範囲は[C344受理記録](experiment-ledger-addendum-c344-c345.md)に保存した。

## C345登録の追加統合

| 項目 | commit |
|---|---|
| merge第1parent・C344結果統合済みmain | 3c69058523ee4e691b2ebd9371f2a7416a1107fd |
| merge第2parent・C345 activation | c81ffe102c3a9280f28a68e572403549ce77fa1d |
| C345 source/preregistration・独立review対象 | 588586870562a8f930b7e2053dcf669ee8d0b650 |
| C344 acceptance base | a7174ae51f71f001901793603ab9f7ddb26ed923 |

通常の2-parent mergeで追加統合した。競合なし。C344受理とC345登録は別commit。
C345のsource commitは七つのOWN追加のみで、後続activationは三文書だけを変更する。
独立reviewで公開済み七ファイルを末尾まで再取得し、テスト済み内容と一致した。
C345のレビュー済み七つのblob、feature全tracked pathのmode/blob、main独自6ファイルを
そのまま保持した。mainのfeatureとの差分は独自6ファイルと本運用記録だけである。

新規64テストは通常111.006秒、CP932 text-open条件112.490秒でPASSし、
failure/error/skip/expected-failure/unexpected-successは全て0。
実loaderは6579候補から既存の一件除外のみで6578 tests / 241 modulesとなり、
元C344の6514 IDs / 239 groupsを同じ順序で保持する。未束縛global0、pyflakes0、
実PowerShell ASTもdispatcher/invoke/run/最終実行blockで0 errors。
これらはLinux上の作成者検証で、C345のnative正式実行結果はまだ存在しない。

## C344結果の統合

| 項目 | commit |
|---|---|
| merge第1parent・直前main | 5581e42049caa8cd236bcdb8e0e3747f0980620f |
| merge第2parent・C344受理 | a7174ae51f71f001901793603ab9f7ddb26ed923 |
| C344実行 | 8d1e1170cd614503deab1e09474fe82de4bba561 |
| C344ログ公開 | 9d163289775373aaf62028a7b8aeacbfb41593a6 |

両方の履歴を保持する通常の2-parent merge。今回の結果統合に競合はない。
受理featureの全tracked pathを同一mode/blobで保持し、main独自6ファイルも保持する。
差分はその6ファイルと本運用記録だけ。accepted source/test/launcherは変更しない。
受理commitはC345のsource/preregistrationと分離している。

## 次の実行と検証範囲

C344は再実行しない。runs/c344-pair-max-training-76ae8eb6e3bf4d08ac577c5fde9e0caa/
以下の489出力と親入力をそのまま保持する。
C345はV5-Bの保存済み目的関数診断として独立review PASS・activation済み。
全120state/domain/splitのterminal損失と24000preupdate履歴を照合し、
C345科学処理では新たなモデル学習・forwardは行わない。
既存回帰には各historical test自身のfixture計算が含まれる。

```text
branch       = feat/sft-target-loss
ExpectedHead = c81ffe102c3a9280f28a68e572403549ce77fa1d
dispatcher   = tools/invoke_active_v2.ps1
```

937 source pins / 8679 protected inputs。C344の489出力を全て保持し、
C345の四つの診断成果物と主記録・実行記録・回帰proofを検証する。
次回はC345のremote latest.log/latest.jsonを取得して正式判定する。
診断PASSはC344候補の能力PASSやGate F合格へ読み替えない。

mainは統合内容を参照するbranch。正式実験launcherは引き続き
feat/sft-target-lossの一意なACTIVE experimentとExpectedHeadを検査する。
完了したC344の古いExpectedHeadやmain merge HEADで次実験を起動しない。

統合時は両parent、未解消indexの不存在、全feature blob/mode、main独自6ファイル、
文書参照を確認した。native成果物の検証根拠は今回取得した実行ログと固定verifierであり、
統合作業のためにC344学習を再実行したわけではない。

## 過去の統合記録

以下は同日の初回統合とR1登録時点の記録。現在の正式状態は上記を参照する。

## 初回統合の対象と履歴

| 項目 | commit |
|---|---|
| 統合前のmain・merge第1parent | `72670d83e6fe0da88e4d0d65118cf3452c7b9599` |
| 統合対象のfeat/sft-target-loss・merge第2parent | `94fca46cfb31fcbb842997809012a1a692f7c45d` |
| 共通ancestor | `ff7e662a42dae12e2d392557080058b7eda2e343` |

統合前はmain側に7件、feature側に2,180件の固有commitがあり、履歴が分岐していた。
両方の履歴を保持する通常の2-parent mergeで統合する。

唯一の競合は`docs/shared-basis-auto-module-partition-report.md`のadd/add。
canonical pathには、C69までの結果と解釈を反映した2026-09-14のfeature版を採用する。
採用blobは`d09cf5c69de7650460bf535b8cb4f41c6a5a44f7`。
mainの2026-09-13初版は第1parentの履歴に保持される。
新しい版は初版の中核仮説を引き継ぐが、例示や条件表現が完全に同一という意味ではない。
この設計文書にある当時の「C70 pending」を現在の実験状態として扱わない。

以下のmain独自6ファイルも、それぞれmainのblobをそのまま保持する。

- `benchmarks/hf_baseline_bench.py`
- `docs/context-memory-kv-replacement-hypothesis-addendum-2026-09-14.md`
- `docs/context-memory-kv-replacement-hypothesis-report.md`
- `docs/multi-axis-shared-basis-hypothesis-report.md`
- `docs/pcalm-layer-local-credit-hypothesis-report.md`
- `docs/shared-basis-runtime-output-impact-report.md`

初回統合では当時のfeatureに存在した全tracked pathのmodeとblobを保持した。
その統合結果のfeatureに対する差分は上記6ファイルと、この運用記録の追加だけだった。

## R1修復の追加統合

修復source/review対象commitは`ca6df52fb72ed0020df7e3d027d738d28870464f`。
文書のみのactivationは`8d1e1170cd614503deab1e09474fe82de4bba561`。
[独立レビュー](c344-r1-post-authoring-review.md)のPASSを確認して登録した。

mainには既存main `a036468b0ff76f219a84c32b78b27b69297eab0a` を第1parent、
R1 activationを第2parentとする通常mergeで取り込む。
R1 featureの全tracked pathsを同一mode/blobで保持し、main独自6ファイルも保持する。
このmain統合記録だけは、現在のC344状態と新しい登録HEADに更新する。
featureのactivation HEADは維持する。

## 根拠文書

- [正式handoff](experiment-ledger-and-handoff.md)
- [C344受理記録](experiment-ledger-addendum-c344-c345.md)
- [C344事前登録](experiment-ledger-addendum-c344-preregistration.md)
- [C344 R1独立レビュー](c344-r1-post-authoring-review.md)
- [C345事前登録](experiment-ledger-addendum-c345-preregistration.md)
- [C345独立レビュー](c345-post-authoring-review.md)
- [会話・引き継ぎ規約](experiment-conversation-handoff-protocol.md)
