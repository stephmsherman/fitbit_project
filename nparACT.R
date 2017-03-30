library(nparACT)

###add path to where data live
path = ""
f=read.csv(paste(path,"all_daily_data_processed_worn.csv",sep=""))
f$key=as.factor(as.character(f$key))
f=f[f$walk_dates!="no_fitbit",]
f$walk_dates=droplevels(f$walk_dates)

individual=split(f, f[,c("walk_dates","key")], drop=F)
summary(individual[[1]]$key)
summary(individual[[1]]$walk_dates)
table(individual[[1]]$date)


for(i in seq_along(names(individual))){
	assign(paste(names(individual)[[i]]),individual[[i]][,c("stepdate","activities_steps")])
}


all=data.frame(part=names(individual), num=seq_along(names(individual)))
df=split(all[,"part"],all$num)

l=lapply(df, function(x) {try(cbind(nparACT_base(toString(x), SR = 1/60, plot=F),name=x))})
l[[20]]=NULL
npcr=do.call("rbind",l)
npcr$name=as.character(npcr$name)
npcr$walk_dates=substring(npcr$name,1,nchar(npcr$name)-4)
npcr$walk_dates=as.factor(npcr$walk_dates)
npcr$key=substring(npcr$name,nchar(npcr$name)-2,nchar(npcr$name))
npcr$key=as.factor(npcr$key)

npcr$name=NULL
write.csv(npcr, paste(path,"npcr_measures.csv",sep=""),row.names=F)

