import streamlit as st
import yaml # PyYAML needs to be installed: pip install PyYAML
import os

# --- Streamlit App Layout (must be first) ---
st.set_page_config(layout="wide", page_title="FX Credit Configuration Viewer")

# Custom CSS to make the layout a bit narrower than full wide
st.markdown("""
<style>
    .main .block-container {
        max-width: 1200px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Load Configuration Data from YAML files ---

@st.cache_data
def load_yaml_file(filename):
    """Load YAML file with caching for better performance"""
    try:
        with open(filename, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        st.error(f"Configuration file not found: {filename}")
        return None
    except yaml.YAMLError as e:
        st.error(f"Error parsing YAML file {filename}: {e}")
        return None

# Load all configuration files
prime_brokers_data = load_yaml_file('prime_brokers.yaml')
customers_data = load_yaml_file('customers.yaml')
sessions_data = load_yaml_file('sessions.yaml')
credit_data = load_yaml_file('credit_data.yaml')

# Convert back to strings for display in expandable sections
def data_to_yaml_string(data):
    """Convert data back to YAML string for display"""
    if data is None:
        return "# Error loading file"
    return yaml.dump(data, default_flow_style=False, sort_keys=False)

prime_brokers_data_str = data_to_yaml_string(prime_brokers_data)
customers_data_str = data_to_yaml_string(customers_data)
sessions_data_str = data_to_yaml_string(sessions_data)
credit_data_str = data_to_yaml_string(credit_data)

st.title("FX Credit Configuration Schema Viewer")



# --- Design Rationale ---
st.header("Design Rationale")
with st.expander("Why YAML and this structure?", expanded=False):
    st.markdown("""
    Why YAML?
    Operations teams need to make emergency credit adjustments during market stress without waiting for developer support. YAML's readability enables this while supporting comments for business logic documentation. Version control integration helps track configuration changes for audit and rollback purposes.
    
    Why separate files?
    Credit data updates multiple times daily from third-party vendors, while customer and session configs change infrequently. Separating these enables different access controls and update procedure.
    
    Why this structure?
    ID-based relationships enable independent updates without complex dependencies. When onboarding new clients, you can add customers and sessions without modifying existing prime broker configurations. This separation is crucial for scaling client onboarding operations.
    """)

# --- Schema Diagram ---
st.header("Configuration Schema Overview")


# Create a clear 2D diagram using HTML/CSS
schema_diagram = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            margin: 0; 
            padding: 20px; 
            background-color: white; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        }
        .container { 
            display: flex; 
            flex-direction: column; 
            gap: 30px; 
            max-width: 1200px; 
            margin: 0 auto;
        }
        .file-section {
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        }
        .file-header {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
        }
        .entities {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }
        .entity {
            background: white;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 12px;
            min-width: 150px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .entity-id {
            font-weight: bold;
            color: #e67e22;
            margin-bottom: 5px;
        }
        .entity-name {
            font-size: 12px;
            color: #666;
        }
        .relationships {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            border: 2px solid #6c5ce7;
        }
        .relationship-title {
            font-size: 18px;
            font-weight: bold;
            color: #6c5ce7;
            margin-bottom: 15px;
        }
        .relationship-group {
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .relationship-type {
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 10px;
        }
        .relationship-item {
            margin: 8px 0;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 5px;
            font-size: 14px;
        }
        .arrow {
            color: #00b894;
            font-weight: bold;
        }
        .credit-amount {
            color: #00b894;
            font-weight: bold;
        }
        .file-prime-brokers { border-color: #e74c3c; }
        .file-customers { border-color: #3498db; }
        .file-sessions { border-color: #00b894; }
        .file-credit { border-color: #f39c12; }
    </style>
</head>
<body>
    <div class="container">
        <!-- Prime Brokers File -->
        <div class="file-section file-prime-brokers">
            <div class="file-header">📁 prime_brokers.yaml</div>
            <div class="entities">
                <div class="entity">
                    <div class="entity-id">CPB_1</div>
                    <div class="entity-name">Central Prime Broker One</div>
                                         <div style="color: #e74c3c; font-size: 12px; margin-top: 5px;">is_central_pb: true</div>
                </div>
                                 <div class="entity">
                     <div class="entity-id">PB_A</div>
                     <div class="entity-name">Prime Broker Alpha</div>
                     <div style="color: #666; font-size: 12px; margin-top: 5px;">is_central_pb: false</div>
                 </div>
                                 <div class="entity">
                     <div class="entity-id">PB_B</div>
                     <div class="entity-name">Prime Broker Beta</div>
                     <div style="color: #666; font-size: 12px; margin-top: 5px;">is_central_pb: false</div>
                 </div>
            </div>
        </div>

        <!-- Customers File -->
        <div class="file-section file-customers">
            <div class="file-header">📁 customers.yaml</div>
            <div class="entities">
                <div class="entity">
                    <div class="entity-id">Cust_1</div>
                    <div class="entity-name">Hedge Fund Gamma</div>
                </div>
                <div class="entity">
                    <div class="entity-id">Cust_2</div>
                    <div class="entity-name">Asset Manager Delta</div>
                </div>
            </div>
        </div>

        <!-- Sessions File -->
        <div class="file-section file-sessions">
            <div class="file-header">📁 sessions.yaml</div>
            <div class="entities">
                <div class="entity">
                    <div class="entity-id">FIXS_C1_PBA_001</div>
                    <div class="entity-name">customer_id: Cust_1<br>pb_id: PB_A<br>protocol: FIX 4.2</div>
                </div>
                <div class="entity">
                    <div class="entity-id">FIXS_C1_PBB_001</div>
                    <div class="entity-name">customer_id: Cust_1<br>pb_id: PB_B<br>protocol: FIX 4.4</div>
                </div>
                <div class="entity">
                    <div class="entity-id">FIXS_C2_PBA_001</div>
                    <div class="entity-name">customer_id: Cust_2<br>pb_id: PB_A<br>protocol: FIX 4.2</div>
                </div>
            </div>
        </div>

        <!-- Credit Data File -->
        <div class="file-section file-credit">
            <div class="file-header">📁 credit_data.yaml (Updated by 3rd Party Vendor)</div>
            <div style="display: flex; gap: 30px;">
                                 <div style="flex: 1;">
                     <h4 style="color: #f39c12; margin-bottom: 10px;">customer_pb_limits:</h4>
                    <div class="entity">
                        <div style="font-size: 12px;">Cust_1 → PB_A: <span class="credit-amount">$1,000,000</span></div>
                        <div style="font-size: 12px;">Cust_1 → PB_B: <span class="credit-amount">$500,000</span></div>
                        <div style="font-size: 12px;">Cust_2 → PB_A: <span class="credit-amount">$2,000,000</span></div>
                    </div>
                </div>
                                 <div style="flex: 1;">
                     <h4 style="color: #f39c12; margin-bottom: 10px;">pb_to_central_pb_limits:</h4>
                    <div class="entity">
                        <div style="font-size: 12px;">PB_A → CPB_1: <span class="credit-amount">$5,000,000</span></div>
                        <div style="font-size: 12px;">PB_B → CPB_1: <span class="credit-amount">$3,000,000</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Relationships Section -->
        <div class="relationships">
            <div class="relationship-title">🔗 Key Relationships & Data Flow</div>
            
            <div class="relationship-group">
                <div class="relationship-type">1. Customer Session Ownership</div>
                <div class="relationship-item">Cust_1 <span class="arrow">owns</span> FIXS_C1_PBA_001, FIXS_C1_PBB_001</div>
                <div class="relationship-item">Cust_2 <span class="arrow">owns</span> FIXS_C2_PBA_001</div>
            </div>

            <div class="relationship-group">
                <div class="relationship-type">2. Session-to-Prime Broker Mapping</div>
                <div class="relationship-item">FIXS_C1_PBA_001 <span class="arrow">routes to</span> PB_A</div>
                <div class="relationship-item">FIXS_C1_PBB_001 <span class="arrow">routes to</span> PB_B</div>
                <div class="relationship-item">FIXS_C2_PBA_001 <span class="arrow">routes to</span> PB_A</div>
            </div>

            <div class="relationship-group">
                <div class="relationship-type">3. Credit Limit Hierarchy</div>
                <div class="relationship-item">Customer <span class="arrow">has credit limit with</span> Prime Broker</div>
                <div class="relationship-item">Prime Broker <span class="arrow">has credit line with</span> Central Prime Broker</div>
                <div class="relationship-item">Central Prime Broker <span class="arrow">provides</span> venue access</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Display the schema diagram
st.components.v1.html(schema_diagram, height=1600)

# --- Prime Brokers Configuration ---
st.header("1. Prime Brokers (`prime_brokers.yaml`)")
st.markdown("""
Defines all prime brokers and identifies the central prime broker. The central PB requirement ensures 
clear venue connectivity and simplifies credit management during client onboarding.

**id:** Unique identifier for the prime broker  
**name:** Full name of the prime broker  
**is_central_pb:** Boolean flag, exactly one PB should be true
""")
with st.expander("View `prime_brokers.yaml` content"):
    st.code(prime_brokers_data_str, language='yaml')

# --- Customers Configuration ---
st.header("2. Customers (`customers.yaml`)")
st.markdown("""
Customer entities for trading activity. Minimal schema keeps essential identifiers for trade routing 
while allowing detailed customer data to be managed in dedicated CRM systems.

**id:** Unique identifier for the customer  
**name:** Customer entity name
""")
with st.expander("View `customers.yaml` content"):
    st.code(customers_data_str, language='yaml')

# --- Sessions Configuration ---
st.header("3. Sessions (`sessions.yaml`)")
st.markdown("""
Trading sessions map customers to prime brokers. 
attribution and troubleshooting during live trading operations.

**session_id:** Unique session identifier (e.g., FIX session ID)  
**customer_id:** Links to customer ID  
**pb_id:** Links to prime broker ID  
**protocol:** Communication protocol (e.g., "FIX 4.2")
""")
with st.expander("View `sessions.yaml` content"):
    st.code(sessions_data_str, language='yaml')

# --- Credit Data Configuration ---
st.header("4. Credit Data (`credit_data.yaml`)")
st.markdown("""
Credit limit information updated by third-party vendors. Separated from static config due to frequent updates 
and different security requirements. 


""")

st.subheader("4.1 `customer_pb_limits`")
st.markdown("""
Direct credit limits between customers and prime brokers. Essential for trade authorization and 
preventing customer trading disruptions.

**customer_id:** Links to customer ID  
**pb_id:** Links to prime broker ID  
**limit_amount:** Maximum credit amount  
**currency:** Limit currency (e.g., "USD")  
**last_updated:** When this limit was last updated
""")

st.subheader("4.2 `pb_to_central_pb_limits`")
st.markdown("""
Credit lines between non-central prime brokers and the central prime broker. Must be monitored to ensure 
prime brokers don't over-extend credit to their customers beyond their own capacity.


""")
with st.expander("View `credit_data.yaml` content"):
    st.code(credit_data_str, language='yaml')

# --- Interactive Query Examples (at the bottom) ---
st.header("Interactive Python Query Examples")
st.markdown("""
Test how the configuration data works with these Python examples.
Select inputs, click execute, and see both results and code.
""")

# Use the already loaded YAML data for interactive queries
prime_brokers = prime_brokers_data
customers = customers_data
sessions = sessions_data
# Use modified credit data from session state if available
credit_data_for_queries = st.session_state.get('modified_credit_data', credit_data)

# Initialize session state for credit data if not exists
if 'modified_credit_data' not in st.session_state:
    st.session_state.modified_credit_data = credit_data.copy() if credit_data else {}

# Check if all files loaded successfully
if not all([prime_brokers, customers, sessions, credit_data_for_queries]):
    st.error("Some configuration files failed to load. Please check that all YAML files are present and valid.")
    st.stop()

# Panel 1: Session to PB Lookup
with st.expander("1 - Session to Prime Broker Lookup", expanded=False):
    st.markdown("Find which prime broker handles any trading session")
    
    # Input controls
    session_ids = [session['session_id'] for session in sessions]
    selected_session = st.selectbox("Select a session:", session_ids, key="session_lookup")
    
    # Execute button
    if st.button("Execute Lookup", key="btn_session"):
        if selected_session:
            # Execute the lookup
            result_pb = None
            for session in sessions:
                if session['session_id'] == selected_session:
                    result_pb = session['pb_id']
                    break
            
            # Show results
            st.markdown("**Results:**")
            if result_pb:
                st.success(f"Session `{selected_session}` routes to Prime Broker `{result_pb}`")
                
                # Find PB details
                pb_name = None
                for pb in prime_brokers:
                    if pb['id'] == result_pb:
                        pb_name = pb['name']
                        break
                if pb_name:
                    st.info(f"Prime Broker Name: {pb_name}")
            else:
                st.error("Session not found")
    
    # Show code snippet
    st.markdown("**Python Code:**")
    st.code("""
def get_pb_for_session(session_id, sessions_data):
    \"\"\"Find the Prime Broker ID for a given session\"\"\"
    for session in sessions_data:
        if session['session_id'] == session_id:
            return session['pb_id']
    return None

# Usage example
pb_id = get_pb_for_session('FIXS_C1_PBA_001', sessions)
print(f"Prime Broker: {pb_id}")
    """, language='python')

# Panel 2: Customer Credit Limits
with st.expander("2 - Customer Credit Limits Query", expanded=False):
    st.markdown("Check all credit limits for a customer across different prime brokers")
    
    # Input controls
    customer_ids = [customer['id'] for customer in customers]
    selected_customer = st.selectbox("Select a customer:", customer_ids, key="credit_lookup")
    
    # Execute button
    if st.button("Execute Query", key="btn_credit"):
        if selected_customer:
            # Execute the lookup
            customer_limits = []
            for limit in credit_data_for_queries['customer_pb_limits']:
                if limit['customer_id'] == selected_customer:
                    customer_limits.append({
                        'pb_id': limit['pb_id'],
                        'amount': limit['limit_amount'],
                        'currency': limit['currency'],
                        'last_updated': limit['last_updated']
                    })
            
            # Show results
            st.markdown("**Results:**")
            if customer_limits:
                total_credit = sum(limit['amount'] for limit in customer_limits)
                st.success(f"Found {len(customer_limits)} credit limit(s)")
                
                for limit in customer_limits:
                    # Get PB name
                    pb_name = None
                    for pb in prime_brokers:
                        if pb['id'] == limit['pb_id']:
                            pb_name = pb['name']
                            break
                    
                    st.write(f"• **{limit['pb_id']}** ({pb_name}): {limit['currency']} {limit['amount']:,}")
                    st.caption(f"  Last updated: {limit['last_updated']}")
                
                st.info(f"**Total Credit Available:** ${total_credit:,}")
            else:
                st.warning("No credit limits found for this customer")
    
    # Show code snippet
    st.markdown("**Python Code:**")
    st.code("""
def get_customer_credit_limits(customer_id, credit_data):
    \"\"\"Get all credit limits for a customer\"\"\"
    limits = []
    for limit in credit_data['customer_pb_limits']:
        if limit['customer_id'] == customer_id:
            limits.append({
                'pb_id': limit['pb_id'],
                'amount': limit['limit_amount'],
                'currency': limit['currency'],
                'last_updated': limit['last_updated']
            })
    return limits

# Usage example
limits = get_customer_credit_limits('Cust_1', credit_data)
total = sum(limit['amount'] for limit in limits)
print(f"Total credit: ${total:,}")
    """, language='python')

# Panel 3: Credit Exposure
with st.expander("3 - Credit Exposure Check", expanded=False):
    st.markdown("Ensure PBs don't exceed their credit lines")
    st.markdown("""
    Critical risk management check. If a prime broker issues more credit to customers than they have available from the central prime broker, it creates exposure that could result in trading failures.
    
    Risk scenarios prevented: Prime broker over-extending credit beyond their limit. High utilization warnings (>90%). Monitoring total exposure per prime broker. Early warning for credit line management.
    """)
    
    # Live Credit Editor - modify limits and see real-time impact
    st.markdown("---")
    st.markdown("**Live Credit Editor** - Modify limits and see real-time impact on calculations below")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Customer → PB Limits:**")
        if st.session_state.modified_credit_data and 'customer_pb_limits' in st.session_state.modified_credit_data:
            # Create dropdown options for customer-PB relationships
            customer_pb_options = []
            for limit in st.session_state.modified_credit_data['customer_pb_limits']:
                option_text = f"{limit['customer_id']} → {limit['pb_id']}"
                customer_pb_options.append(option_text)
            
            if customer_pb_options:
                selected_customer_pb = st.selectbox(
                    "Select Customer → PB relationship:",
                    customer_pb_options,
                    key="customer_pb_selector"
                )
                
                # Find the selected limit
                selected_index = customer_pb_options.index(selected_customer_pb)
                selected_limit = st.session_state.modified_credit_data['customer_pb_limits'][selected_index]
                
                # Show current limit and allow editing
                st.write(f"**Current Limit:** ${selected_limit['limit_amount']:,}")
                
                new_amount = st.number_input(
                    "New Credit Limit ($):",
                    min_value=0,
                    value=selected_limit['limit_amount'],
                    step=100000,
                    key="customer_limit_editor",
                    format="%d"
                )
                
                if new_amount != selected_limit['limit_amount']:
                    st.session_state.modified_credit_data['customer_pb_limits'][selected_index]['limit_amount'] = new_amount
                    st.success(f"Updated {selected_customer_pb} to ${new_amount:,}")
    
    with col2:
        st.markdown("**PB → Central PB Lines:**")
        if st.session_state.modified_credit_data and 'pb_to_central_pb_limits' in st.session_state.modified_credit_data:
            # Create dropdown options for PB-Central PB relationships
            pb_central_options = []
            for limit in st.session_state.modified_credit_data['pb_to_central_pb_limits']:
                option_text = f"{limit['non_central_pb_id']} → {limit['central_pb_id']}"
                pb_central_options.append(option_text)
            
            if pb_central_options:
                selected_pb_central = st.selectbox(
                    "Select PB → Central PB relationship:",
                    pb_central_options,
                    key="pb_central_selector"
                )
                
                # Find the selected limit
                selected_index = pb_central_options.index(selected_pb_central)
                selected_limit = st.session_state.modified_credit_data['pb_to_central_pb_limits'][selected_index]
                
                # Show current limit and allow editing
                st.write(f"**Current Limit:** ${selected_limit['limit_amount']:,}")
                
                new_amount = st.number_input(
                    "New Credit Line ($):",
                    min_value=0,
                    value=selected_limit['limit_amount'],
                    step=500000,
                    key="pb_limit_editor",
                    format="%d"
                )
                
                if new_amount != selected_limit['limit_amount']:
                    st.session_state.modified_credit_data['pb_to_central_pb_limits'][selected_index]['limit_amount'] = new_amount
                    st.success(f"Updated {selected_pb_central} to ${new_amount:,}")
    

    if st.button("Save", help="In production, this would save to credit_data.yaml"):
        st.info("Would update credit_data.yaml")

    st.markdown("---")
    st.markdown("**Credit Exposure Calculator** - Select a prime broker to validate their credit exposure")
    
    # Input controls (non-central PBs only)
    non_central_pbs = [pb['id'] for pb in prime_brokers if not pb.get('is_central_pb', False)]
    selected_pb = st.selectbox("Select a Prime Broker:", non_central_pbs, key="validation_lookup")
    
    # Execute button
    if st.button("Execute Validation", key="btn_validation"):
        if selected_pb:
            # Calculate total issued to customers
            total_issued = 0
            customer_count = 0
            for limit in credit_data_for_queries['customer_pb_limits']:
                if limit['pb_id'] == selected_pb:
                    total_issued += limit['limit_amount']
                    customer_count += 1
            
            # Get PB's credit line with central PB
            pb_credit_line = 0
            for limit in credit_data_for_queries['pb_to_central_pb_limits']:
                if limit['non_central_pb_id'] == selected_pb:
                    pb_credit_line = limit['limit_amount']
                    break
            
            # Calculate metrics
            is_valid = total_issued <= pb_credit_line
            utilization = (total_issued / pb_credit_line * 100) if pb_credit_line > 0 else 0
            available_credit = pb_credit_line - total_issued
            
            # Show results
            st.markdown("**Results:**")
            if is_valid:
                st.success("Credit exposure is within limits")
            else:
                st.error("Credit exposure EXCEEDS central PB credit line")
            
            # Get PB name
            pb_name = None
            for pb in prime_brokers:
                if pb['id'] == selected_pb:
                    pb_name = pb['name']
                    break
            
            st.write(f"**Prime Broker:** {selected_pb} ({pb_name})")
            st.write(f"**Customers served:** {customer_count}")
            st.write(f"**Total issued to customers:** ${total_issued:,}")
            st.write(f"**Credit line from central PB:** ${pb_credit_line:,}")
            st.write(f"**Available credit:** ${available_credit:,}")
            
            # Progress bar for utilization
            st.write(f"**Utilization:** {utilization:.1f}%")
            st.progress(min(utilization / 100, 1.0))
    
    # Show code snippet
    st.markdown("**Python Code:**")
    st.code("""
def validate_pb_credit_exposure(pb_id, credit_data):
    \"\"\"Validate PB credit exposure vs central PB limit\"\"\"
    # Get total credit issued to customers
    total_issued = 0
    for limit in credit_data['customer_pb_limits']:
        if limit['pb_id'] == pb_id:
            total_issued += limit['limit_amount']
    
    # Get PB's credit line with central PB
    pb_credit_line = 0
    for limit in credit_data['pb_to_central_pb_limits']:
        if limit['non_central_pb_id'] == pb_id:
            pb_credit_line = limit['limit_amount']
            break
    
    return {
        'total_issued': total_issued,
        'credit_line': pb_credit_line,
        'is_valid': total_issued <= pb_credit_line,
        'utilization': (total_issued / pb_credit_line * 100) 
                      if pb_credit_line > 0 else 0
    }

# Usage example
result = validate_pb_credit_exposure('PB_A', credit_data)
print(f"Valid: {result['is_valid']}")
print(f"Utilization: {result['utilization']:.1f}%")
    """, language='python')



# --- Error Handling & Edge Cases ---
st.header("Error Handling & Edge Cases")
st.markdown("""
Key validation checks needed when parsing and validating configuration files.
""")

with st.expander("1 - Basic File Validation", expanded=False):
    st.markdown("Load and validate YAML files safely")
    st.markdown("""
    YAML files can have syntax errors, be missing, or contain unexpected data. Proper validation prevents crashes and provides clear error messages.
    
    **Key checks:**  
    • File exists and is readable  
    • Valid YAML syntax  
    • Non-empty content  
    • Required fields present
    """)
    st.code("""
import yaml

def load_config_file(file_path):
    \"\"\"Load YAML file with basic error handling\"\"\"
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            if not data:
                raise ValueError(f"Empty file: {file_path}")
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"YAML error in {file_path}: {e}")
        return None

