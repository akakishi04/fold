# C344までの横断エビデンス整理 — C345実行中の研究メモ

作成日: 2026-11-22（日本時間）。返答区分: **Operational / research synthesis**。

**結論:** 限定された課題を学習できることと、読み出し・データの提示方法・学習配分によって結果が変わることは、複数の比較で確認できている。一方、**名前の区別、値の組合せ、語順、長さが変わっても、既存の能力を保ちながら全seedで正しく対応付ける学習方法は確立していない**。平均値の改善、診断のPASS、限定条件での5/5を、この未解決点の解消と読み替えない。

今回の詳細整理は **C260〜C344の85実験**。C225〜C259の関連結果とGate文書は背景として参照する。C1〜C344を同じ深さで再監査した資料ではない。C345は事前登録だけを参照し、実行結果を含めない。

85件の内訳は、有効な陰性46件、診断整合性PASS34件、限定能力PASS5件。限定能力PASSはC263・C264・C269・C308・C320である。実験の目的と独立性が異なるため、この件数からモデルの「成功率」を計算しない。

## 1. 固定した範囲と読み方

|項目|この資料の境界|
|---|---|
|実験側の固定snapshot|`c81ffe102c3a9280f28a68e572403549ce77fa1d`|
|文書ブランチの基点|main `3986aaa1678ddf28e2f4611ddf131d09a6511acb`|
|最新の正式結果|C344 ACCEPTED VALID NEGATIVE。R1は有効、attempt01はINVALIDのまま|
|進行中|C345 ACTIVE / NOT YET JUDGED。保存済み目的関数・学習履歴の診断|
|次の実験|この資料はC346を設計・登録・実行しない|
|正式Gate|A/B PASSED、C/Dは測定範囲でPASSED、E PASSED、F NOT PASSED|
|成果物|本資料と[85実験のエビデンス索引](cross-experiment-evidence-index-2026-11-22.json)|

この資料は結果の再採点、正式台帳の上書き、production採用判断ではない。現在の正式状態は[handoff](experiment-ledger-and-handoff.md)が管理する。実行中の実験ブランチを無関係な文書変更で進めない規則に従い、`docs/c345-evidence-synthesis-2026-11-22`に保存する。[会話・実行プロトコル §0.1/§0.6](experiment-conversation-handoff-protocol.md)

### 比較の単位

1. **同じC内の対比較**は、初期値・データ・予算など、その実験が固定した範囲で介入の効果を読める。
2. **新seedによる再現実験**は、新しい初期値・提示順に結果が保たれるかを見る。ただし同じ合成課題の再利用であり、独立した外部ベンチマークではない。
3. **保存済み出力・固定checkpointの診断**は、既存結果の内訳や介入時の挙動を調べる。診断PASSは、モデルの能力向上を意味しない。
4. **別のC同士の生の正解率**は、seed・対照・提示範囲・予算が異なる場合、改善曲線として結ばない。

「正解した回答数」「両queryに正解したpair数」「複数基準からなるgate」「全条件を満たしたseed数」は別の単位である。同じ論理問題を言語・名前profile・語順・seedに展開した回答を、全て独立な標本として扱わない。表の集計は記述統計であり、統計的有意性や母集団での成功確率を新たに主張しない。

## 2. プロジェクト全体で、何ができて何が残っているか

|層|得られた証拠|残る境界|
|---|---|---|
|参照計算・会計|Gate Aで数値参照、勾配、保存量、実行量、状態の因果境界を検証|言語能力の証拠ではない|
|高精度コアの学習|Gate Bの限定合成課題で複数seedの学習が成立|小規模CPU測定ではDenseより遅く、一般LLMへの優越ではない|
|圧縮・routing|Gate C/Dは登録された合成課題・runtimeで成立|保存量・論理演算の削減を無条件の実時間短縮へ置き換えない|
|記憶の数値処理|C225〜C230で正しさ、保持量、対照との時間を分離して測定|強い対照と初期化費用を含めると広い速度優位は示されていない|
|テンプレート言語学習|C232でbyte lossが低下|意味の対応付けや有用な会話能力とは別。C233でcoreの一貫した優位は未成立|
|現在のbinding課題|条件によって高精度に学習・転用でき、介入効果も観測|新しい識別条件と既存条件の保持を、全seed・全gateで両立できていない|
|記憶との統合|Gate Fは未達|Writer/Readerの意味精度、訂正・撤回、scope、総記憶費用などの完了と、今回のbinding改善は同義ではない|

