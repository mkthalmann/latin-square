# Get Latin Square Lists

The script has one main job: read a table-like object (either .csv, .txt, or .xlsx) with each item in all relevant conditions and output several lists (whose number is determined by the amount of conditions) based on a Latin Square (see below). In addition to simply splitting up the critical items, all single-condition sub-experiments present in the file will be appended to the lists with the critical (multi-condition) items in full. Currently, this only works with one critical sub-experiment; but extending it to overcome this difficulty should be relatively simple.

The principal intended use case is fully within (conditions are both within-items and within-subjects) linguistic experiments.

## Input File

### Critical Items

The following table is a typical (albeit quite short) example of an input file. Note that all items come in four versions representing a condition (read: a permutation) of the same base item.

| sub_exp | item_number | cond | item                                        |
| ------- | ----------- | ---- | ------------------------------------------- |
| 1       | 1           | a    | dass der Peter den Hans mag.                |
| 1       | 1           | b    | dass den Hans der Peter mag.                |
| 1       | 1           | c    | dass der Peter sicherlich den Hans mag.     |
| 1       | 1           | d    | dass den Hans sicherlich der Peter mag.     |
| 1       | 2           | a    | dass die Frau den Bäcker liebt.             |
| 1       | 2           | b    | dass den Bäcker die Frau liebt.             |
| 1       | 2           | c    | dass die Frau sicherlich den Bäcker liebt.  |
| 1       | 2           | d    | dass den Bäcker sicherlich die Frau liebt.  |
| 1       | 3           | a    | dass das Auto den Fahrer ärgert.            |
| 1       | 3           | b    | dass den Fahrer das Auto ärgert.            |
| 1       | 3           | c    | dass das Auto sicherlich den Fahrer ärgert. |
| 1       | 3           | d    | dass den Fahrer sicherlich das Auto ärgert. |
| 1       | 4           | a    | dass der Vater den Hund tritt.              |
| 1       | 4           | b    | dass den Hund der Vater tritt.              |
| 1       | 4           | c    | dass der Vater sicherlich den Hund tritt.   |
| 1       | 4           | d    | dass den Hund sicherlich der Vater tritt.   |

### Fillers

To add fillers (identifed by single-condition items) to the four output lists, the input table should contain them as different sub-experiments. Here's an example with two distinct filler experiments:

| sub_exp | item_number | cond | item                                          |
| ------- | ----------- | ---- | --------------------------------------------- |
| 2       | 1           | a    | Das Essen riechte lecker.                     |
| 2       | 2           | a    | Das Lied schlagte wie eine Bombe ein.         |
| 2       | 3           | a    | Das Sicherheitsnetz fangte den Akrobaten auf. |
| 2       | 4           | a    | Das Wunder geschehte an Weihnachten.          |
| 3       | 1           | a    | Das Fahrrad tut schnell fahren.               |
| 3       | 2           | a    | Das Mädchen tut ein neues Kleid tragen.       |
| 3       | 3           | a    | Das Radio tut laute Musik spielen.            |
| 3       | 4           | a    | Das Tuch tut im Wind wehen.                   |

## Latin Square

Below is a Latin Square for a 2x2 experiment (where 'a' to 'd' represent the relevant conditions). If the participants are evenly distributed across the four lists (and if enough participants are being tested), you'll have dependent measures by each participant for each item and for each condition of every item (though by different participants). This offers some advantages come statistical analysis. 

|                     | Participant 1 | Participant 2 | Participant 3 | Participant 4 | Participant 5 (same as P1) | ... |
| ------------------- | ------------- | ------------- | ------------- | ------------- | -------------------------- | --- |
| Item 1              | a             | b             | c             | d             | a                          | ... |
| Item 2              | b             | c             | d             | a             | b                          | ... |
| Item 3              | c             | d             | a             | b             | c                          | ... |
| Item 4              | d             | a             | b             | c             | d                          | ... |
| Item 5 (same as I1) | a             | b             | c             | d             | a                          | ... |
| ...                 | ...           | ...           | ...           | ...           | ...                        | ... |

## Feedback

If you have any comments, feature requests or suggestions, please feel free to send me an [e-mail](mailto:maik.thalmann@gmail.com?subject=[GitHub]%20Latin-Square).