def check_required_fields(item, required_fields, item_type):
    \"\"\"Check if required fields are present\"\"\"
    missing = [field for field in required_fields if field not in item]
    if missing:
        print(f"Missing fields in {item_type}: {missing}")
        return False
    return True

# Example usage
prime_brokers = load_config_file('prime_brokers.yaml')
if prime_brokers:
    for pb in prime_brokers:
        check_required_fields(pb, ['id', 'name', 'is_central_pb'], 'prime broker')
    """, language='python')

with st.expander("2 - Business Rule Checks", expanded=False):
    st.markdown("Validate critical business rules")
    st.markdown("""
    Beyond syntax validation, the configuration must satisfy business logic rules. Violating these could lead to trading failures or compliance issues.
    
    **Critical rules:**  
    • Exactly one central prime broker (required for venue access)  
    • No duplicate IDs (prevents ambiguous references)  
    • All references point to valid entities  
    • Referential integrity across files
    """)
    st.code("""
def validate_configuration(prime_brokers, customers, sessions, credit_data):
    \"\"\"Run essential business rule validations\"\"\"
    errors = []
    
    # 1. Must have exactly one central Prime Broker
    central_pbs = [pb for pb in prime_brokers if pb.get('is_central_pb', False)]
    if len(central_pbs) != 1:
        errors.append(f"Need exactly 1 central PB, found {len(central_pbs)}")
    
    # 2. Check for duplicate IDs
    pb_ids = [pb['id'] for pb in prime_brokers]
    if len(pb_ids) != len(set(pb_ids)):
        errors.append("Duplicate Prime Broker IDs")
    
    session_ids = [s['session_id'] for s in sessions]
    if len(session_ids) != len(set(session_ids)):
        errors.append("Duplicate Session IDs")
    
    # 3. Sessions must reference valid customers and PBs
    valid_customers = {c['id'] for c in customers}
    valid_pbs = {pb['id'] for pb in prime_brokers}
    
    for session in sessions:
        if session['customer_id'] not in valid_customers:
            errors.append(f"Session {session['session_id']} has invalid customer")
        if session['pb_id'] not in valid_pbs:
            errors.append(f"Session {session['session_id']} has invalid PB")
    
    # 4. Credit limits must reference valid entities
    for limit in credit_data.get('customer_pb_limits', []):
        if limit['customer_id'] not in valid_customers:
            errors.append(f"Credit limit has invalid customer: {limit['customer_id']}")
        if limit['pb_id'] not in valid_pbs:
            errors.append(f"Credit limit has invalid PB: {limit['pb_id']}")
    
    return errors