根拠: [Gate A](experiments/v05-gate-a-reference-computation.md)、[Gate B](experiments/v05-gate-b-high-precision-core.md)、[Gate C](gate-c-decision-2026-09-14.md)、[Gate D](gate-d-decision-2026-09-14.md)、[ロードマップ](development-roadmap-v0.5.md)、[C230](experiment-ledger-addendum-c230-c231.md)、[C232](experiment-ledger-addendum-c232-c233.md)、[C233](experiment-ledger-addendum-c233-c234.md)。

現在の一連の実験は、主として**圧縮なしのV5-B参照モデルで、文中の名前と値を対応付ける能力を切り分ける作業**である。最終構想の圧縮・記憶・可変長入出力・Visionを統合した完成モデルの評価ではない。Standalone Language Model Milestoneも[提案文書](proposals/standalone-language-model-milestone-proposal.md)ではDRAFT / NOT ADOPTEDであり、採用済みの完了基準にはしない。

### 他の研究系列から持ち越す重要な教訓

C227では、毎回大きな数値系を解き直す対照を、検証済み因子を再利用する対照へ強化すると、H1/H2のquery時間優位は消えた。C230の事前計算は元のH1/H2より12条件全てで速かったが、強い対照には11/12条件で遅い。唯一速かったn256・16queries/updateも、初期化を含む登録phase合計では29.6598ms対28.3935msとなり優位が消えた。**「自分の旧実装より改善した」と「適切な対照に勝った」は別の結論**であり、binding側にもこの比較原則を引き継ぐ。[C227](experiment-ledger-addendum-c227-c228.md)、[C230](experiment-ledger-addendum-c230-c231.md)

## 3. 経緯を、何を切り分けたかで整理する

|系列|主に切り分けたこと|次へ持ち越す知見|
|---|---|---|
|C235〜C247（背景）|TRAIN自体の失敗、サンプリング、語順・値のshortcut、通常入力への曝露|最終minibatch lossだけでは全TRAINを解けたと言えない。データ設計のshortcutをモデルの欠陥と混同しない|
|C248〜C263|tokenへの読み戻し、query源、3対象、語順coverage、core除去、提示順・学習率|読み出し経路は有効な介入点だが、core必要性や汎用的頑健性は未確立|
|C264〜C290|複数文字名、prefix/suffix、query pooling、補助目的関数|名前のどの部分をどう使うかで挙動が変わる。TRAIN fit・平均改善・転用gateは一致しない|
|C291〜C309|初期値、coreと残りの重みの組合せ、残差、coreの学習方針と再現性|一部の失敗は学習経路に敏感。ただし固定coreや低いcore学習率も全seedの解決策ではない|
|C310〜C320|失敗の長さ間対応、値のbalance、長さ配分、固定読み出しと学習し直し|同じcheckpointの長さ転用と、新しい学習方式の効果を分ける。限定転用PASSの射程を守る|
|C321〜C329|内部の文字順による名前区別、明示的学習、混合の粒度、勾配、予算|内部順序の課題は難しく、学習に入れると大幅に改善するが、既存条件との保持に問題が残る|
|C330〜C344|gate内訳、query pooling、支持値loss、長さ4/5の配分、pair-max|改善と新規regressionが同居する。既存の誤りを救った数だけでは介入を評価できない|

各Cの変更変数、対照、cohort、budget、判定、数値、非主張、出典は[索引](cross-experiment-evidence-index-2026-11-22.json)に保存した。`compatibility_family`は検索用のまとまりであり、まとめて再採点してよいという意味ではない。

## 4. 比較実験で効果が確認できたもの

