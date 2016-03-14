c=library(ggplot2)

openrate_content_linegraph <- function(file_from, course) {
  data <- read.csv(file_from)
  data$Date = as.Date(strptime(data$Week, '%d.%m.%Y'))
  glist = list()
  group_set = unique(data$Group)
  for ( i in 1:length(group_set)) {
    group_ele = group_set[i]
    g = ggplot(data = subset(data, Group == group_ele), aes(x=Date,y=OpenRate,group=Content,colour=Content)) + geom_line()+ ylim(0,1) + labs(title=paste('Cumulative open rate for',course))   
    file_save = paste('reports/[graph]openrate_content_',course, i, '.png', sep ='')
    ggsave(file=file_save, width = par("din")[2] * 1.5, height = par("din")[2])
  }
}
openrate_content_linegraph('reports/[strategi]openrate_content_rformat.csv','strategi')
openrate_content_linegraph('reports/[kultur]openrate_content_rformat.csv','kultur')
openrate_content_linegraph('reports/[entre]openrate_content_rformat.csv','entre')


multiplot <- function(plots, plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)

  # Make a list from the ... arguments and plotlist
  # plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                    ncol = cols, nrow = ceiling(numPlots/cols))
  }

 if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}
