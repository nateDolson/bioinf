## Fantasy basketball script for analyzing player statistics
##
##

library(ggplot2)
library(reshape)
library(lubridate)
library(scales)

setwd("~/Documents/Fant\ Stats")
stats <- read.csv("NBAstats.csv")

player_graph <- function(player, dataset){
  print(ggplot(dataset[dataset$player == player,]) + geom_path(aes(x = date, y = fant)) +
    geom_point(aes(x = date, y = fant, color = player)) + facet_wrap(~player))
}

lineup_graph <- function(lineUp, dataset){
  print(ggplot(dataset[dataset$player %in% lineUp,]) + geom_path(aes(x = date, y = fant, color = player)) +
    geom_point(aes(x = date, y = fant, color = player)) + facet_wrap(~player))
}

#code for spliting field goals, threes and 
stats <- data.frame(stats, 
                    colsplit(stats$FG, split = "-", names = c("FG_M", "FG_A")),
                    colsplit(stats$three, split = "-", names = c("three_M", "three_A")),
                    colsplit(stats$FT, split = "-", names = c("FT_M", "FT_A")))

#converstion of data and min to proper format
stats$date <- as.POSIXct(stats$date)

#calcuating fantasy points
#league settings
#Players Stat Category  Value
FGA <-  -1.2 #Field Goals Attempted
FGM <- 3.0 #Field Goals Made
FTA <- -1.88 #Free Throws Attempted 
FTM <- 2.5 #Free Throws Made
M3pt <- 1.2 #3-point Shots Made
PTS <- 1 #Points Scored
OREB <- 2 #Offensive Rebounds
DREB <- 1.5 #Defensive Rebounds
AST <- 2.0 #Assists
ST <- 3.0 #Steals
BLK <- 3.0 #Blocked Shots
TO <- -2.0 #Turnovers
stats$fant <- FGA * stats$FG_A + FGM * stats$FG_M + FTA * stats$FT_A + FTM * stats$FT_M + 
  M3pt * stats$three_M + PTS * stats$Pts + OREB * stats$OR + DREB * (stats$TR - stats$OR) + AST * stats$A + 
  ST * stats$S + BLK * stats$BS + TO * stats$T

#line up 11/18/2012
lineUp <- c("Monta Ellis", "Jose Calderon", "Luol Deng", 
            "LeBron James", "Marcin Gortat", "Larry Sanders", 
            "David Lee", "Tony Parker", "Jarrett Jack", 
            "Nikola Vucevic", "Trevor Ariza", "Byron Mullens")

lineup_graph(lineUp, stats)
player_graph("Jason Thompson", stats)

#free agents
lineUp <- c("Jameer Nelson", "Kyle Korver", "Metta World Peace", 
            "Jason Thompson", "Dante Cunningham", "Jason Maxiell")
lineup_graph(lineUp, stats)