### 4.1 データのcoverageと提示方法は効く

C238では、同じ16promptを全て含むbatchへ変更すると、FullとGRU-onlyの全12cellが8/8に達した。ただし見たpromptのfitである。続くC239では、学習した語順の全TRAIN基準は通るのに、逆の語順への転用は失敗した。C241ではTRAIN正解率100%でも、値を隠しても100%のままで、固定された名前→値の対応だけで解ける設計上のshortcutが残っていた。[C238](experiment-ledger-addendum-c238-c239.md)、[C239](experiment-ledger-addendum-c239-c240.md)、[C241](experiment-ledger-addendum-c241-c242.md)

3対象課題のC259では、2語順から6語順を学習する介入により、同じ実験のHOLDOUTは1704→1984/2160、全条件合格は2/5→4/5となった。しかし候補1seedはTRAINを完全に解いても値の組合せHOLDOUTで失敗した。C262では、初期値と曝露数を合わせても提示順を変えると回答が変わった。**学習例を増やす・順番を変えることは無関係ではないが、それだけで未見の対応付けが保証されるわけでもない。**[C259](experiment-ledger-addendum-c259-c260.md)、[C262](experiment-ledger-addendum-c262-c263.md)

### 4.2 読み出しの構造にも実測上の効果がある

C256のaligned readerは、3対象・元の2語順の課題でHOLDOUT718/720、全条件5/5。parameter数を合わせたEOSのみの対照は248/720、0/5だった。ただし計算量一致の比較ではなく、coreそのものの優位を示す比較でもない。同じ候補を新しい4語順へ移すC257では2/5に留まった。[C256](experiment-ledger-addendum-c256-c257.md)、[C257](experiment-ledger-addendum-c257-c258.md)

C269では、query源をEOSから可視query spanの平均へ変えると、完全gateは4/5→5/5、HOLDOUT正解は1276→1440/1440となり、限定能力PASSを得た。ただし名前profileはTRAINで見ており、未見の名前長への転用を証明する試験ではない。続くC270の未見3文字条件では両方式とも0/5だった。[C269](experiment-ledger-addendum-c269-c270.md)、[C270](experiment-ledger-addendum-c270-c271.md)

C278のquery span平均と末尾を別々に読む変更は、3文字条件の全回答3938→4207/4320、同じ回答に潰れたquery pairは314→95/2160に改善し、全5seedで正解数が増えた。しかし3文字の完全gateは0/5のまま。改善はshared-prefixに強く、shared-suffixには弱かった。この場合のTRAIN/HOLDOUTは値の組合せの区分であり、3文字名自体は学習に使っていない。[C278](experiment-ledger-addendum-c278-c279.md)

### 4.3 内部順序を区別する課題は、学習への導入で改善する

C321では、同じ端点・同じ文字多重集合で内部順序だけが違う名前を、既存checkpointが安定して区別できなかった。mean_lastの正解は2211/4320、last_onlyは2292/4320で、完全gateは両方0/5。query pair collapseはそれぞれ1996/2160、1951/2160だった。[C321](experiment-ledger-addendum-c321-c322.md)

この失敗は「現在の構造では一切学べない」という証明ではない。C324の明示的なinterior学習で、同じ実験内のHOLDOUTは716→1396/1440、両query正解は22→685/720へ改善した。ただし元の課題の保持は2/5→0/5になった。**学べることと、他の条件を壊さずに学べることが別の問題として残った。**[C324・R6の受理結果](experiment-ledger-addendum-c324-c325.md)

## 5. 重要な比較結果を一枚の表にする

矢印は全て**そのCの対照→候補**。異なる行同士を同一cohortの時系列変化として読まない。

