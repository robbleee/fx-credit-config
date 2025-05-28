import streamlit as st
import yaml # PyYAML needs to be installed: pip install PyYAML
import os
import json

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

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")

# Initialize session state for navigation
if 'nav_section' not in st.session_state:
    st.session_state.nav_section = 'overview'

# Navigation buttons that set the current section
if st.sidebar.button("YAML Format Choice", use_container_width=True):
    st.session_state.nav_section = 'yaml_choice'

if st.sidebar.button("Schema Overview", use_container_width=True):
    st.session_state.nav_section = 'overview'

if st.sidebar.button("Configuration Files", use_container_width=True):
    st.session_state.nav_section = 'config_files'

if st.sidebar.button("Interactive Examples", use_container_width=True):
    st.session_state.nav_section = 'interactive'

if st.sidebar.button("Error Handling", use_container_width=True):
    st.session_state.nav_section = 'error_handling'

if st.sidebar.button("Future Extensions", use_container_width=True):
    st.session_state.nav_section = 'future'

if st.sidebar.button("Trade Flow", use_container_width=True):
    st.session_state.nav_section = 'trade_flow'

if st.sidebar.button("Trading Simulation", use_container_width=True):
    st.session_state.nav_section = 'trading'

st.sidebar.markdown("---")
st.sidebar.markdown("**Quick Stats:**")
if prime_brokers_data and customers_data and sessions_data:
    st.sidebar.write(f"Prime Brokers: {len(prime_brokers_data)}")
    st.sidebar.write(f"Customers: {len(customers_data)}")
    st.sidebar.write(f"Sessions: {len(sessions_data['sessions'] if sessions_data and 'sessions' in sessions_data else [])}")
    if credit_data:
        customer_limits = len(credit_data.get('customer_pb_limits', []))
        pb_limits = len(credit_data.get('pb_to_central_pb_limits', []))
        st.sidebar.write(f"Customer Limits: {customer_limits}")
        st.sidebar.write(f"PB Credit Lines: {pb_limits}")

# Display content based on selected section
# Use the already loaded YAML data for interactive queries
prime_brokers = prime_brokers_data
customers = customers_data
sessions = sessions_data['sessions'] if sessions_data and 'sessions' in sessions_data else []
# Use modified credit data from session state if available
credit_data_for_queries = st.session_state.get('modified_credit_data', credit_data)

# Initialize session state for credit data if not exists
if 'modified_credit_data' not in st.session_state:
    st.session_state.modified_credit_data = credit_data.copy() if credit_data else {}

# Check if all files loaded successfully
if not all([prime_brokers, customers, sessions, credit_data_for_queries]):
    st.error("Some configuration files failed to load. Please check that all YAML files are present and valid.")
    st.stop()

if st.session_state.nav_section == 'yaml_choice':
    with st.expander("Why YAML", expanded=True):
        st.markdown("""
        **CSV**
        would be too flat for our hierarchical configuration data. We need nested structures for things like credit limits with multiple fields (customer_id, pb_id, amount, currency, timestamp). CSV also lacks support for comments, which operations teams need for documenting business logic and exceptions.
        
        **XML**
        would work technically but it's verbose and harder for operations teams to read and edit during market stress. The angle bracket syntax makes quick manual edits error-prone. XML also feels outdated for configuration management compared to more modern formats.
        
        **TOML**
        is great for application config but gets unwieldy with deeply nested data structures. Our credit limits and session mappings would become hard to read in TOML format. TOML also has less widespread adoption in financial operations teams.
        
        **YAML**
        gives us the best - it's human-readable like JSON but supports comments for documenting business rules. Operations teams can make emergency credit adjustments without developer support. The indentation-based structure makes relationships clear at a glance. Git diffs are clean and reviewable. Most DevOps tools have excellent YAML support.
        """)

elif st.session_state.nav_section == 'overview':
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
                        <div class="entity-name">customer_id: Cust_1<br>pb_id: PB_A</div>
                    </div>
                    <div class="entity">
                        <div class="entity-id">FIXS_C1_PBB_001</div>
                        <div class="entity-name">customer_id: Cust_1<br>pb_id: PB_B</div>
                    </div>
                    <div class="entity">
                        <div class="entity-id">FIXS_C2_PBA_001</div>
                        <div class="entity-name">customer_id: Cust_2<br>pb_id: PB_A</div>
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

