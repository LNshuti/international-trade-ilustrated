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
  mutate_at(c("export_value", "import_value"), as.numeric) %>%
  group_by(product_name, year) %>%
  summarise(imports = sum(import_value, na.rm = TRUE), exports = sum(export_value, na.rm = TRUE)) 

pop_data <-
  read_csv('../data/processed/API_SP_POP_TOTL_DS2.csv', skip = 4) %>%
  as_tibble() %>%
  janitor::clean_names() %>%
  select('country_name', 'country_code', 'x2020') %>%
  rename(pop_2020='x2020') 

usa_brics <-
  allcountries_trade_df %>% 
  filter(location_code %in% c("USA", "CHN", "RUS", "IND", "ZAF")) %>%
  inner_join(pop_data, by = c("location_code" = "country_code")) %>% 
  left_join(product_labs, by = c("sitc_product_code" = "parent_code")) %>% 
  select(description, everything()) %>%
  ungroup() %>%
  rename(name = description) %>%
  mutate(name = ifelse(grepl("gold|mineraks|aluminium|iron/st|steel|minerals|tin ores|base metal", name), " metals", name)) %>%
  mutate(name = ifelse(grepl("cement|refract bricks", name), "cement & construct mat", name)) %>%
  mutate(name = ifelse(grepl("kraft uncoat|printed matter|book|typewrirers|paper cartons", name), "books & paper", name)) %>%
  mutate(name = ifelse(grepl("clothing ", name), "clothing",name)) %>%
  mutate(name = ifelse(grepl("generator|dc motor|electric motors", name), "generator",name)) %>%
  mutate(name = ifelse(grepl("aircraft|aircrft|airplanes|helicopters", name), "aircrafts", name)) %>%
  mutate(name = ifelse(grepl("special tra|un special code", name), "special transactions", name)) %>%
  mutate(name = ifelse(grepl("communication|radio|telecom|telephone|computers", name), "telecom", name)) %>%
  mutate(name = ifelse(grepl("petroleum|petrol|crude oil|liquid propane", name), "petroleum", name)) %>%
  mutate(name = ifelse(grepl("lifting|constr/mining|pulley", name), "construction", name)) %>%
  mutate(name = ifelse(grepl("medicaments|glycosides|x-ray|pharmaceutical|pharmaceut", name), "healthcare goods", name)) %>%
  mutate(name = ifelse(grepl("furniture", name), "furniture",name)) %>%
  mutate(name = ifelse(grepl("musical", name), "musical instruments",name)) %>%
  mutate(name = ifelse(grepl("garments", name), "garments",name)) %>%
  mutate(name = ifelse(grepl("office equip", name), "office equipment",name)) %>%
  mutate(name = ifelse(grepl("soap in form of bars", name), "bar soap",name)) %>%
  mutate(name = ifelse(grepl("scientific instrumnt", name), "scientific instrument",name)) %>%
  mutate(name = ifelse(grepl("machine parts|gas turb eng", name), "machine parts",name)) %>%
  mutate(name = ifelse(grepl("indus wash", name), "industrial wash equip",name)) %>%
  mutate(name = ifelse(grepl("acyclic monohyd alcohols", name), "acyclic monohyd alcohols",name)) %>%
  mutate(name = ifelse(grepl("electro-thermic equipmnt", name), "electro-thermic equipment",name)) %>%
  mutate(name = ifelse(grepl("textile|suits", name), "textiles",name)) %>%
  mutate(name = ifelse(grepl("cigarettes", name), "cigarettes",name)) %>%
  mutate(name = ifelse(grepl("plastic", name), "plastic",name)) %>%
  mutate(name = ifelse(grepl("batteries", name), "batteries",name)) %>%
  mutate(name = ifelse(grepl("leather", name), "leather",name)) %>%
  mutate(name = ifelse(grepl("fertilizers", name), "fertilizers",name)) %>%
  mutate(name = ifelse(grepl("vehicles|passenger|tyres|tires|motorcycles|buses|semi-trailer", name), "vehicles & parts", name)) %>%
  mutate(name = ifelse(grepl("beans|legumes|cane|wheat|corn|maize|sugar|soy|meal|cereal|hydrogenated|beet|chocolate|food|strawberries|fish|ruit fresh|beef|groundnuts|nutmeg|milk|salt|vegetables|rice|beer|fixed veg oils|whey|mutton|spices|veg prod ne|malt|veg oil hydrogen|bread|pork|potatoes|coffee|vanilla|fixed veg oil|cinnamon",
                             name), "food products", name)) %>%
  mutate(name = str_trim(name)) %>%
  mutate(len_name = str_length(name)) %>%
  group_by(country_name, partner_code) %>%
  arrange(name, desc(export_value)) %>%
  filter(!is.na(name)) %>%
  # assign ranking
  # mutate(rank = 1:n()) %>%
  ungroup()

dbWriteTable(con, "usa_brics", usa_brics, overwrite = TRUE)

summary_df <-
  dbGetQuery(con, 
             'SELECT "country_name", "partner_code", name, rank,  SUM("export_value" - "import_value") as trade_balance FROM usa_brics GROUP BY "country_name", "partner_code", "name", "rank"')

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
  slice(1:10) %>% 
  ungroup()

bottom_df <- 
  summary_tbl %>%
  filter(trade_balance < 0) %>%
  arrange(trade_balance) %>%
  group_by(country_name) %>%
  slice(1:10) %>% 
  ungroup()

top_bottom_df <- 
  bind_rows(top_df, bottom_df) %>%
  #group_by(partner_code) %>%
  arrange(partner_code, desc(trade_balance)) %>%
  #ungroup() %>%
  mutate(trade_bal_abs = abs(trade_balance))


##################### For each country, find its top 10 product imports##################
country_ranking_ <- 
  usa_brics %>% 
  select(country_name, partner_code, import_value, name) %>%
  group_by(country_name, partner_code, import_value) %>%
  slice(1) %>% 
  ungroup() %>%
  group_by(country_name) %>%
  arrange(desc(import_value)) %>%
  # assign ranking
  mutate(rank = 1:n()) %>%
  ungroup()

country_top10_ <- 
  country_ranking_ %>%
  arrange(rank) %>%
  filter(country_name == "China")

tab_1 <-
  country_ranking_ %>%
  select(-rank) %>%
  dplyr::slice(1:10) %>%
  gt() %>%
  #gt(rowname_col = "country_name") %>% 
  fmt_currency(
    columns = import_value,
    currency = "USD"
  ) 

tab_1 %>% gtsave("../output/china_top10_imports.png", expand = 10)
