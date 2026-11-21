# main統合と進行状況 — 2026-11-22

この文書は運用上の統合記録。正式な実験状態は
[experiment-ledger-and-handoff.md](experiment-ledger-and-handoff.md)を参照する。
今回の統合による科学的判定の変更、新Cの登録、production採用はない。

## 現在の進行

| 対象 | 正式状態 | 到達点 |
|---|---|---|
| C342 | ACCEPTED VALID NEGATIVE | mixed45候補のfull gateは2/5 seed。実行は有効だが合格条件は未達。 |
| C343 | ACCEPTED PASS (DIAGNOSTIC INTEGRITY) | C342の保存結果から誤答の所在と集計整合性を確認。モデル能力の合格を意味しない。 |
| C344 | ACTIVE / NOT YET JUDGED | 実装・事前登録・独立レビューを完了。公開された正式結果を待つ段階。 |

Gate A/BはPASSED、C/Dは測定範囲内でPASSED、EはPASSED、FはNOT PASSED。

C343で確認した具体的な課題は、候補のinterior4で**実際の学習対象にも131誤答が残る**こと。
未見の値の組合せだけでは説明できない。内部の因果的な原因は未確定である。
C344は同じデータ・モデル・更新数を保ち、2問ペアの平均CEに対して、
ペア内の大きいCEを使うpair-maxがinterior4を改善し、他領域を維持できるかを検証する。

確認したfeature HEADでは`docs/experiment-run-logs/c344/latest.log`と`latest.json`は存在しない。
これは公開結果がないという確認であり、ユーザーPCで未実行・実行中・実行済み未公開のどれかは判定できない。
72件の作成者テストと独立レビューのPASSは準備段階の検証である。
正式な6,514件の回帰テスト・10モデルの学習について、今回新しい実行結果を得たわけではない。

## 統合対象と履歴

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

featureに存在した全tracked pathのmodeとblobを保持する。
統合結果のfeatureに対する差分は上記6ファイルと、この運用記録の追加だけである。
新しい学習コードやテスト条件の変更は含まない。

## C344の実行branchと登録HEAD

`main`は統合済みの開発内容を参照するbranchとなる。
登録済みC344の正式実行は、引き続き次の組合せを使う。

```text
branch       = feat/sft-target-loss
ExpectedHead = 94fca46cfb31fcbb842997809012a1a692f7c45d
dispatcher   = tools/invoke_active_v2.ps1
```

C344のdispatcher・launcher・executorは実行branchを検査する。
`main`上からの正式起動はbranch不一致で拒否される。
今回のmain統合ではfeature ref、登録HEAD、review済み7ファイル、既存の実行契約を維持する。
実行中のPCでcheckoutを切り替えず、C344の実行・ログ公開は登録済みbranchで完了させる。

正式run後は既存publisherがfeatureの`docs/experiment-run-logs/c344/latest.*`へconsole logを公開する。
科学的execution HEADと、その後に作成されるlog publication commitは別の値である。
ローカルで既に実行が完了していて公開だけ失敗した場合は、ログ輸送を修復し、学習を再実行しない。

## 統合時の確認範囲

- 両parentを含むcommit履歴、唯一の競合の解消、未解消index entryがないこと。
- featureの全tracked pathが同じmode・blobで保持されること。
- main独自6ファイルが同じmode・blobで保持されること。
- C344のreview済みsource/test/launcher/preregistrationが同一であること。
- この文書の参照先が統合tree内に存在すること。

今回の検証は統合の完全性に関するもの。C344の正式native実行や全回帰を再実行したという主張はしない。
次の正式判定はC344の公開ログに基づいて行い、それまでC345へ進まない。

## 根拠文書

- [正式handoff](experiment-ledger-and-handoff.md)
- [C342受理記録](experiment-ledger-addendum-c342-c343.md)
- [C343受理記録](experiment-ledger-addendum-c343-c344.md)
- [C344事前登録](experiment-ledger-addendum-c344-preregistration.md)
- [C344独立レビュー](c344-post-authoring-review.md)
- [会話・引き継ぎ規約](experiment-conversation-handoff-protocol.md)
