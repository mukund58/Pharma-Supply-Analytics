#Architecture

## Drug Supply Risk Analytics Dashboard
v1
```
             FDA openFDA
                  │
                  ▼
          Drug Shortages API
                  │
                  ▼
             Python ETL
                  │
                  ▼
             PostgreSQL
                  │
                  ▼
            SQL Analytics
                  │
          ┌───────┴────────┐
          ▼                ▼
       Analysis         Risk Metrics
          │                │
          └───────┬────────┘
                  ▼
             Streamlit
                  │
                  ▼
        Drug Supply Dashboard
```
v2
```
                         FDA openFDA
                              │
                              ▼
                    Drug Shortages API
                              │
                              ▼
                       Python ETL
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Raw JSON/CSV                Data Cleaning
                 │                         │
                 └────────────┬────────────┘
                              ▼
                         PostgreSQL
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
            Drugs          Companies     Supply Events
                              │
                              ▼
                       SQL Analytics
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
              Trends       Company      Therapeutic
                           Analysis       Analysis
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                         Streamlit
                              │
                              ▼
                  Drug Supply Dashboard


                   PostgreSQL
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
    Status View    Availability View   Dosage View
        │               │                │
        └───────────────┼────────────────┘
                        │
                        ▼
                    dashboard.py
                        │
        ┌───────────────┼──────────────────┐
        ▼               ▼                  ▼
      KPIs            Charts             Filters
        │               │                  │
        └───────────────┼──────────────────┘
                        ▼
                   Streamlit UI
```


## ETL pipeline:
```
             FDA API
                │
                ▼
        Raw JSON response
                │
                ▼
      drug_shortages_raw.csv
                │
                ▼
          Data Cleaning
                │
                ▼
       Clean PostgreSQL tables
                │
                ▼
           SQL Analytics
                │
                ▼
        Streamlit Dashboard

```

## Your data has three different concepts

This is important for the project.

A. Supply status
Current
To Be Discontinued
Resolved
B. FDA update event
New
Reverified
Revised
C. Availability
Available
Limited Availability
Unavailable


## Required fields

Keep:

package_ndc
generic_name
company_name
presentation
status
update_type
initial_posting_date
update_date
therapeutic_category
Optional fields

Keep them nullable:

shortage_reason
availability
discontinued_date
change_date
resolved_note
related_info
related_info_link

## database design
```
                    PostgreSQL
                        │
          ┌─────────────┴─────────────┐
          │                           │
          ▼                           ▼
    drug_supply_records        therapeutic_categories
          │                           │
          │                           │
          ├── package_ndc             ├── package_ndc
          ├── generic_name            └── category
          ├── company_name
          ├── status
          ├── availability
          ├── dosage_form
          ├── shortage_reason
          ├── initial_posting_date
          ├── update_date
          ├── change_date
          └── discontinued_date
```

🎯 Dashboard we'll eventually build
- Page 1 — Overview
FDA DRUG SUPPLY ANALYTICS
```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│  1,601   │ │  1,153   │ │   129    │ │  1,571   │
│ Records  │ │ Current  │ │Companies │ │ Products │
└──────────┘ └──────────┘ └──────────┘ └──────────┘

          Supply Events Over Time

                  📈

┌───────────────────────┬─────────────────────────┐
│ Availability           │ Therapeutic Categories │
│                       │                         │
│ Available             │ Anesthesia             │
│ Limited               │ Psychiatry             │
│ Unavailable           │ Cardiovascular         │
└───────────────────────┴─────────────────────────┘
```
- Page 2 — Drug Analysis
Generic drug
Brand
Dosage form
Manufacturer
Status
Availability
- Page 3 — Company Analysis
Company
Current records
Discontinued records
Availability distribution
- Page 4 — Supply Trends
New vs revised vs reverified
Year/month trends
Current vs resolved
Duration
- Page 5 — Supply Risk Explorer

Filter by:

Company
Drug
Therapeutic category
Dosage form
Availability
Status
Date


