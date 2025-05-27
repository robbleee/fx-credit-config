import streamlit as st
import yaml # PyYAML needs to be installed: pip install PyYAML
import os

# --- Streamlit App Layout (must be first) ---
st.set_page_config(layout="wide", page_title="FX Credit Configuration Viewer")

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

st.title("FX Credit Configuration Schema Viewer ")
st.markdown("""
This application displays the structure and example content of configuration files
used to model FX trading relationships, including Customers, Prime Brokers (PBs),
Sessions, and Credit Limits.
""")

# Show file loading status
if all([prime_brokers_data, customers_data, sessions_data, credit_data]):
    st.success("✅ All configuration files loaded successfully")
    with st.expander("File Loading Details", expanded=False):
        st.write("**Loaded Files:**")
        st.write(f"• `prime_brokers.yaml` - {len(prime_brokers_data)} prime brokers")
        st.write(f"• `customers.yaml` - {len(customers_data)} customers") 
        st.write(f"• `sessions.yaml` - {len(sessions_data)} sessions")
        st.write(f"• `credit_data.yaml` - {len(credit_data.get('customer_pb_limits', []))} customer limits, {len(credit_data.get('pb_to_central_pb_limits', []))} PB limits")
else:
    st.error("❌ Some configuration files failed to load")

# --- Design Rationale ---
st.header("Design Rationale")
with st.expander("Why YAML and this structure?", expanded=False):
    st.markdown("""
    **Why YAML?**
    - **Human-readable**: YAML's syntax is clean and intuitive, making it easy for operations teams to read and modify configuration files
    - **Widely supported**: Excellent tooling and library support across programming languages
    - **Version control friendly**: Text-based format works well with Git for tracking configuration changes
    - **Comments support**: Unlike JSON, YAML allows inline comments for documentation
    - **Hierarchical structure**: Natural representation of nested relationships without excessive brackets
    
    **Why separate files?**
    - **Separation of concerns**: Static configuration (prime brokers, customers, sessions) vs. dynamic data (credit limits)
    - **Update frequency**: Credit data changes frequently and may be updated by external systems, while other configs are more stable
    - **Access control**: Different teams may need different permissions (e.g., only credit team updates credit_data.yaml)
    - **Scalability**: Easier to manage and cache different types of data independently
    
    **Why this specific structure?**
    - **Normalization**: Uses IDs for relationships to avoid data duplication (similar to database foreign keys)
    - **Flexibility**: Easy to add new prime brokers, customers, or sessions without restructuring existing data
    - **Clear relationships**: The linking structure makes it obvious how customers connect to prime brokers through sessions
    - **Audit trail**: Timestamps in credit data enable tracking of when limits were last updated
    - **Currency explicit**: All monetary amounts include currency to avoid ambiguity in multi-currency environments
    """)

# --- Schema Diagram ---
st.header("Configuration Schema Overview")
st.markdown("""
**File Structure & Relationships**: This diagram shows how the four YAML configuration files relate to each other 
and the key relationships between entities.
""")

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
**Purpose**: Defines all Prime Brokers involved in the trading ecosystem, including identifying the central Prime Broker.
* `id`: A unique identifier for the Prime Broker.
* `name`: The full name of the Prime Broker.
* `is_central_pb`: A boolean flag (`true`/`false`) indicating if this PB is the venue's central Prime Broker. There should be exactly one central PB.
""")
with st.expander("View `prime_brokers.yaml` content"):
    st.code(prime_brokers_data_str, language='yaml')

# --- Customers Configuration ---
st.header("2. Customers (`customers.yaml`)")
st.markdown("""
**Purpose**: Defines the clients (e.g., hedge funds, asset managers) who trade on the venue.
* `id`: A unique identifier for the customer.
* `name`: The name of the customer entity.
""")
with st.expander("View `customers.yaml` content"):
    st.code(customers_data_str, language='yaml')

# --- Sessions Configuration ---
st.header("3. Sessions (`sessions.yaml`)")
st.markdown("""
**Purpose**: Defines the technical connections (sessions) customers use to access the venue and maps each session to a specific Prime Broker.
* `session_id`: A unique identifier for the trading session (e.g., FIX session ID).
* `customer_id`: Links to the `id` in `customers.yaml`, identifying which customer owns this session.
* `pb_id`: Links to the `id` in `prime_brokers.yaml`, identifying the Prime Broker associated with this session. For this model, it's a 1:1 mapping of Customer Session to PB.
* `protocol`: The communication protocol used for this session (e.g., "FIX 4.2", "FIX 4.4").
""")
with st.expander("View `sessions.yaml` content"):
    st.code(sessions_data_str, language='yaml')

# --- Credit Data Configuration ---
st.header("4. Credit Data (`credit_data.yaml`)")
st.markdown("""
**Purpose**: Contains real-time or frequently updated credit limit information. This file is expected to be updated by a 3rd party data vendor.

