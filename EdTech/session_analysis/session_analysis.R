st_ss = read.csv('student_session.csv')
std_ss_dur = read.csv('student_ss_dur.csv')
# Kulturledelse KLS3551 Strategi STR3605 (Social)Entrepreneurship ELE3702
std_ss_dur_cou = subset(std_ss_dur, defaultSpaceName=='Social Entrepreneurship ELE3702')
summary(std_ss_dur_cou$duration)

st_dur_ = subset(st_ss, duration != -1)
st_dur = subset(st_dur_, space_1=='Entrepreneurship ELE3702')
tapply(st_dur$duration, st_dur$event_1, mean)
temp = subset(st_dur, event_1== 'Viewed content')
tapply(temp$duration, temp$contentTypeId,mean)
temp = subset(st_dur, event_1== 'Viewed content' & contentTypeId=='file')
summary(temp$duration)

std_ss_dur = read.csv('student_ss_dur.csv')
library(ggplot2)
g = ggplot(std_ss_dur, aes(defaultSpaceName, duration)) + geom_boxplot() 
g + labs(title = 'Boxplot for session length varied by courses', x = 'Courses',y='Session length (s)')
g = ggplot(std_ss_dur, aes(x = 1, duration)) + geom_boxplot()
g + labs(title = 'Boxplot for session length',y='Session length (s)')

---- os analysis
# calculate % of session with a specific duration in the respect to os
std_ss_dur = read.csv('session/student_ss_dur.csv')
dur = 60*5
os_sel = 'Android'
temp = subset(std_ss_dur, os==os_sel)
nrow(temp)
temp1 = subset(temp, duration > dur)
nrow(temp1)/nrow(temp)

# similar to above, duration for each event
std_ss = read.csv('session/student_session.csv')
st_ss = subset(std_ss, duration !=-1)
dur = 60*5
os_sel = 'Windows'
temp1 = subset(st_ss, os ==os_sel)
temp2 = subset(temp1, event_1 == 'Viewed content' & duration > dur)
unq(temp2$session) / unq(temp1$session)


-- student_ss_dur_feats_2.csv analysis
ss = read.csv('session_analysis/student_ss_dur_feats_2.csv')
# add duration from std_ss_dur to this file
library(ggplot2)
g = ggplot(ss, aes(tch_idx, duration_l)) + geom_point(shape = 1) + geom_smooth(method = lm)
g

