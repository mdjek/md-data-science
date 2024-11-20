set -e

mongo <<EOF
db = db.getSiblingDB('mongo_profi_db')
db.createCollection('users')
db.orders.createIndex({"id": -1}) 
EOF