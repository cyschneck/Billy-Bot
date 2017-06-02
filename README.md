# Billy-Bot
Danger, Danger Will Shakespeare!

*A sentiment analysis to track the emotional arcs of Shakespeare's plays*

## Text
Fasta files are edited files from gutenberg files. Edits made for readable for tokenization and not meant to infringe on any rights. For full license information look into the gutenberg file. Fasta file reads as follows: 
```
>charcter<ACT><SCENCE>_<# of times they have spoken this act/scene>
```
## Existing Code
Currently, code is specific for *Hamlet*, but can be eventaully generalized to take in any .fasta formatted Shakespeare play. This progress is ongoing.

## Running Code

## How It Works
Each speaking role that a character is given is treated as a token.
Polarity determines either postive or negative emotions, graphed in either red or blue. Values at 0.00 are considered neutral and are not being properly classifed in the play.
Code produces a .csv file and plots the polarity over time (see graphs below).

## To Run Code
1. Download or clone repo
2. ```python shakespeare_sentiment.py -f hamlet.fasta```
    * Additional arguments to include: specific act, scene and/or character
To run the entire play (no specific character)

```python shakespeare_sentiment.py -f hamlet.fasta```

To run a specific act (no specific character, e.g. Act 3) use -A command followed by the act value (accepts for 3, three, III)

```python shakespeare_sentiment.py -f hamlet.fasta -A 3```

To run a specific act and scene (no specific character, e.g. Act 3, Scene 1) use -A to specify act and -S for the scene, requires both the act and scene to run for a scene

```python shakespeare_sentiment.py -f hamlet.fasta -A 3 -S 1```

To run any combination of acts and scenes for a specific character add the -C command (e.g., Hamlet)

```python shakespeare_sentiment.py -f hamlet.fasta -C hamlet```

```python shakespeare_sentiment.py -f hamlet.fasta -A 3 -C hamlet```

```python shakespeare_sentiment.py -f hamlet.fasta -A 3 -S 1 -C hamlet```

## Future Work
The existing code has been classifed based on the sentiment results of textblob. Textblob was trained on modern movie views and isn't optimized for Old English. Future work will train the classifers on Shakespeare text (e.g. sonnets). . The program was initially trained on contemporary movie reviews so the line of blue dots on the 0 mark represent sentences in a speech that the program considered to be neutral statements. Neutral statements are false positive results and artificially pull up the average polarity of the entire play. Among lines that the program was unable to parse were either due to the antiquity language (“o fie!” 1.2.6) or because the program was not properly trained on Old English word choice (“He was a man, take him for all in all, I shall not look upon his like again” 1.2.14). This process will include labelling specific words in Hamlet with stronger negative associations that are common in Shakespeare’s plays (e.g serpent, foul, fate, ghost, rotten, harrow, villain). Once trained, I expect the overall trend to decline toward largely negative emotions and polairty

## *Hamlet*: Results
### All Characters Across the Play
Full play
![image](https://cloud.githubusercontent.com/assets/22159116/25731457/c44ee148-3103-11e7-97c6-7a4eaca06946.png)
Act I
![image](https://cloud.githubusercontent.com/assets/22159116/25731483/f908050e-3103-11e7-9153-0432b9c1c58b.png)
Act II
![image](https://cloud.githubusercontent.com/assets/22159116/25731501/2262cede-3104-11e7-8454-60d8d59f4a19.png)
Act III
![image](https://cloud.githubusercontent.com/assets/22159116/25731524/456c1818-3104-11e7-800e-897b1beaf260.png)
Act IV
![image](https://cloud.githubusercontent.com/assets/22159116/25731571/865f5e20-3104-11e7-8732-14fcecb1f552.png)
Act V
![image](https://cloud.githubusercontent.com/assets/22159116/25731594/b2d0ffe0-3104-11e7-81b6-abf5ca45f93e.png)

### Emotional Arcs of Specific Characters Throughout their Lines in the Play
Hamlet through the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731620/fc16c892-3104-11e7-9f4c-cefd3667936d.png)
Horatio throughout the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731293/3604aba8-3102-11e7-9ffd-65c50e3b7ba2.png)
Gertrude throughout the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731628/18891016-3105-11e7-9d7a-59fe10c62290.png)
Claudius throughout the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731332/93d66ea6-3102-11e7-8174-71d9945df513.png)
Laertes through the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731727/25012f76-3106-11e7-98a2-137f705b0e77.png)
The Ghost of King Hamlet throughout the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731734/41aa12be-3106-11e7-9a8a-590277d2e1e6.png)
Rosencrantz throughout the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731753/64aad8c0-3106-11e7-9e6d-c385991538a9.png)
Guildenstern throughout the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731759/8c7b9b96-3106-11e7-85c5-38ba5c79bc15.png)
The Players throughout the play
![image](https://cloud.githubusercontent.com/assets/22159116/25731777/a9ed4a12-3106-11e7-9b91-7957908acfdc.png)
