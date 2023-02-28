suppressMessages(suppressWarnings(source("manifest.R")))

# to start an in-memory database
con <- dbConnect(duckdb::duckdb(), dbdir = ":memory:")

country_ids <- 
  read_csv("../data/countries_codes_and_coordinates.csv") %>%
  janitor::clean_names() %>%
  select(alpha_3_code, numeric_code, country,
         contains("lon"), contains("lat")) %>%
  mutate(numeric_code = as.character(numeric_code))

#Combine trade data from 2000 to 2020
trade_data_all_years <-
  list.files(paste0("../../dataverse_files"), recursive = TRUE) %>%
  as_tibble() %>%
  filter(grepl(pattern = "partner_sitcproduct4digit", x = value)) %>%
  filter(grepl(pattern = ".parquet", x = value)) %>%
  filter(grepl(pattern = "2020", x = value)) %>%
  pull(value)

allcountries_trade_df <-
  trade_data_all_years %>%
  map(~arrow::read_parquet(file = paste0("../../dataverse_files/",.x)) %>%
        janitor::clean_names() %>% 
        # filter(location_code %in% c("USA", "CHN", "RUS", "BWA")) %>%
        as_tibble() %>%
        mutate_all(as.character)
  ) %>%
  bind_rows() %>%
  mutate_at(c("export_value", "import_value"), as.numeric)

pop_data <-
  read_csv('../data/processed/API_SP_POP_TOTL_DS2.csv', skip = 4) %>%
  as_tibble() %>%
  janitor::clean_names() %>%
  select('country_name', 'country_code', 'x2020') %>%
  rename(pop_2020='x2020') 

usa_brics <-
  allcountries_trade_df %>% 
  filter(location_code %in% c("USA", "CHN", "RUS", "IND", "ZAF")) %>%
  inner_join(pop_data, by = c("location_code" = "country_code"))

dbWriteTable(con, "usa_brics", usa_brics, overwrite = TRUE)

summary_df <-
  dbGetQuery(con, 
             'SELECT "country_name", "partner_code",  SUM("export_value" - "import_value") as trade_balance FROM usa_brics GROUP BY "country_name", "partner_code"')

summary_tbl <- 
  summary_df %>% 
  mutate(trade_balance = trade_balance/1000000000) %>%
  #filter(from == "AGO") %>%
  mutate(hi_lo = ifelse(trade_balance > 0, 1, 0)) %>%
  mutate(hi_lo = as.factor(hi_lo))

top_df <- 
  summary_tbl %>%
  filter(trade_balance > 0) %>%
  arrange(desc(trade_balance)) %>%
  group_by(country_name) %>%
  slice(1:5) %>% 
  ungroup()

bottom_df <- 
  summary_tbl %>%
  filter(trade_balance < 0) %>%
  arrange(trade_balance) %>%
  group_by(country_name) %>%
  slice(1:5) %>% 
  ungroup()

top_bottom_df <- 
  bind_rows(top_df, bottom_df) %>% 
  arrange(trade_balance) %>%
  mutate(trade_bal_abs = abs(trade_balance))

deficit_cols <- c("1"="#2E74C0", "0"="#CB454A")