**Live Updates**: The credit data is automatically updated by our 3rd party credit data vendor through their API integration. 
Updates occur in real-time as credit conditions change, ensuring the trading system always has current limit information.
The vendor typically pushes updates via secure file transfer or direct API calls to our system.

It is structured into two main sections:
""")

st.subheader("4.1 `customer_pb_limits`")
st.markdown("""
Defines the credit limits individual customers have with their respective Prime Brokers.
* `customer_id`: Links to the `id` in `customers.yaml`.
* `pb_id`: Links to the `id` in `prime_brokers.yaml`.
* `limit_amount`: The maximum credit amount the customer can utilize with this PB.
* `currency`: The currency of the limit amount (e.g., "USD").
* `last_updated`: Timestamp indicating when this credit limit information was last updated (ISO 8601 format).
""")

st.subheader("4.2 `pb_to_central_pb_limits`")
st.markdown("""
Defines the credit lines that non-central Prime Brokers have with the venue's central Prime Broker. This is necessary for clients of non-central PBs to access the venue.
* `non_central_pb_id`: Links to the `id` of a non-central PB in `prime_brokers.yaml`.
* `central_pb_id`: Links to the `id` of the central PB in `prime_brokers.yaml`.
* `limit_amount`: The maximum credit amount the non-central PB has with the central PB.
* `currency`: The currency of the limit amount.
* `last_updated`: Timestamp indicating when this credit limit information was last updated.
""")
with st.expander("View `credit_data.yaml` content"):
    st.code(credit_data_str, language='yaml')

# --- Interactive Credit Limit Editor ---
st.sidebar.markdown("---")
st.sidebar.markdown("### Live Credit Editor")
st.sidebar.markdown("**Modify credit limits and see changes in real-time**")

# Initialize session state for credit data if not exists
if 'modified_credit_data' not in st.session_state:
    st.session_state.modified_credit_data = credit_data.copy() if credit_data else {}

# Customer-PB Credit Limits Editor
st.sidebar.markdown("**Customer → PB Limits:**")
if st.session_state.modified_credit_data and 'customer_pb_limits' in st.session_state.modified_credit_data:
    for i, limit in enumerate(st.session_state.modified_credit_data['customer_pb_limits']):
        with st.sidebar.expander(f"{limit['customer_id']} → {limit['pb_id']}", expanded=False):
            # Create unique keys for each input
            new_amount = st.number_input(
                "Credit Limit ($)",
                min_value=0,
                value=limit['limit_amount'],
                step=100000,
                key=f"customer_limit_{i}",
                help=f"Current: ${limit['limit_amount']:,}"
            )
            
            if new_amount != limit['limit_amount']:
                st.session_state.modified_credit_data['customer_pb_limits'][i]['limit_amount'] = new_amount
                st.sidebar.success(f"Updated to ${new_amount:,}")

# PB-Central PB Credit Lines Editor
st.sidebar.markdown("**PB → Central PB Lines:**")
if st.session_state.modified_credit_data and 'pb_to_central_pb_limits' in st.session_state.modified_credit_data:
    for i, limit in enumerate(st.session_state.modified_credit_data['pb_to_central_pb_limits']):
        with st.sidebar.expander(f"{limit['non_central_pb_id']} → {limit['central_pb_id']}", expanded=False):
            new_amount = st.number_input(
                "Credit Line ($)",
                min_value=0,
                value=limit['limit_amount'],
                step=500000,
                key=f"pb_limit_{i}",
                help=f"Current: ${limit['limit_amount']:,}"
            )
            
            if new_amount != limit['limit_amount']:
                st.session_state.modified_credit_data['pb_to_central_pb_limits'][i]['limit_amount'] = new_amount
                st.sidebar.success(f"Updated to ${new_amount:,}")



# Save changes button (simulated)
if st.sidebar.button("Save", help="In production, this would save to credit_data.yaml"):
    st.sidebar.info("In production, this would update the credit_data.yaml file. But for simplicity of implementation and deployment we are only updating the session state.")
    
    # Show what would be saved
    with st.sidebar.expander("Preview YAML Output", expanded=False):
        st.code(yaml.dump(st.session_state.modified_credit_data, default_flow_style=False), language='yaml')

# --- Interactive Query Examples (at the bottom) ---
st.header("Interactive Python Query Examples")
st.markdown("""
**Test the Schema**: These interactive panels demonstrate how to query the configuration data using Python.
Select inputs, click the execute button, and see both the results and the Python code used.
""")

# Use the already loaded YAML data for interactive queries
prime_brokers = prime_brokers_data
customers = customers_data
sessions = sessions_data
# Use modified credit data from session state if available
credit_data_for_queries = st.session_state.get('modified_credit_data', credit_data)

# Check if all files loaded successfully
if not all([prime_brokers, customers, sessions, credit_data_for_queries]):
    st.error("Some configuration files failed to load. Please check that all YAML files are present and valid.")
    st.stop()

# Panel 1: Session to PB Lookup
with st.expander("1 - Session to Prime Broker Lookup", expanded=False):
    st.markdown("**Find which Prime Broker is associated with any session**")
    
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
    st.markdown("**Check all credit limits for a customer across different Prime Brokers**")
    
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

# Panel 3: Credit Validation
with st.expander("3 - Credit Exposure Validation", expanded=False):
    st.markdown("**Verify Prime Broker doesn't exceed their central Prime Broker credit line**")
    
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

# Add implementation notes
st.markdown("---")
st.markdown("""
**Implementation Notes:**
- **Data Loading**: Use `PyYAML` library to parse YAML configuration files
- **Relationships**: Leverage ID-based relationships to join data across files  
- **Validation**: Implement business logic to ensure credit limits are not exceeded
- **Real-time**: In production, this data would be loaded from databases or APIs with caching for performance
- **Error Handling**: Add proper exception handling and logging for production use
""")

# --- Error Handling & Edge Cases ---
st.header("Error Handling & Edge Cases")
st.markdown("""
**Essential Validation**: Key checks needed when parsing and validating the configuration files.
""")

with st.expander("1 - Basic File Validation", expanded=False):
    st.markdown("**Load and validate YAML files safely**")
    st.markdown("""
    **Why this matters**: YAML files can have syntax errors, be missing, or contain unexpected data structures. 
    Proper validation prevents the application from crashing and provides clear error messages to operators.
    
    **Key checks**:
    - File existence and readability
    - Valid YAML syntax
    - Non-empty content
    - Required fields present in each entity
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
    st.markdown("**Validate critical business rules**")
    st.markdown("""
    **Why this matters**: Beyond syntax validation, the configuration must satisfy business logic rules. 
    Violating these rules could lead to trading failures, compliance issues, or system instability.
    
    **Critical business rules**:
    - Exactly one central Prime Broker (required for venue access)
    - No duplicate IDs (prevents ambiguous references)
    - All session references must point to valid customers and Prime Brokers
    - All credit limit references must point to valid entities
    - Referential integrity across all configuration files
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
    **Why this matters**: This is a critical risk management check. If a Prime Broker issues more credit 
    to customers than they have available from the central Prime Broker, it creates a credit exposure 
    that could result in trading failures or financial losses.
    
    **Risk scenarios prevented**:
    - Prime Broker over-extending credit beyond their central PB limit
    - High utilization warnings (>90%) to prevent hitting limits during trading
    - Monitoring total exposure across all customers per Prime Broker
    - Early warning system for credit line management
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
    st.markdown("**Handle typical edge cases**")
    st.markdown("""
    **Why this matters**: Real-world trading systems encounter various edge cases that, while not 
    necessarily errors, require monitoring and handling. These scenarios can impact trading operations 
    and should be flagged for operational awareness.
    
    **Common scenarios**:
    - Customers with multiple sessions (legitimate but worth tracking)
    - Customers with sessions but no credit limits (potential configuration gap)
    - Stale credit data (outdated information that could affect trading decisions)
    - Invalid timestamps (data quality issues)
    - Orphaned configurations (entities referenced but not defined)
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

st.markdown("---")
st.markdown("""
**Essential Error Handling Checklist:**

1. **File Loading**: Handle missing files and YAML parsing errors
2. **Required Fields**: Ensure all mandatory fields are present
3. **Unique IDs**: Check for duplicate identifiers across entities
4. **Referential Integrity**: Verify all ID references are valid
5. **Central PB Rule**: Exactly one central Prime Broker must exist
6. **Credit Exposure**: PBs cannot exceed their central PB credit lines
7. **Edge Cases**: Handle multiple sessions, missing credit limits, stale data
""")
