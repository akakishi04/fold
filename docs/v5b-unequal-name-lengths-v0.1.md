# V5-B unequal name-length composition — C320

C319 last-only trained from scratch reaches4/5 at unseen6;native mean-plus-last reaches5/5.
Keep the existing mixed readout rather than repeatedly search seeds or tune to a few errors.
The original tasks always use two names of equal length. Passing longer equal-length names
does not test whether length can differ between two entities in the same question.

Freeze all10 C319 states and test2+4 and4+2 names,with both fact orders and both queries.
Every individual name length is already in the trained range. No new vocabulary,longer frame,
training or decoder change. Retain each model's own trained policy and reproduce old outputs
before/after. Prospective baseline primary is fixed before new results;comparison arm retained.

Examples:aa=0;bbbb=1;aa= and aaaa=0;bb=1;bb=. The same values and question relation stay visible.
A failure would expose an untested compositional boundary,not prove a unique cause. A success
would be bounded to these name families/value splits and this retained cohort,not arbitrary
names or fresh-seed reliability. C319's negative and Gate F NOT PASSED remain separate.
