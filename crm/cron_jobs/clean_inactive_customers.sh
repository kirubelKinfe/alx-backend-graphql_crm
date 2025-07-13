#!/bin/bash

# File: clean_inactive_customers.sh

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Running from script directory: $SCRIPT_DIR"

# Save current working directory to restore later
cwd=$(pwd)
echo "Original working directory: $cwd"

# Change to the project root directory (assuming script is in a subdir like scripts/)
cd "$SCRIPT_DIR/.." || { echo "Failed to change directory to project root"; exit 1; }

# Calculate the date one year ago
ONE_YEAR_AGO=$(date -d "1 year ago" '+%Y-%m-%d')

# Run the deletion script
if DELETED_COUNT=$(python manage.py shell -c "
from django.utils import timezone
from datetime import datetime
from crm.models import Customer
count = Customer.objects.filter(
    last_order_date__lt=datetime.strptime('$ONE_YEAR_AGO', '%Y-%m-%d').date()
).delete()[0]
print(count)
"); then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
    echo "Deleted $DELETED_COUNT inactive customers"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - Failed to delete inactive customers" >> /tmp/customer_cleanup_log.txt
    echo "Error: Failed to delete customers"
fi

# Return to original directory
cd "$cwd" || echo "Warning: Could not return to original directory"