# Usage
errors = validate_configuration(prime_brokers, customers, sessions, credit_data)
if errors:
    print("Validation errors:", errors)
else:
    print("Configuration is valid")
    """, language='python')

with st.expander("3 - Credit Exposure Check", expanded=False):
    st.markdown("**Ensure PBs don't exceed their credit lines**")
    st.markdown("""
    Critical risk management check. If a prime broker issues more credit 
    to customers than they have available from the central prime broker, 
    it creates exposure that could result in trading failures.
    
    **Risk scenarios prevented**:
    - Prime broker over-extending credit beyond their limit
    - High utilization warnings (>90%) 
    - Monitoring total exposure per prime broker
    - Early warning for credit line management
    """)
    st.code("""
def check_credit_exposure(prime_brokers, credit_data):
    \"\"\"Check if any PB exceeds their central PB credit line\"\"\"
    warnings = []
    
    # Get non-central PBs
    non_central_pbs = [pb['id'] for pb in prime_brokers if not pb.get('is_central_pb', False)]
    
    for pb_id in non_central_pbs:
        # Calculate total credit issued to customers
        total_issued = 0
        for limit in credit_data.get('customer_pb_limits', []):
            if limit['pb_id'] == pb_id:
                total_issued += limit['limit_amount']
        
        # Get PB's credit line with central PB
        pb_credit_line = 0
        for limit in credit_data.get('pb_to_central_pb_limits', []):
            if limit['non_central_pb_id'] == pb_id:
                pb_credit_line = limit['limit_amount']
                break
        
        # Check for over-exposure
        if total_issued > pb_credit_line:
            warnings.append(f"PB {pb_id}: issued ${total_issued:,} but only has ${pb_credit_line:,} credit line")
        
        # Warn if close to limit
        utilization = (total_issued / pb_credit_line * 100) if pb_credit_line > 0 else 0
        if utilization > 90:
            warnings.append(f"PB {pb_id}: {utilization:.1f}% credit utilization")
    
    return warnings