|C|変更|観測された改善|同時に残った失敗・悪化|
|---|---|---|---|
|[268](experiment-ledger-addendum-c268-c269.md)|CEにquery-pair marginを追加|HOLDOUT1100→1115/1440、collapse114→107/720|完全gate3/5→3/5。正解増15は1seedだけ、shared-suffix collapse38→39|
|[278](experiment-ledger-addendum-c278-c279.md)|mean_span→mean+final dual|3文字全回答3938→4207/4320、全5seedで改善|3文字gate0/5→0/5、suffix側の弱さが残る|
|[288](experiment-ledger-addendum-c288-c289.md)|CEにpair-assignment目的を追加|学習長のTRAIN direct3/5→5/5、4文字全回答3902→4011/4320|4文字gate3/5→1/5。元々通った2seedを失う|
|[308](experiment-ledger-addendum-c308-c309.md)・[309](experiment-ledger-addendum-c309-c310.md)|core学習を遅くする／凍結と比較|C308でcore_slowとcore_frozenは各5/5、full_train4/5|新seedのC309ではslow/frozen各4/5、full3/5。slowのfreezeに対する合格数優位なし|
|[324](experiment-ledger-addendum-c324-c325.md)|interior学習を導入|interior HOLDOUT716→1396/1440、pair22→685/720|元課題保持2/5→0/5、候補の総合条件は0/5|
|[326](experiment-ledger-addendum-c326-c327.md)|同じ曝露をupdate内で混合|interior HOLDOUT1005→1316/1440、全5seedで改善|元の2〜6文字計7048→7015/7200、4seedで元課題正解数が減る|
|[328](experiment-ledger-addendum-c328-c329.md)|後半の学習率を1/10へ|この固定介入にinterior改善はなし|interior1350→1261/1440、全5seedで減少。元課題も合計−53回答|
|[329](experiment-ledger-addendum-c329-c330.md)|同じ軌道を1200→2400updateまで延長|interior1206→1427/1440、pair544→708/720、全5seedで増加|登録された総合paired successは1/5。6文字の完全gateは1/5→1/5|
|[338](experiment-ledger-addendum-c338-c339.md)|表示値へのsupport lossを追加|original2/3/4・interior4の完全正解を保持|6文字1389→1375/1440、表示外の値27→49。候補の完全gate0/5|
|[340](experiment-ledger-addendum-c340-c341.md)|学習長4を5に置換|6文字1396→1439/1440、interior1374→1434/1440|4文字1439→1433/1440。候補完全gate2/5|
|[342](experiment-ledger-addendum-c342-c343.md)|長さ5のみの枠を4/5混合へ|全domainのHOLDOUT集計が増加。original2〜5は全候補で完全正解|候補完全gate2/5。4文字の+50は1seedのみ、別seedで6文字−5|
|[344](experiment-ledger-addendum-c344-c345.md)|通常mean CE→query-pair max CE|6文字HOLDOUT1431→1438/1440|interior1430→1331/1440、pair712→640/720。完全gateは両方2/5だが合格seedが異なる|

この表から「全ての変更が無意味」とは言えない。大きい効果は複数ある。ただし**一つの領域の改善が、全体の安定した解決へ積み上がったという証拠は不足している**。

## 6. 繰り返している失敗の形

### 6.1 値を拾うことと、質問された名前へ結び付けることは違う

二つの値を持つ文に対して、質問する名前だけを変えても同じ値を答える場合がある。両方の正解が異なるので、同じ出力なら少なくとも片方は誤る。ただしcollapseは「片方だけ正解」と同義ではなく、両方不正解の場合もある。逆に、二つの値を入れ替えて答えるswapは出力が変わっていても両方誤りである。

C343で調べたC342候補のinterior TRAINでは、131誤答の全てが**もう一方の表示値**だった。1440query pairの内訳は1312両方正解、125片方正解、3両方不正解で、125collapse・3swapが記録された。これは、実際に学習に提示したinterior例でも対応付けの誤りが残るという観測である。[C343](experiment-ledger-addendum-c343-c344.md)

### 6.2 「queryを完全に無視」とも断定できない

C322では、C321の失敗状態でもqueryを替えると出力スコアは変化していた。C323では両query・両語順で同じargmaxに留まる形が多かった。したがって、**スコアの変化はあるが正しいクラス選択には足りない**という記述が適切である。単純な先頭／末尾fact追従や、内部でquery表現が完全に消えているという断定には進めない。[C322](experiment-ledger-addendum-c322-c323.md)、[C323](experiment-ledger-addendum-c323-c324.md)