elif st.session_state.nav_section == 'config_files':
    # --- Configuration Files ---
    st.header("Configuration Files")
    st.markdown("""
    Here are the configuration files for prime brokers, customers, sessions, and credit data.
    """)

    # Prime Brokers File
    st.subheader("1. Prime Brokers (`prime_brokers.yaml`)")
    st.markdown("""
    We could define all prime brokers and identify the central prime broker. The central PB requirement would ensure 
    clear venue connectivity and simplify credit management during client onboarding.

    **id:** Unique identifier for the prime broker  
    **name:** Full name of the prime broker  
    **is_central_pb:** Boolean flag, exactly one PB should be true
    """)
    with st.expander("📁 View prime_brokers.yaml content"):
        st.code(prime_brokers_data_str, language='yaml')

    # Customers File
    st.subheader("2. Customers (`customers.yaml`)")
    st.markdown("""
    Customer entities for trading activity. We could keep a minimal schema with essential identifiers for trade routing 
    while allowing detailed customer data to be managed in dedicated CRM systems.

    **id:** Unique identifier for the customer  
    **name:** Customer entity name
    """)
    with st.expander("📁 View customers.yaml content"):
        st.code(customers_data_str, language='yaml')

    # Sessions File
    st.subheader("3. Sessions (`sessions.yaml`)")
    st.markdown("""
    Trading sessions map customers to prime brokers. 

    **session_id:** Unique session identifier  
    **customer_id:** Links to customer ID  
    **pb_id:** Links to prime broker ID
    """)
    with st.expander("📁 View sessions.yaml content"):
        st.code(sessions_data_str, language='yaml')

    # Credit Data File
    st.subheader("4. Credit Data (`credit_data.yaml`)")
    st.markdown("""
    We could separate credit limit information since it's updated frequently by third-party vendors. This separation enables 
    different security requirements and update procedures.
    """)

    st.markdown("**4.1 `customer_pb_limits`**")
    st.markdown("""
    Direct credit limits between customers and prime brokers. These would be essential for trade authorization and 
    preventing customer trading disruptions.

    **customer_id:** Links to customer ID  
    **pb_id:** Links to prime broker ID  
    **limit_amount:** Maximum credit amount  
    **currency:** Limit currency (e.g., "USD")  
    **last_updated:** When this limit was last updated
    """)

    st.markdown("**4.2 `pb_to_central_pb_limits`**")
    st.markdown("""
    Credit lines between non-central prime brokers and the central prime broker. We'd need to monitor these to ensure 
    prime brokers don't over-extend credit to their customers beyond their own capacity.
    """)
    
    with st.expander("📁 View credit_data.yaml content"):
        st.code(credit_data_str, language='yaml')

