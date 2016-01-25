course = strategy
course_createfile = subset(course, event_1 == 'Created a file')
subset(course_createfile, select = c(name, Date))
course_deletefile = subset(course, event_1 == 'Deleted content' & contentTypeId == 'file')
subset(course_deletefile, select  = c(name, Date))

### plot views for Date
name_file = 'Groups and dates for the first presentation.docx'
file = subset(data, name == name_file)
file$Date = factor(file$Date)
b = table(file$Date)
plot(b, type = 'l', main = name_file)

### users anaylysis
user = unique(course$distinct_id)
user_view_set = subset(course, event_1 == 'Viewed content' | event_1 == 'Viewed link')
sort(table(user_view_set$distinct_id))
user_view_set$distinct_id = factor(user_view_set$distinct_id)
a = table(user_view_set$distinct_id)
boxplot(as.vector(a)))
b = table(factor(user_view_set$Date))
plot(b, type = 'l')


usr_id = '55d1d4a19997410800eefc73'
user = subset(user_view_set, distinct_id == usr_id)
plot(table(user$Date), type = 'l', main = paste(usr_id,'views by date', sep = ' '))
sort(table(factor(user$name)))
subset(user, select = c(city, os, usingStandaloneApp, screen_height, initial_referring_domain, region, device, browser))

55d1d4a19997410800eefc80 55cb1daa21dade120022d7ea 55d1d40f9997410800eefbe5 55d1d5bd9997410800eefd92 55d1c04dc55fa508003dc674 55d1d5399997410800eefd31
55d1d4a19997410800eefc5b 55d1d4a19997410800eefca3

55d1d7809997410800eefe9d 55d1d7809997410800eefe9f 55d5d189c8154d08000f72bc 55e41d9fe8728a08001e9431 55e6d17db0e8dd0800a761e9 55d1c04dc55fa508003dc677

55d1c04dc55fa508003dc664 55d1c04dc55fa508003dc66c 55d1d40f9997410800eefbfd 55d1d4a19997410800eefc9f 55d1d5d39997410800eefdae 55d1d6279997410800eefdcf (16)
55d1c04dc55fa508003dc696 55d1d4a19997410800eefc71 55d1d5399997410800eefd2d 55d1d5bd9997410800eefd93 55d1d6769997410800eefe1d 55d1d7809997410800eefe95(21)

55d1d4a19997410800eefc4c 55d1d4a19997410800eefc56 55d1d4a19997410800eefc73 55d1d7b49997410800eefecc 55d1d4a19997410800eefc72 55d1d5399997410800eefd2f(25)
55d1d4a19997410800eefca0 55d1d40f9997410800eefbf8 55d1d65f9997410800eefe03 55d1d40f9997410800eefbd0 55d1d5809997410800eefd6d 55d1d7609997410800eefe6d (27,30)



### why users logged in but not viewed content in lastweek
course_weekly = strategy_7_13
user_view_set = subset(course_weekly, event_1 == 'Viewed content' | event_1 == 'Viewed link')
user_view = unique(user_view_set$distinct_id)
user_not_view = setdiff(unique(course_weekly$distinct_id), user_view)
subset(course_weekly,distinct_id == 'user_not_view', select = c(event_1, time_1, city, os, usingStandaloneApp, screen_height, initial_referring_domain, region, device, browser))


lec = 'Sosialent-groups-read this.docx'
lec = 'Forelesning 4- verdikonfigurasjoner 2015 BGO.pptx'
user_view_lec = subset(user_view_set, name == lec)
user_not_view_lec = setdiff(unique(user_view_set$distinct_id), unique(user_view_lec$distinct_id))

## num of users viewed fol but not lec
fol = 'Information - the activety plan is updated (29.08)' 
fol = 'Forelesningsslides'
user_view_fol = subset(course_weekly, event_1 == 'Viewed folder' & name == fol)
user_fol_not_lec = setdiff(unique(user_view_fol$distinct_id), unique(user_view_lec$distinct_id))
select = c(event_1, time_1, name,city, os, usingStandaloneApp, screen_height, initial_referring_domain, region, device, browser)

set_fol_not_lec = subset(course_weekly, distinct_id %in% user_fol_not_lec)
viewfolder = subset(set_fol_not_lec, event_1 == 'Viewed folder')
a = table(factor(viewfolder$name))
barplot(a, names.arg = c('Artikler og annet','Case competition','Facebookgruppe','Forelesningsslides','Informasjonkurset','Padlets','Prosjektoppgaven','Videolinker'))
viewfolder_fol = subset(viewfolder, name == fol)

viewfile = subset(set_fol_not_lec, event_1 == 'Viewed content')
viewfile$name = factor(viewfile$name)
sort(table(viewfile$name))
temp = subset(viewfile, name  == 'Sosialent-groups-with contact info.docx')

temp = subset(viewfile, name %in% c('Forelesning 2-BGO.pptx','Forelesning 5 - konsern BGO.pptx','Forelesning 1.pptx',
     'Introduksjon STR3605 H2015 BGO.pptx','Forelesning 3 - kap5.pptx','Lecture 5 English Final (1) student version.pptx',
     'Lecture 4 Value Configuration English 2015 Final.pp', lec)

*****
strategi :
448 views of Forelesningsslides folder, 79 of them actually viewed files in folder (66%). 33% backed to space view
entre :
156 views Information - the activety plan is updated (29.08) folder, 34 viewed files in folder (21%)
*****
*****
strategi:
 Forelesning 2-BGO.pptx                      Forelesning 5 - konsern BGO.pptx                                  STR3605 Artikler.pdf 
                                                    3                                                     3                                                     3 
                                   Forelesning 1.pptx                   Introduksjon STR3605 H2015 BGO.pptx                             Forelesning 3 - kap5.pptx 
                                                    6                                                     7                                                     8 
     Lecture 5 English Final (1) student version.pptx                 Oversiktsplan for STR3605 Bergen.docx                     Skriv om konfidensialitet H15.doc 
                                                    9                                                    16                                                    16 
Lecture 4 Value Configuration English 2015 Final.pptx                      Anbefalingsskriv H15 STR3605.doc                              Prosjektoppgaven H15.pdf 
                                                   18                                                    21                                                    26 

127 users who have accessed 'Forelesningsslides'.
53 users opened folder but not viewed file. 50 of 53 have viewed contents ( 3 only viewed folder/space)
41 of 50 viewed wrong file (should view weekly lecture)
entre:
34/39 users have accessed 'Information - the activety plan is updated (29.08)', not viewed file. 26 of 39 viewed content. 
21 of 26 viewed wrong file
*****
unq = function(x) { return (length(unique(x)))}
std_strategi = subset(student, space_1 == 'Strategi STR3605')
std_kultur = subset(student, space_1 == 'Kulturledelse KLS3551')
std_entre = subset(student, space_1 == 'Entrepreneurship ELE3702')

std_16 = subset(student, Date > '2015-09-16')
temp = subset(std_21,event_1=='Viewed folder' & name =='Informasjon om Kulturledelse KLS3551')
unq(temp$distinct_id)













