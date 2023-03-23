library(broom) #for glance function
library(tidyverse) #Data shaping and visualization
library(cjar) #For data extraction
library(caret) #For Data Modeling

cja_auth() #Authenticating to CJA for extraction

#How many Data Views are available to me?
dv <- cja_get_dataviews(expansion = c('name', 'description')) 

#Getting all the information about the data view I'm working from
dims <- cja_get_dimensions(dataviewId = 'dv')
mets <- cja_get_metrics(dataviewId = 'dv')
calcmets <- cja_get_calculatedmetrics(dataviewId = 'dv')
dr <- cja_get_dateranges(
  locale = "en_US",
  filterByIds = NULL,
  limit = 10,
  page = 0,
  expansion = "definition",
  includeType = "all")

#Extract Directly into R
mc <- cja_freeform_table(dataviewId = 'dv',
                         date_range = c("2020-12-01", "2020-12-31"),
                         dimensions = c('CRMID'),
                         metrics = c('order','calls',
                                     'call.Orders','inStore.Orders',
                                     'inStore.Purchases','Mobile.Orders',
                                     'web.Purchases','web.Revenue',
                                     'revenue','survey.Score'),
                         top = 50000,
                         page = 0)

#I pulled gender separately
Gen <- cja_freeform_table(dataviewId = 'dv',
                          date_range = c("2020-12-01", "2020-12-31"),
                          dimensions = c('gender','CRMID'),
                          top = 50000,
                          page = 0)

#Join Gender
Data <- left_join(mc, Gen, by = c("CRMID" = "CRMID"))

#Saved to CSV
write.csv(Data, "C:/filepath/Data.csv")

final<- read.csv("C:/filepath/Data.csv")

#Now drop CRM ID for modeling
final<-final %>%
  select(-'CRMID')

#Final Data Set
head(final)

#Basic KMeans
kclust <- kmeans(final, centers = 3)
kclust$centers 

glance(kclust) #Just to see what it looks like

#Determine the amount of clusters to use

kclusts <- tibble(k = 1:9) %>%
  mutate(
    kclust = map(k, ~kmeans(final, .x)),
    glanced = map(kclust, glance),
    augmented = map(kclust, augment, final)
  )

clusterings <- kclusts %>%
  unnest(glanced, .drop = TRUE)

ggplot(clusterings, aes(k, tot.withinss)) +
  geom_line()+
  xlab("Number of Clusters")+
  ylab("Within groups sum of squares")+
  theme(axis.text.y=element_blank(),
        axis.ticks.y=element_blank(),
        panel.background = element_blank())

#What does it look like?
assignments <- kclusts %>%
  unnest(augmented)
ggplot(assignments, aes(Revenue, Purchases)) +
  geom_point(aes(color = .cluster), alpha=0.3) +
  facet_wrap(~ k)


#Model the data and add the Final clusters to my dataset
kclusts <- kmeans(final, centers = 5) #using five from our discovery
kclusts$centers

finalk <- augment(kclusts, final)

#What do these groups look like?
finalk <- finalk %>%
  mutate(cluster = as.integer(.cluster))%>%
  select(-.cluster)

segments <- finalk %>% 
  group_by(cluster) %>% 
  summarise_all("mean")









