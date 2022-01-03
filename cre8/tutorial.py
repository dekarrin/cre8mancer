from typing import Callable, Any, Optional

from .activities import OwnedActivities, Jobs
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
    
    sb.section = "1.1.) -- Money"
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
    
    sb.section = "1.2.) -- Creative Juice"
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
    
    sb.section = "1.3.) -- Seeds & (i)deas"
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
    
    sb.section = "1.4.) -- Game Time"
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
    # | $0 (0.00J)                      $1/C 0.0000J/C |        x{:d} |
    # | |                                 | 999h60m55s |      RUNNING |
    # +------------------------------------------------+--------------+
    act_card = layout.bar() + '\n' + layout.make_act_card(example_job, 0.0) + '\n' + layout.bar()
    sb.default_content = act_card
    sb.content = act_card
    sb.section = "2.) Activities"
    sb.outln("- this is an activity, glub. you see these on the main screen!")
    add()
    
    sb.outln("- Easy, this is a clicker, right? So those have gotta 8e the things you click on.")
    sb.outln("- yeah, you're exactly right!")
    sb.outln("- Am I ever wrong? ::::)")
    sb.outln("- p frequently but not this time! glub 38D")
    add()
    
    sb.outln("- okay, now every activity is either a 'job' or an 'outlet'. this one is a job, but outlets and jobs all look p much the same as this one!")
    sb.outln("- W8. If they all look the same, then it's really dum8 to have different kinds of activities.")
    sb.outln("- theres a difference tho! jobs will almost always get you more money, but outlets are better for getting more juice. oh and also outlets usually require a lotta juice to go.")
    sb.outln("- But some jo8s cost juice too! It's waaaaaaaay ar8itrary.")
    sb.outln("- ofc its arbitrary its a game 383")
    sb.outln("- Fair, I guess. For now. Still seems really, really dum8 to me 8ut I can roll with it.")
    add()

    draw = format.Draw(act_card, mutate=False)
    draw.corner_char = draw.horz_char = draw.vert_char = '*'

    sb.section = '2.1.) -- Name'
    sb.content = draw.rect((0, 0), (13, 2))
    sb.outln("- this is the name of the activity!")
    add()

    sb.outln("This one is called 'Eat Bagels', it's a v important job!")
    add()
    
    sb.outln("The names don't really mean much, but they are a fun way to categorize the different levels of tasks!")
    add()
    
    sb.section = '2.2.) -- Instances'
    sb.outln("So, next thing up! You can have more than one copy of an activity running.")
    add()
    
    sb.outln("These are called 'instances'")
    add()    
    
    sb.content = draw.rect((37, 0), (50, 2))
    sb.outln("This part here gives information on your copies of the activity!")
    sb.outln("The first number in parenthesis is how much buying another copy will cost.")
    sb.outln("$20 here!")
    sb.outln("And the '1x' after that shows how many copies of this activity there are!")
    sb.outln("But it's only the ones that are 'active'. You can set some of them to inactive if you want to lower the costs to run the activity, but it also lowers the reward!")
    add()
    
    sb.outln("If you do set some instances inactive, the number of inactive copies that you have will be shown after the colon, where it says ':0' is the example.")
    add()

    sb.section = "2.3.) -- Costs"
    sb.content = draw.rect((0, 1), (13, 3))
    sb.outln("- this part is how much it costs to start this activity, to 'click' it!")
    sb.outln("the first number is how many dollars it costs to start, and the second one is how much juice it will take up while running.")
    add()

    sb.outln("Remember, you'll get the juice back once its done running! The dollars you will not get back.")  # note about jobs always giving more than they cost
    sb.outln("The costs are updated for the number of instances of that active that you have active, more on that in a bit.")
    add()
    
    sb.section = '2.4.) -- Production'
    sb.content = draw.rect((33, 1), (50, 3))
    sb.outln("- This section here is the production numbers for the activity! It tells you how much juice and money you'll get once the activity finishes")
    sb.outln("- this one will give you $1 and no juice. That's really sad! How can you get more juice?")
    add()
    
    sb.outln("- Remember how there are both jobs and outlets? Jobs are best for giving money back and usually won't get you a whole lotta juice, but they dont cost very much to start.")
    add()
    
    sb.content = "SHOW OUTLET CARD HERE"
    sb.outln("Outlets are the opposite! You need a lot of money to get them going, and they don't usually give you much back, but they give you permanent increases to juice.")
    add()
    
    sb.outln("Okay! Back to the job we were looking at before.")
    add()

    sb.section = "2.5.) -- Duration"
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
    
    sb.content = draw.overtype_lines((0, 1), running_card.split('\n'))
    sb.outln("Once it finishes, it'll go back to being an X")
    add()
    
    sb.outln("There it is!")
    add()
    
    sb.outln("And of course, the number to the right is the countdown to completion!")
    add()
    
    sb.section = '2.6.) -- Automations'
    sb.outln("The last item on the activity card is the Automations section! Glub!")
    add()
    
    sb.content = draw.rect((50, 0), (64, 4))
    sb.outln("That's this side on the right")
    add()
    
    sb.outln("You won't have any at first, but, glub! you will eventually. glub.")
    
    auto_job = example_job.copy()
    auto_job.automations += 1
    auto_job.automated = True
    auto_card = layout.make_act_card(auto_job, 0.0)
    sb.content = draw.overtype_lines((0, 1), auto_card.split('\n'))
    sb.default_content = sb.content
    sb.outln("Here's how it looks when you DO get automations!")
    add()
    
    sb.outln("The multiplier tells how much the automations are multiplying your production!")
    sb.outln("The first automation tier you buy doesn't give you any multiplier, but every one after that does.")
    add()
    
    sb.default_content = None
    sb.content = ''
    sb.section = "3.) Store"
    sb.outln("Next we gotta talk about the store! It's where you buy more copies and glub! Also more automations!")
    add()
    
    example_jobdef = Jobs[0]
    sb.content = layout.bar() + '\n'
    sb.content += layout.make_act_store_listing(example_jobdef, 1, 0) + '\n'
    sb.content += layout.bar()
    sb.default_content = sb.content
    draw = format.Draw(text=sb.content, mutate=False)
    draw.corner_char = draw.vert_char = draw.horz_char = '*'
    sb.outln("So this is what an item in the store looks like! glub!")
    add()
    
    sb.section = '3.1.) -- Price'
    sb.content = draw.rect((0, 0), (17, 2))
    sb.outln("This is the item and how much it costs.")
    add()
    
    sb.outln("The price will go up slowly with each one that you buy!")
    add()
        
    # +---------------------------------------------------------------+
    # | $20 Eat Bagels                 - $0/C (0.00J)   | AUTO x1     |
    # | 1s                             + $1/C (0.0000J) | 1i          |
    # +---------------------------------------------------------------+
    
    sb.section = "3.2.) -- Duration"
    sb.content = draw.rect((0, 1), (5, 3))
    sb.outln("Right there is a reminder of how long that task takes.")
    add()
    
    sb.outln("It doesn't really mean anyfin in the store, its just a reminder 38)")
    add()
    
    sb.section = "3.3.) -- Cost & Production"
    sb.content = draw.rect((31, 0), (50, 3))
    sb.outln("Glub! This section is tells you what will happen after you buy another copy of this activity.")
    add()
    
    sb.outln("There's two different lines there, one to show cost, and one to show production.")
    add()
    
    sb.content = draw.rect((31, 0), (50, 2))
    sb.outln("The line starting with a '-' is what it costs to run the instance of the activity after you've bought it.")
    add()
    
    sb.outln("This is the eat bagels task, which doesnt ever cost anything to run. So let's take a look at something that DOES cost something!")
    add()
    
    example_cost_act = Jobs[1]
    next_task_card = layout.make_act_store_listing(example_cost_act, 1, 0) + '\n'
    sb.content = draw.overtype_lines((0, 1), next_task_card.split('\n'))
    mcost = format.money(example_cost_act.money_cost(1))[1:]  # no dollar sign
    s = "s" if example_cost_act.money_cost(1) != 1 else ""
    jcost = "{:.4f}".format(example_cost_act.juice_cost(1))
    
    sb.outln("These numbers are much more interesting glub!")
    sb.outln()
    sb.outln("If you bought a copy of the {:s} activity, starting a run of it would take {:s} dollar{:s} and {:s} juice, plus whatever it costs to run any copies you already have.".format(example_cost_act.name, mcost, s, jcost))
    add()
    
    sb.outln("Back to our friend, {:s}!".format(example_jobdef.name))
    add()
    
    sb.content = draw.rect((31, 1), (50, 3))
    sb.outln("The line starting with a '+' is how much stuff you'll get from running the activity once you've bought another copy.")
    add()
    
    mprod = format.money(example_jobdef.money_rate(1))[1:]  # no dollar sign
    s = "s" if example_jobdef.money_rate(1) != 1 else ""
    sb.outln("{:s} is a p low-tier activity, so it only gives you {:s} dollar{:s}. And it doesn't give you any juice at all!".format(example_jobdef.name, mprod, s))
    sb.outln()
    sb.outln("But if it did, that's where it would be!")
    add()
    
    sb.outln("Just like with cost, the production gets added to all other active instances once you start a run.")
    add()
    
    sb.section = "3.4.) -- Automation Price"
    sb.outln("Next up, the automation section!")
    add()
    
    sb.content = draw.rect((50, 0), (64, 3))
    sb.outln("This part gives how much it costs to buy the next tier of automation, and how much it will multiply your production.")
    add()
    
    sb.outln("Automations are really good, so they aren't cheap glub! The price for automations will always be in (i)deas, which you can only get by meditating.")
    add()
    
    sb.content = ''
    sb.default_content = ''
    sb.section = "4.) Good Luck"
    sb.outln("- Welp, looks like that's it.")
    sb.outln("- yeah that's all we got for you here! you should give playing a shot!")
    sb.outln("- Right, and if you can't figure something out, don't worry! We got your 8ack ::::)")
    sb.outln("- yush! you can send jello a DM on our main discord at dekarrin#0314, or you can open an issue on the GitHub page!")
    add()
    
    sb.outln("- i hope ur clicking goes well!")
    sb.outln("- Awwwwwwww yeah. Good luck out there.")
    add()
    
    sb.outln("(close this window to end the tutorial)")
    add()
