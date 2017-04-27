# Billy-Bot
Danger, Danger Will Shakespeare

*A sentiment analysis to track the emotional arcs of Shakespeare's plays*

## How it works
Each speaking role that a character is given is treated as a token. Speeches longer than
200 words are broken apart into smaller tokens with a max length of 200 words. In order to
maintain an accurate and full sentiment analysis of a sentences, tokens will be taken only
from completed sentences. This will prioritize a token that is <200 words as long as doing so will maintain the integrity of the sentence. Tokens that are from the same speech will be tagged internally.

The following a single monologue taken from Hamlet. The entire speech is 275 words, as a result it will take up two tokens. Neither token is 200 words long as to do so would break into a single sentence. Note, syntax errors like 'tis and wish'd are taken care of when filtered into program, becoming tis and wished respectfully.
##### *Token Example*
##### Assigned to Character='HAMLET' is 167 words, tagged='CONTAINS CHILD, (CHILD ID)'
    To be, or not to be: that is the question:
    Whether ’tis nobler in the mind to suffer
    The slings and arrows of outrageous fortune,
    Or to take arms against a sea of troubles,
    And by opposing end them? To die: to sleep;
    No more; and by a sleep to say we end
    The heart-ache and the thousand natural shocks
    That flesh is heir to, ’tis a consummation
    Devoutly to be wish’d. To die, to sleep;
    To sleep: perchance to dream: ay, there’s the rub;
    For in that sleep of death what dreams may come
    When we have shuffled off this mortal coil,
    Must give us pause: there’s the respect
    That makes calamity of so long life;
    For who would bear the whips and scorns of time,
    The oppressor’s wrong, the proud man’s contumely,
    The pangs of despised love, the law’s delay,
    The insolence of office and the spurns
    That patient merit of the unworthy takes,
    When he himself might his quietus make
    With a bare bodkin?
##### Assigned to Character='HAMLET' is 108 words, tagged='CONTAINS PARENT, (PARENT ID)'
    Who would fardels bear,
    To grunt and sweat under a weary life,
    But that the dread of something after death,
    The undiscover’d country from whose bourn
    No traveller returns, puzzles the will
    And makes us rather bear those ills we have
    Than fly to others that we know not of?
    Thus conscience does make cowards of us all;
    And thus the native hue of resolution
    Is sicklied o’er with the pale cast of thought,
    And enterprises of great pith and moment
    With this regard their currents turn awry,
    And lose the name of action.–Soft you now!
    The fair Ophelia! Nymph, in thy orisons
    Be all my sins remember’d.

Once the tokens have been created they are assigned a number of identifying features. Each token will have a tag that assigns it to a particular character as well as an optional tag to identify it as a child or parent (if needed). It will also be given a relative location within the entire play.
