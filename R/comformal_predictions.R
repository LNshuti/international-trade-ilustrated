library(rstanarm)
library(conformalbayes)
data("Loblolly")

####################### Import data #################################
suppressMessages(suppressWarnings(source("manifest.R")))

# to start an in-memory database
con <- dbConnect(duckdb::duckdb(), dbdir = ":memory:")

product_labs <- 
  readxl::read_excel("../data/SITCCodeandDescription.xlsx") %>%
  janitor::clean_names()

country_ids <- 
  read_csv("../data/countries_codes_and_coordinates.csv") %>%
  janitor::clean_names() %>%
  select(alpha_3_code, numeric_code, country,
         contains("lon"), contains("lat")) %>%
  mutate(numeric_code = as.character(numeric_code))

#Combine trade data from 2000 to 2020
trade_data_all_years <-
  list.files(paste0("../../dataverse-files"), recursive = TRUE) %>%
  as_tibble() %>%
  filter(grepl(pattern = "partner_sitcproduct4digit", x = value)) %>%
  filter(grepl(pattern = ".parquet", x = value)) %>%
  filter(grepl(pattern = "2020", x = value)) %>%
  pull(value)

allcountries_trade_df <-
  trade_data_all_years %>%
  map(~arrow::read_parquet(file = paste0("../../dataverse-files/",.x)) %>%
        janitor::clean_names() %>% 
        # filter(location_code %in% c("USA", "CHN", "RUS", "BWA")) %>%
        as_tibble() %>%
        mutate_all(as.character)
  ) %>%
  bind_rows() %>%
  mutate_at(c("export_value", "import_value"), as.numeric) #%>%
  # group_by(product_name, year) %>%
  # summarise(imports = sum(import_value, na.rm = TRUE), 
  #           exports = sum(export_value, na.rm = TRUE)) 

pop_data <-
  read_csv('../data/processed/API_SP_POP_TOTL_DS2.csv', skip = 4) %>%
  as_tibble() %>%
  janitor::clean_names() %>%
  select('country_name', 'country_code', 'x2020') %>%
  rename(pop_2020='x2020') 





fit_idx = sample(nrow(Loblolly), 50)
d_fit = Loblolly[fit_idx, ]
d_test = Loblolly[-fit_idx, ]

# fit a simple linear regression
m = stan_glm(height ~ sqrt(age), data=d_fit,
             chains=1, control=list(adapt_delta=0.999), refresh=0)

# prepare conformal predictions
m = loo_conformal(m)

# make predictive intervals
pred_ci = predictive_interval(m, newdata=d_test, prob=0.9)
print(head(pred_ci))
#>             5%       95%
#> 1  -0.15888597  5.600095
#> 29 25.43314599 30.988491
#> 57 48.67648127 54.182655
#> 2  -0.09561987  5.447242
#> 30 25.42970114 30.938488
#> 72 58.01173186 63.596592

# are we covering?
mean(pred_ci[, "5%"] <= d_test$height &
       d_test$height <= pred_ci[, "95%"])
#> [1] 0.9117647
#> 
library(conformalbayes)
library(rstanarm)
library(ggplot2)

sim_data = function(n=50) {
  x = rnorm(n)
  y = 3 - 2*x + rt(n, df=2)
  data.frame(x=x, y=y)
}

d_fit = sim_data()

ggplot(d_fit, aes(x, y)) +
  geom_point() +
  geom_smooth(method=lm, formula=y~x)

# fit the model
m = stan_glm(y ~ x, data=d_fit, chains=1, refresh=0)

d_test = sim_data(2000)

interv_model = predictive_interval(m, newdata=d_test, prob=0.50)

# are the points covered
covered_model = with(d_test, interv_model[, 1] <= y & y <= interv_model[, 2])

ggplot(d_test, aes(x, y, color=covered_model, group=1)) +
  geom_point(size=0.4) +
  geom_linerange(aes(ymin=interv_model[, 1],
                     ymax=interv_model[, 2]), alpha=0.4) +
  labs(color="Covered?") +
  geom_smooth(method=lm, formula=y~x, color="black")


m = loo_conformal(m)
print(m)


interv_jack = predictive_interval(m, newdata=d_test, prob=0.50)

# are the points covered
covered_jack = with(d_test, interv_jack[, 1] <= y & y <= interv_jack[, 2])

ggplot(d_test, aes(x, y, color=covered_jack, group=1)) +
  geom_point(size=0.4) +
  geom_linerange(aes(ymin=interv_jack[, 1],
                     ymax=interv_jack[, 2]), alpha=0.4) +
  labs(color="Covered?") +
  geom_smooth(method=lm, formula=y~x, color="black")