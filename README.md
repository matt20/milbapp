# milbapp
Working through the process of creating a simple EDA app for Minor League Baseball (MiLB). 

Problem statement: I was unable to find a resource which allowed me to filter MiLB statistics by date windows. There are options which
allow you to track player performance over time, but none which allow you to see the stats for every player during that timeframe. This distinction 
is crucial for the actual act of uncovering prospects as they are in the midst of skill development. For example, say there is a prospect who is doing
everything right except he is striking out too much. This app will allow you to split the statistics by dates, allowing you to see if he has made any 
improvements in the strikeout department. Player development is not linear, and often times a player's skills will see development over the course of the 
season. Missing those developments will lead to you having an outdated opinion on a player's future value. My goal was to be able to identify players 
as the skill development is happening. 

Original solution: I was utilizing an Excel template I had created which allowed me to copy & paste saved exported CSVs from FanGraphs.com to back out the 
statistics over a given time frame. This Excel file became cumbersome and slow, and required too much manual intervention. 

New solution: I decided to learn enough SQL and Python to essentially build the same solution without requiring nearly as much manual intervention.

There are a few scripts working in the background to keep this app up to date. 
  -The first script scrapes FanGraphs and automatically downloads the new data. 
  -The second script cleans and transforms the data before pushing it to a local database. 
  -The third script queries the local database and writes the results to a CSV which is then pushed to my github repository. 

The app updates each day to reflect the new data available from FanGraphs. 

Disclaimer: this is an imperfect method for creating this app. The alternative, and much more robust solution, would be to utilize the PyBaseball package in
Python, or the baseballR package in R, to download every single pitch thrown in MiLB and calculate all of the stats myself. Given the additional learning curve 
and issues that would certainly pop up while undertaking a project of that size, I decided to take some shortcuts to reach essentially the same endpoint. It is 
my goal to eventually build up my skills to the point where working with 100,000+ new rows of 155 variables each week (!) is more approachable and then to 
start building out the necessary database and Python scripts.
