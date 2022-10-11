# cre8orforge

A silly little idler that is themed around the creative process. It's intended to
be integrated with Discord bots or other text-chat clients, but it is very much playable
on its own.

Eventually, it is planned to have expanding gameplay that unfolds in 3 stages; the
first is the starting 'clicker' idler, the second is a gacha training game based
around the completion of a high-tier activity from the first stage, and the third
builds on grown gacha that assemble into groups and help you attain goals on a
galactic scale.

For now, focus is on the first stage; we want a good solid first game mode before
expanding.

## Goals

* Be playable and fun to use over a text-based chat client
* Make it fun to participate outside the game in a chat community

Another goal:

* Never ever charge a cent of real world money

8asically we got really fed up with shitty game mechanics preying on human psychology to pull money outta them,
shit's disgusting as hell. We 8nt goin down that route, get fucked 8efore we do that shit.

Cre8orForge will 8e free as in 8eer and free as in freedom for as long as we can legally ensure that this is the
case. We will *never* allow any microtransaction that reel-world money can be used for.

## Dev Setup
Make shore you have python 3.8+ with support for Tkinter installed, then clone the repo:

```bash
git clone git@github.com:dekarrin/cre8orforge.git
```

That's pretty much it! There are no additional dependencies at this time, so no
virtual environment is needed. This is 8y design.

## Dev Execution

Once installed following the Dev Setup section above, the bash script `cf.sh` at the root of the program
can be directly invoked, as it will automatically find the local virtual environment, activate that,
then start the Python script for the game. Handy, right? ::::)

You can run it with the GUI by giving it the `gui` argument:

```bash
./cf.sh gui
```

Or, you can run it as a CLI directly using the commands, such as:

```bash
# get the status of the current idle game (or make a new one if we dont have one yet)
./cf.sh status

# show the store listings:
./cf.sh store

# click on the first job to start an execution of it and show overall game status
$ ./cf.sh click job 0
```

If you need any further help, try running with `-h`:

```bash
./cf.sh -h
```