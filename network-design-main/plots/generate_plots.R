library(grid)
library(doBy)
library(ggplot2)
library(reshape2)
library(plyr)

mb2 <- read.table("../analyses/mb.txt", header = TRUE);

mb2_fun <- function(x) (x+1)*(x+1) + 1

# mb2 <- subset(mb2, topology != "HX" & topology != "FT2")

LEGEND_PROPS <- 
  theme_bw(18) +
  theme(panel.border = element_rect(colour="black", size=1.0, linetype="solid")) +
  theme(panel.grid.major = element_line(colour = 'grey', linetype = 'solid')) +
  theme(legend.key.height=grid::unit(1, "lines")) +
  theme(legend.background = element_rect(colour="black", size=.5, linetype="solid")) +
  theme(plot.margin=unit(c(0.3, 0.1, 0.1, 0), "cm")) +
  theme(legend.key = element_blank()) 
#  theme(axis.text.x = element_text(angle = 0, hjust = 0)) +
#  theme(legend.position=c(0.2, 0.73))

PLOT_MB <- ggplot(data=mb2, aes(x=max_radix, y=endpoints, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
  scale_shape_manual(values=c(16, 17, 18, -1, 19, 20))+
#  geom_function( fun=mb2_fun, linetype = 1) +
#  scale_y_log10() +
#  scale_x_log10() +
  labs(x = "maximum radix", y = "#endpoints") 

m <- PLOT_MB + LEGEND_PROPS;
ggsave("plot_MB2.pdf",width=7,height=4)



data_sf <- read.table("../cost-power-analysis/results/cost_power_cables-qdr56/sf_a-2q.txt", header = TRUE);
data_pf <- read.table("../cost-power-analysis/results/cost_power_cables-qdr56/pf.txt", header = TRUE);
data_df <- read.table("../cost-power-analysis/results/cost_power_cables-qdr56/df_full.txt", header = TRUE);
data_ft3 <- read.table("../cost-power-analysis/results/cost_power_cables-qdr56/ft3.txt", header = TRUE);
data_del3 <- read.table("../cost-power-analysis/results/cost_power_cables-qdr56/del3.txt", header = TRUE);
data_prod3 <- read.table("../cost-power-analysis/results/cost_power_cables-qdr56/prod3.txt", header = TRUE);


x <- rbind(data.frame( endpoints  = as.numeric(data_sf$endpoints),
                       radix = as.numeric(data_sf$radix),
                       k_r = as.numeric(data_sf$k_r),
                       p = as.numeric(data_sf$p),
                       routers = as.numeric(data_sf$routers),
                       total_cost = as.numeric(data_sf$total_cost),
                       total_power = as.numeric(data_sf$total_power),
                       cost_per_endpoint_indir = as.numeric(data_sf$cost_per_endpoint_indir),
                       power_per_endpoint_indir = as.numeric(data_sf$power_per_endpoint_indir),
                       cost_per_endpoint_dir = as.numeric(data_sf$cost_per_endpoint_dir),
                       power_per_endpoint_dir = as.numeric(data_sf$power_per_endpoint_dir),
                       topology = rep("SF", length(data_sf$endpoints))),
           data.frame( endpoints  = as.numeric(data_pf$endpoints),
                       radix = as.numeric(data_pf$radix),
                       k_r = as.numeric(data_pf$k_r),
                       p = as.numeric(data_pf$p),
                       routers = as.numeric(data_pf$routers),
                       total_cost = as.numeric(data_pf$total_cost),
                       total_power = as.numeric(data_pf$total_power),
                       cost_per_endpoint_indir = as.numeric(data_pf$cost_per_endpoint_indir),
                       power_per_endpoint_indir = as.numeric(data_pf$power_per_endpoint_indir),
                       cost_per_endpoint_dir = as.numeric(data_pf$cost_per_endpoint_dir),
                       power_per_endpoint_dir = as.numeric(data_pf$power_per_endpoint_dir),
                       topology = rep("PF", length(data_pf$endpoints))),
           data.frame( endpoints  = as.numeric(data_df$endpoints),
                       radix = as.numeric(data_df$radix),
                       k_r = as.numeric(data_df$k_r),
                       p = as.numeric(data_df$p),
                       routers = as.numeric(data_df$routers),
                       total_cost = as.numeric(data_df$total_cost),
                       total_power = as.numeric(data_df$total_power),
                       cost_per_endpoint_indir = as.numeric(data_df$cost_per_endpoint_indir),
                       power_per_endpoint_indir = as.numeric(data_df$power_per_endpoint_indir),
                       cost_per_endpoint_dir = as.numeric(data_df$cost_per_endpoint_dir),
                       power_per_endpoint_dir = as.numeric(data_df$power_per_endpoint_dir),
                       topology = rep("DF", length(data_df$endpoints))),
           data.frame( endpoints  = as.numeric(data_ft3$endpoints),
                       radix = as.numeric(data_ft3$radix),
                       k_r = as.numeric(data_ft3$k_r),
                       p = as.numeric(data_ft3$p),
                       routers = as.numeric(data_ft3$routers),
                       total_cost = as.numeric(data_ft3$total_cost),
                       total_power = as.numeric(data_ft3$total_power),
                       cost_per_endpoint_indir = as.numeric(data_ft3$cost_per_endpoint_indir),
                       power_per_endpoint_indir = as.numeric(data_ft3$power_per_endpoint_indir),
                       cost_per_endpoint_dir = as.numeric(data_ft3$cost_per_endpoint_dir),
                       power_per_endpoint_dir = as.numeric(data_ft3$power_per_endpoint_dir),
                       topology = rep("FT3", length(data_ft3$endpoints))),
           data.frame( endpoints  = as.numeric(data_del3$endpoints),
                       radix = as.numeric(data_del3$radix),
                       k_r = as.numeric(data_del3$k_r),
                       p = as.numeric(data_del3$p),
                       routers = as.numeric(data_del3$routers),
                       total_cost = as.numeric(data_del3$total_cost),
                       total_power = as.numeric(data_del3$total_power),
                       cost_per_endpoint_indir = as.numeric(data_del3$cost_per_endpoint_indir),
                       power_per_endpoint_indir = as.numeric(data_del3$power_per_endpoint_indir),
                       cost_per_endpoint_dir = as.numeric(data_del3$cost_per_endpoint_dir),
                       power_per_endpoint_dir = as.numeric(data_del3$power_per_endpoint_dir),
                       topology = rep("DEL3", length(data_del3$endpoints))),
           data.frame( endpoints  = as.numeric(data_prod3$endpoints),
                       radix = as.numeric(data_prod3$radix),
                       k_r = as.numeric(data_prod3$k_r),
                       p = as.numeric(data_prod3$p),
                       routers = as.numeric(data_prod3$routers),
                       total_cost = as.numeric(data_prod3$total_cost),
                       total_power = as.numeric(data_prod3$total_power),
                       cost_per_endpoint_indir = as.numeric(data_prod3$cost_per_endpoint_indir),
                       power_per_endpoint_indir = as.numeric(data_prod3$power_per_endpoint_indir),
                       cost_per_endpoint_dir = as.numeric(data_prod3$cost_per_endpoint_dir),
                       power_per_endpoint_dir = as.numeric(data_prod3$power_per_endpoint_dir),
                       topology = rep("PROD3", length(data_prod3$endpoints)))
)

x <- subset(x, topology != "FT3" & topology != "PROD3" & topology != "DEL3")
x <- subset(x, endpoints < 50000)

LEGEND_PROPS <- 
  theme_bw(20) +
  theme(panel.border = element_rect(colour="black", size=1.0, linetype="solid")) +
  theme(panel.grid.major = element_line(colour = 'grey', linetype = 'solid')) +
  theme(legend.key.height=grid::unit(1, "lines")) +
  theme(legend.background = element_rect(colour="black", size=.5, linetype="solid")) +
  theme(plot.margin=unit(c(0.3, 0.1, 0.1, 0), "cm")) +
  theme(legend.key = element_blank()) 
#  theme(axis.text.x = element_text(angle = 0, hjust = 0)) +
#  theme(legend.position=c(0.2, 0.73))

PLOT_COST_TOTAL <- ggplot(data=x, aes(x=endpoints, y=total_cost, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
#  scale_y_log10() +
#  scale_x_log10() +
  labs(x = "#endpoints", y = "network cost [$]") 

PLOT_COST_ENDPOINT_INDIR <- ggplot(data=x, aes(x=endpoints, y=cost_per_endpoint_indir, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
  scale_y_log10() +
  scale_x_log10() +
  labs(x = "#endpoints", y = "network cost / endpoint (indir) [$]") 

PLOT_COST_ENDPOINT_DIR <- ggplot(data=x, aes(x=endpoints, y=cost_per_endpoint_dir, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
  scale_y_log10() +
  scale_x_log10() +
  labs(x = "#endpoints", y = "network cost / endpoint (dir) [$]") 

PLOT_POWER_TOTAL <- ggplot(data=x, aes(x=endpoints, y=total_power, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
#  scale_y_log10() +
#  scale_x_log10() +
  labs(x = "#endpoints", y = "network power [W]") 

PLOT_POWER_ENDPOINT_INDIR <- ggplot(data=x, aes(x=endpoints, y=power_per_endpoint_indir, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
  scale_y_log10() +
  scale_x_log10() +
  labs(x = "#endpoints", y = "network power / endpoint (indir) [W]") 

PLOT_POWER_ENDPOINT_DIR <- ggplot(data=x, aes(x=endpoints, y=power_per_endpoint_dir, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
  scale_y_log10() +
  scale_x_log10() +
  labs(x = "#endpoints", y = "network power / endpoint (dir) [W]") 

PLOT_SCALABILITY_INDIR <- ggplot(data=x, aes(x=radix, y=endpoints, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
  scale_y_log10() +
  scale_x_log10() +
  labs(x = "total radix", y = "#endpoints (indirect)") 

PLOT_SCALABILITY_DIR <- ggplot(data=x, aes(x=radix, y=routers, shape=topology, color=topology)) +
  geom_point(size=3) +
  geom_line() +
  scale_y_log10() +
  scale_x_log10() +
  labs(x = "total radix", y = "#endpoints (direct)") 


m <- PLOT_COST_TOTAL + LEGEND_PROPS;
ggsave("plot_cost_total.pdf",width=7,height=4)

m <- PLOT_COST_ENDPOINT_INDIR + LEGEND_PROPS;
ggsave("plot_cost_per_endpoint_indirect.pdf",width=7,height=4)

m <- PLOT_COST_ENDPOINT_DIR + LEGEND_PROPS;
ggsave("plot_cost_per_endpoint_direct.pdf",width=7,height=4)

m <- PLOT_POWER_TOTAL + LEGEND_PROPS;
ggsave("plot_power_total.pdf",width=7,height=4)

m <- PLOT_POWER_ENDPOINT_INDIR + LEGEND_PROPS;
ggsave("plot_power_per_endpoint_indirect.pdf",width=7,height=4)

m <- PLOT_POWER_ENDPOINT_DIR + LEGEND_PROPS;
ggsave("plot_power_per_endpoint_direct.pdf",width=7,height=4)

m <- PLOT_SCALABILITY_INDIR + LEGEND_PROPS;
ggsave("plot_scalability_indirect.pdf",width=7,height=4)

m <- PLOT_SCALABILITY_DIR + LEGEND_PROPS;
ggsave("plot_scalability_direct.pdf",width=7,height=4)
