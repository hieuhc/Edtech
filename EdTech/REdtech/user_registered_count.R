student = read.csv('student.csv')
student$Date = as.Date(strptime(student$time_1, '%Y-%m-%d %H:%M:%S'))
student$Weeknum = strftime(student$time_1,format='%W')
student$Weekday = weekdays(student$Date)
student$Hour = strftime(student$time_1, format='%H')
student = subset(student, defaultSpaceName %in% c('Strategi STR3605','Kulturledelse KLS3551','Social Entrepreneurship ELE3702'))
student$defaultSpaceName = as.factor(student$defaultSpaceName)
teacher = read.csv('teacher.csv')
teacher$Date = as.Date(strptime(teacher$time_1, '%Y-%m-%d %H:%M:%S'))
start = '2015-11-23'
end = '2015-11-29'
student_w = subset(student, Date >= start & Date <= end)

#################################
unq <- function(x) {
	return (length(unique(x)))
}
course_name = 'Strategi STR3605'
#'Strategi STR3605','Kulturledelse KLS3551','Social Entrepreneurship ELE3702'
student_course = subset(student, defaultSpaceName == course_name)
student_course_w = subset(student_w, defaultSpaceName == course_name)
log_in_rate = unq(student_course_w$distinct_id)/unq(student_course$distinct_id)
log_in_rate
open_rate <- function(dt, dt_w) {
	student_num = unq(dt$distinct_id)
	unq_rate <- function(x) {
		return (length(unique(x)) / student_num)
	}
	# file
	temp = subset(dt_w,  event_1 == 'Viewed content' & contentTypeId == 'file')
	temp$name = factor(temp$name)
	res =  tapply(temp$distinct_id, temp$name, unq_rate)
	write.table(res, 'temp.csv', append = FALSE, quote = TRUE, sep = ',')
	# note
	print('note')
	temp = subset(dt_w,  event_1 == 'Viewed content' & contentTypeId == 'note')
	temp$name = factor(temp$name)
	res = tapply(temp$distinct_id, temp$name, unq_rate)
	write.table(res, 'temp.csv', append = TRUE, quote = TRUE, sep = ',')
	# link
	print('link')
	temp = subset(dt_w,  event_1 == 'Viewed link')
	temp$name = factor(temp$name)
	res = tapply(temp$distinct_id, temp$name, unq_rate)
	write.table(res, 'temp.csv', append = TRUE, quote = TRUE, sep = ',')
}
	

testf <- function (x)(y) {
	return x

####### students who don't view content/link
10/04 - 10/11
Strategi
"55d1d40f9997410800eefbc9" "55d1d4a19997410800eefc9b" "55d1d40f9997410800eefbdf" "55d1d6279997410800eefdcf" "55d1d4a19997410800eefc6b" "55d1d4a19997410800eefc55"
 [7] "55d1d40f9997410800eefbfd" "55d1d7749997410800eefe85" "55d1d40f9997410800eefbe3" "55d1c04dc55fa508003dc65f" "55d1d4a19997410800eefc4e" "55d1d5d39997410800eefdae"
[13] "55d1d3769997410800eefbad" "55d1d6769997410800eefe16" "55d1d40f9997410800eefbf9" "55d1d6769997410800eefe1b" "55d1d63f9997410800eefded" "55d1d40f9997410800eefbd6"
[19] "55d1c04dc55fa508003dc67d" "55d1d6769997410800eefe22" "55d1c04dc55fa508003dc677" "55d1d4a19997410800eefcb3" "55d1d7609997410800eefe6c" "55d1d4a19997410800eefc96"
[25] "55d1d40f9997410800eefbf3"



######## plot number of views by weekday
course_name = 'Social Entrepreneurship ELE3702'
#'Strategi STR3605','Kulturledelse KLS3551','Social Entrepreneurship ELE3702'
student_course = subset(student, defaultSpaceName == course_name)
student_course_view = subset(student_course, event_1=='Viewed announcements')

library(ggplot2)
g = ggplot(data = student, aes(x = Hour, fill = defaultSpaceName)) + geom_bar(position=position_dodge())
g
g + scale_x_discrete(limits=c("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"))

g = ggplot(data = za_less2h, aes(x = sex, y = duration)) + geom_boxplot()
g

with(subset(za_p, sex == 'male' & duration < 7200), sort(tapply(duration, level2, mean)))

####### Folders view
course_name = 'Strategi STR3605'
#'Strategi STR3605','Kulturledelse KLS3551','Social Entrepreneurship ELE3702'
student_course = subset(student, defaultSpaceName == course_name)
student_course_v = subset(student_course, event_1=='Viewed folder')
student_course_v$contentName_2 = factor(student_course_v$contentName_2)
# kultur folder
g = ggplot(data = student_course_v, aes(x = contentName_2)) + geom_bar(position=position_dodge(), fill="#FF9999",colour="black")
g + scale_x_discrete(labels = c("Informasjon om Kulturledelse KLS3551" = "Informasjon om ...", "1. Forelesning - Kunstledelse"="1. 1. Forelesning...",
"INVITASJON - Jarle Bernhoft"="INVITASJON ...","Frilanser"="Frilanser","Veiledningstid"="Veiledningstid"," Kunstneriske grupper"=" Kunstneriske grupper",
"Produksjon"="Produksjon","Nettverk"="Nettverk","Festival"="Festival","Siste forelesning"="Siste forelesning", 
"Kulturpolitikk - Sigrid RÃ¸yseng"="Kulturpolitikk"))
g

# strategi folder
t = ggplot(data = student_course_v, aes(x = contentName_2)) + geom_bar(position=position_dodge(), fill="#FF9999",colour="black")
t + scale_x_discrete(labels = c("AdobeConnect - linker til webinar"="AdobeConnect","Case competition - take a look inside"="Case \n competition",
"Fasit pÃ¥ Multiple Choice eksamen"="Multiple Choice \n eksamen","Eksempeloppgaver H2014"="Eksempeloppgaver \n H2014","Informasjon om kurset"="Informasjon \n om kurset",
"Prosjektoppgaven og innmelding"="Prosjektoppgaven \n og innmelding"))
t




















