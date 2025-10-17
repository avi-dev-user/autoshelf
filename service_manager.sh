#!/bin/bash
# AutoShelf Service Manager
# Easy installation and management of AutoShelf as a system service

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project info
PROJECT_NAME="AutoShelf"
VERSION="1.0.0"
USERNAME=$(whoami)
SERVICE_NAME="autoshelf@${USERNAME}.service"

echo -e "${BLUE}📂 $PROJECT_NAME v$VERSION - Service Manager${NC}"
echo "=================================================="

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ This service manager only works on Linux${NC}"
    exit 1
fi

# Check if systemd is available
if ! command -v systemctl &> /dev/null; then
    echo -e "${RED}❌ systemctl not found. This system doesn't use systemd${NC}"
    exit 1
fi

# Function to check if service is installed
is_service_installed() {
    systemctl --user list-unit-files | grep -q "autoshelf@.service" 2>/dev/null
}

# Function to check if service is running
is_service_running() {
    systemctl --user is-active "$SERVICE_NAME" &>/dev/null
}

# Function to install service
install_service() {
    echo -e "${BLUE}📦 Installing AutoShelf service...${NC}"
    
    # Create systemd user directory
    mkdir -p "$HOME/.config/systemd/user"
    
    # Copy service file
    if [[ ! -f "autoshelf@.service" ]]; then
        echo -e "${RED}❌ Service file autoshelf@.service not found${NC}"
        exit 1
    fi
    
    cp "autoshelf@.service" "$HOME/.config/systemd/user/"
    echo -e "${GREEN}✅ Service file installed${NC}"
    
    # Reload systemd and enable service
    systemctl --user daemon-reload
    systemctl --user enable "$SERVICE_NAME"
    
    echo -e "${GREEN}✅ Service $SERVICE_NAME installed and enabled${NC}"
    echo -e "${YELLOW}📋 The service will start automatically on login${NC}"
    
    # Ask if user wants to start now
    echo ""
    read -p "Start the service now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_service
    fi
}

# Function to uninstall service
uninstall_service() {
    echo -e "${BLUE}🗑️  Uninstalling AutoShelf service...${NC}"
    
    # Stop service if running
    if is_service_running; then
        systemctl --user stop "$SERVICE_NAME"
        echo -e "${YELLOW}⏹️  Service stopped${NC}"
    fi
    
    # Disable and remove
    systemctl --user disable "$SERVICE_NAME" 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/autoshelf@.service"
    systemctl --user daemon-reload
    
    echo -e "${GREEN}✅ Service uninstalled${NC}"
}

# Function to start service
start_service() {
    echo -e "${BLUE}▶️  Starting AutoShelf service...${NC}"
    
    if ! is_service_installed; then
        echo -e "${RED}❌ Service not installed. Run: $0 install${NC}"
        exit 1
    fi
    
    systemctl --user start "$SERVICE_NAME"
    
    if is_service_running; then
        echo -e "${GREEN}✅ Service started successfully${NC}"
        show_status
    else
        echo -e "${RED}❌ Failed to start service${NC}"
        systemctl --user status "$SERVICE_NAME" --no-pager
        exit 1
    fi
}

# Function to stop service
stop_service() {
    echo -e "${BLUE}⏹️  Stopping AutoShelf service...${NC}"
    
    if is_service_running; then
        systemctl --user stop "$SERVICE_NAME"
        echo -e "${GREEN}✅ Service stopped${NC}"
    else
        echo -e "${YELLOW}⚠️  Service is not running${NC}"
    fi
}

# Function to restart service
restart_service() {
    echo -e "${BLUE}🔄 Restarting AutoShelf service...${NC}"
    
    if ! is_service_installed; then
        echo -e "${RED}❌ Service not installed${NC}"
        exit 1
    fi
    
    systemctl --user restart "$SERVICE_NAME"
    
    if is_service_running; then
        echo -e "${GREEN}✅ Service restarted successfully${NC}"
        show_status
    else
        echo -e "${RED}❌ Failed to restart service${NC}"
        exit 1
    fi
}