# Usage
warnings = check_credit_exposure(prime_brokers, credit_data)
for warning in warnings:
    print(f"WARNING: {warning}")
    """, language='python')

with st.expander("4 - Common Edge Cases", expanded=False):
    st.markdown("Handle typical edge cases")
    st.markdown("""
    Real-world trading systems encounter various edge cases that aren't necessarily errors but require monitoring. These can impact operations and should be flagged.
    
    **Common scenarios:**  
    • Customers with multiple sessions (legitimate but worth tracking)  
    • Customers with sessions but no credit limits (configuration gap)  
    • Stale credit data (outdated information)  
    • Invalid timestamps (data quality issues)
    """)
    st.code("""
def check_edge_cases(customers, sessions, credit_data):
    \"\"\"Check for common edge cases\"\"\"
    issues = []
    
    # 1. Customers with multiple sessions (allowed but worth noting)
    customer_sessions = {}
    for session in sessions:
        customer_id = session['customer_id']
        if customer_id not in customer_sessions:
            customer_sessions[customer_id] = []
        customer_sessions[customer_id].append(session['session_id'])
    
    for customer_id, session_list in customer_sessions.items():
        if len(session_list) > 1:
            issues.append(f"Customer {customer_id} has {len(session_list)} sessions")
    
    # 2. Customers without credit limits
    customers_with_sessions = {s['customer_id'] for s in sessions}
    customers_with_credit = {l['customer_id'] for l in credit_data.get('customer_pb_limits', [])}
    
    customers_no_credit = customers_with_sessions - customers_with_credit
    for customer_id in customers_no_credit:
        issues.append(f"Customer {customer_id} has sessions but no credit limits")
    
    # 3. Check for stale data (older than 24 hours)
    from datetime import datetime, timedelta
    stale_threshold = datetime.now() - timedelta(hours=24)
    
    for limit in credit_data.get('customer_pb_limits', []):
        if 'last_updated' in limit:
            try:
                last_updated = datetime.fromisoformat(limit['last_updated'].replace('Z', '+00:00'))
                if last_updated < stale_threshold:
                    issues.append(f"Stale credit data for {limit['customer_id']}->{limit['pb_id']}")
            except ValueError:
                issues.append(f"Invalid timestamp: {limit['last_updated']}")
    
    return issues

# Usage
issues = check_edge_cases(customers, sessions, credit_data)
for issue in issues:
    print(f"NOTICE: {issue}")
    """, language='python')



# --- Future Extensibility ---
st.header("Future Extensibility")
st.markdown("""
How to structure this schema for future requirements like dynamic credit updates and per-instrument limits.
""")

with st.expander("Conditional Credit Rules Engine", expanded=False):
    st.markdown("Vendor-submitted expressive rules for dynamic credit adjustments")
    st.markdown("""
    Instead of static credit limits, vendors can submit conditional rules that automatically adjust credit based on real-time market conditions, customer behavior, and risk metrics.
    
    **Expressive rule language:** Vendors define complex conditions using JSON-based expressions. Rules can reference market data, customer trading patterns, time of day, volatility metrics. Multiple conditions can be combined with logical operators (AND, OR, NOT).
    
    **Real-time evaluation:** Rules are evaluated continuously against live market feeds. Credit adjustments happen automatically when conditions are met. All changes are logged with full audit trails showing which rule triggered the change.
    
    **Vendor competition:** Multiple vendors can submit competing rules for the same customer. System selects the most conservative (lowest risk) limit when rules conflict. Vendors are scored based on prediction accuracy and risk management performance.
    """)
    
    st.code("""
# Vendor-submitted conditional credit rules
vendor_credit_rules:
  - rule_id: "alpha_low_volatility"
    vendor_id: "CreditVendor_Alpha"
    customer_id: "Cust_1"
    pb_id: "PB_A"
    
    condition: "market_volatility < 0.15"
    action: "increase_limit"
    adjustment: 1.2
    max_limit: 1500000
    
    expires_at: "2024-01-22T09:00:00Z"
    vendor_confidence: 0.85
        
  - rule_id: "beta_trading_hours"
    vendor_id: "CreditVendor_Beta"
    customer_id: "Cust_1"
    pb_id: "PB_A"
    
    condition: "trading_hours AND customer_pnl_positive"
    action: "increase_limit"
    adjustment: 1.15
    max_limit: 1300000
    
    expires_at: "2024-01-22T09:00:00Z"
    vendor_confidence: 0.92

