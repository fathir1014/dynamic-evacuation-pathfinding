# src/core/risk.py

def calculate_risk(node):
    return (
        0.4 * node.smoke +
        0.3 * node.debris +
        0.2 * node.liquid +
        0.1 * node.crowd
    )