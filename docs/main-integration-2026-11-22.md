# main統合と進行状況 — 2026-11-25

正式状態は[最新handoff](experiment-ledger-and-handoff.md)を参照する。
C346 attempt-01のINVALID記録、保持必須だったC272の歴史的sealの復元、
独立レビュー済みの同じC346の再実行登録をmainへ統合した。

## 現在の判定

C346は **INVALID EXECUTION / RETRY SAME C346**。
正式状態はC346 ACTIVE / INVALID ATTEMPT RECOVERYで、科学的な結果は未成立。
C345の診断PASS、C344のVALID NEGATIVE、Gate F NOT PASSEDを維持する。
C347は未登録。今回は文書だけの修復で、実行コードのrevisionは **C346-R0** のまま。

6件のnative cleanup、lock、親の保存結果検証、目的関数preflightは通過した。
回帰のC272 test24で保持必須の歴史的sealがhandoffに存在せず停止した。
157modules開始、156完了、3,693tests実行、3,692成功、1failure、0errors/skips。
15モデルの正式学習・評価は開始していない。ログ公開は成功している。

C345受理時のhandoff更新f5fc8e8でsealが最初に欠落した。
C273の既存修復記録とauthoring-runtime gateが定めたappend-only契約を復元し、
受理済みのテスト・C346 OWN7ファイル・manifest・テスト選択・科学条件は変更していない。
詳しい原因、進行範囲、保持条件は[C346修復記録](c346-recovery-r1.md)に保存した。

## 統合したcommit

|項目|commit|
|---|---|
|merge第1parent・統合前main|cdf7e37ce52d8ab96ef73f92b47706924dd52859|
|merge第2parent・再実行用feature activation|622e623faa0c3c698a18033eb8b4bca554088918|
|修復文書・独立review対象|728fdf12e436cb5ba7373400b247dfd6e54425bc|
|失敗した実行HEAD|e19e872577d7f574920e83b568499666f2cd41e4|
|失敗ログの公開commit|3b70c50464ac60ff202c8c8fad4d01c200ed9d06|
|変更していないC346 source/preregistration|be76c4c53c36105638e59e059af241078758b628|

両parentの履歴を保持する通常の2-parent merge。競合なし。
featureの全tracked pathのmode/blobを保持し、main独自6ファイルも元のまま保持する。
mainとfeatureの差分は従来の独自6ファイルと本統合記録のみ。
この統合は実験の追加実行ではなく、正式実行用feature HEADも進めない。

## 独立レビューと最終文書の確認

[修復後レビュー](c346-r1-post-authoring-review.md)はcommit728fdf1の5変更文書・証拠と
7つのOWNファイルをremoteからEOFまで再取得してPASS。
実loaderは6,653候補/6,652選択/243modules、OWN74、親6,578IDsの同順序prefixと
登録済み両IDhashを確認した。sole exclusionは既存C204の1件のみ。
作成者の関連11件は0.262327秒、独立担当の11件は0.233961秒で全件成功した。

さらに、最終activation622e623のremote handoffとreview文書を独立再取得し、
review metadata以外の修復内容とOWN7ファイルの不変性を確認した。
**その最終handoff実bytesに対するC272..C282の11件は0.173536秒で全件PASS**。
failure/error/skip/expected-failure/unexpected-successは全て0。
実際のexecutor guardは検証の前後ともPASSし、featureはclean、ACTIVEはC346一つ。
この最終確認では、不変なsourceの全loader構築を重ねて実行してはいない。

最終handoffは14,062bytes、SHA256:
`a37c119f54d003347c6639d276f0caf6c39060be51949aa31fcc587e4f1b8d48`。
最終独立review receipt SHA256:
`5179ee1924e457b01724b97e1a71b24cfca53bbde65bd8710a149007e6723346`。

