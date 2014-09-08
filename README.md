# WaffleWaffle

WaffleWaffle is:
- an experiment in [under-engineering](http://www.underengineering.com/2014/05/22/DIY-NoSql/)
- a project to learn some javascript ([d3.js](http://bost.ocks.org/mike/path/) and jquery)
- a bit of flask practice
- a fun way of telling people that their meeting / presentation is boring

WaffleWaffle is a way of voting whether the thing you're watching is boring.  Each browser gets up to
one vote every 10 seconds.  Votes have a half-life such that they essentially disappear after 5 minutes.

I could imagine something like this being more useful with a few more buttons to guage different sorts
of sentiment.  I was thinking that it could be a great way for students to tell their lecturers to 
either speed up or (more likely) slow down.

Perhaps this is also the natural conclusion of micro-blogging?  You cannot get more micro (nano?) than
only being able to post 1 binary bit of data every 10 seconds :)

You can try an example deployment of WaffleWaffle on [Heroku](wafflewaffle.herokuapp.com)

Having met most of my objectives, I am unlikely to do any of the following but if you do something similar
I'd love to play with it...

## Thanks
* [Grahamhar](https://github.com/grahamhar) for the QR Code goodness

## TODO
* Make it look a bit prettier
  * a nicer graph
* Remove some "accuracy" to improve performance
* Stop taking up loads of memory and make mobiles get hot
