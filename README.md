# FX Credit Configuration Schema Viewer

A Streamlit application that demonstrates a YAML-based configuration schema for FX trading systems, including Prime Brokers, Customers, Sessions, and Credit Limits.

## Features

- **Interactive Schema Visualization**: 2D diagram showing relationships between configuration files
- **Live Query Examples**: Interactive Python demos for common queries
- **Error Handling Examples**: Production-ready validation and error handling patterns
- **Design Rationale**: Explanation of YAML structure and design decisions

## Configuration Files

The application uses four YAML configuration files:

- `prime_brokers.yaml` - Prime Broker definitions and central PB designation
- `customers.yaml` - Customer entity definitions  
- `sessions.yaml` - Trading session configurations linking customers to PBs
- `credit_data.yaml` - Credit limits and exposure data (updated by 3rd party vendor)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Schema Overview**: View the visual diagram showing file relationships
2. **Interactive Queries**: Test Python code examples for:
   - Session to Prime Broker lookup
   - Customer credit limit queries  
   - Credit exposure validation
3. **Error Handling**: Review production validation patterns
4. **Configuration Details**: Explore each YAML file structure

## File Structure

```
.
├── app.py                 # Main Streamlit application
├── prime_brokers.yaml     # Prime Broker configuration
├── customers.yaml         # Customer definitions
├── sessions.yaml          # Trading session mappings
├── credit_data.yaml       # Credit limits and exposure data
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Key Design Principles

- **YAML for readability** - Human-friendly configuration format
- **Normalized structure** - ID-based relationships between entities
- **Separate static/dynamic data** - Different update frequencies
- **Explicit relationships** - Clear mapping between customers, sessions, and PBs
- **Audit-friendly timestamps** - Track when credit data was last updated 