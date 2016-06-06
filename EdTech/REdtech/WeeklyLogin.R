# additional function
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

#libraries
library(ggplot2)
library(scales)

# Date range
start = '2016-01-20'
end = '2016-06-06'
std <- read.csv("../data/data/student.csv")
std_origin <- std

spaceNames = c('Bases de Datos', 'Statistics and computerized information analysis')
std = subset(std_origin, space_1 %in% spaceNames)
std$space_1 = factor(std$space_1)
std$Date = as.Date(strptime(std$time_1, "%Y-%m-%d %H:%M:%S"))
std = subset(std, Date >= start)
std$weekNum = strftime(std$Date, format = '%W')
std$dateHour = as.POSIXct(strptime(strftime(strptime(std$time_1, "%Y-%m-%d %H:%M:%S"), format='%m-%d:%H'), '%m-%d:%H'), tz='Europe/Oslo')
dfWeek = aggregate(std$distinct_id, list(course = std$space_1, week = std$weekNum), lenUnq)
dfDay = aggregate(std$distinct_id, list(course=std$space_1, day=std$Date), lenUnq)
dfHour = aggregate(std$distinct_id, list(course=std$space_1, hour=std$dateHour), lenUnq)
dfWeek_percen = exportPercentage(dfWeek)
dfDay_percen = exportPercentage(dfDay)
# drawing
# weekly log-in
gWeekly = ggplot(data = dfWeek_percen, aes(x=week, y=percentage, group=course, color=course)) + geom_line() 
gWeekly = gWeekly + xlab('Week') + ylab('% log-in') + ggtitle('Weekly % log-in per course')
gWeekly
# daily log-in
gDaily = ggplot(data=dfDay_percen, aes(x=day, y=percentage, group=course, color=course)) + geom_line()
gDaily = gDaily + xlab('Date') + ylab('% log-in') + ggtitle('Daily % log-in per course')
gDaily = gDaily + scale_x_date(date_labels='%m.%d')
gDaily
# hourly log-in
gHourly = ggplot(data=dfHour, aes(x=hour, y=x, group=course, color=course)) + geom_line()
gHourly = gHourly + scale_x_datetime(breaks = date_breaks("12 hour"), labels = date_format('%m-%d:%H','Europe/Oslo'))
gHourly = gHourly + xlab('Hour') + ylab('Number of log-in') + ggtitle('Hourly log-in per course')
gHourly


