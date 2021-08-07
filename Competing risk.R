library(cmprsk)
library(randomForestSRC)
library(survival)
library(ranger)
library(ggplot2)
library(dplyr)
library(ggfortify)
library(ggRandomForests)
library("survival")
library("survminer")
# read data
path="/Users/jadonzhou/Research Projects/Healthcare Predictives/Edoxaban vs warfarin database/Hip fractures/DatabasePSM.csv"
databaseName="DatabasePSM"
Data <- read.csv(path)
str(Data)
# Cumulative incidence functions
CI.overall <- cuminc(ftime = Data$Time, fstatus = Data$Event)
plot(CI.overall, curvlab = c("New onset pancreas cancer", "New onset non-pancreatic cancer","Non-pancreatic cancer mortality"), xlab = "Days")

# Cumulative incidence functions stratified by drug use
CI.4vs5 <- cuminc(ftime = Data$AllTime, fstatus = Data$AllEvent,group = Data$ARB.v.s..ACEI)
plot(CI.4vs5, lty = c(1, 1, 2, 2,3,3,4,4,5,5,6,6,7,7), 
     col = c("black", "blue", "red","green","purple","orange","black","blue","red","green","purple","orange"), 
     curvlab = c("New onset pancreas cancer, ACEI", "New onset pancreas cancer, ARB","New onset non-pancreatic cancer, ACEI", "New onset non-pancreatic cancer, ARB","Non-pancreatic cancer mortality, ACEI", "Non-pancreatic cancer mortality, ARB"), 
     xlab = "Observation time, days", 
     ylim = c(0.0, 0.3),xlim = c(0.0, 7000),
     ylab='Cumulative incidence functions')+title("After matching")
CI.4vs5$Tests


# Cumulative incidence functions stratified by drug use
CI.4vs5 <- cuminc(ftime = Data$AllTime, fstatus = Data$AllEvent,group = Data$ARB.v.s..ACEI)
plot(CI.4vs5, lty = c(1, 1, 2, 2), 
     col = c("black", "blue", "red","green"), 
     curvlab = c("New onset pancreatic cancer, ACEI", "New onset pancreatic cancer, ARB","Non-pancreatic cancers, ACEI", "Non-pancreatic cancers, ARB"), 
     xlab = "Observation time, days", 
     ylim = c(0.0, 0.3),
     ylab='Cumulative incidence functions')+title("Before 1:1 matching")
CI.4vs5$Tests

# Cumulative incidence functions stratified by drug use
Data <- read.csv("/Users/jadonzhou/Research Projects/Healthcare Predictives/ACEI ARB Cancer/2. Breast, Ovarian, Prostate cancer/1. Breast and ovarian/Database PSM.csv")
CI.4vs5 <- cuminc(ftime = Data$Time, fstatus = Data$Event,group = Data$ARB.v.s..ACEI)
plot(CI.4vs5, lty = c(1, 1), 
     col = c("black", "blue"), 
     curvlab = c("New onset breast cancer, ACEI", "New onset breast cancer, ARB"), 
     xlab = "Observation time, days", 
     ylim = c(0.0, 0.3),
     ylab='Cumulative incidence functions')+title("After matching")
CI.4vs5$Tests


# cause-specific hazard model
summary(coxph(formula=Surv (AllTime, AllEvent=="1") ~Edoxaban.v.s..warfarin, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="2") ~Edoxaban.v.s..warfarin, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="3") ~Edoxaban.v.s..warfarin, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="4") ~SGLT2I.v.s..DPP4I, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="5") ~SGLT2I.v.s..DPP4I, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="6") ~Statins, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="7") ~Statins, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="8") ~Statins, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="9") ~Statins, data = Data))
summary(coxph(formula=Surv (AllTime, AllEvent=="10") ~Statins, data = Data))

#
x=cbind(Data[1:5000,]$ARB.v.s..ACEI)
crr(Data[1:5000,]$Time, Data[1:5000,]$Event, x,failcode=2)




#######################
library(ggsci)
library(cowplot)
library(survival)
library(cmprsk)
set.seed(2)
df = data.frame(
  Time = rexp(100),
  genotype = factor(sample(1:3,100,replace=TRUE)),
  Event = factor(sample(0:1,100,replace=TRUE),0:1,c('no event', 'death'))
)

fit <- cuminc(Data$Time, Data$Event, group = Dta$Statins)
# handles cuminc objects
ggcompetingrisks(fit)
ggcompetingrisks(fit, multiple_panels = FALSE)
ggcompetingrisks(fit, conf.int = TRUE)
ggcompetingrisks(fit, multiple_panels = FALSE, conf.int = TRUE)


ggcompetingrisks (fit, xlab = "Observation time, days", 
                  ylab = "Cumulative incidence",
                  xlim = c(0, 5),
                  break.time.by = 10,
                  fontsize = 5,
                  ggtheme = theme_bw(),
                  font.main = 18,
                  font.x =  16,
                  font.y = 16,
                  font.tickslab = 12,
                  palette = c("green", "blue", "red"),
                  multiple_panels = FALSE,
                  conf.int = FALSE)


# handles survfitms objects
library(survival)
df <- data.frame(time = ss, group = gg, status = cc, strt)
fit2 <- survfit(Surv(time, status, type="mstate") ~ 1, data=df)
ggcompetingrisks(fit2)
fit3 <- survfit(Surv(time, status, type="mstate") ~ group, data=df)
ggcompetingrisks(fit3)
ggcompetingrisks(fit3) + theme_cowplot() + scale_fill_jco()







