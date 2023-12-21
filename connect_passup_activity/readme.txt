This directory is to build a connection between the avearge boardings and the pass-ups

To run this parts, we need "bus_stops_in_order" and unzip it first.

The part1 is to use Apriori method to find the support of each "route+stop" in the dataset of "2022_fall_pass-ups.csv".

The part2 is to evaluate the severity of each "route+direction" according to the total support of the "route+direction" and the
number of stops in the "route+direction".

The part3 is to get a boarding ranking of each "route+stop" according to the avearge boardings in the dataset of "passenger_activity_2022_fall.csv"

The part4 is to get the avearage boardings of every stop in each "route+direction".

The part5 is to get the pass-up support of every stop in each "route+direction".

The part6 is to connect the pass-up support to the average boardings for every stop in the Top15 routes that suffer most from pass-ups.