# Function to show service status
show_status() {
    echo -e "${BLUE}📊 AutoShelf Service Status${NC}"
    echo "================================"
    
    if is_service_installed; then
        echo -e "Installation: ${GREEN}✅ Installed${NC}"
        
        if is_service_running; then
            echo -e "Status: ${GREEN}✅ Running${NC}"
        else
            echo -e "Status: ${RED}❌ Stopped${NC}"
        fi
        
        # Show detailed systemctl status
        echo ""
        systemctl --user status "$SERVICE_NAME" --no-pager || true
        
        # Show recent logs
        echo ""
        echo -e "${BLUE}📋 Recent logs:${NC}"
        journalctl --user -u "$SERVICE_NAME" --no-pager -n 10 || true
        
    else
        echo -e "Installation: ${RED}❌ Not installed${NC}"
        echo -e "Status: ${RED}❌ Not available${NC}"
    fi
}

# Function to show logs
show_logs() {
    echo -e "${BLUE}📋 AutoShelf Service Logs${NC}"
    echo "============================"
    
    if ! is_service_installed; then
        echo -e "${RED}❌ Service not installed${NC}"
        exit 1
    fi
    
    echo "Press Ctrl+C to exit log viewer"
    echo ""
    journalctl --user -u "$SERVICE_NAME" -f
}

# Function to enable/disable auto-start
toggle_autostart() {
    if ! is_service_installed; then
        echo -e "${RED}❌ Service not installed${NC}"
        exit 1
    fi
    
    if systemctl --user is-enabled "$SERVICE_NAME" &>/dev/null; then
        systemctl --user disable "$SERVICE_NAME"
        echo -e "${YELLOW}⏸️  Auto-start disabled${NC}"
    else
        systemctl --user enable "$SERVICE_NAME"
        echo -e "${GREEN}✅ Auto-start enabled${NC}"
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  install      Install AutoShelf as a systemd service"
    echo "  uninstall    Remove the AutoShelf service"
    echo "  start        Start the service"
    echo "  stop         Stop the service"
    echo "  restart      Restart the service"
    echo "  status       Show service status and logs"
    echo "  logs         Show live service logs"
    echo "  autostart    Toggle auto-start on login"
    echo "  help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 install       # Install and enable service"
    echo "  $0 start         # Start the service now"
    echo "  $0 status        # Check if service is running"
    echo "  $0 logs          # Watch live logs"
}

# Function to show interactive menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo "1) Install service"
    echo "2) Start service"
    echo "3) Stop service" 
    echo "4) Restart service"
    echo "5) Show status"
    echo "6) Show logs"
    echo "7) Toggle auto-start"
    echo "8) Uninstall service"
    echo "9) Exit"
    echo ""
    read -p "Choose an option (1-9): " choice
    
    case $choice in
        1) install_service ;;
        2) start_service ;;
        3) stop_service ;;
        4) restart_service ;;
        5) show_status ;;
        6) show_logs ;;
        7) toggle_autostart ;;
        8) uninstall_service ;;
        9) echo -e "${BLUE}👋 Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}❌ Invalid option${NC}"; show_menu ;;
    esac
}

# Main execution
if [[ $# -eq 0 ]]; then
    show_menu
else
    case $1 in
        "install") install_service ;;
        "uninstall") uninstall_service ;;
        "start") start_service ;;
        "stop") stop_service ;;
        "restart") restart_service ;;
        "status") show_status ;;
        "logs") show_logs ;;
        "autostart") toggle_autostart ;;
        "help"|"-h"|"--help") show_help ;;
        *) 
            echo -e "${RED}❌ Unknown command: $1${NC}"
            show_help
            exit 1
            ;;
    esac
fi