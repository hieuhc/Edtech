# additional function
Sys.setlocale("LC_TIME", "en_US.UTF-8")
lenUnq = function(x){ length(unique(x))}

exportPercentage = function(df) {
  for (i in 1: nrow(df)){
    if (df$course[i] == 'KLS3551 Kulturledelse'){
      df$percentage[i] = df$x[i] / 42
    }
    else if(df$course[i] == 'MRK3480 Forbrukeratferd'){
      df$percentage[i] = df$x[i] / 325
    }
    else if (df$course[i] == 'ORG3402 Organisasjonsatferd og ledelse'){
      df$percentage[i] = df$x[i] / 578
    }
    else if(df$course[i] == 'ENT4100 Idea evaluation'){
      df$percentage[i] = df$x[i] / 24
    }
    else if (df$course[i] == 'STV4028 Process Tracing ...'){
      df$percentage[i] = df$x[i] / 11
    }
    else if(df$course[i] == 'Bases de Datos'){
      df$percentage[i] = df$x[i] / 16
    }
    else if (df$course[i] == 'Statistics and computerized information analysis'){
      df$percentage[i] = df$x[i] / 19
    }
  }
  df
}

exportAverage = function(df, std) {
  numWeek = lenUnq(std$weekNum)
  for (i in 1: nrow(df)){
    df$average[i] = df$x[i] / numWeek
  }
  df
}
#libraries
library(ggplot2)
library(scales)

# Date range
start = '2016-01-20'
end = '2016-06-06'
std <- read.csv("../data/data/student.csv")
std_origin <- std

spaceNames = c('ENT4100 Idea evaluation', 'STV4028 Process Tracing ...')
std = subset(std_origin, space_1 %in% spaceNames)
std$space_1 = factor(std$space_1)
std$Date = as.Date(strptime(std$time_1, "%Y-%m-%d %H:%M:%S"))
std$weekDay = weekdays(std$Date)
std$weekNum = strftime(std$Date, format = '%W')
std = subset(std, Date >= start)
dfWeek = aggregate(std$distinct_id, list(course = std$space_1, week = std$weekDay), length)
# dfWeek_average = exportAverage(dfWeek, std)

# drawing
# weekday log-in
gWeekly = ggplot(data = dfWeek, aes(x=week, y=x, group=course, color=course)) + geom_line() 
gWeekly = gWeekly + xlab('Week') + ylab('Averaged count log-in') + ggtitle('Weekday averaged log-in per course')
gWeekly = gWeekly + scale_x_discrete(limits=c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"))
gWeekly