# Rule evaluation results
current_evaluation:
  timestamp: "2024-01-15T14:30:00Z"
  customer_id: "Cust_1"
  pb_id: "PB_A"
  base_limit: 1000000
  
  rule_results:
    - rule_id: "alpha_low_volatility"
      condition_met: true
      suggested_limit: 1200000
      
    - rule_id: "beta_trading_hours"  
      condition_met: true
      suggested_limit: 1150000
      
  final_decision:
    selected_limit: 1150000  # Most conservative
    selected_rule: "beta_trading_hours"
    reason: "lower_risk_option"
    """, language='yaml')

with st.expander("Dynamic Credit Updates via API", expanded=False):
    st.markdown("Real-time credit adjustments through API endpoints")
    st.markdown("""
    Move beyond static YAML files to enable real-time credit updates through RESTful APIs. Vendors and risk systems can push credit changes instantly.
    
    **Real-time API endpoints:** POST /api/credit/update for immediate limit changes. GET /api/credit/status for current limits and utilization. WebSocket streams for live credit notifications to trading systems.
    
    **Event-driven updates:** Credit changes trigger immediate notifications to all connected trading systems. Message queues ensure reliable delivery even during system outages. Automatic rollback capabilities if updates fail validation.
    
    **Audit and versioning:** Every credit change creates an immutable audit record. Version numbers track configuration evolution. Ability to query historical credit states for compliance reporting.
    """)
    
    st.code("""
# API endpoint examples for dynamic credit updates

POST /api/v1/credit/update
{
  "customer_id": "Cust_1",
  "pb_id": "PB_A", 
  "new_limit": 1500000,
  "currency": "USD",
  "reason": "market_volatility_decrease",
  "expires_at": "2024-01-15T18:00:00Z",
  "updated_by": "risk_system_alpha"
}

Response:
{
  "status": "success",
  "previous_limit": 1000000,
  "new_limit": 1500000,
  "version": 47,
  "effective_at": "2024-01-15T14:30:15Z",
  "audit_id": "aud_789123"
}

GET /api/v1/credit/customer/Cust_1/status
{
  "customer_id": "Cust_1",
  "total_available_credit": 2650000,
  "total_used_credit": 850000,
  "limits_by_pb": [
    {
      "pb_id": "PB_A",
      "limit": 1500000,
      "used": 450000,
      "available": 1050000,
      "last_updated": "2024-01-15T14:30:15Z"
    },
    {
      "pb_id": "PB_B", 
      "limit": 1150000,
      "used": 400000,
      "available": 750000,
      "last_updated": "2024-01-15T12:15:30Z"
    }
  ],
  "version": 47
}

# WebSocket stream for real-time notifications
ws://api/v1/credit/stream
{
  "event_type": "credit_limit_updated",
  "customer_id": "Cust_1",
  "pb_id": "PB_A",
  "old_limit": 1000000,
  "new_limit": 1500000,
  "timestamp": "2024-01-15T14:30:15Z",
  "reason": "market_volatility_decrease",
  "version": 47
}
    """, language='json')

with st.expander("Per-Instrument Credit Limits", expanded=False):
    st.markdown("Granular credit control at the instrument level")
    st.markdown("""
    Current schema has aggregate credit limits per customer-PB relationship. For per-instrument limits:
    
    **Instrument hierarchy:** Define instrument categories (FX majors, minors, exotics). Set limits at category and individual instrument levels. Inherit limits from parent categories with overrides.
    
    **Multi-dimensional limits:** Credit limits by instrument, tenor, notional size. Time-based limits (daily, weekly, monthly). Concentration limits to prevent over-exposure to single instruments.
    
    **Real-time monitoring:** Track utilization per instrument in real-time. Alert when approaching instrument-specific limits. Automatic rejection of trades exceeding limits.
    """)
    
    st.code("""
# Extended structure for per-instrument limits
instrument_credit_limits:
  - customer_id: "Cust_1"
    pb_id: "PB_A"
    instrument_limits:
      categories:
        - category: "fx_majors"
          instruments: ["EURUSD", "GBPUSD", "USDJPY"]
          limit_amount: 500000
          currency: "USD"
        - category: "fx_minors" 
          instruments: ["EURGBP", "EURJPY", "GBPJPY"]
          limit_amount: 200000
          currency: "USD"
      
      specific_overrides:
        - instrument: "EURUSD"
          limit_amount: 300000  # Override category limit
          max_tenor_days: 30
          max_notional_per_trade: 50000
          
      concentration_limits:
        - rule: "max_single_instrument"
          percentage_of_total: 0.4  # Max 40% in any single instrument
        - rule: "max_exotic_exposure"
          category: "fx_exotics"
          percentage_of_total: 0.1  # Max 10% in exotics
          
  current_utilization:
    - customer_id: "Cust_1"
      pb_id: "PB_A"
      instrument: "EURUSD"
      used_amount: 150000
      available_amount: 150000
      last_updated: "2024-01-15T14:30:00Z"
    """, language='yaml')

st.markdown("""
#### Key extensibility principles:

**Vendor ecosystem:** Enable multiple credit vendors to compete by submitting sophisticated rules. Create marketplace dynamics where vendors are rewarded for accurate risk assessment. Allow customers to choose preferred vendor strategies or let system auto-select best performers.

**Expressive rule language:** Support complex conditional logic with market data, customer metrics, and ML predictions. Enable vendors to encode their proprietary risk models as executable rules. Provide sandbox environment for vendors to test rules before production deployment.

**Real-time adaptation:** Continuously evaluate rules against live market conditions. Automatic credit adjustments without manual intervention. Immediate response to changing market dynamics and customer behavior patterns.

**Risk management:** Always select most conservative limit when multiple vendors suggest different amounts. Implement circuit breakers and maximum adjustment limits. Comprehensive audit trails showing which vendor rule triggered each credit change.