### 6.3 TRAINというラベルだけで「学習済み」と読まない

現在のデータでは、TRAIN/HOLDOUTは主に**値の組合せ**の区分である。original6のTRAINは、見慣れた値の組合せでも、6文字の名前・promptはfitに一度も使っていない。C344の実際の提示数は、論理TRAIN rowごとにoriginal2/3が各200、original4/5が各50、interior4が100、original6が0だった。[C344 preregistration](experiment-ledger-addendum-c344-preregistration.md)、[C344の完了・計画照合](experiment-ledger-addendum-c344-c345.md)

|評価上の状況|適切な読み方|
|---|---|
|実際に提示したinterior TRAINで誤る|学習対象そのもののfit不足を含む|
|提示していない6文字のTRAIN区分で誤る|既知の値の組合せを、新しい名前長に移す失敗|
|HOLDOUT区分で誤る|未学習の値の組合せへの転用失敗。名前長などの軸も別に確認する|
|normal正解でもmask/order gateで落ちる|回答正解と、登録された証拠利用・一貫性基準を区別する|

### 6.4 平均改善の裏で、新しい誤りが作られる

C342のinterior HOLDOUTは101回答を救い、30回答を新たに誤りへ変えたため、差引+71だった。original6は55救済・6新規誤りで+49。候補HOLDOUTに残った6文字の6誤答は全て対照が正解していた回答だった。[C342](experiment-ledger-addendum-c342-c343.md)、[C343](experiment-ledger-addendum-c343-c344.md)

C344ではこの入れ替わりがさらに明確である。

|interior4|正解数（対照→候補）|救済|新規誤り|差引|
|---|---:|---:|---:|---:|
|実際に学習したTRAIN回答|2864→2728 / 2880|16|152|−136|
|HOLDOUT回答|1430→1331 / 1440|10|109|−99|
|TRAIN両query正解pair|1424→1293 / 1440|16|147|−131|
|HOLDOUT両query正解pair|712→640 / 720|8|80|−72|

対照のinterior誤答は全て救っている一方、候補のinterior誤答は全て新規である。**同じ難問が残り続けただけ、という説明ではこの結果を説明できない。**ただし、これだけで忘却の時点や内部機序が分かったわけではない。候補が一度正解を学んでから失ったかは、最終checkpoint同士の比較では分からない。[C344](experiment-ledger-addendum-c344-c345.md)

## 7. loss・目的関数について、何が分かり何が未確定か

### 7.1 補助指標を改善しても、最終回答が改善するとは限らない

C268の最後の学習batchではpair penaltyが0でもHOLDOUT失敗が残った。C288では学習長のTRAIN directが5/5になっても4文字gateが悪化した。C290の固定checkpoint診断でも、補助marginを満たすことと正しい256分類の回答が一致しない例がある。特定の補助制約を達成することは、課題の完全gateを達成する十分条件ではない。[C268](experiment-ledger-addendum-c268-c269.md)、[C288](experiment-ledger-addendum-c288-c289.md)、[C290](experiment-ledger-addendum-c290-c291.md)

### 7.2 支持値への確率と、支持値内の選択を分ける

C339は、C338の全720strataを集計した追記を含めて読む必要がある。original6 HOLDOUTでは、support NLLは0.059862129→0.082290481に悪化した一方、within-pair NLLは0.148967192→0.142362736に改善し、正解数は1389→1375に減った。選択されたseed338004の悪化例だけを全体へ一般化してはいけない。[C339・全cohort追記](experiment-ledger-addendum-c339-c340.md)

ここでは、表示された二値のどちらかへ確率を置くことと、その二値の中から正しい方へ確率を置くことを分離している。平均NLLの改善とargmax正解数の改善も別である。confidenceの平均変化から、全回答の改善や全seedで同じ機構が働いたと推測しない。

### 7.3 C344のpair-maxは何を変更したか

