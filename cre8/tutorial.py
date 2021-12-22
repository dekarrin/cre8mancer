from typing import Callable, Any


def generate_welcome_tutorial(add_step: Callable[[str, str], Any], status_line):
    msg = "This game is an idle clicker where you try to earn money to fund a buncha creative stuff!\n"
    msg += "\nIt's themed around the creative process."
    tut.add_step(output=msg)
    
    msg = "It's also designed to be played from the command line, which explains why it looks so 8ad!\n"
    msg += "Luckily for you, we've put together this little GUI version so you can more easily test it.\n\n"
    tut.add_step(output=msg)
    
    msg = "(ty btw for that, your feedback is v much appreciated glub)\n"
    msg += "\nMmmmmmmm, yeah, I guess this game wouldn't happen without your tireless efforts,"
    msg += "8eta tester. So we should thank you for that."
    tut.add_step(output=msg)
    
    msg = "Anyways! On to the actual game, glub!"
    tut.add_step(output=msg)
    
    content = mock_game.game.status_line
    output = "- Okay, so this thing is the main status line.\n"
    output += "\n"
    output += "- mmm, glub? the what now? which part?"
    
    tut.add_step(content=content, output=output)
    
    content = mock_game.game.status_line + '\n'
    content += "\________________  _______________/\n"
    content += "                 \/\n"
    content += "          THIS THING, 8ITCH"
    output = "- That thing.\n"
    output += "\n- wow rude.\n"
    output += "\n- Hey, 8ut at least you know what I'm talking a8out ::::P"
    tut.add_step(content=content, output=output)
    
    content = mock_game.game.status_line
    output = "- okay, glub, but what does each part mean?!\n"
    output += "\n- Oh my gog, calm down, I was getting to that! Now, check this..."
    tut.add_step(content=content, output=output)
    
    content = mock_game.game.status_line + '\n'
    content += '\/'
    
    output = "- This first num8er here, that's how much money you got.\n"
    output += "\n- it says 0 glub"
    output += "\n- Well, yeah it says 0! You think you get to start off with money? May8e in happy fantasy human land, sure. 8ut this 8nt that, chief. You start with $0."
    output += "\n- okay miss im-so-smart-spider, how do we get more money then?"
    tut.add_step(content=content, output=output)
    
    content = mock_game.game.status_line
    output = "- You gotta click an activity! Jobs usually make the most money, 8ut outlets can get you some change too, sometimes.\n"
    output += "- makes sense, glub. With the click button that's usually there.\n"
    output += "- Yeah, having that show up IN this tutorial would have 8een a little too complic8ed."
    
    tut.add_step(output, content)
    
    content = mock_game.game.status_line + '\n'
    content += "   \___________/"
    
    output = "- okay! i got the next one! so, this here is how much juice you have.\n"
    output += "- Hahahahahahahaha, juice you say? Sounds lewd.\n"
    output += "- omg its not lewd!!! >.< CREATIVE juice!\n"
    output += "- Sure, whatever you say ::::) So what does it do?"
    tut.add_step(output, content)
    
    content = mock_game.game.satus_line
    output = "- oh, it mostly powers Outlets! when you do an outlet, you gotta have enough creative juice to start it! and that juice is used as long as the Outlet is running. but dont worry! you'll get it back when the Outlet is done running. The first number is how much you have free, and the 2nd number is how much total you have!"
    output += "- ..."
    output += "- hey you okay?"
    output += "- Oh, yeah. Sorry, can't expect me to keep my eyes open during that long-ass speech."
    output += "- um. glub 38/ im not really sure how to make this more interesting?"
    tut.add_step(output, content)
    
    output = "- Easy, I got this. Check it."
    tut.add_step(output)
    
    content = mock_game.game.status_line
    content += "                   \_____/"
    
    output = "- So this one is pretty complic8ed, so you should 8e thanking me that *I'm* the one telling you a8out it ::::) Just the kind of friend that I am."
    output += "\n- shes such a good friend that she brags about it instead of actually explaining 383"
    output += "\n- Quiet, you! Anyways, that part is your Seeds and (i)deas... ...pfft"
    output += "\n- what?"
    output += "\n- Heheheheheheheheh. Seed XXXXD"
    
    tut.add_step(output, content)
    
    content = mock_game.game.status_line
    output = "- ...oh my fucking god could you stop making everyfin dirty for 2 seconds"
    output += "- Look, I'm just saying the names. You decided on them, not me ::::) ...8wahahahahaha, seeds."
    output += "- ARE YOU GONNA EXPLAIN IT OR JUST KEEPING MAKING DIRTY JOKES GLUB?!"
    output += "- Okay, okay, Fine, jeez."
    tut.add_step(output, content)
    
    output = "So, Seeds are built up over time 8y progressing. Once you have at least one, you can medit8 to turn them into (i)deas."
    output += "\n- okay imma meditate all the time then! glub!"
    output += "\n- What, no? Dum8ass, that's gonna 8reak everyth8ng!!!!!!!!"
    output += "\n- ... 38("
    output += "\n- What?"
    tut.add_step(output)
    
    output = "- im not a dumbass glub 38'(("
    output += "\n- W8, seriously?"
    output += "\n- yes seriously that was rly mean im turning off the display! GLUB!"
    output +- "\n- You can't just-"
    
    tut.add_step(output)
    
    output = "Oh my gog, she actually did it."
    tut.add_step(output, "")
    
    output = "- Hmmph >38T"
    output += "- Are you really going to 8e like this?"
    output += "- idk are you really going to keep being a '8itch'?"
    output += "- *sigh* Look, I'm SORRY, okay?"
    output += "- you mean it?"
    output += "- Sure, whatever. Now may8e give the screen 8ack?"
    output += "- nuh-uh. not until you SOUND like you mean it"
    output += "- ... Okay. Fine. I'm sorry. I won't do it again."
    output += "- okay."
    output += "- Okay?"
    output += "- okay. here."
    
    tut.add_step(output)
    
    content = mock_game.game.status_line
    output = "- Thank fuck. Okay, sorry a8out interruption, now 8ack to 8usiness."
    output += "\n- yay! now, why wouldn't i want to spend all the time meditating?"
    output += "\n- Right, so that will reset the entire game. Except for (i)deas you already have, of course."
    output += "\n- oooooooooh i get it, so it's like the prestige of this thing!"
    output += "\n- Exactly!"
    tut.add_step(output, content)
    
    output = "- but what do you even DO with (i)deas glub?"
    output += "\n- Good question! Right now they're pretty much only used for buying automations."
    output += "\n- 38?"
    output += "\n- Automations let your activities run without clicking."
    output += "\n- wait you mean i gotta prestige before i can even make the idler be idle?"
    tut.add_step(output)
    
    output = "- Well, yeah. 8ut it shouldn't take too long to get your first seed. ppfpptptatfff"
    output += "\n- 38T well anyways, that makes sense so far."
    output = "\n- Of course it did, after all, it was me who explained it to you ::::)"
    output += "\n- i feel so special"
    output += "\n- You should! Hey, wanna take the last part of the status line? To make up for that crap 8efore."
    tut.add_step(output)
    
    content += "\n                             \____/"
    output = "- sure! it's p easy, the last one is just game time! it's the number of seconds since the game was started."
    output += "- Perfect! See, I told you you were a little 8adass :::;)"
    output += "- glub! 38D"
    
    tut.add_step(output, content)
    
    content = mock_game.game.status_line
    
    output = "- And that's it for the status line!"
    output = "- ooh, what's next?"
    output = "- How a8out the activity card?"
    output = "- Yeah, let's do it!"   