実PowerShell7.5.4でdispatcher/invoke/run/最終ExpectedHead入りblockをAST検証し、
全て0errors。最終blockは91tokens、SHA256:
`daff6709d7fb48028dfb544877b6b27983eaa34c1c73965910dda9b96da3adb0`。
Linux上の文書・作成者確認であり、Windowsの正式6,652tests/15モデル完走は未実施。

## 再実行の境界

```text
branch       = feat/sft-target-loss
ExpectedHead = 622e623faa0c3c698a18033eb8b4bca554088918
dispatcher   = tools/invoke_active_v2.ps1
```

6,652tests/243modulesと15models/36,000updates、944sources/9,177inputs、
固定した全gate、最終再読、保存結果の再構成、fresh verifierを維持する。
一部成功済みテストの使い回しや自動再試行は行わない。
失敗attempt-01のログ/metadataはexact Git copyとして保存済みで、native folderも保持する。
C346が再びINVALIDなら同じC346だけを修復する。C347へは進まない。
実行中はfeatureを凍結し、完了後に新しいremote latest.log/latest.jsonを判定する。

## 以下は2026-11-22時点の履歴

以下の古い状態・ExpectedHeadは当時の記録であり、今回の再実行には使用しない。

# main統合と進行状況 — 2026-11-22

正式な実験状態は[experiment-ledger-and-handoff.md](experiment-ledger-and-handoff.md)を参照する。
今回、C345の受理、C344までの横断整理、独立レビュー済みC346の登録をmainへ統合した。

## 現在の進行

|対象|正式状態|到達点|
|---|---|---|
|C344|ACCEPTED VALID NEGATIVE|pair-max候補はfull gate 2/5seed、固定した優越・保持条件は未達。|
|C345|ACCEPTED PASS (DIAGNOSTIC INTEGRITY ONLY)|保存済み損失・履歴の診断は成立。interiorの全10seed/split比較で両損失が対照より高かった。|
|C346|ACTIVE / NOT YET JUDGED|両AdamW学習率を初期化時から半分にする3arm比較。実装・作成者検証・独立remote reviewを完了し、正式実行待ち。|

Gate A/BはPASSED、C/Dは測定範囲内でPASSED、EはPASSED、FはNOT PASSED。
production採用はない。C344 attempt-01のINVALID記録とR1受理を保持する。
C345のPASSは診断の整合性に限定し、C344の能力判定を変更しない。

## C345受理と原因について判明したこと

科学実行HEADはc81ffe102c3a9280f28a68e572403549ce77fa1d、ログ公開は
25ff2f93ce63c9668f3111672caf75db095d2f45。受理はf5fc8e89b5bb3d2749df91aa3b503596a6be1fc2。
6,578tests / 241modules、244process終了コード0、937sources / 8,679inputs、
全最終再読とfresh verifierが成立。公開された630診断レコードを照合した。
consoleにないsource_trace_sha256やユーザー環境の生artifactを独立取得したとは主張しない。

interior TRAINのpair-max損失は0.020316586→0.192509275、正答は2864→2728/2880。
HOLDOUT損失は0.045815971→0.499002482、正答は1430→1331/1440。
平均CEも悪化し、全10seed/splitで両終端損失が高い。
一方、original6は集計上改善し、seed344002はinterior正答が各splitで2件増えている。
目的関数と正答率が常に同方向になるという一般化はしない。

norm>1は1975→5830/12000。ただし正確なclipping回数や原因の証明ではない。
固定評価対象の終端状態が対照より悪かったことは確認できたが、学習率・clipping・
勾配配分・収束不足のどれが機序かは未確定。詳細は[C345受理記録](experiment-ledger-addendum-c345-c346.md)。

## 統合した履歴

