library(janitor, include.only = "clean_names")
library(ggplot2)
library(cowplot, include.only = "plot_grid") 
library(coefplot)
library(kableExtra, exclude = "group_rows") 
library(tidyverse) 
library(tidymodels) 
devtools::source_url("https://github.com/jjcurtin/lab_support/blob/main/fun_eda.R?raw=true")
devtools::source_url("https://github.com/jjcurtin/lab_support/blob/main/fun_plots.R?raw=true")
#load data
d <- read_csv("humor_r.csv") 

#calculate the total violation value
d$violation1 <- d$violation1_1 + d$violation1_2 + d$violation1_3 + d$violation1_4 + d$violation1_5
d$violation2 <- d$violation2_1 + d$violation2_2 + d$violation2_3 + d$violation2_4 + d$violation2_5
d$violation3 <- d$violation3_1 + d$violation3_2 + d$violation3_3 + d$violation3_4 + d$violation3_5
d$violation4 <- d$violation4_1 + d$violation4_2 + d$violation4_3 + d$violation4_4 + d$violation4_5
d$violation5 <- d$violation5_1 + d$violation5_2 + d$violation5_3 + d$violation5_4 + d$violation5_5

state <- c(d$state,d$state,d$state,d$state,d$state)
funny <- c(d$funny1,d$funny2,d$funny3,d$funny4,d$funny5)
arousal <- c(d$arousal1,d$arousal2,d$arousal3,d$arousal4,d$arousal5)
violation <- c(d$violation1,d$violation2,d$violation3,d$violation4,d$violation5)
jump <- c(d$jump1,d$jump2,d$jump3,d$jump4,d$jump5)
accept <- c(d$accept1,d$accept2,d$accept3,d$accept4,d$accept5)
d2<- data.frame(state,funny,arousal,violation,jump,accept)


d2 |> plot_grouped_box_violin("state", "funny")
d2 |> plot_grouped_box_violin("arousal", "funny")
m2 <- lm(funny ~ state*arousal*jump,data = d2)
summary(m2)
d2 |> plot_scatter("violation", "funny")
d2 |> plot_grouped_box_violin("accept", "funny")
m4 <- lm(funny ~ violation*accept*jump,data = d2)
summary(m4)
d2 |> plot_grouped_box_violin("jump", "funny")
m5 <- lm(funny ~ jump,data = d2)
summary(m5)
