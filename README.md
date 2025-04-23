# ThingsBoardCIS5370
CIS5370 Final Project 

# Secure Role-Based Access Control for IoT Sensor Data

## Project Overview
This project implements a secure Role-Based Access Control (RBAC) system for IoT environmental monitoring using ThingsBoard platform.

## Features
- **Virtual Sensor Simulation**: Python scripts generating realistic environmental data
- **MQTT Communication**: Secure data transmission between sensors and platform
- **Role-Based Access Control**: Three-tier permission system (Tenant, Admin, Customer)
- **Custom Dashboards**: Role-specific views of environmental data
- **API Security**: REST API authentication with role enforcement
- **Environmental Monitoring**: Simulated sensors for temperature, humidity, CO2, and particulate matter

## Tech Stack
- **Platform**: ThingsBoard Cloud
- **Communication Protocol**: MQTT
- **Programming Language**: Python
- **Data Format**: JSON
- **Authentication**: Token-based access control

## Role Permissions

| Role | Access | Description |
|------|--------|-------------|
| **Tenant** | Sensor Data, Dashboards, Devices | Complete access to all platform features. Can modify dashboards, configure devices, and manage users. |
| **Admin** | Sensor Data, Dashboards | Access to view telemetry dashboards but cannot modify device configurations. |
| **Customer** | Sensor Data | Limited to viewing non-sensitive data only. Cannot modify dashboards or device settings. |

## Installation

### Prerequisites
- ThingsBoard Cloud account
- Python 3.7+
- MQTT client library

### Setup Instructions
1. Clone this repository:
   ```
   git clone https://github.com/OscarInfanzon00/ThingsBoardCIS5370.git
   ```
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure ThingsBoard:
   - Create device profiles
   - Generate access tokens
   - Set up role permissions

4. Run the virtual sensor simulator:
   ```
   python sensor_simulator.py
   ```

## Dashboard Configuration
- Role-specific dashboards restrict access based on user permissions
- Widget visibility is controlled by user roles
- Data visualization updates in real-time

## Security Features
- Token-based authentication for API access
- Permission scopes limit dashboard and device interactions
- Audit logging tracks all user actions
- Fine-grained widget-level access control

## Security Testing
- **Penetration Testing**: Validated against privilege escalation attempts
- **API Testing**: Confirmed token enforcement across all endpoints
- **Audit Validation**: Verified all access attempts are properly logged

## Future Enhancements
- Integration with OAuth2 and LDAP protocols
- Advanced alert mechanisms for security breach detection
- Support for complex organizational structures
- Real-time monitoring tools for administrative oversight

## Team Members
- **Oscar Infanzon** (oinfa004@fiu.edu): Dashboard implementation and MQTT simulation
- **Mauricio Esteves** (meste059@fiu.edu): System architecture and integration
- **Jahnavi Chowdary Nidamanuru** (jnida003@fiu.edu): Security research and documentation

## License
This project is released under the MIT License.

## Acknowledgments
- Florida International University Computer Science Department
- ThingsBoard open-source community