|項目|commit|
|---|---|
|統合前main|3986aaa1678ddf28e2f4611ddf131d09a6511acb|
|merge第1parent・横断整理文書branch|45c18e39399a6f5ec073257d860377ecb624bd51|
|merge第2parent・C346 activation|e19e872577d7f574920e83b568499666f2cd41e4|
|C346 source/preregistration・独立レビュー対象|be76c4c53c36105638e59e059af241078758b628|
|C345受理|f5fc8e89b5bb3d2749df91aa3b503596a6be1fc2|

第1parentは旧mainを直接親に持つ文書commitであり、main、文書branch、featureの
全履歴を保持する通常の2-parent merge。競合なし。
横断整理のMarkdownとJSON indexは文書branchと同一blobでfeature受理にも保存済み。
これらはC344までの固定snapshotであり、文中の「C345 pending」は作成時点の記録。
C345の解決は受理文書と最新handoffに記録した。

feature全tracked pathのmode/blob、レビューしたC346七つのOWN blob、
main独自6ファイルを保持する。mainのfeatureとの差分は独自6ファイルと本統合記録だけ。
C345受理、C346 source、文書だけのactivationは別commitである。

## C346で変えることと検証済み範囲

同じpair-max目的のまま非core/core学習率を0.005/0.0005から0.0025/0.00025へ変更。
通常CE、通常学習率pair-max、半学習率pair-maxの3armをfresh5seedで比較する。
同一初期値・入力列・2,400updates・mixed45配分・architecture・clipping・scorerを固定し、
15fitsの終了後に評価する。通常CEの半学習率armはないためfactorial相互作用は主張しない。

固定gateは候補全5seedの完全gate、二つの対照に対する240の非悪化条件、
default pair-maxに対するinteriorのTRAIN/HOLDOUT×answer/pairの4集計strict gain。
損失値は記述指標。headroomがない場合も登録条件を変更せず、subgateを分けて報告する。

作成者検証74testsは通常105.273秒、CP932既定text-open模擬101.910秒でPASS。
failure/error/skip/expected-failure/unexpected-successは全て0。
実loaderは6,653候補から既存C204の1件除外のみで6,652tests / 243modules。
親6,578IDsを同順序で保持し、新規は48science+26infrastructure。
4Pythonのpyflakes、333code objects / 2,327global loadsの未定義名監査、
実PowerShell7.5.4のdispatcher/invoke/run/標準block ASTは全てPASS。
独立担当はcommit済み七つのremote実ファイルをEOFまで取得し、固定済みSHAと照合した。
この確認はソフトウェア作成者検証であり、Windows正式実験の結果はまだ存在しない。

## 次の正式実行

```text
branch       = feat/sft-target-loss
ExpectedHead = e19e872577d7f574920e83b568499666f2cd41e4
dispatcher   = tools/invoke_active_v2.ps1
```

6,652tests / 243modulesの後、15models / 36,000updates / 41,130forwardsを実行する。
944source pins / 9,177protected inputs、C345の全491outputsを保護し、
全最終再読・saved reconstruction・fresh verifierを要求する。
C346-R0は明示的なC345helper経由でC344-R1のcleanup境界を再利用する。
親diagnosticの5引数とC346学習・再構成の6/4引数を区別する。

mainは統合内容の参照branch。正式実行はfeatureの一意ACTIVEとExpectedHeadを検査する。
受理済みC344/C345の再実行は不要。次はC346のremote latest.log/latest.jsonを判定する。
INVALIDなら同じC346の実行修復だけを行い、C347へ進まない。

## 根拠文書

- [C345受理記録](experiment-ledger-addendum-c345-c346.md)
- [C346事前登録](experiment-ledger-addendum-c346-preregistration.md)
- [C346独立レビュー](c346-post-authoring-review.md)
- [横断整理](cross-experiment-evidence-synthesis-2026-11-22.md)
- [横断evidence index](cross-experiment-evidence-index-2026-11-22.json)
- [正式handoff](experiment-ledger-and-handoff.md)

## 旧記録：C344受理とC345登録

以下は今回の統合前に保存されていた運用記録。現在の状態は上記を参照する。

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