C344は、48回答のfull-256-class CE平均を、24query pairそれぞれの大きいCEを取る平均へ変えた。pair内のCEをa,bとすると、`max(a,b) = (a+b)/2 + |a-b|/2`。同じlogits上では、pair-maxは通常平均CEにpair内の差への項を加えた量になる。実装は同値のときの勾配を対称に分配する`torch.maximum`を使う。[C344 source](../fold_lm/v05_benchmarks/model_c344_pair_max_training.py)、[C344 preregistration](experiment-ledger-addendum-c344-preregistration.md)

この定義から、勾配の配分が変わることは分かる。しかし**正解率が悪化した原因が勾配の不足・clipping・収束不足だとは、まだ言えない**。異なるarmの最終logitsで、どちらの目的関数がどれだけ改善・悪化したかを、同じ尺度で調べる必要がある。これがC345の問いにつながる。

## 8. 原因の推測を、証拠の強さで並べる

|候補となる説明|現在の評価|根拠と未解決点|
|---|---|---|
|学習データのcoverage・配分・提示順への感度|**複数の対比較で支持**|C238/259/262/324/326/329/340/342で結果が動く。ただしcoverage、balance、token数、勾配履歴が同時に変わる場合がある|
|名前から値を選ぶ読み出しと、それを学習する経路の組合せが不安定|**有力な作業仮説**|C256/278の読み出し効果、C297〜299のcoreと他重みの相互作用、C308/309の再現性、C343/344の誤りが整合。ただし故障箇所を一つのmoduleに同定していない|
|目的関数と完全gateのずれ|**特定の目的では観測済み**|C268/288/290/338。C344の最終surrogate lossと回答悪化の関係はC345待ち|
|全てが同じgradient conflictで説明できる|**支持不足**|C327の全parameter dotは18/60で負だが、50/60で二つのTRAIN損失の負の平均勾配 `−(g_old+g_inside)/2` が両損失を一次近似で下げる方向だった。終端の幾何からAdamWの全軌道を断定できない|
|常に学習量が足りない|**一般形では支持不足**|C295の800→1600updateでも2seedのTRAIN失敗が残る。C329延長は大きく効いたが全gate未達。C288ではTRAIN fit達成後にも転用が失敗する|
|単純にcoreを除去／凍結すれば解決|**支持不足**|C260除去も3/5、C309のslow/frozenも4/5。除去はparameter数やclipping等も変える|
|名前長の偶奇、capacity不足、optimizerやclippingが唯一の原因|**未証明**|特定例と整合することはあるが、競合仮説を排除する対比較がない。C345も因果的な証明にはならない|
|モデル全体が学習不能・構想全体が成立しない|**現データからは結論できない**|限定能力PASSと大きな介入効果が実在する。ただしそれらは実用LLMやGate Fの完成証拠でもない|

追加の根拠: [C260](experiment-ledger-addendum-c260-c261.md)、[C295](experiment-ledger-addendum-c295-c296.md)、[C297](experiment-ledger-addendum-c297-c298.md)、[C298](experiment-ledger-addendum-c298-c299.md)、[C299](experiment-ledger-addendum-c299-c300.md)、[C308](experiment-ledger-addendum-c308-c309.md)、[C309](experiment-ledger-addendum-c309-c310.md)、[C327](experiment-ledger-addendum-c327-c328.md)。

C297〜C299は同じ3初期値を使って要素を分解した、互いに依存する比較である。coreと他の重みの組合せの重要性を示す手掛かりにはなるが、独立した新seedで同じ原因が再現したという件数には加えない。C327の残る10条件で、あらゆる共通下降方向が存在しないと証明したわけでもない。

現時点で最も妥当なまとめは、**小さな合成binding課題でも、読める情報を正しい回答へ安定して変換する学習が、提示分布と学習経路に強く依存している**というもの。これは観測を説明する作業仮説であり、単一の内部原因の確定ではない。

## 9. C345が答えられることと、その後の判断

