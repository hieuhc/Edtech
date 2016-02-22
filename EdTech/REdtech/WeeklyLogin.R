# additional function
lenUnq = function(x){ length(unique(x))}

#libraries
library(ggplot2)
library(scales)

# Date range
start = '2016-01-20'
end = '2016-02-21'

spaceNames = c('KLS3551 Kulturledelse', 'MRK3480 Forbrukeratferd', 'Organisasjonsatferd og ledelse')
std <- read.csv("../data/data/student.csv")
std = subset(std, space_1 != '')
std$space_1 = factor(std$space_1)
std$Date = as.Date(strptime(std$time_1, "%Y-%m-%d %H:%M:%S"))
std = subset(std, Date >= start)
std$weekNum = strftime(std$Date, format = '%W')
std$dateHour = as.POSIXct(strptime(strftime(strptime(std$time_1, "%Y-%m-%d %H:%M:%S"), format='%m-%d:%H'), '%m-%d:%H'), tz='Europe/Oslo')
dfWeek = aggregate(std$distinct_id, list(course = std$space_1, week = std$weekNum), lenUnq)
dfDay = aggregate(std$distinct_id, list(course=std$space_1, day=std$Date), lenUnq)
dfHour = aggregate(std$distinct_id, list(course=std$space_1, hour=std$dateHour), lenUnq)
# drawing
# weekly log-in
gWeekly = ggplot(data = dfWeek, aes(x=week, y=x, group=course, color=course)) + geom_line() 
gWeekly = gWeekly + xlab('Week') + ylab('Number of log-in') + ggtitle('Weekly log-in per course')
gWeekly
# daily log-in
gDaily = ggplot(data=dfDay, aes(x=day, y=x, group=course, color=course)) + geom_line()
gDaily = gDaily + xlab('Date') + ylab('Number of log-in') + ggtitle('Daily log-in per course')
gDaily = gDaily + scale_x_date(date_labels='%m.%d')
gDaily
# daily log-in
gHourly = ggplot(data=dfHour, aes(x=hour, y=x, group=course, color=course)) + geom_line()
gHourly = gHourly + scale_x_datetime(breaks = date_breaks("12 hour"), labels = date_format('%m-%d:%H','Europe/Oslo'))
gHourly = gHourly + xlab('Hour') + ylab('Number of log-in') + ggtitle('Hourly log-in per course')
gHourly