**Performance tracking:** Score vendors based on prediction accuracy and risk-adjusted returns. Track rule performance over different market conditions. Enable data-driven vendor selection and rule optimization.
""")



# Trade Flow Diagram - moved here from the end
st.header("Trade Rejection Flow")
st.markdown("""
Visual representation of how a trade gets rejected when a customer exceeds their credit limit with their Prime Broker.
""")

# Create trade flow diagram
trade_flow_diagram = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { 
            margin: 0; 
            padding: 20px; 
            background-color: white; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: #333;
        }
        .flow-container { 
            display: flex; 
            flex-direction: column; 
            gap: 20px; 
            max-width: 1200px; 
            margin: 0 auto;
        }
        .flow-row {
            display: flex;
            align-items: center;
            gap: 15px;
            justify-content: space-between;
        }
        .flow-row.reverse {
            flex-direction: row-reverse;
        }
        .flow-step {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            flex: 1;
            max-width: 280px;
        }
        .step-number {
            background: #007bff;
            color: white;
            border-radius: 50%;
            width: 35px;
            height: 35px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
            font-size: 14px;
        }
        .step-content {
            flex: 1;
        }
        .step-title {
            font-weight: bold;
            margin-bottom: 3px;
            color: #2c3e50;
            font-size: 14px;
        }
        .step-description {
            font-size: 11px;
            color: #666;
            margin-bottom: 5px;
        }
        .step-data {
            background: #f8f9fa;
            padding: 6px;
            border-radius: 4px;
            font-family: monospace;
            font-size: 10px;
            line-height: 1.2;
        }
        .arrow-horizontal {
            font-size: 20px;
            color: #007bff;
            flex-shrink: 0;
        }
        .arrow-down {
            font-size: 20px;
            color: #007bff;
            margin: 10px 0;
        }
        .arrow-down-right {
            text-align: right;
            font-size: 20px;
            color: #007bff;
            margin: 10px 0;
            padding-right: 80px;
        }
        .arrow-down-left {
            text-align: left;
            font-size: 20px;
            color: #007bff;
            margin: 10px 0;
            padding-left: 80px;
        }
        .success { background: linear-gradient(135deg, #d4edda, #c3e6cb); }
        .processing { background: linear-gradient(135deg, #fff3cd, #ffeaa7); }
        .error { background: linear-gradient(135deg, #f8d7da, #f5c6cb); }
        .system { background: linear-gradient(135deg, #d1ecf1, #bee5eb); }
        .communication { background: linear-gradient(135deg, #e2e3e5, #d6d8db); }
        
        .participants {
            display: flex;
            justify-content: space-around;
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .participant {
            text-align: center;
            padding: 15px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            min-width: 120px;
        }
        .participant-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .participant-role {
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="flow-container">
        <!-- Participants -->
       

        <!-- Row 1: Left to Right (Steps 1-3) -->
        <div class="flow-row">
            <div class="flow-step success">
                <div class="step-number">1</div>
                <div class="step-content">
                    <div class="step-title">Customer Submits Trade</div>
                    <div class="step-description">Customer sends trade order via FIX session</div>
                    <div class="step-data">
                        Session: FIXS_C1_PBA_001<br>
                        Customer: Cust_1<br>
                        Instrument: EURUSD<br>
                        Notional: $600,000
                    </div>
                </div>
            </div>
            
            <div class="arrow-horizontal">→</div>
            
            <div class="flow-step processing">
                <div class="step-number">2</div>
                <div class="step-content">
                    <div class="step-title">OneChronos Receives Trade</div>
                    <div class="step-description">Platform receives FIX message and begins validation</div>
                    <div class="step-data">
                        Trade ID: TRD_789456<br>
                        Lookup: Cust_1 → PB_A<br>
                        Timestamp: 14:30:15Z
                    </div>
                </div>
            </div>
            
            <div class="arrow-horizontal">→</div>
            
            <div class="flow-step system">
                <div class="step-number">3</div>
                <div class="step-content">
                    <div class="step-title">Credit Limit Lookup</div>
                    <div class="step-description">Check customer's credit limit with PB</div>
                    <div class="step-data">
                        Query: Cust_1 → PB_A<br>
                        Limit: $1,000,000 USD<br>
                        Updated: 08:00:00Z
                    </div>
                </div>
            </div>
        </div>

        <!-- Down Arrow - positioned at right to follow flow -->
        <div class="arrow-down-right">↓</div>

        <!-- Row 2: Right to Left (Steps 4-6) -->
        <div class="flow-row reverse">
            <div class="flow-step system">
                <div class="step-number">4</div>
                <div class="step-content">
                    <div class="step-title">Current Exposure Calculation</div>
                    <div class="step-description">Calculate current exposure across all positions</div>
                    <div class="step-data">
                        GBPUSD: $250,000<br>
                        USDJPY: $200,000<br>
                        Total: $450,000<br>
                        Available: $550,000
                    </div>
                </div>
            </div>
            
            <div class="arrow-horizontal">←</div>
            
            <div class="flow-step error">
                <div class="step-number">5</div>
                <div class="step-content">
                    <div class="step-title">Credit Limit Breach Detected</div>
                    <div class="step-description">New trade would exceed credit limit</div>
                    <div class="step-data">
                        New: $600,000<br>
                        Current: $450,000<br>
                        Total: $1,050,000<br>
                        <strong style="color: #dc3545;">BREACH: $50,000</strong>
                    </div>
                </div>
            </div>
            
            <div class="arrow-horizontal">←</div>
            
            <div class="flow-step error">
                <div class="step-number">6</div>
                <div class="step-content">
                    <div class="step-title">Trade Rejection</div>
                    <div class="step-description">OneChronos rejects trade and sends rejection</div>
                    <div class="step-data">
                        FIX: ExecutionReport<br>
                        ExecType: Rejected (8)<br>
                        Reason: Credit exceeded<br>
                        Available: $550,000
                    </div>
                </div>
            </div>
        </div>

        <!-- Down Arrow - positioned at left to follow flow -->
        <div class="arrow-down-left">↓</div>

        <!-- Row 3: Left to Right (Steps 7-8) -->
        <div class="flow-row">
            <div class="flow-step communication">
                <div class="step-number">7</div>
                <div class="step-content">
                    <div class="step-title">Alert & Notification</div>
                    <div class="step-description">Trigger alerts and begin communication</div>
                    <div class="step-data">
                        • Internal alert to ops team<br>
                        • Customer notification<br>
                        • PB notification<br>
                        • Audit log entry
                    </div>
                </div>
            </div>
            
            <div class="arrow-horizontal">→</div>
            
            <div class="flow-step processing">
                <div class="step-number">8</div>
                <div class="step-content">
                    <div class="step-title">Resolution Process Begins</div>
                    <div class="step-description">Coordinate with customer and PB to resolve</div>
                    <div class="step-data">
                        Options:<br>
                        • Temporary credit increase<br>
                        • Reduce positions<br>
                        • Split trade
                    </div>
                </div>
            </div>
            
            <!-- Empty space to balance the row -->
            <div style="flex: 1; max-width: 280px;"></div>
        </div>
    </div>
</body>
</html>
"""

# Display the trade flow diagram
st.components.v1.html(trade_flow_diagram, height=600)

st.markdown("---")

st.markdown("## Resolution Steps")

with st.expander("1 - Verify Limit Breach", expanded=False):
    st.markdown("Steps to confirm the credit limit that was breached")
    st.markdown("""
    **Immediate verification:** Query current credit configuration to confirm the exact limit that was breached. Check both the configured limit amount and current utilization. Verify the timestamp of the reject against recent credit updates.
    
    **Audit trail verification:** Check database audit trail to confirm the exact credit limit that was active at the time of the rejected trade. This is critical because credit limits may have changed between the trade attempt and the investigation. Query the credit history table with the exact timestamp of the trade rejection.
    
    **Data sources to check:** Current credit_data.yaml or database for the customer-PB limit. Real-time position system for current exposure calculation. Recent trade history to understand what pushed over the limit. Credit limit audit trail for historical limits at trade time.
    
    **Key questions to answer:** What was the exact credit limit at the time of the rejected trade? What is the current utilized amount? What was the trade size that caused the breach? Are there any pending trades that haven't settled yet? Have there been any credit limit changes since the trade attempt?
    """)
    
    st.code("""
# Verification queries to run immediately

# 1. Get current credit limit
SELECT limit_amount, currency, last_updated 
FROM credit_limits 
WHERE customer_id = 'Cust_1' AND pb_id = 'PB_A'
AND effective_from <= NOW() AND (effective_to IS NULL OR effective_to > NOW());

# 2. Get exact credit limit at time of trade (CRITICAL)
SELECT limit_amount, effective_from, effective_to, version
FROM credit_limits_history 
WHERE customer_id = 'Cust_1' AND pb_id = 'PB_A'
AND effective_from <= '2024-01-15T14:30:15Z'  -- exact trade timestamp
AND (effective_to IS NULL OR effective_to > '2024-01-15T14:30:15Z')
ORDER BY effective_from DESC LIMIT 1;

# 3. Calculate current utilization
SELECT SUM(notional_amount) as current_exposure
FROM open_positions 
WHERE customer_id = 'Cust_1' AND pb_id = 'PB_A';

# 4. Get recent trade that caused breach
SELECT trade_id, instrument, notional_amount, timestamp, reject_reason
FROM trade_log 
WHERE customer_id = 'Cust_1' AND pb_id = 'PB_A' 
AND status = 'REJECTED' 
ORDER BY timestamp DESC LIMIT 1;

# 5. Check for pending settlements
SELECT SUM(notional_amount) as pending_amount
FROM pending_settlements 
WHERE customer_id = 'Cust_1' AND pb_id = 'PB_A';

# 6. Check for any credit changes since trade attempt
SELECT old_limit, new_limit, change_timestamp, changed_by, reason
FROM credit_audit_log
WHERE customer_id = 'Cust_1' AND pb_id = 'PB_A'
AND change_timestamp >= '2024-01-15T14:30:15Z'  -- since trade time
ORDER BY change_timestamp ASC;
    """, language='sql')

