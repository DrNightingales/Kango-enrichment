# Kango-enrichment
A simple script to create readings and translations for a list of japanese kango



##### Examples and usage
By default the script accepts a CSV file with 3 columns  as an input. The columns should contain the following headers - **kango**, **reading**, **translation**. Values of **reading** and/or **translation** may be missing in some/all rows. The output is a CSV file of the same format with missing cells having been filled where possible. If option `-T` is provided it will change output to a JSON file of the format:
```javascript
[
{  // word 1
  'kango': 'some_japanese_hyerogliphs',
  'reading': 'hirana_reading',
  'translation': 'english_translation_of_the_word',
  'examples': ['example 1 from tatoeba',
            // Some more examples
            'example n form tatoeba']
}, 
// some more words
// ...
]
```
*sample_intput.csv*
| kango | reading  | translation             |
| ----- | -------- | ----------------------- |
| 先生  | | |

*sample_output.csv*
| kango | reading  | translation             |
| ----- | -------- | ----------------------- |
| 先生  | せんせい | Teacher, doctor, master |

Default usage would be:

```bash
python csv_modifier.py sample_input.csv sample_output.csv 
```

*N.B.* If the output file exists it will be overwritten

dsl_search.py can be used to find separate values in the dsl file, however it is much better to use programs like goldendict to explore dsl dictionariesю

##### Dependencies

- [pykakasi](https://github.com/miurahr/pykakasi)
- `tatoeba_links.db` provided by [Tatoeba Project](https://tatoeba.org/en) under the Creative Commons license

