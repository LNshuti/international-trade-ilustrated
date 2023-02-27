
suppressMessages(suppressWarnings(source("manifest.R")))

# to start an in-memory database
con <- dbConnect(duckdb::duckdb(), dbdir = ":memory:")

country_ids <- 
  read_csv("../data/countries_codes_and_coordinates.csv") %>%
  janitor::clean_names() %>%
  select(alpha_3_code, numeric_code) %>%
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

deficit_plot <- 
  ggplot(data = top_bottom_df, 
         aes(x=partner_code, 
             y=trade_balance, 
             color=hi_lo, 
             label=partner_code)) + 
  geom_point(data = top_bottom_df, aes(size=trade_bal_abs)) +
  scale_color_manual(values = deficit_cols) + 
  geom_hline(yintercept = 0, color="gray30") +
  guides(size="none", color="none") +
  scale_y_continuous(limits=c(-200, 450), labels = scales::dollar) +
  facet_wrap(~ country_name, ncol = 1) +
  ggrepel::geom_text_repel(data= top_bottom_df,
                           size = 2,
                           box.padding = 0.7) +
  labs(x=NULL,
       y = "Trade Balance In Billions USD",  title = "",
       caption = "Data source: \nAtlas of Economic Complexity from the Growth Lab at Harvard University.\nhttps://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/H8SFD2.") +
  theme(plot.caption = element_text(size = 8, hjust = 0),
        axis.title.x=element_blank(),
        axis.title.y=element_blank(), 
        plot.caption.position =  "plot",
        panel.background = element_blank()) +
  theme_minimal() +
  theme(axis.text.x = element_blank()) 

ggsave(deficit_plot,
       filename = paste0("../output/deficit_plot_us_chn_rus.png"),
       width = 8, height = 6)