elif st.session_state.nav_section == 'interactive':
    # --- Interactive Query Examples (at the bottom) ---
    st.header("Interactive Python Query Examples")
    st.markdown("""
    Here are some examples showing how we could work with the configuration data in practice.
    You can select inputs, click execute, and see both results and code.
    """)

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
        st.markdown("Check PB exposure against their credit lines")
        st.markdown("""
        This would be a critical risk management check. If a prime broker issues more credit to customers than they have available from the central prime broker, it creates exposure that could result in trading failures.
        
        **Risk scenarios we'd want to prevent:** Prime broker over-extending credit beyond their limit. High utilization warnings (>90%). Monitoring total exposure per prime broker. Early warning for credit line management.
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

    with st.expander("4 - Per-Instrument Credit Limits", expanded=False):
        st.markdown("Granular credit control at the instrument level")
        st.markdown("""
        Currently the schema has aggregate credit limits per customer-PB relationship. For per-instrument limits, we could implement:
        
        **Instrument hierarchy:** We could define instrument categories (FX majors, minors, exotics). Set limits at category and individual instrument levels. Inherit limits from parent categories with overrides.
        
        **Multi-dimensional limits:** We could add credit limits by instrument, tenor, notional size. Time-based limits (daily, weekly, monthly). Concentration limits to prevent over-exposure to single instruments.
        
        **Real-time monitoring:** We'd track utilization per instrument in real-time. Alert when approaching instrument-specific limits. Automatically reject trades exceeding limits.
        """)
        
        st.code("""
# Extended credit data structure with per-instrument limits
instrument_credit_config = {
    "customer_id": "Cust_1",
    "pb_id": "PB_A",
    "aggregate_limit": 1000000,  # Overall limit
    "instrument_limits": {
        "categories": {
            "FX_MAJORS": {
                "limit": 800000,
                "instruments": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF"]
            },
            "FX_MINORS": {
                "limit": 150000,
                "instruments": ["EURGBP", "EURJPY", "GBPJPY"]
            },
            "FX_EXOTICS": {
                "limit": 50000,
                "instruments": ["USDTRY", "USDZAR", "USDMXN"]
            }
        },
        "individual_overrides": {
            "EURUSD": {"limit": 500000},  # Override within FX_MAJORS
            "USDTRY": {"limit": 25000}    # Override within FX_EXOTICS
        }
    },
    "concentration_limits": {
        "max_single_instrument_pct": 60,  # Max 60% in any single instrument
        "max_category_pct": 80             # Max 80% in any category
    }
}

def validate_instrument_trade(customer_id, pb_id, instrument, notional, current_positions):
    \"\"\"Validate trade against per-instrument credit limits\"\"\"
    config = get_instrument_credit_config(customer_id, pb_id)
    
    # Get instrument category and limits
    category = get_instrument_category(instrument, config)
    instrument_limit = get_effective_instrument_limit(instrument, config)
    
    # Calculate current exposures
    current_instrument_exposure = current_positions.get(instrument, 0)
    current_category_exposure = sum(current_positions.get(instr, 0) 
                                  for instr in config["instrument_limits"]["categories"][category]["instruments"])
    total_exposure = sum(current_positions.values())
    
    # Check limits
    checks = {
        "aggregate_limit": {
            "current": total_exposure + notional,
            "limit": config["aggregate_limit"],
            "passed": (total_exposure + notional) <= config["aggregate_limit"]
        },
        "instrument_limit": {
            "current": current_instrument_exposure + notional,
            "limit": instrument_limit,
            "passed": (current_instrument_exposure + notional) <= instrument_limit
        },
        "category_limit": {
            "current": current_category_exposure + notional,
            "limit": config["instrument_limits"]["categories"][category]["limit"],
            "passed": (current_category_exposure + notional) <= config["instrument_limits"]["categories"][category]["limit"]
        },
        "concentration_check": {
            "instrument_pct": ((current_instrument_exposure + notional) / config["aggregate_limit"] * 100),
            "max_pct": config["concentration_limits"]["max_single_instrument_pct"],
            "passed": ((current_instrument_exposure + notional) / config["aggregate_limit"] * 100) <= config["concentration_limits"]["max_single_instrument_pct"]
        }
    }
    
    # Overall validation result
    all_passed = all(check["passed"] for check in checks.values())
    
    return {
        "trade_allowed": all_passed,
        "checks": checks,
        "instrument": instrument,
        "category": category,
        "notional": notional
    }

# Usage example
current_positions = {
    "EURUSD": 300000,
    "GBPUSD": 200000,
    "USDJPY": 150000
}

result = validate_instrument_trade("Cust_1", "PB_A", "EURUSD", 250000, current_positions)
print(f"Trade allowed: {result['trade_allowed']}")
for check_name, check_result in result['checks'].items():
    print(f"{check_name}: {check_result['current']:,} / {check_result['limit']:,} - {'PASS' if check_result['passed'] else 'FAIL'}")
        """, language='python')

elif st.session_state.nav_section == 'error_handling':
    # --- Error Handling & Edge Cases ---
    st.header("Error Handling & Edge Cases")
    st.markdown("""
    Here are some key validation checks we'd want to implement when parsing and validating configuration files.
    """)

    with st.expander("1 - Basic File Validation", expanded=False):
        st.markdown("Load and validate YAML files safely")
        st.markdown("""
        YAML files can have syntax errors, be missing, or contain unexpected data. We could implement proper validation to prevent crashes and provide clear error messages.
        
        **Key checks we'd implement:**  
        • File exists and is readable  
        • Valid YAML syntax  
        • Non-empty content  
        • Required fields present
        """)
        
        st.code("""
def load_and_validate_yaml(filename, required_fields):
    \"\"\"Safely load YAML with validation\"\"\"
    try:
        # Check file exists
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Configuration file not found: {filename}")
        
        # Load YAML
        with open(filename, 'r') as file:
            data = yaml.safe_load(file)
        
        # Check not empty
        if not data:
            raise ValueError(f"File {filename} is empty or contains no valid data")
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Required field '{field}' missing in {filename}")
        
        return data
        
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax in {filename}: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to load {filename}: {e}")

# Usage
try:
    prime_brokers = load_and_validate_yaml('prime_brokers.yaml', ['PB_A', 'CPB_1'])
    print("Prime brokers loaded successfully")
except Exception as e:
    print(f"Error: {e}")
        """, language='python')

    with st.expander("2 - Business Rule Checks", expanded=False):
        st.markdown("Validate critical business rules")
        st.markdown("""
        Beyond syntax validation, we'd need the configuration to satisfy business logic rules. Violating these could lead to trading failures or compliance issues.
        
        **Critical rules we'd enforce:**  
        • Exactly one central prime broker (required for venue access)  
        • No duplicate IDs (prevents ambiguous references)  
        • All references point to valid entities  
        • Referential integrity across files
        """)
        
        st.code("""
def validate_business_rules(prime_brokers, customers, sessions, credit_data):
    \"\"\"Validate critical business rules\"\"\"
    errors = []
    
    # Check exactly one central PB
    central_pbs = [pb for pb in prime_brokers.values() 
                   if pb.get('is_central_pb', False)]
    if len(central_pbs) != 1:
        errors.append(f"Must have exactly 1 central PB, found {len(central_pbs)}")
    
    # Check for duplicate IDs
    all_pb_ids = list(prime_brokers.keys())
    if len(all_pb_ids) != len(set(all_pb_ids)):
        errors.append("Duplicate prime broker IDs found")
    
    # Check referential integrity - sessions reference valid entities
    for session in sessions['sessions']:
        if session['customer_id'] not in customers:
            errors.append(f"Session {session['session_id']} references unknown customer {session['customer_id']}")
        if session['pb_id'] not in prime_brokers:
            errors.append(f"Session {session['session_id']} references unknown PB {session['pb_id']}")
    
    # Check credit limits reference valid entities
    for limit in credit_data['customer_pb_limits']:
        if limit['customer_id'] not in customers:
            errors.append(f"Credit limit references unknown customer {limit['customer_id']}")
        if limit['pb_id'] not in prime_brokers:
            errors.append(f"Credit limit references unknown PB {limit['pb_id']}")
    
    return errors

# Usage
errors = validate_business_rules(prime_brokers, customers, sessions, credit_data)
if errors:
    for error in errors:
        print(f"VALIDATION ERROR: {error}")
else:
    print("All business rules validated successfully")
        """, language='python')

    with st.expander("3 - Credit Exposure Check", expanded=False):
        st.markdown("**Ensure PBs don't exceed their credit lines**")
        st.markdown("""
        This would be a critical risk management check. If a prime broker issues more credit 
        to customers than they have available from the central prime broker, 
        it creates exposure that could result in trading failures.
        
        **Risk scenarios we'd prevent:**
        - Prime broker over-extending credit beyond their limit
        - High utilization warnings (>90%) 
        - Monitoring total exposure per prime broker
        - Early warning for credit line management
        """)
        
        st.code("""
def validate_credit_exposure(credit_data, warning_threshold=0.9):
    \"\"\"Check PB credit exposure vs central PB limits\"\"\"
    issues = []
    
    # Calculate total credit issued by each PB
    pb_issued = {}
    for limit in credit_data['customer_pb_limits']:
        pb_id = limit['pb_id']
        if pb_id not in pb_issued:
            pb_issued[pb_id] = 0
        pb_issued[pb_id] += limit['limit_amount']
    
    # Check against PB credit lines
    for limit in credit_data['pb_to_central_pb_limits']:
        pb_id = limit['non_central_pb_id']
        pb_credit_line = limit['limit_amount']
        total_issued = pb_issued.get(pb_id, 0)
        
        utilization = total_issued / pb_credit_line if pb_credit_line > 0 else 0
        
        if total_issued > pb_credit_line:
            issues.append({
                'type': 'BREACH',
                'pb_id': pb_id,
                'issued': total_issued,
                'limit': pb_credit_line,
                'excess': total_issued - pb_credit_line
            })
        elif utilization > warning_threshold:
            issues.append({
                'type': 'WARNING',
                'pb_id': pb_id,
                'utilization': utilization * 100,
                'issued': total_issued,
                'limit': pb_credit_line
            })
    
    return issues

# Usage
issues = validate_credit_exposure(credit_data)
for issue in issues:
    if issue['type'] == 'BREACH':
        print(f"CRITICAL: PB {issue['pb_id']} exceeded limit by ${issue['excess']:,}")
    else:
        print(f"WARNING: PB {issue['pb_id']} at {issue['utilization']:.1f}% utilization")
        """, language='python')

    with st.expander("4 - Common Edge Cases", expanded=False):
        st.markdown("Handle typical edge cases")
        st.markdown("""
        Real-world trading systems encounter various edge cases that aren't necessarily errors but we'd want to monitor. These can impact operations and should be flagged.
        
        **Common scenarios we'd track:**  
        • Customers with multiple sessions (legitimate but worth tracking)  
        • Customers with sessions but no credit limits (configuration gap)  
        • Stale credit data (outdated information)  
        • Invalid timestamps (data quality issues)
        """)
        
        st.code("""
def check_edge_cases(customers, sessions, credit_data, max_age_hours=24):
    \"\"\"Check for common edge cases and data quality issues\"\"\"
    warnings = []
    
    # Check for customers with multiple sessions
    customer_sessions = {}
    for session in sessions['sessions']:
        customer_id = session['customer_id']
        if customer_id not in customer_sessions:
            customer_sessions[customer_id] = []
        customer_sessions[customer_id].append(session['session_id'])
    
    for customer_id, session_list in customer_sessions.items():
        if len(session_list) > 1:
            warnings.append(f"Customer {customer_id} has {len(session_list)} sessions: {session_list}")
    
    # Check for customers with sessions but no credit limits
    customers_with_sessions = set(s['customer_id'] for s in sessions['sessions'])
    customers_with_credit = set(l['customer_id'] for l in credit_data['customer_pb_limits'])
    
    missing_credit = customers_with_sessions - customers_with_credit
    for customer_id in missing_credit:
        warnings.append(f"Customer {customer_id} has sessions but no credit limits")
    
    # Check for stale credit data
    from datetime import datetime, timedelta
    cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
    
    for limit in credit_data['customer_pb_limits']:
        try:
            last_updated = datetime.fromisoformat(limit['last_updated'].replace('Z', '+00:00'))
            if last_updated < cutoff_time:
                age_hours = (datetime.now() - last_updated.replace(tzinfo=None)).total_seconds() / 3600
                warnings.append(f"Stale credit data for {limit['customer_id']} → {limit['pb_id']} (age: {age_hours:.1f}h)")
        except (ValueError, KeyError):
            warnings.append(f"Invalid timestamp for {limit['customer_id']} → {limit['pb_id']}")
    
    return warnings

# Usage
warnings = check_edge_cases(customers, sessions, credit_data)
for warning in warnings:
    print(f"EDGE CASE: {warning}")
        """, language='python')

elif st.session_state.nav_section == 'future':
    # --- Future Extensibility ---
    st.header("Future Extensibility")
    st.markdown("""
    Here's how we could structure this schema for future requirements like dynamic credit updates and per-instrument limits.
    """)

    with st.expander("Conditional Credit Rules Engine", expanded=False):
        st.markdown("Vendor-submitted expressive rules for dynamic credit adjustments")
        st.markdown("""
        Instead of static credit limits, we could allow vendors to submit conditional rules that automatically adjust credit based on real-time market conditions, customer behavior, and risk metrics.
        
        **Expressive rule language:** We could let vendors define complex conditions using JSON-based expressions. Rules could reference market data, customer trading patterns, time of day, volatility metrics. Multiple conditions could be combined with logical operators (AND, OR, NOT).
        
        **Real-time evaluation:** We'd evaluate rules continuously against live market feeds. Credit adjustments would happen automatically when conditions are met. All changes would be logged with full audit trails showing which rule triggered the change.
        
        **Vendor competition:** We could allow multiple vendors to submit competing rules for the same customer. The system would select the most conservative (lowest risk) limit when rules conflict. Vendors could be scored based on prediction accuracy and risk management performance.
        """)
        
        st.code("""
# Example: Vendor-submitted credit rule in JSON format
credit_rule = {
    "rule_id": "VENDOR_A_VOLATILITY_RULE_001",
    "vendor_id": "CreditVendor_A",
    "customer_id": "Cust_1",
    "pb_id": "PB_A",
    "base_limit": 1000000,
    "conditions": {
        "AND": [
            {"market_volatility": {"EURUSD": {"<": 0.15}}},
            {"time_of_day": {"between": ["08:00", "17:00"]}},
            {"customer_pnl_30d": {">": -50000}}
        ]
    },
    "adjustments": {
        "if_true": {"multiply": 1.2},  # Increase limit by 20%
        "if_false": {"multiply": 0.8}  # Decrease limit by 20%
    }
}

def evaluate_credit_rule(rule, market_data, customer_metrics):
    \"\"\"Evaluate a vendor credit rule against current conditions\"\"\"
    base_limit = rule["base_limit"]
    
    # Evaluate conditions
    conditions_met = evaluate_conditions(rule["conditions"], market_data, customer_metrics)
    
    # Apply adjustments
    if conditions_met:
        adjusted_limit = base_limit * rule["adjustments"]["if_true"]["multiply"]
    else:
        adjusted_limit = base_limit * rule["adjustments"]["if_false"]["multiply"]
    
    return {
        "rule_id": rule["rule_id"],
        "vendor_id": rule["vendor_id"],
        "original_limit": base_limit,
        "adjusted_limit": int(adjusted_limit),
        "conditions_met": conditions_met,
        "timestamp": datetime.now().isoformat()
    }

# Usage example
market_data = {"EURUSD_volatility": 0.12}
customer_metrics = {"pnl_30d": -25000}

result = evaluate_credit_rule(credit_rule, market_data, customer_metrics)
print(f"Adjusted limit: ${result['adjusted_limit']:,}")
        """, language='python')

    with st.expander("Dynamic Credit Updates via API", expanded=False):
        st.markdown("Real-time credit adjustments through API endpoints")
        st.markdown("""
        We could move beyond static YAML files to enable real-time credit updates through RESTful APIs. Vendors and risk systems could push credit changes instantly.
        
        **Real-time API endpoints:** We'd implement POST /api/credit/update for immediate limit changes. GET /api/credit/status for current limits and utilization. WebSocket streams for live credit notifications to trading systems.
        
        **Event-driven updates:** Credit changes would trigger immediate notifications to all connected trading systems. Message queues would ensure reliable delivery even during system outages. We could add automatic rollback capabilities if updates fail validation.
        
        **Audit and versioning:** Every credit change would create an immutable audit record. Version numbers would track configuration evolution. We'd have the ability to query historical credit states for compliance reporting.
        """)
        
        st.code("""
from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/api/credit/update', methods=['POST'])
def update_credit_limit():
    \"\"\"API endpoint to update credit limits in real-time\"\"\"
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['customer_id', 'pb_id', 'new_limit', 'vendor_id', 'reason']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create audit record
        audit_record = {
            "timestamp": datetime.now().isoformat(),
            "customer_id": data["customer_id"],
            "pb_id": data["pb_id"],
            "old_limit": get_current_limit(data["customer_id"], data["pb_id"]),
            "new_limit": data["new_limit"],
            "vendor_id": data["vendor_id"],
            "reason": data["reason"],
            "version": get_next_version()
        }
        
        # Update credit limit
        success = update_credit_database(data["customer_id"], data["pb_id"], 
                                       data["new_limit"], audit_record)
        
        if success:
            # Notify all trading systems via WebSocket
            notify_trading_systems({
                "type": "CREDIT_UPDATE",
                "customer_id": data["customer_id"],
                "pb_id": data["pb_id"],
                "new_limit": data["new_limit"]
            })
            
            return jsonify({
                "status": "success",
                "audit_id": audit_record["version"],
                "message": f"Credit limit updated to ${data['new_limit']:,}"
            }), 200
        else:
            return jsonify({"error": "Failed to update credit limit"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/credit/status/<customer_id>/<pb_id>', methods=['GET'])
def get_credit_status(customer_id, pb_id):
    \"\"\"Get current credit limit and utilization\"\"\"
    try:
        current_limit = get_current_limit(customer_id, pb_id)
        current_exposure = calculate_current_exposure(customer_id, pb_id)
        utilization = (current_exposure / current_limit * 100) if current_limit > 0 else 0
        
        return jsonify({
            "customer_id": customer_id,
            "pb_id": pb_id,
            "current_limit": current_limit,
            "current_exposure": current_exposure,
            "utilization_percent": round(utilization, 2),
            "available_credit": current_limit - current_exposure,
            "last_updated": get_last_update_time(customer_id, pb_id)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Usage example - updating credit limit
import requests

update_data = {
    "customer_id": "Cust_1",
    "pb_id": "PB_A", 
    "new_limit": 1500000,
    "vendor_id": "RiskVendor_B",
    "reason": "Improved credit rating"
}

response = requests.post('http://localhost:5000/api/credit/update', 
                        json=update_data)
print(f"Update result: {response.json()}")
        """, language='python')

    with st.expander("Per-Instrument Credit Limits", expanded=False):
        st.markdown("Granular credit control at the instrument level")
        st.markdown("""
        Currently the schema has aggregate credit limits per customer-PB relationship. For per-instrument limits, we could implement:
        
        **Instrument hierarchy:** We could define instrument categories (FX majors, minors, exotics). Set limits at category and individual instrument levels. Inherit limits from parent categories with overrides.
        
        **Multi-dimensional limits:** We could add credit limits by instrument, tenor, notional size. Time-based limits (daily, weekly, monthly). Concentration limits to prevent over-exposure to single instruments.
        
        **Real-time monitoring:** We'd track utilization per instrument in real-time. Alert when approaching instrument-specific limits. Automatically reject trades exceeding limits.
        """)
        
        st.code("""
# Extended credit data structure with per-instrument limits
instrument_credit_config = {
    "customer_id": "Cust_1",
    "pb_id": "PB_A",
    "aggregate_limit": 1000000,  # Overall limit
    "instrument_limits": {
        "categories": {
            "FX_MAJORS": {
                "limit": 800000,
                "instruments": ["EURUSD", "GBPUSD", "USDJPY", "USDCHF"]
            },
            "FX_MINORS": {
                "limit": 150000,
                "instruments": ["EURGBP", "EURJPY", "GBPJPY"]
            },
            "FX_EXOTICS": {
                "limit": 50000,
                "instruments": ["USDTRY", "USDZAR", "USDMXN"]
            }
        },
        "individual_overrides": {
            "EURUSD": {"limit": 500000},  # Override within FX_MAJORS
            "USDTRY": {"limit": 25000}    # Override within FX_EXOTICS
        }
    },
    "concentration_limits": {
        "max_single_instrument_pct": 60,  # Max 60% in any single instrument
        "max_category_pct": 80             # Max 80% in any category
    }
}

def validate_instrument_trade(customer_id, pb_id, instrument, notional, current_positions):
    \"\"\"Validate trade against per-instrument credit limits\"\"\"
    config = get_instrument_credit_config(customer_id, pb_id)
    
    # Get instrument category and limits
    category = get_instrument_category(instrument, config)
    instrument_limit = get_effective_instrument_limit(instrument, config)
    
    # Calculate current exposures
    current_instrument_exposure = current_positions.get(instrument, 0)
    current_category_exposure = sum(current_positions.get(instr, 0) 
                                  for instr in config["instrument_limits"]["categories"][category]["instruments"])
    total_exposure = sum(current_positions.values())
    
    # Check limits
    checks = {
        "aggregate_limit": {
            "current": total_exposure + notional,
            "limit": config["aggregate_limit"],
            "passed": (total_exposure + notional) <= config["aggregate_limit"]
        },
        "instrument_limit": {
            "current": current_instrument_exposure + notional,
            "limit": instrument_limit,
            "passed": (current_instrument_exposure + notional) <= instrument_limit
        },
        "category_limit": {
            "current": current_category_exposure + notional,
            "limit": config["instrument_limits"]["categories"][category]["limit"],
            "passed": (current_category_exposure + notional) <= config["instrument_limits"]["categories"][category]["limit"]
        },
        "concentration_check": {
            "instrument_pct": ((current_instrument_exposure + notional) / config["aggregate_limit"] * 100),
            "max_pct": config["concentration_limits"]["max_single_instrument_pct"],
            "passed": ((current_instrument_exposure + notional) / config["aggregate_limit"] * 100) <= config["concentration_limits"]["max_single_instrument_pct"]
        }
    }
    
    # Overall validation result
    all_passed = all(check["passed"] for check in checks.values())
    
    return {
        "trade_allowed": all_passed,
        "checks": checks,
        "instrument": instrument,
        "category": category,
        "notional": notional
    }

# Usage example
current_positions = {
    "EURUSD": 300000,
    "GBPUSD": 200000,
    "USDJPY": 150000
}

result = validate_instrument_trade("Cust_1", "PB_A", "EURUSD", 250000, current_positions)
print(f"Trade allowed: {result['trade_allowed']}")
for check_name, check_result in result['checks'].items():
    print(f"{check_name}: {check_result['current']:,} / {check_result['limit']:,} - {'PASS' if check_result['passed'] else 'FAIL'}")
        """, language='python')

elif st.session_state.nav_section == 'trade_flow':
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
        </style>
    </head>
    <body>
        <div class="flow-container">
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

elif st.session_state.nav_section == 'trading':
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
                    
                    # Calculate net position change (BUY = +, SELL = -)
                    position_change = notional if side == "BUY" else -notional
                    new_exposure = current_exposure + position_change
                    
                    # For credit limit checking, use absolute value of exposure
                    abs_new_exposure = abs(new_exposure)
                    customer_breach = abs_new_exposure > customer_limit
                    
                    # Check PB credit line (only for non-central PBs)
                    pb_breach = False
                    pb_total_exposure = 0
                    pb_credit_line = 0
                    
                    if customer_pb != "CPB_1":  # Only check PB limits for non-central PBs
                        # Calculate PB total exposure to all customers (using absolute values)
                        for pos_key, exposure in st.session_state.positions.items():
                            if pos_key.endswith(f"|{customer_pb}"):
                                pb_total_exposure += abs(exposure)
                        
                        # Add this new trade to PB exposure (absolute value)
                        pb_new_total = pb_total_exposure + abs(new_exposure) - abs(current_exposure)
                        
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
                        order['reject_reason'] = f"Customer credit limit exceeded. Limit: ${customer_limit:,}, Would be: ${abs_new_exposure:,}"
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
                    
                    utilization = (abs(exposure) / customer_limit * 100) if customer_limit > 0 else 0
                    
                    st.write(f"**{customer_id} → {pb_id}**")
                    st.write(f"Net Position: ${exposure:,} | Credit Used: ${abs(exposure):,} / ${customer_limit:,} ({utilization:.1f}%)")
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
                        pb_exposures[pb_id] += abs(exposure)
                
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
                        st.write(f"Total Credit Used: ${total_exposure:,} / ${pb_credit_line:,} ({pb_utilization:.1f}%)")
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
    with st.expander("Order Book", expanded=True):
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

    # Interactive 2D Relationship Diagram
    st.subheader("Relationship Network")

    
    # Create the 2D visualization using D3.js
    relationship_diagram = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ 
                margin: 0; 
                padding: 20px; 
                background: white; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            #network {{ 
                width: 100%; 
                height: 700px; 
                border: 1px solid #ddd; 
                border-radius: 8px;
                background: #fafafa;
            }}
            .legend {{
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(255,255,255,0.95);
                padding: 15px;
                border-radius: 8px;
                border: 1px solid #ddd;
                font-size: 12px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                margin: 8px 0;
            }}
            .legend-color {{
                width: 16px;
                height: 16px;
                margin-right: 8px;
                border-radius: 50%;
                border: 1px solid #ccc;
            }}
            .tooltip {{
                position: absolute;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 8px;
                border-radius: 4px;
                font-size: 12px;
                pointer-events: none;
                z-index: 1000;
            }}
            .node-label {{
                font-size: 11px;
                font-weight: bold;
                text-anchor: middle;
                fill: #333;
                pointer-events: none;
            }}
        </style>
    </head>
    <body>
        <div style="position: relative;">
            <svg id="network"></svg>
            <div class="legend">
                <div style="font-weight: bold; margin-bottom: 10px;">Network Legend</div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #e74c3c;"></div>
                    <span>Customers</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #3498db;"></div>
                    <span>Prime Brokers</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #f39c12;"></div>
                    <span>Central PB</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color" style="background: #27ae60;"></div>
                    <span>Sessions</span>
                </div>
            </div>
        </div>
        
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <script>
            // Data from configuration
            const customers = {json.dumps(list(customers))};
            const primeBrokers = {json.dumps(list(prime_brokers.values()) if isinstance(prime_brokers, dict) else prime_brokers)};
            const sessions = {json.dumps(sessions)};
            
            // Set up SVG
            const width = 1000;
            const height = 700;
            const svg = d3.select("#network")
                .attr("width", width)
                .attr("height", height);
            
            // Create tooltip
            const tooltip = d3.select("body").append("div")
                .attr("class", "tooltip")
                .style("opacity", 0);
            
            // Prepare nodes and links
            const nodes = [];
            const links = [];
            
            // Add customer nodes
            customers.forEach((customer, i) => {{
                nodes.push({{
                    id: customer.id,
                    name: customer.name,
                    type: 'customer',
                    x: 150,
                    y: 100 + i * 80,
                    color: '#e74c3c'
                }});
            }});
            
            // Add prime broker nodes
            primeBrokers.forEach((pb, i) => {{
                const x = pb.is_central_pb ? 750 : 500;
                nodes.push({{
                    id: pb.id,
                    name: pb.name,
                    type: pb.is_central_pb ? 'central_pb' : 'pb',
                    x: x,
                    y: 100 + i * 100,
                    color: pb.is_central_pb ? '#f39c12' : '#3498db'
                }});
            }});
            
            // Add session nodes and create links
            sessions.forEach((session, i) => {{
                const customerNode = nodes.find(n => n.id === session.customer_id);
                const pbNode = nodes.find(n => n.id === session.pb_id);
                
                if (customerNode && pbNode) {{
                    // Add session node
                    const sessionNode = {{
                        id: session.session_id,
                        customer_id: session.customer_id,
                        pb_id: session.pb_id,
                        type: 'session',
                        x: (customerNode.x + pbNode.x) / 2,
                        y: (customerNode.y + pbNode.y) / 2 + (i % 3 - 1) * 30,
                        color: '#27ae60'
                    }};
                    nodes.push(sessionNode);
                    
                    // Add links
                    links.push({{
                        source: customerNode.id,
                        target: sessionNode.id,
                        type: 'customer-session'
                    }});
                    links.push({{
                        source: sessionNode.id,
                        target: pbNode.id,
                        type: 'session-pb'
                    }});
                }}
            }});
            
            // Add PB to Central PB links
            primeBrokers.forEach(pb => {{
                if (!pb.is_central_pb) {{
                    const centralPb = primeBrokers.find(p => p.is_central_pb);
                    if (centralPb) {{
                        links.push({{
                            source: pb.id,
                            target: centralPb.id,
                            type: 'pb-central',
                            stroke: '#e67e22',
                            strokeWidth: 3
                        }});
                    }}
                }}
            }});
            
            // Create force simulation
            const simulation = d3.forceSimulation(nodes)
                .force("link", d3.forceLink(links).id(d => d.id).distance(100))
                .force("charge", d3.forceManyBody().strength(-300))
                .force("center", d3.forceCenter(width / 2, height / 2))
                .force("x", d3.forceX().x(d => {{
                    if (d.type === 'customer') return 150;
                    if (d.type === 'central_pb') return 750;
                    if (d.type === 'pb') return 500;
                    return width / 2;
                }}).strength(0.3))
                .force("y", d3.forceY().y(d => {{
                    if (d.type === 'customer') return 100 + customers.findIndex(c => c.id === d.id) * 80;
                    if (d.type === 'pb' || d.type === 'central_pb') return 100 + primeBrokers.findIndex(p => p.id === d.id) * 100;
                    return height / 2;
                }}).strength(0.3));
            
            // Create links
            const link = svg.append("g")
                .selectAll("line")
                .data(links)
                .enter().append("line")
                .attr("stroke", d => d.stroke || "#95a5a6")
                .attr("stroke-width", d => d.strokeWidth || 2)
                .attr("stroke-opacity", 0.7);
            
            // Create nodes
            const node = svg.append("g")
                .selectAll("g")
                .data(nodes)
                .enter().append("g")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));
            
            // Add circles for nodes
            node.append("circle")
                .attr("r", d => {{
                    if (d.type === 'customer') return 20;
                    if (d.type === 'central_pb') return 25;
                    if (d.type === 'pb') return 22;
                    return 15; // sessions
                }})
                .attr("fill", d => d.color)
                .attr("stroke", "#fff")
                .attr("stroke-width", 2)
                .on("mouseover", function(event, d) {{
                    tooltip.transition().duration(200).style("opacity", .9);
                    tooltip.html(`
                        <strong>${{d.type.toUpperCase()}}</strong><br/>
                        ID: ${{d.id}}<br/>
                        ${{d.name ? 'Name: ' + d.name + '<br/>' : ''}}
                        ${{d.customer_id ? 'Customer: ' + d.customer_id + '<br/>' : ''}}
                        ${{d.pb_id ? 'PB: ' + d.pb_id : ''}}
                    `)
                    .style("left", (event.pageX + 10) + "px")
                    .style("top", (event.pageY - 28) + "px");
                    
                    d3.select(this).attr("r", d => {{
                        if (d.type === 'customer') return 24;
                        if (d.type === 'central_pb') return 30;
                        if (d.type === 'pb') return 26;
                        return 18;
                    }});
                }})
                .on("mouseout", function(event, d) {{
                    tooltip.transition().duration(500).style("opacity", 0);
                    d3.select(this).attr("r", d => {{
                        if (d.type === 'customer') return 20;
                        if (d.type === 'central_pb') return 25;
                        if (d.type === 'pb') return 22;
                        return 15;
                    }});
                }});
            
            // Add labels
            node.append("text")
                .attr("class", "node-label")
                .attr("dy", ".35em")
                .text(d => d.id)
                .style("font-size", d => d.type === 'session' ? "9px" : "11px");
            
            // Update positions on simulation tick
            simulation.on("tick", () => {{
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);
                
                node
                    .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
            }});
            
            // Drag functions
            function dragstarted(event, d) {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }}
            
            function dragged(event, d) {{
                d.fx = event.x;
                d.fy = event.y;
            }}
            
            function dragended(event, d) {{
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }}
        </script>
    </body>
    </html>
    """
    
    # Display the 2D visualization
    st.components.v1.html(relationship_diagram, height=550)