C345は、C344の10状態、6domain、両splitの保存済みlogitsと全24000学習trace行を使う。科学的な新規forward・gradient・update・model-state-loadは0。51840normal回答、25920query pair、120終端要約、60対比較を再構成し、各状態12個、全10状態で120個の固定200step blockと、180個のcycle/slot/profile別groupを調べる。[C345 preregistration](experiment-ledger-addendum-c345-preregistration.md)

### 結果が出た後に使う解釈表

|C345で観測した場合|支持される限定的な読み方|それだけでは言えないこと|
|---|---|---|
|同じdomain/splitで、候補の終端pair-max lossが対照より高く、回答も悪い|その固定評価対象では、候補はpair-max尺度でも対照より悪い終端状態だった|最適化が唯一の原因、学習延長すれば直る、収束済み／未収束の断定|
|終端pair-max lossが低いのに回答が悪い|平均surrogate改善と回答・pair基準の悪化が共存する|全TRAIN目的が改善した、どの補助目的も無効、他のcohortでも同じ|
|特定slot/profileや後半blockでloss/normが変わる|保存されたbatch条件とその変化に関連がある|その成分が特定domainの誤りを起こした、特定例を学習後に忘れた|
|seedごとに方向が異なる|一つの集計説明では不足。全seedを保持して説明を分ける必要がある|都合のよいseedだけ選べば解決した|
|差が小さい、または混在する|この診断だけでは原因を一つに絞れない|追加の係数探索を自動的に始めてよい|

判定を歪めないため、次を固定する。

- 終端lossは**domain/split別の平均**。曝露回数で重み付けした学習目的全体ではない。
- original6 TRAINの名前はfitされていない。
- slot4はoriginal4・original5・interior4の混合。slot4 lossを特定familyのlossとして扱わない。
- norm>1の件数は閾値超過の記述。正確なclipping発動回数や、因果的な障害の証明ではない。
- traceは各update前のminibatch測定。最後のtrace行は最終checkpointの全cohort lossではない。
- 診断PASSならC344の`candidate_gate=false / eligible_seed_count=2`を保存する。好ましいlossの符号をPASS条件に追加しない。

これらは[現在のhandoff](experiment-ledger-and-handoff.md)と[事前登録](experiment-ledger-addendum-c345-preregistration.md)にある境界であり、本資料による後付け変更ではない。

## 10. 今後の実験選びに持ち越す基準

### 優先する問い

**第一は、C345によって実際に狭まった不確実性に対して、一つの対比較を作ること。** lossがどう動いたかを確認する前に、pair-max係数、学習率、pooling、幅を同時に変えない。次の正式Cの設計・固定gate・source・レビューは、C345判定後に別途行う。

**第二は、fit・転用・保持を同時に読むこと。** 候補の新領域改善だけでなく、対照で正解だった回答の新規誤り、各seedの合格交代、既存domainの保持を表示する。平均だけで研究の進歩を判断しない。

**第三は、新seedと新しい評価分布を区別すること。** C308→309、C315→316のような再現性確認は有用だが、同じtaskを繰り返し観察して設計している事実は残る。将来広い能力を主張する段階では、開発に使っていないname/value/order/templateの評価を、別の固定contractとして設計する必要がある。このメモでは新しいholdoutを生成・登録しない。[C308](experiment-ledger-addendum-c308-c309.md)、[C309](experiment-ledger-addendum-c309-c310.md)、[C315](experiment-ledger-addendum-c315-c316.md)、[C316](experiment-ledger-addendum-c316-c317.md)

### 各結果で残すと再利用しやすい記録

|記録|必要な理由|
|---|---|
|model seedとschedule seed、同じ初期値か、継続軌道か|初期値と提示順の効果を混同しない|
|論理splitと、実際にfitした名前・prompt・曝露数|TRAINラベルだけで暗記やfitを主張しない|
|updates、rows、非padding token、parameters、計測範囲|同じupdate数を同じ学習費用と呼ばない|
|回答、query pair、両語順、mask、seed gate|単位の違う成功・失敗を混ぜない|
|rescued / regressed / persistent wrong|差引改善の内側にある誤りの入れ替わりを残す|
|wrong_observed / absent_digit / outside_catalog|表示値の選択と、値への支持そのものを分ける|
|full256 CE、登録objective、mean/max、集計重み|違うloss定義を直接比較しない|
|実行HEAD、publication、logのbyte/SHA、invalid attempt|科学的な証拠と、実行・輸送上の失敗を分ける|

