# Kango-enrichment
Simple script to create readings and translations for a list of japanese kango



##### Examples and usage

*sample.csv*

| kango | reading  | translation             |
| ----- | -------- | ----------------------- |
| 先生  | せんせい | Teacher, doctor, master |

By default CSV file must contain fields **kango, reading  and translation** in the first row, which are used as a header (but the output file won't have the heading), separated by | .

Default usage would be:

```bash
python csv_modifier.py INPUT_FILE OUTPUT_FILE
```

But you can check more options in --help menu, however most of them are yet under development.

*N.B.* If the output file exists it will be overwritten

dsl_search.py can be used to find separate values in the dsl file, however it is much better to use programs like goldendict to explore dsl dictionariesю

##### Dependencies

- [pykakasi]: https://github.com/miurahr/pykakasi	"Github repo"

