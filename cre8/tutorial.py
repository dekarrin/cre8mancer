from typing import Callable, Any, Optional

from .activities import OwnedActivities
from . import layout
from . import format


class StepBuilder:
    def __init__(self, default_output: Optional[str] = None, default_content: Optional[str] = None):
        self.default_output = default_output
        self.default_content = default_content
        self.output = default_output
        self.content = default_content
        self.section = None
        
    def outln(self, line=''):
        if self.output is None:
            self.output = line.strip('\n')
        else:
            self.output += '\n' + line
            
    def mainln(self, line=''):
        if self.content is None:
            self.content = line.strip('\n')
        else:
            self.content += '\n' + line
            
    def reset(self):
        self.section = None
        self.output = self.default_output
        self.content = self.default_content
        

def generate(add_step: Callable[[str, str, str], Any], status_line, example_job: OwnedActivities):
    sb = StepBuilder()
    def add():
        add_step(sb.output, sb.content, sb.section)
        sb.reset()
    
    sb.outln("This game is an idle clicker where you try to earn money to fund a buncha creative stuff!")
    sb.outln("It's themed around the creative process.")
    add()
    
    sb.outln("It's also designed to be played from the command line, which explains why it looks so 8ad!")
    sb.outln("Luckily for you, we've put together this little GUI version so you can more easily test it.")
    add()
    
    sb.outln("- (ty btw for that, your feedback is v much appreciated glub)")
    sb.outln("- Mmmmmmmm, yeah, I guess this game wouldn't happen without your tireless efforts, 8eta tester. So we should")
    sb.outln("thank you for that.")
    add()
    
    sb.outln("Anyways! On to the actual game, glub!")
    add()
    
    sb.mainln(status_line)
    sb.default_content = status_line
    sb.section = "1.) Status Line"
    sb.outln("- Okay, so this thing is the main status line.")
    sb.outln("- mmm, glub? the what now? which part?")
    add()
    
    sb.mainln("\________________  _______________/")
    sb.mainln("                 \/")
    sb.mainln("          THIS THING, 8ITCH")
    sb.outln("- That thing.")
    sb.outln("- wow rude.")
    sb.outln("- Hey, 8ut at least you know what I'm talking a8out ::::P")
    add()
    
    sb.outln("- okay, glub, but what does each part mean?!")
    sb.outln("- Oh my gog, calm down, I was getting to that! Now, check this...")
    add()
    
    sb.section = "1.1.) Money"
    sb.mainln('\/')
    sb.outln("- This first num8er here, that's how much money you got.")
    sb.outln("- it says 0 glub")
    sb.outln("- Well, yeah it says 0! You think you get to start off with money? May8e in happy fantasy human land, sure. 8ut this 8nt that, chief. You start with $0.")
    sb.outln("- okay miss im-so-smart-spider, how do we get more money then???")
    add()
    
    sb.outln("- You gotta click an activity! Jobs usually make the most money, 8ut outlets can get you some change too, sometimes.")
    sb.outln("- makes sense, glub. With the click button that's usually there.")
    sb.outln("- Yeah, having that show up IN this tutorial would have 8een a little too complic8ed.")
    add()
    
    sb.section = "1.2.) Creative Juice"
    sb.mainln("   \___________/")
    sb.outln("- okay! i got the next one! so, this here is how much juice you have.")
    sb.outln("- Hahahahahahahaha, juice, huh? Sounds lewd.")
    sb.outln("- omg its not lewd!!! >.< CREATIVE juice!")
    sb.outln("- Sure, whatever you say ::::) So what does it do?")
    add()
    
    sb.outln("- oh, it mostly powers Outlets! when you do an outlet, you gotta have enough creative juice to start it! and that juice is used as long as the Outlet is running. but dont worry! you'll get it back when the Outlet is done running. The first number is how much you have free, and the 2nd number is how much total you have!")
    sb.outln("- ...")
    sb.outln("- hey you okay?")
    sb.outln("- Oh, yeah. Sorry, can't expect me to keep my eyes open during that 8oring, 8oring, 8ORING speech.")
    sb.outln("- um. glub 38/ im not really sure how to make this more interesting?")
    add()
    
    sb.outln("- Easy, I got this. Check it.")
    add()
    
    sb.section = "1.3.) Seeds & (i)deas"
    sb.mainln("                   \_____/")
    sb.outln("- So this one is pretty complic8ed, 8ut don't worry, you got *me* telling you a8out it ::::) Just the kind of friend that I am.")
    sb.outln("- shes SUCH a good friend that she brags about it instead of actually explaining 383")
    sb.outln("- Quiet, you! Anyways, this part is your Seeds and (i)deas... ...pfft")
    sb.outln("- what?")
    sb.outln("- Heheheheheheheheh. Seed XXXXD")
    add()
    
    sb.outln("- ...oh my fucking god could you stop making everyfin dirty for 2 seconds")
    sb.outln("- Look, I'm just saying the names. You decided on them, not me ::::) ...8wahahahahaha, seeds.")
    sb.outln("- ARE YOU GONNA EXPLAIN IT OR JUST KEEPING MAKING DIRTY JOKES GLUB?!")
    sb.outln("- Okay, okay, Fine, jeez.")
    add()
    
    sb.outln("So, Seeds are built up over time 8y progressing. Once you have at least one, you can medit8 to turn them into (i)deas.")
    sb.outln("- okay imma meditate all the time then! glub!")
    sb.outln("- What, no? That's gonna 8reak everyth8ng, you dum8ass glu8!!!!!!!!")
    sb.outln("- ... 38(")
    sb.outln("- What?")
    add()
    
    sb.outln("- im not a dumbass glub, glub 38'((")
    sb.outln("- W8, seriously?")
    sb.outln("- yes seriously that was rly mean im not doing this anymore. im turning off the display! GLUB!")
    sb.outln("- Deka, you can't just-")
    add()
    
    sb.default_content = ''
    sb.content = ''
    sb.outln("Oh my gog, she actually did it.")
    add()
    
    sb.outln("- Hmmph >38T")
    sb.outln("- Are you really going to 8e like this?")
    sb.outln("- idk are you really going to keep being a '8itch'?")
    sb.outln("- *sigh* Look, I'm SORRY, okay?")
    sb.outln("- you mean it?")
    sb.outln("- Sure, whatever. Now may8e give the screen 8ack?")
    sb.outln("- nuh-uh. not until you SOUND like you mean it")
    sb.outln("- ... Okay. Fine. Deka, I'm sorry. I respect you and your glu88ing, and I was rude. I won't do it again.")
    sb.outln("- okay.")
    sb.outln("- Okay?")
    sb.outln("- yes. thank you. here.")
    add()
    
    sb.default_content = status_line
    sb.content = status_line
    sb.outln("- Thank fuck. Okay, sorry a8out interruption, now 8ack to 8usiness.")
    sb.outln("- yay! now, why wouldn't i want to spend all the time meditating?")
    sb.outln("- Right, so that will reset the entire game. Except for (i)deas you already have, of course.")
    sb.outln("- oooooooooh i get it, so it's like the prestige of this thing!")
    sb.outln("- Exactly!")
    add()
    
    sb.outln("- but what do you even DO with (i)deas glub?")
    sb.outln("- Good question! Right now they're pretty much only used for buying automations.")
    sb.outln("- 38?")
    sb.outln("- Automations let your activities run without clicking.")
    sb.outln("- wait you mean i gotta prestige before i can even make the idler be idle?")
    add()
    
    sb.outln("- Well, yeah. 8ut it shouldn't take too long to get your first seed. ppfpptptatfff")
    sb.outln("- 38T well anyways, that makes sense so far.")
    sb.outln("- Of course it did, after all, it was me who explained it to you ::::)")
    sb.outln("- i feel so special")
    sb.outln("- You should! Hey, wanna take the last part of the status line? To make up for that crap 8efore.")
    add()
    
    sb.section = "1.4.) Game Time"
    sb.mainln("                             \____/")
    sb.outln("- sure! it's p easy, the last one is just game time! it's the number of seconds since the game was started.")
    sb.outln("- Perfect! See, I told you you were a little 8adass :::;)")
    sb.outln("- glub! i dont remember you saying that but ill take the compliment 38D")
    add()
    
    sb.outln("- And that's it for the status line!")
    sb.outln("- ooh, what's next?")
    sb.outln("- How a8out the activity card?")
    sb.outln("- Yeah, let's do it!")
    add()
    
    # +------------------------------------------------+--------------+
    # | Eat Bagels                          ($20) x1:0 |    (No auto) |
    # | $0 (0.00J)                    $100/C, 0.03CJ/C |        x{:d} |
    # | |                                 | 999h60m55s |      RUNNING |
    # +------------------------------------------------+--------------+
    act_card = layout.bar() + '\n' + layout.make_act_card(example_job, 0.0) + '\n' + layout.bar()
    sb.default_content = act_card
    sb.content = act_card
    sb.section = "2.) Activities"
    sb.outln("- this is the activity card, glub. you see these on the main screen")
    add()
    
    sb.outln("Every activity is either a 'job' or an 'outlet'. This one happens to be a Job, but they all look pretty much the same as this!")
    add()

    draw = format.Draw(act_card, mutate=False)
    draw.corner_char = draw.horz_char = draw.vert_char = '*'

    sb.section = '2.1.) Name and Cost'
    sb.content = draw.rect((0, 0), (13, 2))
    sb.outln("- this is the name of the activity!")
    add()

    sb.outln("This one is called 'Eat Bagels', it's a v important job!")
    add()

    sb.content = draw.rect((0, 1), (13, 3))
    sb.outln("- this part is how much it costs to start this activity, to 'click' it!")
    sb.outln("the first number is how many dollars it costs to start, and the second one is how much juice it will take up while running.")
    add()

    sb.outln("Remember, you'll get the juice back once its done running! The dollars you will not get back.")  # note about jobs always giving more than they cost
    sb.outln("The costs are updated for the number of instances of that active that you have active, more on that in a bit.")
    add()

    sb.section = "2.2.) Duration"
    sb.content = draw.rect((0, 2), (36, 4))
    sb.outln("Ooh, this is the exciting part, the progress bar! This tells how long you have to wait for the activity to finish!")
    add()

    sb.outln("If it's not running at all, it'll be an X, like you see here! But once you give somefin a click...")
    add()

    # quick make fake act
    running_job = example_job.copy()
    running_job.execute(0.0)
    running_card = layout.make_act_card(running_job, 0.3)
    sb.content = draw.overtype_lines((0, 1), running_card.split('\n'))
    sb.outln("Then the progress bar shows up!")
    add()

    sb.outln("Once it finishes, it'll go back to being an X")
    add()


    #put this one down for circling the next item cost
    #sb.content = draw.rect((36, 0), (44, 2))
    sb.outln("- ooh, this number is important for buying more instances!")
    