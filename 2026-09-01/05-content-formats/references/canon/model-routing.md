# Model routing by shot type

> **This ships empty on purpose.** The original held one company's own material, which would make
> your output look like theirs. The structure below is the part that transfers. Fill it in once and
> every format in this repo starts reading from it.
>
> Fastest way to fill it: run `funnel-builder` or `member-business-interview` in the same workspace
> first. Their corpus pass produces most of what goes here, in your buyers' own words.

Which generation model owns which kind of shot. **Verify every id and parameter against the tool's
own docs before you write it down here**, because a wrong id fails at spend time.

```
shot type: <e.g. product on a plain ground>
model: <exact model id>
parameters: <the ones that matter, with values>
verified: <date, and where you checked>
cost per generation: <number>
never use for: <the failure mode>
```

Two rules worth keeping whatever your stack is:

- **A model call is for judgement.** Composition arithmetic is arithmetic. Write the rule.
- **One paid generation at a time** until a format is proven. Never batch a set you have not seen a
  single example of.
