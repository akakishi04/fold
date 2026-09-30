# V5-B answer-wise hardest-rival auxiliary — C291

C290 confirms a surrogate gap:a correct-versus-swapped two-answer sum can satisfy its margin even
when an individual answer loses the256-class argmax. For289002 quad HOLDOUT,the auxiliary arms met
all144 pair margins but missed one answer;the always-on mean pair penalty was about4.53e-11.
C290 did not determine whether cross-answer compensation or a third-class competitor caused this.

C291 tests a complete loss replacement rather than another withdrawal-time sweep. Keep ordinary CE
in every arm;compare CE alone,CE+the old pair-sum auxiliary,and CE+answer-wise hardest-rival softplus.
For each TRAIN row,the latter asks the correct answer to exceed the strongest of its255 alternatives.
A strong answer in a neighboring query cannot cancel that row's penalty. This mathematical property
is NOT evidence that its gradient will train the actual model better or improve length transfer.

There is no new architecture,tokenization,training length,budget,data source or answer-time filter.
Fresh seeds and concurrent controls are mandatory. Coefficient and margin stay .25 and1,but the
loss/gradient scale is not matched;aggregation and rival set change jointly. A positive result tests
the objective package,not an isolated mechanism. Retain all old masked capability checks.
No Gate F promotion,production adoption or broad language-model capability claim follows automatically.