with st.expander("2 - Customer Communication", expanded=False):
    st.markdown("Immediate communication steps with the customer")
    st.markdown("""
    **Immediate notification:** Contact customer within 5 minutes of reject via phone and email. Provide specific details: rejected trade size, current limit, current utilization. Explain exactly how much additional credit is needed.
    
    **Information to provide:** Current credit limit amount and utilization percentage. Specific trade details that were rejected. Available options for resolution (temporary increase, reduce positions, etc.). Timeline for different resolution options.
    
    **Customer options:** Request temporary credit increase (if justified by market conditions). Reduce existing positions to free up credit capacity. Split large trade into smaller sizes that fit within remaining limit. Wait for existing trades to settle and free up credit.
    """)
    
    st.code("""
# Customer notification template
{
  "alert_type": "credit_limit_breach",
  "customer_id": "Cust_1",
  "pb_id": "PB_A",
  "timestamp": "2024-01-15T14:30:15Z",
  
  "breach_details": {
    "rejected_trade": {
      "instrument": "EURUSD",
      "notional": 500000,
      "side": "BUY"
    },
    "current_limit": 1000000,
    "current_utilization": 750000,
    "available_credit": 250000,
    "shortfall": 250000
  },
  
  "resolution_options": [
    {
      "option": "temporary_increase",
      "description": "Request 500K temporary increase",
      "timeline": "15-30 minutes",
      "requirements": "Risk approval needed"
    },
    {
      "option": "reduce_positions", 
      "description": "Close 250K existing positions",
      "timeline": "Immediate",
      "requirements": "Customer decision"
    },
    {
      "option": "split_trade",
      "description": "Execute 250K now, 250K later",
      "timeline": "Immediate for first part",
      "requirements": "Customer agreement"
    }
  ]
}
    """, language='json')

with st.expander("3 - Prime Broker Coordination", expanded=False):
    st.markdown("Communication and coordination steps with the Prime Broker")
    st.markdown("""
    **Immediate PB contact:** Notify PB risk team of the credit breach and customer request. Provide current exposure calculations and trade details. Discuss available options for credit increase or risk mitigation.
    
    **PB decision factors:** Customer's trading history and P&L performance. Current market conditions and volatility. PB's own credit line utilization with central PB. Regulatory and internal risk limits.
    
    **Coordination process:** PB reviews customer creditworthiness and current exposure. PB checks their own credit line capacity with central PB. Joint decision on temporary increase amount and duration. Document approval process for audit trail.
    """)
    
    st.code("""
# PB coordination workflow
{
  "pb_notification": {
    "pb_id": "PB_A",
    "customer_id": "Cust_1", 
    "breach_amount": 250000,
    "current_pb_utilization": 3200000,
    "pb_credit_line": 5000000,
    "available_pb_capacity": 1800000
  },
  
  "pb_risk_assessment": {
    "customer_pnl_30d": 45000,
    "customer_max_drawdown": 0.03,
    "avg_daily_volume": 850000,
    "credit_score": "A-",
    "relationship_tenure": "18_months"
  },
  
  "approval_workflow": [
    {
      "step": 1,
      "action": "pb_risk_review",
      "approver": "pb_risk_manager",
      "timeline": "10_minutes"
    },
    {
      "step": 2, 
      "action": "central_pb_check",
      "approver": "central_pb_system",
      "timeline": "5_minutes"
    },
    {
      "step": 3,
      "action": "final_approval",
      "approver": "pb_head_of_credit", 
      "timeline": "15_minutes"
    }
  ]
}
    """, language='json')

with st.expander("4 - Resolution Implementation", expanded=False):
    st.markdown("Steps to implement the agreed resolution and restore trading")
    st.markdown("""
    **Temporary credit increase:** Update credit limit in real-time system with expiration time. Notify all trading systems of the new limit. Set automatic alerts before expiration. Schedule follow-up review for permanent increase.
    
    **Position reduction:** Identify specific positions to close with customer. Execute closing trades to free up credit capacity. Confirm new available credit amount. Re-submit original rejected trade if still desired.
    
    **Trade modification:** Split large trade into smaller acceptable sizes. Execute first portion immediately. Queue remaining portions for later execution. Monitor credit utilization throughout the process.
    
    **System updates:** Update all trading systems with new credit parameters. Test trade submission to confirm resolution. Document all changes for audit and compliance. Set up monitoring for future breaches.
    """)
    
    st.code("""
# Resolution implementation steps

# 1. Temporary credit increase
POST /api/v1/credit/temporary-increase
{
  "customer_id": "Cust_1",
  "pb_id": "PB_A",
  "increase_amount": 500000,
  "new_total_limit": 1500000,
  "expires_at": "2024-01-15T18:00:00Z",
  "approved_by": "pb_risk_manager_001",
  "reason": "market_opportunity"
}

# 2. Verify system update
GET /api/v1/credit/customer/Cust_1/current-limits
{
  "pb_limits": [
    {
      "pb_id": "PB_A",
      "limit": 1500000,
      "used": 750000, 
      "available": 750000,
      "expires_at": "2024-01-15T18:00:00Z"
    }
  ]
}

# 3. Re-submit original trade
POST /api/v1/trades/submit
{
  "customer_id": "Cust_1",
  "pb_id": "PB_A",
  "instrument": "EURUSD",
  "notional": 500000,
  "side": "BUY",
  "reference": "retry_after_credit_increase"
}

# 4. Set monitoring alerts
POST /api/v1/alerts/create
{
  "alert_type": "credit_expiration_warning",
  "customer_id": "Cust_1", 
  "pb_id": "PB_A",
  "trigger_time": "2024-01-15T17:30:00Z",
  "message": "Temporary credit increase expires in 30 minutes"
}
    """, language='json')

st.markdown("""
**Resolution timeline summary:**

**0-5 minutes:** Verify breach details and current utilization. Contact customer with specific information and options.

**5-15 minutes:** Coordinate with PB risk team. Assess customer creditworthiness and PB capacity.

**15-30 minutes:** Obtain necessary approvals for credit increase. Implement system changes and verify updates.

**30+ minutes:** Re-submit trades and confirm resolution. Set up monitoring and follow-up processes.

**Key success factors:** Fast response time to minimize trading disruption. Clear communication with all parties. Proper documentation for audit compliance. Proactive monitoring to prevent future breaches.
""")

# --- Trading Simulation ---
st.header("Trading Simulation")
st.markdown("""
Submit orders to see credit limit validation. Orders will be rejected if they breach customer or PB credit limits.
""")

# Initialize session state for order book and positions
if 'order_book' not in st.session_state:
    st.session_state.order_book = []

if 'positions' not in st.session_state:
    st.session_state.positions = {}

if 'trade_id_counter' not in st.session_state:
    st.session_state.trade_id_counter = 1