これは既存実験の必須schemaを変更する指示ではない。今後新しいcontractを設計するとき、何を失わず記録するかのチェック項目である。

### 同じ理由だけで繰り返さないもの

- 「collapseが残るので損失項や集約方法を変える」という一般論だけで、既に陰性だった特定のC268/C288/C338/C344処方を再試行しない。新しい検証可能な機構と固定比較が必要。
- 「低いcore学習率なら安定する」とC308の5/5だけを採用根拠にしない。C309の反例を併記する。
- 固定checkpointの読み出し置換で一部が救われたことを、その置換で最初から学習すれば優れる証拠にしない。C317/318の固定診断とC319の学習比較を分ける。
- 一つの良いseed、良い語長、良い集計を選んで正式gateを緩めない。

陰性は、その処方・cohort・予算での結論であり、全ての将来の関連方法を禁止する証明ではない。[C268](experiment-ledger-addendum-c268-c269.md)、[C288](experiment-ledger-addendum-c288-c289.md)、[C317](experiment-ledger-addendum-c317-c318.md)、[C318](experiment-ledger-addendum-c318-c319.md)、[C319](experiment-ledger-addendum-c319-c320.md)

## 11. 証拠の完全性と今回行った確認

### 今回、独立に確認した範囲

C260〜C344について、各受理報告・`latest.log`・`latest.json`の**255ファイル**を固定snapshotとbyte単位で照合した。85件全てについて、公開logのLFからWindows CRLFを復元した場合を含め、publisherが記録したbyte数とSHA256が一致した。各publication commitはmetadataのexecution HEADを唯一のparentとし、変更pathは当該logとreceiptの2ファイルだけだった。これらのblob・digest・HEADは[索引](cross-experiment-evidence-index-2026-11-22.json)に保存した。

これは**公開された証拠の同一性・輸送の確認**である。今回、ユーザー環境にしかない`runs/`、dataset、NPZ、checkpointを読み直したり、学習・推論を再実行したりしていない。元の受理時に報告範囲が限定されていた実験を、後から「全native artifact再検証済み」へ格上げしない。数値の出典は受理報告と公開consoleであり、診断で再利用したcheckpointは新しい独立試行に数えない。

### 運用上の失敗と科学的陰性を分ける

C324の最終R6、C344の最終R1のように、有効な試行へ到達する前のINVALIDがある。古いattemptは履歴として残し、性能の悪いseedや有効な陰性として加算しない。C344 attempt01の`execution_log_publish=PASS`はlog公開成功であって、科学実行成功ではなかった。[C324](experiment-ledger-addendum-c324-c325.md)、[C344](experiment-ledger-addendum-c344-c345.md)

C344の6514tests・239modules・930source pins・8183protected inputsの確認は、結果を信頼するための実行証拠である。これらの件数が増えたことはモデル能力の向上ではない。実行費用を将来扱う場合も、科学計算、回帰検査、保護・再検証、log輸送を区別して測る。[C344](experiment-ledger-addendum-c344-c345.md)

## 12. 保存物と更新方法

- 本資料: 人が読む知見、比較表、原因仮説、C345後の解釈境界。
- [cross-experiment-evidence-index-2026-11-22.json](cross-experiment-evidence-index-2026-11-22.json): C260〜C344の85件を検索できる、出典付き文献索引・要約。正式な実験出力artifactや学習datasetではない。

この日付の資料はC344までのsnapshotとして保持する。C345の判定後は、その結果を別の正式受理記録に残した上で、この資料のどの仮説が支持・弱化・未解決になったかを追記または後続の横断整理に記録する。古い推測を、当時すでに確認できていた事実へ書き換えない。
