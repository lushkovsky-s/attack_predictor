
from flask import Flask, request, jsonify
import neo4j

import storage
from utils import count_stats

app = Flask(__name__)


@app.route('/attack')
@count_stats
def attack():
    vm_id = request.args.get('vm_id')
   
    if not vm_id:
        return 'Query parameter "vm_id" required', 400

    attackers = storage.vms.get_attackers(vm_id)
    ids = {vm[0]['id'] for vm in attackers }

    return jsonify(list(ids))

@app.route('/stats')
def stats():
    count, avg_time = storage.stats.get()
    vms_count = storage.vms.get_count()
    return jsonify({"vm_count": vms_count, "request_count": count, "average_request_time": avg_time})
