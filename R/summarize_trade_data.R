
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

usa_chn_rus <-
  allcountries_trade_df %>% 
  filter(location_code %in% c("USA", "CHN", "RUS"))


dbWriteTable(con, "usa_chn_rus", usa_chn_rus, overwrite = TRUE)
summary_df <- dbGetQuery(con, 'SELECT "location_code", "partner_code",  SUM("export_value" - "import_value") as trade_balance FROM usa_chn_rus GROUP BY "location_code", "partner_code"')
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
  group_by(location_code) %>%
  slice(1:5) %>% 
  ungroup()

bottom_df <- 
  summary_tbl %>%
  filter(trade_balance < 0) %>%
  arrange(trade_balance) %>%
  group_by(location_code) %>%
  slice(1:5) %>% 
  ungroup()

top_bottom_df <- bind_rows(top_df, bottom_df) %>% arrange(trade_balance)

deficit_cols <- c("1"="#2E74C0", "0"="#CB454A")

deficit_plot <- 
  ggplot(data = top_bottom_df, aes(x=partner_code, y=trade_balance, color=hi_lo, label=partner_code)) + 
  geom_point(size= 2) +
  scale_color_manual(values = deficit_cols) + 
  geom_hline(yintercept = 0, color="gray30") +
  guides(color=FALSE) +
  facet_wrap(~ location_code, ncol = 1) +
  ggrepel::geom_text_repel(data= top_bottom_df, size = 2) +
  labs(x=NULL, y = "Trade Balance In Billions $",  title = "",
       caption = "Data source: \nAtlas of Economic Complexity from the Growth Lab at Harvard University.\nhttps://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/H8SFD2.") +
  theme(plot.caption = element_text(size = 8, hjust = 0),
        axis.title.x=element_blank(),
        axis.title.y=element_blank(), 
        plot.caption.position =  "plot",
        panel.background = element_blank()
  ) +
  ggthemes::theme_economist_white()+ 
  theme(axis.text.x = element_blank())

ggsave(deficit_plot,
       filename = paste0("../output/deficit_plot_us_chn_rus.png"),
       width = 8, height = 6)

################################################################################
# China Export Details 
################################################################################
product_details <- 
  list.files(paste0("../../dataverse_files"), recursive = TRUE) %>%
  as_tibble() %>%
  filter(grepl(pattern = "country", x = value)) %>%
  filter(grepl(pattern = "country_sitcproductsection", x = value)) %>%
  filter(grepl(pattern = ".parquet", x = value)) %>% 
  pull(value)

allcountries_trade_df <-
  read.table("../data/SITC_Rev_3_english_structure.txt", sep='\t',header=TRUE) %>%
  janitor::clean_names() %>% 
  # filter(location_code %in% c("USA", "CHN", "RUS", "BWA")) %>%
  as_tibble() %>%
  mutate_all(as.character) %>%
  bind_rows() %>%
  mutate_at(c("export_value", "import_value"), as.numeric)

  
    

china_df <- 
  usa_chn_rus %>% 
  filter(location_code == "CHN") %>%
  group_by(sitc_product_code) %>%
  summarise(total_exports = sum(export_value)) %>% 
  arrange(desc(total_exports))

df1 = read.csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/sunburst-coffee-flavors-complete.csv')
df2 = read.csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/coffee-flavors.csv')

fig <- plot_ly(
  type='treemap',
  ids=df1$ids,
  labels=df1$labels,
  parents=df1$parents,
  domain=list(column=0))

fig <- fig %>% add_trace(
  type='treemap',
  ids=df2$ids,
  labels=df2$labels,
  parents=df2$parents,
  maxdepth=1,
  domain=list(column=1))
fig <- fig %>% layout(grid=list(columns=2, rows=1))
fig

#ggsave(deficit_plot, "output/deficit_plot_us_chn_rus.png")

# trade_bal_2020 <- 
#   ggplot(data = top_bottom_df, 
#          mapping = aes(x = partner_code, y = trade_balance, fill = hi_lo)) + 
#   geom_col() + 
#   guides(fill=FALSE) +
#   facet_wrap(~ location_code, ncol=1, scales = "free_y") +
#    
# ggsave(trade_bal_2020,
#        filename = paste0(repo_path, "/output/deficit_plot_us_chn_rus.png"),
#        width = 8, height = 4)