# Trading interface in expandable panels
with st.expander("New Order Ticket", expanded=True):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #dee2e6;">
        <h4 style="margin-top: 0; color: #2c3e50;">Order Entry</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Order inputs
        selected_customer = st.selectbox("Customer:", [customer['id'] for customer in customers], key="trade_customer")
        instrument = st.selectbox("Instrument:", ["EURUSD", "GBPUSD", "USDJPY", "EURGBP", "AUDUSD"], key="trade_instrument")
        side = st.selectbox("Side:", ["BUY", "SELL"], key="trade_side")
        notional = st.number_input("Notional ($):", min_value=1000, max_value=10000000, value=100000, step=10000, key="trade_notional")
        
        if st.button("Submit Order", type="primary", use_container_width=True):
            # Find customer's PB from sessions
            customer_pb = None
            for session in sessions:
                if session['customer_id'] == selected_customer:
                    customer_pb = session['pb_id']
                    break
            
            if customer_pb:
                # Calculate current exposure for customer
                current_exposure = 0
                position_key = f"{selected_customer}|{customer_pb}"
                if position_key in st.session_state.positions:
                    current_exposure = st.session_state.positions[position_key]
                
                # Get credit limit
                customer_limit = 0
                for limit in credit_data_for_queries['customer_pb_limits']:
                    if limit['customer_id'] == selected_customer and limit['pb_id'] == customer_pb:
                        customer_limit = limit['limit_amount']
                        break
                
                # Check customer credit limit
                new_exposure = current_exposure + notional
                customer_breach = new_exposure > customer_limit
                
                # Check PB credit line (only for non-central PBs)
                pb_breach = False
                pb_total_exposure = 0
                pb_credit_line = 0
                
                if customer_pb != "CPB_1":  # Only check PB limits for non-central PBs
                    # Calculate PB total exposure to all customers
                    for pos_key, exposure in st.session_state.positions.items():
                        if pos_key.endswith(f"|{customer_pb}"):
                            pb_total_exposure += exposure
                    
                    # Add this new trade to PB exposure
                    pb_new_total = pb_total_exposure + notional
                    
                    # Get PB credit line with central PB
                    for limit in credit_data_for_queries['pb_to_central_pb_limits']:
                        if limit['non_central_pb_id'] == customer_pb:
                            pb_credit_line = limit['limit_amount']
                            break
                    
                    # Check PB credit line
                    pb_breach = pb_new_total > pb_credit_line
                
                # Create order
                order = {
                    'trade_id': f"TRD_{st.session_state.trade_id_counter:06d}",
                    'timestamp': "2024-01-15T" + str(14 + len(st.session_state.order_book) % 10) + f":{30 + len(st.session_state.order_book) % 30:02d}:00Z",
                    'customer_id': selected_customer,
                    'pb_id': customer_pb,
                    'instrument': instrument,
                    'side': side,
                    'notional': notional,
                    'status': 'PENDING'
                }
                
                # Validate and execute or reject
                if customer_breach:
                    order['status'] = 'REJECTED'
                    order['reject_reason'] = f"Customer credit limit exceeded. Limit: ${customer_limit:,}, Would be: ${new_exposure:,}"
                    st.error(f"Order REJECTED: Customer {selected_customer} would exceed credit limit with {customer_pb}")
                    st.error(f"Current exposure: ${current_exposure:,}, New trade: ${notional:,}, Limit: ${customer_limit:,}")
                elif pb_breach:
                    order['status'] = 'REJECTED'
                    order['reject_reason'] = f"PB credit line exceeded. PB limit: ${pb_credit_line:,}, Would be: ${pb_new_total:,}"
                    st.error(f"Order REJECTED: PB {customer_pb} would exceed credit line with Central PB")
                    st.error(f"PB current exposure: ${pb_total_exposure:,}, New trade: ${notional:,}, PB limit: ${pb_credit_line:,}")
                else:
                    order['status'] = 'EXECUTED'
                    # Update positions
                    st.session_state.positions[position_key] = new_exposure
                    st.success(f"Order EXECUTED: {side} ${notional:,} {instrument}")
                    if customer_pb == "CPB_1":
                        st.info(f"Direct Central PB trade - New exposure for {selected_customer}: ${new_exposure:,} / ${customer_limit:,}")
                    else:
                        st.info(f"New exposure for {selected_customer} with {customer_pb}: ${new_exposure:,} / ${customer_limit:,}")
                
                # Add to order book
                st.session_state.order_book.append(order)
                st.session_state.trade_id_counter += 1
            else:
                st.error("No PB found for this customer")

    with col2:
        st.subheader("Current Positions")
        
        if st.session_state.positions:
            # Show customer positions
            st.write("**Customer Positions:**")
            for position_key, exposure in st.session_state.positions.items():
                customer_id, pb_id = position_key.split('|')
                
                # Get customer limit
                customer_limit = 0
                for l in credit_data_for_queries['customer_pb_limits']:
                    if l['customer_id'] == customer_id and l['pb_id'] == pb_id:
                        customer_limit = l['limit_amount']
                        break
                
                utilization = (exposure / customer_limit * 100) if customer_limit > 0 else 0
                
                st.write(f"**{customer_id} → {pb_id}**")
                st.write(f"Exposure: ${exposure:,} / ${customer_limit:,} ({utilization:.1f}%)")
                st.progress(min(utilization / 100, 1.0))
                st.write("---")
            
            # Show PB credit line utilization
            st.write("**PB Credit Lines:**")
            pb_exposures = {}
            
            # Calculate total exposure per PB (excluding CPB_1 since it's the central PB)
            for position_key, exposure in st.session_state.positions.items():
                customer_id, pb_id = position_key.split('|')
                if pb_id != "CPB_1":  # Only track non-central PBs
                    if pb_id not in pb_exposures:
                        pb_exposures[pb_id] = 0
                    pb_exposures[pb_id] += exposure
            
            # Display PB credit line utilization
            if pb_exposures:
                for pb_id, total_exposure in pb_exposures.items():
                    # Get PB credit line with central PB
                    pb_credit_line = 0
                    for limit in credit_data_for_queries['pb_to_central_pb_limits']:
                        if limit['non_central_pb_id'] == pb_id:
                            pb_credit_line = limit['limit_amount']
                            break
                    
                    pb_utilization = (total_exposure / pb_credit_line * 100) if pb_credit_line > 0 else 0
                    
                    st.write(f"**{pb_id} → Central PB**")
                    st.write(f"Total Exposure: ${total_exposure:,} / ${pb_credit_line:,} ({pb_utilization:.1f}%)")
                    st.progress(min(pb_utilization / 100, 1.0))
                    st.write("---")
            else:
                st.write("No non-central PB exposures yet")
                
            # Show CPB_1 direct exposures separately
            cpb_direct_exposure = 0
            for position_key, exposure in st.session_state.positions.items():
                customer_id, pb_id = position_key.split('|')
                if pb_id == "CPB_1":
                    cpb_direct_exposure += exposure
            
            if cpb_direct_exposure > 0:
                st.write("**Central PB Direct Exposures:**")
                st.write("**CPB_1 Direct Trading**")
                st.write(f"Total Direct Exposure: ${cpb_direct_exposure:,}")
                st.write("(No credit line limit - Central PB capacity)")
                st.write("---")
        
        else:
            st.write("No positions yet")
        
        # Reset button
        if st.button("Reset All Positions", use_container_width=True):
            st.session_state.positions = {}
            st.session_state.order_book = []
            st.session_state.trade_id_counter = 1
            st.success("All positions and orders cleared!")
            st.rerun()

# Order Book as a proper table
with st.expander("Order Book", expanded=False):
    if st.session_state.order_book:
        # Create DataFrame for better table display
        import pandas as pd
        
        # Show recent orders (last 15)
        recent_orders = st.session_state.order_book[-15:]
        
        # Prepare data for table
        table_data = []
        for order in reversed(recent_orders):
            status_text = "EXECUTED" if order['status'] == 'EXECUTED' else "REJECTED"
            table_data.append({
                'Status': status_text,
                'Trade ID': order['trade_id'],
                'Time': order['timestamp'].split('T')[1][:8],  # Just time part
                'Customer': order['customer_id'],
                'PB': order['pb_id'],
                'Side': order['side'],
                'Instrument': order['instrument'],
                'Notional': f"${order['notional']:,}",
                'Reject Reason': order.get('reject_reason', '')[:50] + '...' if order.get('reject_reason', '') and len(order.get('reject_reason', '')) > 50 else order.get('reject_reason', '')
            })
        
        df = pd.DataFrame(table_data)
        
        # Display table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Trade ID": st.column_config.TextColumn("Trade ID", width="medium"),
                "Time": st.column_config.TextColumn("Time", width="small"),
                "Customer": st.column_config.TextColumn("Customer", width="small"),
                "PB": st.column_config.TextColumn("PB", width="small"),
                "Side": st.column_config.TextColumn("Side", width="small"),
                "Instrument": st.column_config.TextColumn("Instrument", width="small"),
                "Notional": st.column_config.TextColumn("Notional", width="medium"),
                "Reject Reason": st.column_config.TextColumn("Reject Reason", width="large")
            }
        )
    else:
        st.write("No orders submitted yet")


